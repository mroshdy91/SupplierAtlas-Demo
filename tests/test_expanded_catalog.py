"""Cross-family regressions for reviewed source cells, relationships and bounded output."""
import json
from pathlib import Path

import pytest

from supplier_atlas.models import DiscoverRequest, GetRequest, SearchRequest
from supplier_atlas.query import Catalog, QueryError

ROOT = Path(__file__).parents[1]


@pytest.fixture
def catalog():
    return Catalog(ROOT / "data/catalog.sqlite", "expanded-test-key")


def table(catalog, model, name, **kwargs):
    result = catalog.get(GetRequest(ids=[model], fields=[], tables=[{"table_id":model+"."+name, **kwargs}]))
    return result["products"][0]["data"][0]


def mapping(result, index=0):
    return dict(zip([c["code"] for c in result["columns"]],result["rows"][index]["values"],strict=True))


def test_all_official_catalogs_have_reviewed_data():
    data = json.loads((ROOT / "datasets/alsharqa/catalog.json").read_text(encoding="utf-8"))
    sources = {s["id"]:s for s in data["sources"]}
    represented = {sources[r["source_ref"]]["document_id"] for t in data["tables"] for r in t["rows"]}
    assert len(data["documents"]) == len(represented) == 22
    assert len(data["schemas"]) == len(data["tables"]) == 76
    assert sum(len(t["rows"]) for t in data["tables"]) == 3707
    assert all(r["review_status"] == "accepted" for t in data["tables"] for r in t["rows"])


def test_all_defaults_and_schema_details_fit_budget(catalog):
    data = json.loads((ROOT / "datasets/alsharqa/catalog.json").read_text(encoding="utf-8"))
    for p in data["products"]:
        if p["kind"] == "model":
            result = catalog.get(GetRequest(ids=[p["id"]]))
            assert "error" not in result["products"][0]
            assert not result["products"][0]["data"]
    for schema in data["schemas"]:
        assert catalog.discover(DiscoverRequest(schema_id=schema["id"]))["schema"]["id"] == schema["id"]
    for t in data["tables"]:
        result = table(catalog,t["product_id"],t["id"].removeprefix(t["product_id"]+"."))
        assert result["returned"] == min(20,len(t["rows"]))
        assert bool(result["next_cursor"]) == (len(t["rows"]) > 20)


def test_ceiling_cross_page_coordinates_and_unknown_cells(catalog):
    result = table(catalog,"alsharqa.scd","supply_patterns",columns=["airflow","side_airflow_b","throw_b_50fpm"],
        filters=[{"field":"size_label","value":"21x24"},{"field":"ways","value":3},
                 {"field":"neck_velocity","value":800}])
    row = mapping(result)
    assert row == {"size_label":"21x24","ways":3,"neck_velocity":800,"airflow":2800,
                   "side_airflow_b":1094,"throw_b_50fpm":40}
    assert result["rows"][0]["source_ref"].endswith("pdf18")
    malformed = table(catalog,"alsharqa.scd","supply_patterns",
        filters=[{"field":"size_label","value":"6x18"},{"field":"ways","value":2},
                 {"field":"neck_velocity","value":250}])
    assert mapping(malformed)["side_airflow_b"] == {"status":"unknown"}
    assert mapping(malformed)["side_airflow_a"] == {"status":"not_applicable"}
    ambiguous = table(catalog,"alsharqa.scd","supply_patterns",
        filters=[{"field":"size_label","value":"6x21 left / 9x21 right"}],limit=1)
    assert mapping(ambiguous)["neck_width"] == {"status":"unknown"}
    assert any("left" in note and "right" in note for note in ambiguous["notes"])


def test_source_error_is_not_repaired_or_treated_as_zero(catalog):
    result=table(catalog,"alsharqa.access-door","dimensions",filters=[{"field":"nominal_size","value":12}])
    assert mapping(result)["b"] == {"status":"unknown"}
    assert not table(catalog,"alsharqa.access-door","dimensions",filters=[{"field":"b","value":0}])["rows"]
    result=table(catalog,"alsharqa.scdp","supply",filters=[{"field":"neck_velocity","value":600}],limit=1)
    assert mapping(result)["pressure_drop"] == .94
    assert any("0.094" in note for note in result["notes"])


def test_big_matrix_pagination_is_complete_without_duplicates(catalog):
    cursor, ids = None, []
    while True:
        page=table(catalog,"alsharqa.scd","supply_patterns",columns=["nc"],limit=40,cursor=cursor)
        ids.extend(r["id"] for r in page["rows"])
        cursor=page["next_cursor"]
        if cursor is None:
            break
    assert len(ids) == len(set(ids)) == 763


def test_new_units_and_dimensionally_invalid_conversion(catalog):
    # Exact conversion: 40 m3/h = 40/3.6 L/s. Use exact integer 900 m3/h = 250 L/s.
    result=table(catalog,"alsharqa.mrp","flow-dimensions",
        filters=[{"field":"allowable_flow_max","value":250,"unit":"L/s"}])
    assert mapping(result)["diameter"] == 200
    result=table(catalog,"alsharqa.sfsd-series","closure-velocity",
        filters=[{"field":"velocity","value":10.16,"unit":"m/s"}])
    assert mapping(result)["velocity"] == 2000
    result=table(catalog,"alsharqa.sfsd-series","closed-pressure",
        filters=[{"field":"pressure","value":101.6,"unit":"mmH2O"}])
    assert mapping(result)["pressure"] == 4
    with pytest.raises(QueryError,match="Incompatible unit"):
        catalog.search(SearchRequest(category="dampers.fire_smoke",table={
            "schema_id":"alsharqa.sfsd-series.leakage-ratings.v1",
            "filters":[{"field":"temperature","value":350,"unit":"degC"}]}))


def test_rating_pairs_are_not_combined(catalog):
    result=catalog.search(SearchRequest(category="dampers.fire_smoke",table={
        "schema_id":"alsharqa.sfsd-series.leakage-ratings.v1",
        "filters":[{"field":"leakage_class","value":"II"},{"field":"temperature","value":350}]}))
    assert result["products"] == []
    result=catalog.search(SearchRequest(category="dampers.fire_smoke",table={
        "schema_id":"alsharqa.sfsd-series.leakage-ratings.v1",
        "filters":[{"field":"leakage_class","value":"II"},{"field":"temperature","value":250}]}))
    assert "not independently verified" in result["products"][0]["evidence"]["context"]["status"]
    assert result["products"][0]["evidence"]["notes"]


def test_projected_rows_omit_unrequested_catalog_and_deduplicate_sources(catalog):
    result=catalog.get(GetRequest(ids=["alsharqa.scd"],fields=[],include_sources=True,tables=[{
        "table_id":"alsharqa.scd.supply_patterns","columns":["nc"],"limit":20}]))["products"][0]
    assert "variants" not in result
    assert len(result["tables"]) == 1
    assert len(result["data"][0]["row_sources"]) == 1
    assert len(result["data"][0]["rows"]) == 20
