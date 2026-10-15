"""Normalize visually checked audit expectations; never copy values from the catalog."""
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def main():
    samples = {}
    comparisons = 0
    files = ["ceiling_fire", "linear_outlets", "special_outlets", "acoustics_duct_dampers"]
    for name in files:
        report = json.loads((ROOT / f"docs/audits/{name}.json").read_text(encoding="utf-8"))
        for check in report.get("checks", report.get("sample_checks", [])):
            table = check.get("table", check.get("table_id"))
            row_id = check["row_id"]
            if name == "ceiling_fire":
                expected = {check["column"]: check["published"]}
            elif name == "linear_outlets":
                expected = check["published"]
            elif name == "special_outlets":
                expected = check["expected_published_values"]
            else:
                expected = check["expected"]
            comparisons += len(expected)
            sample = samples.setdefault(row_id, {"row_id": row_id, "table_id": table,
                "source_ref": check.get("source_ref", check.get("pdf_locator")),
                "audit": f"docs/audits/{name}.json", "expected": {}})
            assert sample["table_id"] == table
            for code, value in expected.items():
                if code in sample["expected"]:
                    assert sample["expected"][code] == value, (row_id, code)
                sample["expected"][code] = value
    fixture = {"date": "2026-10-15", "basis": "Four fresh-context source reviewers; rendered-PDF visual samples. See audit ledgers for method and limitations. Not exhaustive.",
        "comparisons_in_ledgers": comparisons, "unique_rows": len(samples),
        "unique_cells": sum(len(s["expected"]) for s in samples.values()),
        "samples": [samples[k] for k in sorted(samples)]}
    path = ROOT / "tests/fixtures/alsharqa_visual_samples.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in fixture.items() if k != "samples"}))


if __name__ == "__main__":
    main()
