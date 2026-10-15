"""Regression expectations read independently from rendered supplier PDFs."""
import json
from pathlib import Path

from supplier_atlas.models import GetRequest
from supplier_atlas.query import Catalog

ROOT = Path(__file__).parents[1]


def test_visual_source_samples():
    fixture = json.loads((ROOT / "tests/fixtures/alsharqa_visual_samples.json").read_text(encoding="utf-8"))
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    with catalog.connect() as db:
        for sample in fixture["samples"]:
            row = db.execute("SELECT * FROM table_rows WHERE id=?", (sample["row_id"],)).fetchone()
            assert row is not None, sample["row_id"]
            assert row["table_id"] == sample["table_id"]
            assert row["source_ref_id"] == sample["source_ref"]
            actual = json.loads(row["values_json"])
            for code, expected in sample["expected"].items():
                assert actual[code] == expected, (sample["row_id"], code, actual[code], expected, sample["audit"])


def test_corrected_ceiling_series_and_source_note():
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    table = catalog.get(GetRequest(ids=["alsharqa.scd"], fields=[], tables=[{
        "table_id": "alsharqa.scd.supply_patterns", "columns": ["side_airflow_b"],
        "filters": [{"field": "size_label", "value": "21x24"}, {"field": "ways", "value": 1}]
    }]))["products"][0]["data"][0]
    codes = [c["code"] for c in table["columns"]]
    values = [dict(zip(codes, r["values"], strict=True)) for r in table["rows"]]
    assert [r["side_airflow_b"] for r in values] == [871, 1053, 1400, 1748, 2100, 2452, 2800]
    assert not any("2800 versus total" in note for note in table["notes"])


def test_published_temperature_and_geometry_context_survives_projection():
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    for model, page in [("alsharqa.afvd", 3), ("alsharqa.acvd-multiblade", 6)]:
        context = catalog.get(GetRequest(ids=[model], fields=[], tables=[{
            "table_id": model + ".dimensions", "columns": ["blade_count"], "limit": 1
        }]))["products"][0]["data"][0]["context"]
        assert context["operating_temperature_c"] == {"min": -40, "max": 100}
        assert context["technical_context_pdf_page"] == page
    context = catalog.get(GetRequest(ids=["alsharqa.splitter-damper"], fields=[], tables=[{
        "table_id": "alsharqa.splitter-damper.dimension-rules", "columns": ["a_min"], "limit": 1
    }]))["products"][0]["data"][0]["context"]
    assert context["trunk_division_rules"] == {
        "A": "((W3 * D3) / ((W2 * D2) + (W3 * D3))) * W1",
        "B": "((W2 * D2) / ((W2 * D2) + (W3 * D3))) * W1"}
    assert context["calculation_status"] == "published relationships only; not evaluated"
