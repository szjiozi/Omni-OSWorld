import base64
import unittest
from unittest.mock import MagicMock, patch

from desktop_env.providers.aws.launch_config import OSWORLD_SERVICE_DROP_IN
from desktop_env.providers.aws.service_bootstrap import (
    DROP_IN_PATH,
    ensure_osworld_service_x11_wait,
)


class AwsServiceBootstrapTests(unittest.TestCase):
    @patch("desktop_env.providers.aws.service_bootstrap.boto3.client")
    def test_installs_and_verifies_drop_in_via_ssm(self, client):
        ssm = MagicMock()
        client.return_value = ssm
        ssm.describe_instance_information.return_value = {
            "InstanceInformationList": [
                {"InstanceId": "i-123", "PingStatus": "Online"}
            ]
        }
        ssm.send_command.return_value = {
            "Command": {"CommandId": "command-123"}
        }
        ssm.get_command_invocation.side_effect = [
            {"Status": "InProgress"},
            {"Status": "Success"},
        ]

        with patch(
            "desktop_env.providers.aws.service_bootstrap.time.sleep"
        ):
            ensure_osworld_service_x11_wait(
                "us-east-1",
                "i-123",
                timeout_seconds=60,
                poll_seconds=0,
            )

        client.assert_called_once_with("ssm", region_name="us-east-1")
        parameters = ssm.send_command.call_args.kwargs
        self.assertEqual(parameters["InstanceIds"], ["i-123"])
        self.assertEqual(parameters["DocumentName"], "AWS-RunShellScript")
        commands = parameters["Parameters"]["commands"]
        self.assertTrue(any(DROP_IN_PATH in command for command in commands))
        encoded = commands[2].split("'")[3]
        self.assertEqual(
            base64.b64decode(encoded).decode("utf-8"),
            OSWORLD_SERVICE_DROP_IN,
        )
        joined_commands = "\n".join(commands)
        self.assertEqual(commands[0], "set -eu")
        self.assertNotIn("pipefail", joined_commands)
        self.assertIn("systemctl restart osworld.service", joined_commands)
        self.assertIn("StartLimitIntervalSec=0", joined_commands)
        self.assertIn("xdpyinfo", joined_commands)
        self.assertNotIn("password", joined_commands.lower())
        self.assertNotIn("cookie", joined_commands.lower())

    @patch("desktop_env.providers.aws.service_bootstrap.boto3.client")
    def test_command_failure_is_not_silenced(self, client):
        ssm = MagicMock()
        client.return_value = ssm
        ssm.describe_instance_information.return_value = {
            "InstanceInformationList": [{"PingStatus": "Online"}]
        }
        ssm.send_command.return_value = {
            "Command": {"CommandId": "command-123"}
        }
        ssm.get_command_invocation.return_value = {
            "Status": "Failed",
            "StandardErrorContent": "systemctl failed",
        }

        with self.assertRaisesRegex(RuntimeError, "status=Failed"):
            ensure_osworld_service_x11_wait(
                "us-east-1",
                "i-123",
                timeout_seconds=60,
                poll_seconds=0,
            )


if __name__ == "__main__":
    unittest.main()
