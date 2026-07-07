from sp_ri_coverage.gap import build_gap_rows


def test_full_coverage_yields_zero_gap():
    ri_coverage = {
        "CoveragesByTime": [
            {
                "Groups": [
                    {
                        "Attributes": {"instanceTypeFamily": "m5"},
                        "Coverage": {"CoverageHours": {"CoverageHoursPercentage": "100.0"}},
                    }
                ]
            }
        ]
    }
    on_demand = {
        "ResultsByTime": [
            {
                "Groups": [
                    {"Keys": ["m5"], "Metrics": {"UnblendedCost": {"Amount": "500.0"}}}
                ]
            }
        ]
    }
    rows = build_gap_rows(ri_coverage, on_demand)
    assert rows[0]["gap_pct"] == 0.0
    assert rows[0]["estimated_monthly_savings"] == 0.0


def test_zero_coverage_estimates_savings():
    ri_coverage = {
        "CoveragesByTime": [
            {
                "Groups": [
                    {
                        "Attributes": {"instanceTypeFamily": "c6g"},
                        "Coverage": {"CoverageHours": {"CoverageHoursPercentage": "0.0"}},
                    }
                ]
            }
        ]
    }
    on_demand = {
        "ResultsByTime": [
            {
                "Groups": [
                    {"Keys": ["c6g"], "Metrics": {"UnblendedCost": {"Amount": "1000.0"}}}
                ]
            }
        ]
    }
    rows = build_gap_rows(ri_coverage, on_demand)
    assert rows[0]["gap_pct"] == 100.0
    assert rows[0]["estimated_monthly_savings"] > 0
