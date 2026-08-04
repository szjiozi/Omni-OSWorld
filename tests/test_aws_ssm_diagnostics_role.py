import unittest

from scripts.python.setup_aws_ssm_diagnostics_role import (
    SSM_CORE_POLICY,
    TRUST_POLICY,
)
from scripts.python.diagnose_aws_ppt_web_w1 import (
    DIAGNOSTIC_COMMANDS,
    _redact_diagnostics,
)


class AwsSsmDiagnosticsRoleTests(unittest.TestCase):
    def test_only_ec2_can_assume_the_role(self):
        statement = TRUST_POLICY["Statement"]

        self.assertEqual(len(statement), 1)
        self.assertEqual(
            statement[0]["Principal"],
            {"Service": "ec2.amazonaws.com"},
        )
        self.assertEqual(statement[0]["Action"], "sts:AssumeRole")

    def test_core_policy_has_no_unrelated_data_or_iam_access(self):
        actions = {
            action
            for statement in SSM_CORE_POLICY["Statement"]
            for action in statement["Action"]
        }

        self.assertIn("ssm:UpdateInstanceInformation", actions)
        self.assertIn("ssmmessages:OpenControlChannel", actions)
        self.assertIn("ec2messages:GetMessages", actions)
        self.assertFalse(
            any(
                action.startswith(prefix)
                for action in actions
                for prefix in ("iam:", "s3:", "secretsmanager:")
            )
        )

    def test_diagnostic_commands_do_not_read_browser_or_home_data(self):
        commands = "\n".join(DIAGNOSTIC_COMMANDS)

        self.assertIn("journalctl -u osworld", commands)
        self.assertIn("systemctl status osworld", commands)
        for forbidden in (
            "Cookies",
            "Login Data",
            "OneDrive",
            ".config/google-chrome",
            "/home/user",
        ):
            self.assertNotIn(forbidden, commands)

    def test_debugger_pin_is_redacted(self):
        self.assertEqual(
            _redact_diagnostics(" * Debugger PIN: 123-456-789\n"),
            " * Debugger PIN: <redacted>\n",
        )


if __name__ == "__main__":
    unittest.main()
