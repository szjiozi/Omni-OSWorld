import unittest

from scripts.python.preflight_aws_ppt_web_w0 import (
    evaluate_preflight,
    format_text,
    summarize,
)


COMPLETE_ENV = {
    "AWS_PROFILE": "test-sso",
    "AWS_REGION": "us-east-1",
    "AWS_SUBNET_ID": "subnet-0123456789abcdef0",
    "AWS_SECURITY_GROUP_ID": "sg-0123456789abcdef0",
    "AWS_INSTANCE_TYPE": "t3.xlarge",
    "AWS_CONNECTION_MODE": "public",
    "ENABLE_TTL": "true",
    "DEFAULT_TTL_MINUTES": "120",
    "AWS_SCHEDULER_ROLE_NAME": "osworld-scheduler-ec2-terminate",
    "AWS_EC2_INSTANCE_PROFILE_NAME": "osworld-ec2-ssm-diagnostics",
}


class AwsPptWebW0PreflightTests(unittest.TestCase):
    def test_complete_preflight_has_no_blockers(self):
        checks = evaluate_preflight(
            COMPLETE_ENV,
            which=lambda command: "/usr/local/bin/aws" if command == "aws" else None,
            python_version=(3, 12, 1),
        )

        self.assertEqual(
            summarize(checks),
            {"pass": 13, "warning": 0, "blocked": 0},
        )

    def test_missing_configuration_is_reported_without_values(self):
        checks = evaluate_preflight(
            {"AWS_SECRET_ACCESS_KEY": "must-not-appear"},
            which=lambda _command: None,
            python_version=(3, 11, 9),
        )
        output = format_text(checks)

        self.assertEqual(summarize(checks)["blocked"], 10)
        self.assertNotIn("must-not-appear", output)
        self.assertIn("No AWS API calls were made", output)

    def test_invalid_ttl_and_identifiers_are_blocking(self):
        environ = {
            **COMPLETE_ENV,
            "AWS_SUBNET_ID": "not-a-subnet",
            "AWS_SECURITY_GROUP_ID": "not-a-security-group",
            "ENABLE_TTL": "false",
            "DEFAULT_TTL_MINUTES": "never",
        }

        checks = evaluate_preflight(
            environ,
            which=lambda _command: "/usr/local/bin/aws",
            python_version=(3, 14, 0),
        )
        blocked_names = {
            check.name for check in checks if check.status == "blocked"
        }

        self.assertEqual(
            blocked_names,
            {
                "aws_subnet_id",
                "aws_security_group_id",
                "ttl_enabled",
                "ttl_minutes",
            },
        )

    def test_w0_allows_cloud_resources_to_be_created_in_w1(self):
        environ = {
            "AWS_PROFILE": "test-sso",
            "AWS_REGION": "us-east-1",
            "AWS_INSTANCE_TYPE": "t3.xlarge",
            "AWS_CONNECTION_MODE": "public",
            "ENABLE_TTL": "true",
            "DEFAULT_TTL_MINUTES": "180",
        }

        checks = evaluate_preflight(
            environ,
            which=lambda command: "/usr/local/bin/aws" if command == "aws" else None,
            python_version=(3, 12, 1),
            stage="w0",
        )

        self.assertEqual(
            summarize(checks),
            {"pass": 9, "warning": 4, "blocked": 0},
        )

    def test_unknown_stage_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "stage"):
            evaluate_preflight(COMPLETE_ENV, stage="future")

    def test_w1_requires_a_scheduler_role(self):
        environ = {
            key: value
            for key, value in COMPLETE_ENV.items()
            if key != "AWS_SCHEDULER_ROLE_NAME"
        }

        checks = evaluate_preflight(
            environ,
            which=lambda command: "/usr/local/bin/aws" if command == "aws" else None,
            python_version=(3, 12, 1),
            stage="w1",
        )

        blocked_names = {
            check.name for check in checks if check.status == "blocked"
        }
        self.assertEqual(blocked_names, {"ttl_scheduler_role"})

    def test_w1_requires_the_diagnostic_instance_profile(self):
        environ = {
            key: value
            for key, value in COMPLETE_ENV.items()
            if key != "AWS_EC2_INSTANCE_PROFILE_NAME"
        }

        checks = evaluate_preflight(
            environ,
            which=lambda command: "/usr/local/bin/aws" if command == "aws" else None,
            python_version=(3, 12, 1),
            stage="w1",
        )

        blocked_names = {
            check.name for check in checks if check.status == "blocked"
        }
        self.assertEqual(blocked_names, {"aws_ec2_instance_profile_name"})


if __name__ == "__main__":
    unittest.main()
