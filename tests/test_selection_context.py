"""Prevent compact evidence from dropping applicability conditions."""
import json
import runpy
from pathlib import Path

import pytest

from supplier_atlas.ingestion import validate_package
from supplier_atlas.models import DiscoverRequest, GetRequest, SearchRequest
from supplier_atlas.query import Catalog

ROOT = Path(__file__).parents[1]


def test_seven_engineering_scenarios():
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    methods = {"discover_catalog": (catalog.discover, DiscoverRequest),
               "search_products": (catalog.search, SearchRequest), "get_products": (catalog.get, GetRequest)}
    transcript = json.loads((ROOT / "docs/evaluations/selection_native_before.json").read_text(encoding="utf-8"))
    results = [methods[c["tool"]][0](methods[c["tool"]][1](**c["request"])) for c in transcript["calls"]]
    runpy.run_path(str(ROOT / "scripts/evaluate_selection.py"))["verify"](results)


def test_class_only_search_keeps_rating_temperature():
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    result = catalog.search(SearchRequest(category="dampers.fire_smoke", table={
        "schema_id": "alsharqa.sfsd-series.leakage-ratings.v1",
        "filters": [{"field": "leakage_class", "value": "II"}]}))
    evidence = result["products"][0]["evidence"]
    assert [c["code"] for c in evidence["columns"]] == ["leakage_class", "temperature"]
    assert evidence["rows"][0]["values"] == ["II", 250]
    assert evidence["columns"][1]["unit"] == "degF"
    assert "not independently verified" in evidence["context"]["status"]


def test_every_projection_retains_declared_context_and_notes():
    data = json.loads((ROOT / "datasets/alsharqa/catalog.json").read_text(encoding="utf-8"))
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    schemas = {s["id"]: s for s in data["schemas"]}
    for table in data["tables"]:
        schema = schemas[table["schema_id"]]
        if not schema.get("context_columns"):
            continue
        result = catalog.get(GetRequest(ids=[table["product_id"]], fields=[], tables=[{
            "table_id": table["id"], "columns": [schema["row_key"][0]], "limit": 1}]))["products"][0]["data"][0]
        codes = [c["code"] for c in result["columns"]]
        assert set(schema["context_columns"]) <= set(codes)
        assert result["context"] == table["context"]
        assert result["notes"] == table["notes"]
        assert result["rows"][0]["values"] == [table["rows"][0]["values"][c] for c in codes]


def test_empty_numeric_result_explains_bounds_without_changing_semantics():
    catalog = Catalog(ROOT / "data/catalog.sqlite")
    result = catalog.search(SearchRequest(category="air_outlets.flow_bar_diffusers", table={
        "schema_id": "alsharqa.sfb-ht.performance.v1", "filters": [
            {"field": "slot_opening", "value": 25}, {"field": "airflow_per_length", "value": 36},
            {"field": "nc", "op": "lte", "value": 15}]}))
    assert not result["products"]
    assert "qualified bounds" in result["empty_result_hint"]
    result = catalog.get(GetRequest(ids=["alsharqa.sfb-ht.25"], fields=[], tables=[{
        "table_id": "alsharqa.sfb-ht.performance", "columns": ["nc"],
        "filters": [{"field": "airflow_per_length", "value": 36}]}]))
    assert result["products"][0]["data"][0]["rows"][0]["values"][-1] == {"value": 10, "qualifier": "lt"}


@pytest.mark.parametrize("invalid", [["absent"], ["airflow", "airflow"], "airflow", [1]])
def test_invalid_context_dependencies_rejected(invalid):
    data = json.loads((ROOT / "datasets/alsharqa/catalog.json").read_text(encoding="utf-8"))
    data["schemas"][0]["context_columns"] = invalid
    with pytest.raises(ValueError, match="Invalid context columns"):
        validate_package(data)
