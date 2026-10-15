import copy
import json
import sqlite3
from pathlib import Path

import pytest
from jsonschema import ValidationError
from pydantic import ValidationError as InputError

from supplier_atlas.ingestion import build, validate_package
from supplier_atlas.models import DiscoverRequest, GetRequest, SearchRequest
from supplier_atlas.query import Catalog, QueryError

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT / "datasets/alsharqa/catalog.json"
CAT = "air_outlets.ceiling_diffusers"
SUPPLY = "ceiling_diffuser.supply.v1"


@pytest.fixture
def catalog(tmp_path):
    db = tmp_path / "catalog.sqlite"
    build(PACKAGE, db)
    return Catalog(db, "test-key")


def get_rows(catalog, **kwargs):
    table = {"table_id": "alsharqa.scd.supply", **kwargs}
    return catalog.get(GetRequest(ids=["alsharqa.scd.6x6"], tables=[table]))["products"][0]["data"][0]


def test_reference_cells_and_bound_preservation(catalog):
    table = get_rows(catalog)
    assert table["rows"][0]["values"] == [63, .018, {"value": 18, "qualifier": "lt"}, 16, 4, 7]
    assert table["rows"][2]["values"] == [100, .046, 19, 25, 6, 11]
    assert table["rows"][-1]["values"] == [200, .186, 36, 50, 11, 15]
    assert table["context"]["room_effect_db"] == 8


def test_return_has_distinct_schema(catalog):
    result = catalog.get(GetRequest(ids=["alsharqa.scd.12x12"], tables=[{"table_id": "alsharqa.scd.return"}]))
    table = result["products"][0]["data"][0]
    assert [c["code"] for c in table["columns"]] == ["airflow", "pressure_drop", "nc"]
    assert table["rows"][1]["values"] == [300, .031, 23]
    assert table["rows"][-1]["values"] == [800, .220, 47]


def test_default_has_descriptors_not_rows(catalog):
    result = catalog.get(GetRequest(ids=["alsharqa.scd"]))["products"][0]
    assert result["data"] == []
    assert [t["row_count"] for t in result["tables"]] == [21, 21]
    assert len(result["variants"]) == 3


def test_same_row_and_same_variant(catalog):
    # 6x6 reaches 200 CFM, and has NC 19 elsewhere, but never at the same point.
    result = catalog.search(SearchRequest(category=CAT, properties=[{"field": "neck_width", "value": 6}],
        table={"schema_id": SUPPLY, "filters": [{"field": "airflow", "op": "gte", "value": 200},
                                                {"field": "nc", "op": "lte", "value": 19}]}))
    assert result["products"] == []


def test_search_matching_evidence(catalog):
    result = catalog.search(SearchRequest(category=CAT, fields=["neck_width"], table={"schema_id": SUPPLY,
        "filters": [{"field": "airflow", "value": 100}, {"field": "nc", "value": 19}]}))
    match = result["products"][0]
    assert match["matching_variant"] == "alsharqa.scd.6x6"
    assert match["evidence"]["rows"][0]["values"] == [100, 19]
    assert match["properties"]["neck_width"]["value"] == 6


def test_qualified_values_are_not_exact_numbers(catalog):
    assert not get_rows(catalog, filters=[{"field": "nc", "op": "lt", "value": 19}])["rows"]
    assert get_rows(catalog, filters=[{"field": "nc", "value": 19}])["rows"][0]["values"][0] == 100


def test_projection_retains_operating_axis_notes(catalog):
    result = get_rows(catalog, columns=["nc"])
    assert [c["code"] for c in result["columns"]] == ["airflow", "nc"]
    assert result["notes"] and result["context"] and result["source"]


def test_unit_conversion_and_wrong_units(catalog):
    match = catalog.search(SearchRequest(category=CAT, properties=[{"field": "neck_width", "value": 152.4, "unit": "mm"}]))
    assert match["products"][0]["matching_variant"] == "alsharqa.scd.6x6"
    with pytest.raises(QueryError, match="Incompatible unit"):
        catalog.search(SearchRequest(category=CAT, properties=[{"field": "neck_width", "value": 6, "unit": "Pa"}]))


def test_pagination_complete_and_bound_to_query(catalog):
    ids, cursor = [], None
    for _ in range(4):
        page = get_rows(catalog, limit=2, cursor=cursor)
        ids.extend(r["id"] for r in page["rows"])
        cursor = page["next_cursor"]
    assert len(ids) == len(set(ids)) == 7 and cursor is None
    cursor = get_rows(catalog, limit=2)["next_cursor"]
    result = catalog.get(GetRequest(ids=["alsharqa.scd.6x6"], tables=[{
        "table_id": "alsharqa.scd.supply", "limit": 2, "cursor": cursor, "columns": ["nc"]}]))
    assert "Invalid cursor" in result["products"][0]["error"]


