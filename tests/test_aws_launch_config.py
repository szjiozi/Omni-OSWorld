import base64
import re
import unittest
from concurrent.futures import ThreadPoolExecutor

from desktop_env.providers.aws.launch_config import (
    AwsLaunchConfig,
    OSWORLD_SERVICE_DROP_IN,
    OSWORLD_SERVICE_USER_DATA,
    load_launch_config,
)
from desktop_env.providers.aws.manager import can_manage_process_signals, resolve_ami_id
from desktop_env.providers.aws.provider import select_connection_address


class AwsLaunchConfigTests(unittest.TestCase):
    def test_defaults_are_cost_optimized(self):
        config = load_launch_config({})

        self.assertEqual(
            config,
            AwsLaunchConfig(
                instance_type="t3.xlarge",
                volume_size_gib=30,
                volume_iops=4000,
                volume_throughput_mibps=1000,
                volume_encrypted=True,
                resource_project="OSWorld",
                instance_profile_name=None,
                resource_role=None,
            ),
        )
        self.assertEqual(
            config.block_device_mapping(),
            {
                "DeviceName": "/dev/sda1",
                "Ebs": {
                    "VolumeSize": 30,
                    "VolumeType": "gp3",
                    "Throughput": 1000,
                    "Iops": 4000,
                    "Encrypted": True,
                    "DeleteOnTermination": True,
                },
            },
        )
        self.assertEqual(
            config.tag_specifications(),
            [
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Project", "Value": "OSWorld"},
                        {"Key": "ManagedBy", "Value": "OSWorld"},
                    ],
                },
                {
                    "ResourceType": "volume",
                    "Tags": [
                        {"Key": "Project", "Value": "OSWorld"},
                        {"Key": "ManagedBy", "Value": "OSWorld"},
                    ],
                },
            ],
        )
        self.assertEqual(config.instance_profile_parameter(), {})
        self.assertEqual(
            config.user_data_parameter(),
            {"UserData": OSWORLD_SERVICE_USER_DATA},
        )
        self.assertIn("ExecStartPre=", OSWORLD_SERVICE_DROP_IN)
        self.assertIn("xdpyinfo", OSWORLD_SERVICE_DROP_IN)
        self.assertIn("StartLimitIntervalSec=0", OSWORLD_SERVICE_DROP_IN)
        self.assertIn("base64 --decode", OSWORLD_SERVICE_USER_DATA)
        self.assertNotIn("$(seq", OSWORLD_SERVICE_USER_DATA)
        encoded = re.search(
            r"printf '%s' '([^']+)'",
            OSWORLD_SERVICE_USER_DATA,
        ).group(1)
        self.assertEqual(
            base64.b64decode(encoded).decode("utf-8"),
            OSWORLD_SERVICE_DROP_IN,
        )
        self.assertNotIn("password", OSWORLD_SERVICE_USER_DATA.lower())
        self.assertNotIn("cookie", OSWORLD_SERVICE_USER_DATA.lower())

    def test_environment_overrides_are_applied(self):
        config = load_launch_config(
            {
                "AWS_INSTANCE_TYPE": "m7i.xlarge",
                "AWS_EBS_VOLUME_SIZE_GIB": "40",
                "AWS_EBS_IOPS": "5000",
                "AWS_EBS_THROUGHPUT_MIBPS": "250",
                "AWS_EBS_ENCRYPTED": "false",
                "AWS_RESOURCE_PROJECT": "OSWorld-PPT-Web",
                "AWS_EC2_INSTANCE_PROFILE_NAME": "osworld-ec2-ssm-diagnostics",
                "AWS_RESOURCE_ROLE": "AnnotationWorker",
            }
        )

        self.assertEqual(config.instance_type, "m7i.xlarge")
        self.assertEqual(config.volume_size_gib, 40)
        self.assertEqual(config.volume_iops, 5000)
        self.assertEqual(config.volume_throughput_mibps, 250)
        self.assertFalse(config.volume_encrypted)
        self.assertEqual(config.resource_project, "OSWorld-PPT-Web")
        self.assertEqual(
            config.instance_profile_parameter(),
            {
                "IamInstanceProfile": {
                    "Name": "osworld-ec2-ssm-diagnostics",
                }
            },
        )
        self.assertEqual(config.resource_role, "AnnotationWorker")
        self.assertIn(
            {"Key": "Role", "Value": "AnnotationWorker"},
            config.tag_specifications()[0]["Tags"],
        )

    def test_existing_instance_type_is_the_reset_fallback(self):
        config = load_launch_config({}, default_instance_type="m6i.large")

        self.assertEqual(config.instance_type, "m6i.large")

    def test_invalid_values_fail_before_an_aws_call(self):
        invalid_environments = (
            {"AWS_INSTANCE_TYPE": "not valid"},
            {"AWS_EBS_VOLUME_SIZE_GIB": "large"},
            {"AWS_EBS_IOPS": "2999"},
            {"AWS_EBS_THROUGHPUT_MIBPS": "100"},
            {"AWS_EBS_ENCRYPTED": "sometimes"},
            {"AWS_RESOURCE_PROJECT": "  "},
            {"AWS_EC2_INSTANCE_PROFILE_NAME": "not valid"},
            {"AWS_RESOURCE_ROLE": "bad!role"},
        )

        for environ in invalid_environments:
            with self.subTest(environ=environ):
                with self.assertRaises(ValueError):
                    load_launch_config(environ)

    def test_connection_address_is_explicit(self):
        instance = {
            "PrivateIpAddress": "10.0.0.5",
            "PublicIpAddress": "203.0.113.10",
        }

        self.assertEqual(select_connection_address(instance, "private"), "10.0.0.5")
        self.assertEqual(select_connection_address(instance, "public"), "203.0.113.10")

    def test_missing_or_invalid_connection_address_fails(self):
        with self.assertRaisesRegex(ValueError, "public IP"):
            select_connection_address({"PrivateIpAddress": "10.0.0.5"}, "public")
        with self.assertRaisesRegex(ValueError, "AWS_CONNECTION_MODE"):
            select_connection_address({"PrivateIpAddress": "10.0.0.5"}, "internet")

    def test_private_ami_override_precedes_official_map(self):
        self.assertEqual(
            resolve_ami_id(
                "us-east-1",
                (1920, 1080),
                {"AWS_AMI_ID": "ami-0123456789abcdef0"},
            ),
            "ami-0123456789abcdef0",
        )
        self.assertEqual(
            resolve_ami_id("us-east-1", (1920, 1080), {}),
            "ami-0d23263edb96951d8",
        )

    def test_invalid_private_ami_override_fails_before_aws_call(self):
        with self.assertRaisesRegex(ValueError, "AWS_AMI_ID"):
            resolve_ami_id(
                "us-east-1",
                (1920, 1080),
                {"AWS_AMI_ID": "private-ami"},
            )

    def test_background_allocators_do_not_manage_process_signals(self):
        self.assertTrue(can_manage_process_signals())
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.assertFalse(executor.submit(can_manage_process_signals).result())


if __name__ == "__main__":
    unittest.main()
