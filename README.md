# Savings Plan / RI Coverage Gap Report

Cross-references Savings Plan and Reserved Instance coverage against on-demand
spend and produces a report showing exactly which instance families/services
are paying full on-demand price when they shouldn't be.

## Why

Cost Explorer's coverage views are per-metric and don't merge SP + RI +
on-demand into a single "here's your gap, here's the estimated monthly
savings" view. This tool does that merge.

## Features

- Pulls Savings Plan utilization (`GetSavingsPlansUtilization`)
- Pulls RI coverage (`GetReservationCoverage`)
- Pulls on-demand spend by instance family (`GetCostAndUsage`)
- Computes coverage gap % and estimated monthly savings if closed
- Outputs markdown table or HTML report (Jinja2 template)

## Quickstart

```bash
pip install -e .
sp-ri-gap report --days 30 --output html --out-file coverage_gap.html
```

## Architecture

```
src/sp_ri_coverage/
├── aws_client.py   # Cost Explorer + Savings Plans API calls
├── gap.py          # coverage gap + savings estimation logic
├── report.py       # markdown / HTML rendering
└── cli.py          # entrypoint (argparse)
```

## Roadmap

- [ ] Add per-account breakdown (not just per-family)
- [ ] Support Compute Savings Plans vs. EC2 Instance Savings Plans distinction
- [ ] Recommend specific SP purchase commitment based on gap trend

## License

MIT — see [LICENSE](LICENSE).