def test_batch_partial_error(catalog):
    result = catalog.get(GetRequest(ids=["missing", "alsharqa.scd.9x9"]))
    assert result["products"][0]["error"] == "Product not found"
    assert result["products"][1]["properties"]["neck_area"]["value"] == .56


def test_unknown_field_and_injection_rejected(catalog):
    with pytest.raises(QueryError, match="Unknown"):
        catalog.search(SearchRequest(category=CAT, table={"schema_id": SUPPLY,
            "filters": [{"field": "airflow'); DROP TABLE products; --", "value": 1}]}))
    assert catalog.discover(DiscoverRequest())["categories"][0]["models"] == 1


def test_read_only_and_response_budget(catalog):
    with catalog.connect() as db, pytest.raises(sqlite3.OperationalError):
        db.execute("DELETE FROM products")
    catalog.max_bytes = 100
    with pytest.raises(QueryError, match="budget"):
        catalog.discover(DiscoverRequest())


def test_import_rebuild_no_duplicates(tmp_path):
    db = tmp_path / "catalog.sqlite"
    first, second = build(PACKAGE, db), build(PACKAGE, db)
    assert first == second and first["rows"] == 42
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT count(*) FROM products").fetchone()[0] == 4


@pytest.mark.parametrize("problem", ["duplicate", "variant", "unreviewed", "type", "extra"])
def test_invalid_import_rejected(problem):
    data = json.loads(PACKAGE.read_text())
    row = data["tables"][0]["rows"][0]
    if problem == "duplicate":
        data["tables"][0]["rows"].append(copy.deepcopy(row))
    elif problem == "variant":
        row["variant_id"] = "alsharqa.scd"
    elif problem == "unreviewed":
        row["review_status"] = "pending"
    elif problem == "type":
        row["values"]["airflow"] = "63 cfm"
    else:
        row["values"]["marketing"] = "best ever"
    with pytest.raises((ValueError, ValidationError)):
        validate_package(data)


def test_bad_source_hash_preserves_existing_snapshot(tmp_path):
    db = tmp_path / "catalog.sqlite"
    build(PACKAGE, db)
    original = db.read_bytes()
    (tmp_path / "alsharqa").mkdir()
    (tmp_path / "alsharqa/ceiling-diffusers.pdf").write_bytes(b"wrong")
    with pytest.raises(ValueError, match="fingerprint"):
        build(PACKAGE, db, tmp_path)
    assert original == db.read_bytes()


def test_request_limits():
    with pytest.raises(InputError):
        GetRequest(ids=["a"] * 6)
    with pytest.raises(InputError):
        SearchRequest(category=CAT, limit=0)


def test_heterogeneous_sparse_and_heavy_data(tmp_path):
    # A synthetic second category verifies generic behavior without publishing fake supplier facts.
    data = json.loads(PACKAGE.read_text())
    data["categories"].append({"id": "test.pumps", "label": "SYNTHETIC pumps"})
    for kind, name, parent in [("model", "test.pump", None), ("variant", "test.pump.a", "test.pump")]:
        data["products"].append({"id": name, "kind": kind, "parent_id": parent, "category_id": "test.pumps",
            "brand_key": "synthetic", "model_code": "TEST", "label": name, "values": {}, "source_ref": "alsharqa-p7"})
    data["schemas"].append({"id": "test.curve.v1", "category_id": "test.pumps", "label": "Synthetic", "version": 1,
        "columns": [{"code": "flow", "type": "number", "unit": "L/s"},
                    {"code": "head", "type": "number", "unit": "m", "required": False}],
        "row_key": ["flow"], "context_schema": {"type": "object"}})
    data["tables"].append({"id": "test.curve", "product_id": "test.pump", "schema_id": "test.curve.v1",
        "context": {}, "notes": ["Synthetic test only"], "source_ref": "alsharqa-p7", "rows": [
        {"id": f"test.{i}", "variant_id": "test.pump.a", "values": {"flow": i},
         "source_ref": "alsharqa-p7", "review_status": "accepted"} for i in range(5000)]})
    package = tmp_path / "test.json"
    package.write_text(json.dumps(data))
    db = tmp_path / "test.sqlite"
    build(package, db)
    catalog = Catalog(db)
    result = catalog.get(GetRequest(ids=["test.pump"], tables=[{"table_id": "test.curve", "limit": 10}]))
    table = result["products"][0]["data"][0]
    assert table["returned"] == 10 and table["next_cursor"]
    assert table["rows"][0]["values"][1] == {"status": "not_supplied"}
    assert len(json.dumps(result)) < 12000

