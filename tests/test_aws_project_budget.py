import unittest
from decimal import Decimal

from scripts.python.setup_aws_project_budget import (
    PROJECT_TAG_KEY,
    PROJECT_TAG_VALUE,
    _reconcile_notifications,
    build_budget,
    build_notifications,
    cost_allocation_tag_status,
    parse_budget_amount,
)


class FakeBudgets:
    def __init__(self):
        self.notification = {
            "NotificationType": "ACTUAL",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": 80.0,
            "ThresholdType": "PERCENTAGE",
            "NotificationState": "ALARM",
        }
        self.created_subscribers = []
        self.deleted_subscribers = []

    def describe_notifications_for_budget(self, **_kwargs):
        return {"Notifications": [self.notification]}

    def describe_subscribers_for_notification(self, **_kwargs):
        return {
            "Subscribers": [
                {"SubscriptionType": "EMAIL", "Address": "old@example.com"}
            ]
        }

    def create_subscriber(self, **kwargs):
        self.created_subscribers.append(kwargs["Subscriber"])

    def delete_subscriber(self, **kwargs):
        self.deleted_subscribers.append(kwargs["Subscriber"])


class AwsProjectBudgetTests(unittest.TestCase):
    def test_budget_is_filtered_to_the_project_tag(self):
        budget = build_budget(amount=Decimal("20.00"))

        self.assertEqual(
            budget["FilterExpression"],
            {
                "Tags": {
                    "Key": PROJECT_TAG_KEY,
                    "Values": [PROJECT_TAG_VALUE],
                    "MatchOptions": ["EQUALS"],
                }
            },
        )
        self.assertEqual(
            budget["BudgetLimit"],
            {"Amount": "20.00", "Unit": "USD"},
        )
        self.assertFalse(budget["CostTypes"]["IncludeTax"])
        self.assertFalse(budget["CostTypes"]["IncludeSupport"])
        self.assertFalse(budget["CostTypes"]["IncludeSubscription"])

    def test_notifications_match_the_intended_thresholds(self):
        notifications = build_notifications("budget@example.com")

        self.assertEqual(
            [
                (
                    item["Notification"]["NotificationType"],
                    item["Notification"]["Threshold"],
                )
                for item in notifications
            ],
            [("ACTUAL", 80.0), ("FORECASTED", 100.0)],
        )
        self.assertTrue(
            all(
                item["Subscribers"]
                == [
                    {
                        "SubscriptionType": "EMAIL",
                        "Address": "budget@example.com",
                    }
                ]
                for item in notifications
            )
        )

    def test_tag_status_requires_the_exact_project_key(self):
        response = {
            "CostAllocationTags": [
                {"TagKey": "Other", "Status": "Active"},
                {"TagKey": PROJECT_TAG_KEY, "Status": "Inactive"},
            ]
        }

        self.assertEqual(cost_allocation_tag_status(response), "Inactive")
        self.assertIsNone(cost_allocation_tag_status({"CostAllocationTags": []}))

    def test_invalid_amount_and_email_are_rejected(self):
        for raw_value in ("0", "-1", "not-a-number"):
            with self.subTest(raw_value=raw_value):
                with self.assertRaises(ValueError):
                    parse_budget_amount(raw_value)
        with self.assertRaises(ValueError):
            build_notifications("not-an-email")

    def test_notification_reconcile_replaces_stale_email_subscriber(self):
        budgets = FakeBudgets()

        _reconcile_notifications(
            budgets,
            "123456789012",
            "project-budget",
            build_notifications("new@example.com")[:1],
        )

        self.assertEqual(
            budgets.deleted_subscribers,
            [{"SubscriptionType": "EMAIL", "Address": "old@example.com"}],
        )
        self.assertEqual(
            budgets.created_subscribers,
            [{"SubscriptionType": "EMAIL", "Address": "new@example.com"}],
        )


if __name__ == "__main__":
    unittest.main()
