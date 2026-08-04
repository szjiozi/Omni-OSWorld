import unittest
from unittest.mock import ANY, MagicMock, call, patch

from desktop_env.providers.aws.launch_config import AwsLaunchConfig
from desktop_env.providers.aws.scheduler_utils import (
    delete_instance_termination_schedules,
)
from desktop_env.providers.aws.provider import AWSProvider


class AwsSchedulerCleanupTests(unittest.TestCase):
    @patch("desktop_env.providers.aws.scheduler_utils.boto3.client")
    def test_all_paginated_instance_schedules_are_deleted(self, client):
        scheduler = MagicMock()
        client.return_value = scheduler
        scheduler.list_schedules.side_effect = [
            {
                "Schedules": [
                    {"Name": "osworld-ttl-i-123-1", "GroupName": "default"}
                ],
                "NextToken": "next",
            },
            {
                "Schedules": [
                    {"Name": "osworld-ttl-i-123-2", "GroupName": "default"}
                ]
            },
        ]

        deleted = delete_instance_termination_schedules(
            "us-east-1",
            "i-123",
        )

        self.assertEqual(deleted, 2)
        self.assertEqual(scheduler.list_schedules.call_count, 2)
        self.assertEqual(scheduler.delete_schedule.call_count, 2)

    @patch(
        "desktop_env.providers.aws.provider."
        "delete_instance_termination_schedules"
    )
    @patch("desktop_env.providers.aws.provider.boto3.client")
    def test_provider_close_terminates_and_deletes_schedule(
        self,
        client,
        delete_schedules,
    ):
        provider = AWSProvider.__new__(AWSProvider)
        provider.region = "us-east-1"

        provider.stop_emulator("i-123")

        client.return_value.terminate_instances.assert_called_once_with(
            InstanceIds=["i-123"]
        )
        delete_schedules.assert_called_once_with(
            "us-east-1",
            "i-123",
            ANY,
        )

    @patch(
        "desktop_env.providers.aws.provider."
        "ensure_osworld_service_x11_wait",
        side_effect=RuntimeError("bootstrap failed"),
    )
    @patch(
        "desktop_env.providers.aws.provider."
        "schedule_instance_termination"
    )
    @patch(
        "desktop_env.providers.aws.provider."
        "delete_instance_termination_schedules"
    )
    @patch("desktop_env.providers.aws.provider.load_launch_config")
    @patch("desktop_env.providers.aws.provider.boto3.client")
    def test_reset_bootstrap_failure_cleans_replacement(
        self,
        client,
        load_config,
        delete_schedules,
        schedule_termination,
        ensure_service,
    ):
        ec2 = MagicMock()
        client.return_value = ec2
        ec2.describe_instances.return_value = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceType": "t3.xlarge",
                            "SecurityGroups": [{"GroupId": "sg-123"}],
                            "SubnetId": "subnet-123",
                            "State": {"Name": "running"},
                        }
                    ]
                }
            ]
        }
        ec2.run_instances.return_value = {
            "Instances": [{"InstanceId": "i-new"}]
        }
        load_config.return_value = AwsLaunchConfig(
            instance_type="t3.xlarge",
            volume_size_gib=30,
            volume_iops=4000,
            volume_throughput_mibps=1000,
            volume_encrypted=True,
            resource_project="OSWorld-PPT-Web",
            instance_profile_name="osworld-ec2-ssm-diagnostics",
        )
        provider = AWSProvider.__new__(AWSProvider)
        provider.region = "us-east-1"

        with self.assertRaisesRegex(RuntimeError, "bootstrap failed"):
            provider.revert_to_snapshot("i-old", "ami-12345678")

        self.assertEqual(
            ec2.terminate_instances.call_args_list,
            [
                call(InstanceIds=["i-old"]),
                call(InstanceIds=["i-new"]),
            ],
        )
        delete_schedules.assert_has_calls(
            [
                call("us-east-1", "i-old", ANY),
                call("us-east-1", "i-new", ANY),
            ]
        )
        schedule_termination.assert_called_once()
        ensure_service.assert_called_once_with(
            "us-east-1",
            "i-new",
            ANY,
        )


if __name__ == "__main__":
    unittest.main()
