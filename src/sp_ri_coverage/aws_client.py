"""Cost Explorer wrappers for Savings Plan utilization, RI coverage, and
on-demand spend by instance family."""
from __future__ import annotations

import datetime as dt

import boto3


def _window(days: int) -> tuple[str, str]:
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def get_savings_plans_utilization(days: int = 30, profile: str | None = None) -> dict:
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ce = session.client("ce")
    start, end = _window(days)
    return ce.get_savings_plans_utilization(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
    )


def get_ri_coverage(days: int = 30, profile: str | None = None) -> dict:
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ce = session.client("ce")
    start, end = _window(days)
    return ce.get_reservation_coverage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        GroupBy=[{"Type": "DIMENSION", "Key": "INSTANCE_TYPE_FAMILY"}],
    )


def get_on_demand_cost_by_family(days: int = 30, profile: str | None = None) -> dict:
    """On-demand spend grouped by instance type family.

    TODO: this currently groups by SERVICE as a stand-in — swap the GroupBy
    key to INSTANCE_TYPE_FAMILY once purchase-option filtering is added
    (Cost Explorer requires a Filter on PURCHASE_TYPE=OnDemand for this to
    be meaningful; add that filter here).
    """
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    ce = session.client("ce")
    start, end = _window(days)
    return ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        Filter={"Dimensions": {"Key": "PURCHASE_TYPE", "Values": ["On Demand Instances"]}},
        GroupBy=[{"Type": "DIMENSION", "Key": "INSTANCE_TYPE"}],
    )
