"""Command-line entrypoint: `sp-ri-gap report ...`"""
from __future__ import annotations

import argparse

from sp_ri_coverage.aws_client import get_on_demand_cost_by_family, get_ri_coverage
from sp_ri_coverage.gap import build_gap_rows
from sp_ri_coverage.report import render_html, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sp-ri-gap")
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="Generate a coverage gap report")
    report.add_argument("--days", type=int, default=30)
    report.add_argument("--profile", type=str, default=None)
    report.add_argument("--output", choices=["markdown", "html"], default="markdown")
    report.add_argument("--out-file", type=str, default=None, help="Write to file instead of stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "report":
        ri_coverage = get_ri_coverage(days=args.days, profile=args.profile)
        on_demand = get_on_demand_cost_by_family(days=args.days, profile=args.profile)
        rows = build_gap_rows(ri_coverage, on_demand)

        content = render_html(rows) if args.output == "html" else render_markdown(rows)

        if args.out_file:
            with open(args.out_file, "w") as f:
                f.write(content)
        else:
            print(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
