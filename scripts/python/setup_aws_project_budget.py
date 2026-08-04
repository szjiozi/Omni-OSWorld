#!/usr/bin/env python3
"""Prepare or apply the tag-filtered OSWorld PowerPoint Web budget."""

from __future__ import annotations

import argparse
import json
import os
from decimal import Decimal, InvalidOperation
from typing import Any

import boto3
from botocore.exceptions import ClientError


DEFAULT_BUDGET_NAME = "osworld-ppt-web-project-monthly"
DEFAULT_BUDGET_AMOUNT = Decimal("20.00")
PROJECT_TAG_KEY = "Project"
PROJECT_TAG_VALUE = "OSWorld-PPT-Web"


def parse_budget_amount(raw_value: str) -> Decimal:
    try:
        amount = Decimal(raw_value)
    except InvalidOperation as exc:
        raise ValueError("budget amount must be a decimal number") from exc
    if amount <= 0:
        raise ValueError("budget amount must be greater than zero")
    return amount.quantize(Decimal("0.01"))


def build_budget(
    budget_name: str = DEFAULT_BUDGET_NAME,
    amount: Decimal = DEFAULT_BUDGET_AMOUNT,
) -> dict[str, Any]:
    if not budget_name.strip():
        raise ValueError("budget name must not be empty")
    return {
        "BudgetName": budget_name,
        "BudgetLimit": {
            "Amount": format(amount, "f"),
            "Unit": "USD",
        },
        "CostTypes": {
            "IncludeTax": False,
            "IncludeSubscription": False,
            "UseBlended": False,
            "IncludeRefund": True,
            "IncludeCredit": True,
            "IncludeUpfront": True,
            "IncludeRecurring": True,
            "IncludeOtherSubscription": False,
            "IncludeSupport": False,
            "IncludeDiscount": True,
            "UseAmortized": False,
        },
        "TimeUnit": "MONTHLY",
        "BudgetType": "COST",
        "FilterExpression": {
            "Tags": {
                "Key": PROJECT_TAG_KEY,
                "Values": [PROJECT_TAG_VALUE],
                "MatchOptions": ["EQUALS"],
            }
        },
    }


def build_notifications(email: str) -> list[dict[str, Any]]:
    email = email.strip()
    if not email or "@" not in email:
        raise ValueError("a valid budget notification email is required")
    subscriber = {
        "SubscriptionType": "EMAIL",
        "Address": email,
    }
    return [
        {
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 80.0,
                "ThresholdType": "PERCENTAGE",
            },
            "Subscribers": [subscriber],
        },
        {
            "Notification": {
                "NotificationType": "FORECASTED",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 100.0,
                "ThresholdType": "PERCENTAGE",
            },
            "Subscribers": [subscriber],
        },
    ]


def cost_allocation_tag_status(response: dict[str, Any]) -> str | None:
    for tag in response.get("CostAllocationTags", []):
        if tag.get("TagKey") == PROJECT_TAG_KEY:
            return tag.get("Status")
    return None


def _notification_key(
    notification: dict[str, Any],
) -> tuple[str, str, float, str | None]:
    return (
        notification["NotificationType"],
        notification["ComparisonOperator"],
        float(notification["Threshold"]),
        notification.get("ThresholdType"),
    )


def _is_not_found(exc: ClientError) -> bool:
    return exc.response.get("Error", {}).get("Code") == "NotFoundException"


