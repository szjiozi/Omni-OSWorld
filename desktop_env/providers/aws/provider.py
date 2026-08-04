import boto3
from botocore.exceptions import ClientError

import logging
import os
from desktop_env.providers.base import Provider

# TTL configuration
from desktop_env.providers.aws.config import ENABLE_TTL, DEFAULT_TTL_MINUTES, AWS_SCHEDULER_ROLE_ARN
from desktop_env.providers.aws.launch_config import load_launch_config
from desktop_env.providers.aws.scheduler_utils import (
    delete_instance_termination_schedules,
    schedule_instance_termination,
)
from desktop_env.providers.aws.service_bootstrap import (
    ensure_osworld_service_x11_wait,
)

logger = logging.getLogger("desktopenv.providers.aws.AWSProvider")
logger.setLevel(logging.INFO)

WAIT_DELAY = 15
MAX_ATTEMPTS = 10


def select_connection_address(instance: dict, connection_mode: str | None = None) -> str:
    """Select an instance address explicitly for local or in-VPC controllers."""

    mode = (connection_mode or os.getenv("AWS_CONNECTION_MODE", "private")).strip().lower()
    if mode not in {"private", "public"}:
        raise ValueError("AWS_CONNECTION_MODE must be 'private' or 'public'")

    field = "PublicIpAddress" if mode == "public" else "PrivateIpAddress"
    address = instance.get(field, "")
    if not address:
        raise ValueError(f"Instance does not have a {mode} IP address")
    return address


