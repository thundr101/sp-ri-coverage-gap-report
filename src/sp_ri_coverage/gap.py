"""Merge SP utilization + RI coverage + on-demand spend into gap rows.

Each row represents one instance family and answers: "what % of this
family's usage is still on-demand, and what would closing that gap save
per month at typical SP discount rates?"
"""
from __future__ import annotations

from typing import Any

# Rough blended discount assumption for a 1yr No-Upfront Compute Savings Plan.
# TODO: pull actual discount % from the SP rate card / Price List API instead
# of hardcoding — this is a placeholder for the v0.1 estimate.
ASSUMED_SP_DISCOUNT = 0.28


def build_gap_rows(
    ri_coverage: dict[str, Any],
    on_demand: dict[str, Any],
) -> list[dict[str, Any]]:
    """Combine RI coverage % with on-demand spend to compute gap $ estimate.

    ri_coverage: raw response from get_ri_coverage()
    on_demand: raw response from get_on_demand_cost_by_family()
    """
    coverage_by_family: dict[str, float] = {}
    for group in ri_coverage.get("CoveragesByTime", [{}])[0].get("Groups", []):
        family = group["Attributes"].get("instanceTypeFamily", "Unknown")
        pct = float(
            group["Coverage"]["CoverageHours"]["CoverageHoursPercentage"]
        )
        coverage_by_family[family] = pct

    on_demand_by_family: dict[str, float] = {}
    for group in on_demand.get("ResultsByTime", [{}])[0].get("Groups", []):
        family = group["Keys"][0] if group.get("Keys") else "Unknown"
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        on_demand_by_family[family] = on_demand_by_family.get(family, 0.0) + amount

    rows: list[dict[str, Any]] = []
    for family, spend in on_demand_by_family.items():
        coverage_pct = coverage_by_family.get(family, 0.0)
        gap_pct = max(0.0, 100.0 - coverage_pct)
        estimated_monthly_savings = spend * (gap_pct / 100.0) * ASSUMED_SP_DISCOUNT

        rows.append(
            {
                "family": family,
                "coverage_pct": round(coverage_pct, 1),
                "gap_pct": round(gap_pct, 1),
                "on_demand_spend": round(spend, 2),
                "estimated_monthly_savings": round(estimated_monthly_savings, 2),
            }
        )

    rows.sort(key=lambda r: r["estimated_monthly_savings"], reverse=True)
    return rows
