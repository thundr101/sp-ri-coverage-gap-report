"""Render coverage gap rows as markdown or a standalone HTML report."""
from __future__ import annotations

from typing import Any

from jinja2 import Template

_HTML_TEMPLATE = Template(
    """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Savings Plan / RI Coverage Gap Report</title>
  <style>
    body { font-family: -apple-system, sans-serif; margin: 2rem; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
    th { background: rgb(35,47,62); color: white; }
    tr:nth-child(even) { background: #f7f7f7; }
    .savings { color: rgb(255,153,0); font-weight: bold; }
  </style>
</head>
<body>
  <h1>Savings Plan / RI Coverage Gap Report</h1>
  <table>
    <tr>
      <th>Instance Family</th>
      <th>Coverage %</th>
      <th>Gap %</th>
      <th>On-Demand Spend</th>
      <th>Est. Monthly Savings</th>
    </tr>
    {% for row in rows %}
    <tr>
      <td>{{ row.family }}</td>
      <td>{{ row.coverage_pct }}%</td>
      <td>{{ row.gap_pct }}%</td>
      <td>${{ "%.2f"|format(row.on_demand_spend) }}</td>
      <td class="savings">${{ "%.2f"|format(row.estimated_monthly_savings) }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>
"""
)


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = ["## Savings Plan / RI Coverage Gap Report\n"]
    lines.append("| Family | Coverage % | Gap % | On-Demand Spend | Est. Monthly Savings |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| {r['family']} | {r['coverage_pct']}% | {r['gap_pct']}% | "
            f"${r['on_demand_spend']:.2f} | ${r['estimated_monthly_savings']:.2f} |"
        )
    return "\n".join(lines) + "\n"


def render_html(rows: list[dict[str, Any]]) -> str:
    return _HTML_TEMPLATE.render(rows=rows)