class AWSProvider(Provider):


    def start_emulator(self, path_to_vm: str, headless: bool, *args, **kwargs):
        logger.info("Starting AWS VM...")
        ec2_client = boto3.client('ec2', region_name=self.region)

        try:
            # Check the current state of the instance
            response = ec2_client.describe_instances(InstanceIds=[path_to_vm])
            state = response['Reservations'][0]['Instances'][0]['State']['Name']
            logger.info(f"Instance {path_to_vm} current state: {state}")

            if state == 'running':
                # If the instance is already running, skip starting it
                logger.info(f"Instance {path_to_vm} is already running. Skipping start.")
                return

            if state == 'stopped':
                # Start the instance if it's currently stopped
                ec2_client.start_instances(InstanceIds=[path_to_vm])
                logger.info(f"Instance {path_to_vm} is starting...")

                # Wait until the instance reaches 'running' state
                waiter = ec2_client.get_waiter('instance_running')
                waiter.wait(
                    InstanceIds=[path_to_vm],
                    WaiterConfig={'Delay': WAIT_DELAY, 'MaxAttempts': MAX_ATTEMPTS}
                )
                logger.info(f"Instance {path_to_vm} is now running.")
            else:
                # For all other states (terminated, pending, etc.), log a warning
                logger.warning(f"Instance {path_to_vm} is in state '{state}' and cannot be started.")

        except ClientError as e:
            logger.error(f"Failed to start the AWS VM {path_to_vm}: {str(e)}")
            raise


    def get_ip_address(self, path_to_vm: str) -> str:
        logger.info("Getting AWS VM IP address...")
        ec2_client = boto3.client('ec2', region_name=self.region)

        try:
            response = ec2_client.describe_instances(InstanceIds=[path_to_vm])
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    private_ip_address = instance.get('PrivateIpAddress', '')
                    public_ip_address = instance.get('PublicIpAddress', '')
                    
                    if public_ip_address:
                        vnc_url = f"http://{public_ip_address}:5910/vnc.html"
                        logger.info("="*80)
                        logger.info(f"🖥️  VNC Web Access URL: {vnc_url}")
                        logger.info(f"📡 Public IP: {public_ip_address}")
                        logger.info(f"🏠 Private IP: {private_ip_address}")
                        logger.info("="*80)
                        print(f"\n🌐 VNC Web Access URL: {vnc_url}")
                        print(f"📍 Please open the above address in the browser for remote desktop access\n")
                    else:
                        logger.warning("No public IP address available for VNC access")
                    
                    return select_connection_address(instance)
            return ''  # Return an empty string if no IP address is found
        except ClientError as e:
            logger.error(f"Failed to retrieve IP address for the instance {path_to_vm}: {str(e)}")
            raise

    def save_state(self, path_to_vm: str, snapshot_name: str):
        logger.info("Saving AWS VM state...")
        ec2_client = boto3.client('ec2', region_name=self.region)

        try:
            image_response = ec2_client.create_image(InstanceId=path_to_vm, Name=snapshot_name)
            image_id = image_response['ImageId']
            logger.info(f"AMI {image_id} created successfully from instance {path_to_vm}.")
            return image_id
        except ClientError as e:
            logger.error(f"Failed to create AMI from the instance {path_to_vm}: {str(e)}")
            raise

    def revert_to_snapshot(self, path_to_vm: str, snapshot_name: str):
        logger.info(f"Reverting AWS VM to snapshot AMI: {snapshot_name}...")
        ec2_client = boto3.client('ec2', region_name=self.region)
        new_instance_id = None

        try:
            # Step 1: Retrieve the original instance details
            instance_details = ec2_client.describe_instances(InstanceIds=[path_to_vm])
            instance = instance_details['Reservations'][0]['Instances'][0]
            # Resolve security groups with fallbacks
            security_groups = [sg['GroupId'] for sg in instance.get('SecurityGroups', []) if 'GroupId' in sg]
            if not security_groups:
                env_sg = os.getenv('AWS_SECURITY_GROUP_ID')
                if env_sg:
                    security_groups = [env_sg]
                    logger.info("SecurityGroups missing on instance; using AWS_SECURITY_GROUP_ID from env")
                else:
                    raise ValueError("No security groups found on instance and AWS_SECURITY_GROUP_ID not set")

            # Resolve subnet with fallbacks
            subnet_id = instance.get('SubnetId')
            if not subnet_id:
                nis = instance.get('NetworkInterfaces', []) or []
                if nis and isinstance(nis, list):
                    for ni in nis:
                        if isinstance(ni, dict) and ni.get('SubnetId'):
                            subnet_id = ni.get('SubnetId')
                            break
                if not subnet_id:
                    env_subnet = os.getenv('AWS_SUBNET_ID')
                    if env_subnet:
                        subnet_id = env_subnet
                        logger.info("SubnetId missing on instance; using AWS_SUBNET_ID from env")
                    else:
                        raise ValueError("SubnetId not available on instance, NetworkInterfaces, or environment")

            launch_config = load_launch_config(
                default_instance_type=instance.get("InstanceType") or "t3.xlarge"
            )
            
            # Step 2: Terminate the old instance (skip if already terminated/shutting-down)
            state = (instance.get('State') or {}).get('Name')
            if state in ['shutting-down', 'terminated']:
                logger.info(f"Old instance {path_to_vm} is already in state '{state}', skipping termination.")
            else:
                try:
                    ec2_client.terminate_instances(InstanceIds=[path_to_vm])
                    logger.info(f"Old instance {path_to_vm} has been terminated.")
                except ClientError as e:
                    error_code = getattr(getattr(e, 'response', {}), 'get', lambda *_: None)('Error', {}).get('Code') if hasattr(e, 'response') else None
                    if error_code in ['InvalidInstanceID.NotFound', 'IncorrectInstanceState']:
                        logger.info(f"Ignore termination error for {path_to_vm}: {error_code}")
                    else:
                        raise
            delete_instance_termination_schedules(
                self.region,
                path_to_vm,
                logger,
            )

            # Step 3: Launch a new instance from the snapshot(AMI) with performance optimization
            logger.info(f"Launching a new instance from AMI {snapshot_name}...")
            
            # TTL configuration follows the same env flags as allocation (centralized)
            enable_ttl = ENABLE_TTL
            default_ttl_minutes = DEFAULT_TTL_MINUTES
            ttl_seconds = max(0, default_ttl_minutes * 60)

            run_instances_params = {
                "MaxCount": 1,
                "MinCount": 1,
                "ImageId": snapshot_name,
                "InstanceType": launch_config.instance_type,
                "EbsOptimized": True,
                "InstanceInitiatedShutdownBehavior": "terminate",
                "TagSpecifications": launch_config.tag_specifications(),
                "NetworkInterfaces": [
                    {
                        "SubnetId": subnet_id,
                        "AssociatePublicIpAddress": True,
                        "DeviceIndex": 0,
                        "Groups": security_groups
                    }
                ],
                "BlockDeviceMappings": [launch_config.block_device_mapping()]
            }
            run_instances_params.update(launch_config.instance_profile_parameter())
            run_instances_params.update(launch_config.user_data_parameter())
            
            new_instance = ec2_client.run_instances(**run_instances_params)
            new_instance_id = new_instance['Instances'][0]['InstanceId']
            logger.info(f"New instance {new_instance_id} launched from AMI {snapshot_name}.")

            # Schedule termination before waiting or bootstrapping so that an
            # interrupted reset still has a cloud-side cleanup path.
            try:
                if enable_ttl:
                    schedule_instance_termination(
                        self.region,
                        new_instance_id,
                        ttl_seconds,
                        AWS_SCHEDULER_ROLE_ARN,
                        logger,
                    )
            except Exception as e:
                logger.warning(
                    f"Failed to create EventBridge Scheduler for "
                    f"{new_instance_id}: {e}"
                )

            logger.info(f"Waiting for instance {new_instance_id} to be running...")
            ec2_client.get_waiter('instance_running').wait(InstanceIds=[new_instance_id])

            logger.info(f"Instance {new_instance_id} is ready.")
            if launch_config.instance_profile_name:
                ensure_osworld_service_x11_wait(
                    self.region,
                    new_instance_id,
                    logger,
                )
            else:
                logger.warning(
                    "No EC2 instance profile configured; relying on UserData "
                    "for the OSWorld X11 wait drop-in"
                )

            try:
                instance_details = ec2_client.describe_instances(InstanceIds=[new_instance_id])
                instance = instance_details['Reservations'][0]['Instances'][0]
                public_ip = instance.get('PublicIpAddress', '')
                if public_ip:
                    vnc_url = f"http://{public_ip}:5910/vnc.html"
                    logger.info("="*80)
                    logger.info(f"🖥️  New Instance VNC Web Access URL: {vnc_url}")
                    logger.info(f"📡 Public IP: {public_ip}")
                    logger.info(f"🆔 New Instance ID: {new_instance_id}")
                    logger.info("="*80)
                    print(f"\n🌐 New Instance VNC Web Access URL: {vnc_url}")
                    print(f"📍 Please open the above address in the browser for remote desktop access\n")
            except Exception as e:
                logger.warning(f"Failed to get VNC address for new instance {new_instance_id}: {e}")

            return new_instance_id

        except Exception as e:
            logger.error(f"Failed to revert to snapshot {snapshot_name} for the instance {path_to_vm}: {str(e)}")
            if new_instance_id:
                logger.info(
                    "Terminating replacement instance %s after reset failure.",
                    new_instance_id,
                )
                try:
                    ec2_client.terminate_instances(
                        InstanceIds=[new_instance_id]
                    )
                finally:
                    delete_instance_termination_schedules(
                        self.region,
                        new_instance_id,
                        logger,
                    )
            raise


    def stop_emulator(self, path_to_vm, region=None):
        logger.info(f"Stopping AWS VM {path_to_vm}...")
        ec2_client = boto3.client('ec2', region_name=self.region)

        try:
            ec2_client.terminate_instances(InstanceIds=[path_to_vm])
            logger.info(f"Instance {path_to_vm} has been terminated.")
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code not in {
                "InvalidInstanceID.NotFound",
                "IncorrectInstanceState",
            }:
                logger.error(f"Failed to stop the AWS VM {path_to_vm}: {str(e)}")
                raise
            logger.info(
                "Instance %s is already absent or terminal: %s",
                path_to_vm,
                error_code,
            )
        delete_instance_termination_schedules(
            self.region,
            path_to_vm,
            logger,
        )