def _reconcile_notifications(
    budgets: Any,
    account_id: str,
    budget_name: str,
    desired: list[dict[str, Any]],
) -> None:
    existing = budgets.describe_notifications_for_budget(
        AccountId=account_id,
        BudgetName=budget_name,
    ).get("Notifications", [])
    existing_by_key = {_notification_key(item): item for item in existing}
    desired_by_key = {
        _notification_key(item["Notification"]): item for item in desired
    }

    for key, notification in existing_by_key.items():
        if key not in desired_by_key:
            budgets.delete_notification(
                AccountId=account_id,
                BudgetName=budget_name,
                Notification=notification,
            )

    for key, item in desired_by_key.items():
        if key not in existing_by_key:
            budgets.create_notification(
                AccountId=account_id,
                BudgetName=budget_name,
                Notification=item["Notification"],
                Subscribers=item["Subscribers"],
            )
            continue

        existing_subscribers = budgets.describe_subscribers_for_notification(
            AccountId=account_id,
            BudgetName=budget_name,
            Notification=existing_by_key[key],
        ).get("Subscribers", [])
        existing_addresses = {
            (subscriber["SubscriptionType"], subscriber["Address"])
            for subscriber in existing_subscribers
        }
        desired_subscribers = {
            (subscriber["SubscriptionType"], subscriber["Address"])
            for subscriber in item["Subscribers"]
        }
        for subscriber in existing_subscribers:
            subscriber_key = (
                subscriber["SubscriptionType"],
                subscriber["Address"],
            )
            if subscriber_key not in desired_subscribers:
                budgets.delete_subscriber(
                    AccountId=account_id,
                    BudgetName=budget_name,
                    Notification=existing_by_key[key],
                    Subscriber=subscriber,
                )
        for subscriber in item["Subscribers"]:
            subscriber_key = (
                subscriber["SubscriptionType"],
                subscriber["Address"],
            )
            if subscriber_key not in existing_addresses:
                budgets.create_subscriber(
                    AccountId=account_id,
                    BudgetName=budget_name,
                    Notification=existing_by_key[key],
                    Subscriber=subscriber,
                )


def apply_budget(
    session: boto3.Session,
    account_id: str,
    budget: dict[str, Any],
    notifications: list[dict[str, Any]],
) -> str:
    cost_explorer = session.client("ce", region_name="us-east-1")
    tag_response = cost_explorer.list_cost_allocation_tags(
        TagKeys=[PROJECT_TAG_KEY],
    )
    status = cost_allocation_tag_status(tag_response)
    if status != "Active":
        raise RuntimeError(
            f"{PROJECT_TAG_KEY} cost allocation tag is not ACTIVE "
            f"(current status: {status or 'not discovered'})"
        )

    budgets = session.client("budgets", region_name="us-east-1")
    budget_name = budget["BudgetName"]
    try:
        budgets.describe_budget(
            AccountId=account_id,
            BudgetName=budget_name,
        )
    except ClientError as exc:
        if not _is_not_found(exc):
            raise
        budgets.create_budget(
            AccountId=account_id,
            Budget=budget,
            NotificationsWithSubscribers=notifications,
            ResourceTags=[
                {
                    "Key": PROJECT_TAG_KEY,
                    "Value": PROJECT_TAG_VALUE,
                }
            ],
        )
        return "created"

    budgets.update_budget(
        AccountId=account_id,
        NewBudget=budget,
    )
    _reconcile_notifications(
        budgets,
        account_id,
        budget_name,
        notifications,
    )
    return "updated"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--profile", default=os.getenv("AWS_PROFILE", "osworld-dev"))
    parser.add_argument("--budget-name", default=DEFAULT_BUDGET_NAME)
    parser.add_argument(
        "--amount",
        default=format(DEFAULT_BUDGET_AMOUNT, "f"),
    )
    parser.add_argument("--email", default=os.getenv("AWS_BUDGET_EMAIL", ""))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    amount = parse_budget_amount(args.amount)
    budget = build_budget(args.budget_name, amount)

    prepared = {
        "Budget": budget,
        "Notifications": (
            build_notifications(args.email)
            if args.email
            else "set --email or AWS_BUDGET_EMAIL before --apply"
        ),
    }
    print(json.dumps(prepared, indent=2, sort_keys=True))
    if not args.apply:
        print("PREPARED no AWS write calls were made")
        return 0
    if not args.email:
        raise ValueError("--email or AWS_BUDGET_EMAIL is required with --apply")

    session = boto3.Session(profile_name=args.profile, region_name="us-east-1")
    account_id = session.client("sts").get_caller_identity()["Account"]
    result = apply_budget(
        session,
        account_id,
        budget,
        build_notifications(args.email),
    )
    print(f"APPLIED {result} {budget['BudgetName']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
