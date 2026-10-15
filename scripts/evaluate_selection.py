"""Replay guided native engineering tasks, verify evidence, measure real MCP payloads.

Run after prepare/build. Optional evaluation dependency: tiktoken.
This is not a blinded agent trial or a proof of globally minimal tokens.
"""
import asyncio
import copy
import json
from pathlib import Path

from mcp import Client

from supplier_atlas.ingestion import encoded
from supplier_atlas.query import Catalog
from supplier_atlas.server import create_server

ROOT = Path(__file__).parents[1]


def row(table):
    return dict(zip([c["code"] for c in table["columns"]], table["rows"][0]["values"], strict=True))


def verify(results):
    ceiling = results[17]["products"][0]
    assert ceiling["matching_variant"] == "alsharqa.scd.6x6"
    assert row(ceiling["evidence"]) == {"airflow": 100, "pressure_drop": .046, "nc": 19, "throw_50fpm": 11}
    assert ceiling["evidence"]["context"]["room_effect_db"] == 8
    flow = results[23]["products"][0]["evidence"]
    assert row(flow) == {"slot_opening": 25, "airflow_per_length": 58, "static_pressure": 18, "nc": 16, "throw_0_5m_s": 4}
    assert flow["context"]["active_length_mm"] == 1200
    assert flow["context"]["room_absorption_db"] == 10
    assert flow["context"]["plenum_effect_included"] is False
    assert all(not results[i]["products"] for i in [15, 16, 18, 20, 21, 22, 25])
    assert "qualified bounds" in results[25]["empty_result_hint"]
    bound = row(results[28]["products"][0]["data"][0])
    assert bound["nc"] == {"value": 10, "qualifier": "lt"}
    sound = results[29]["products"][0]["data"]
    assert row(sound[0])["static_pressure_drop"] == .36
    assert row(sound[1])["static_pressure_loss"] == .211
    assert .211 * 249.08891 < 60 < .36 * 249.08891
    assert sound[0]["notes"] and sound[1]["notes"]
    slot = results[30]["products"][0]["data"]
    assert row(slot[0])["nc"] == 33
    assert slot[1]["context"]["pressure_operating_airflow_status"] == "not supplied"
    fire = results[26]["products"][0]["evidence"]
    assert row(fire) == {"leakage_class": "II", "temperature": 250}
    assert "not independently verified" in fire["context"]["status"]


async def main():
    import tiktoken

    transcript = json.loads((ROOT / "docs/evaluations/selection_native_before.json").read_text(encoding="utf-8"))
    encoding = tiktoken.get_encoding("cl100k_base")

    def tokens(value):
        return len(encoding.encode(value if isinstance(value, str) else encoded(value)))

    results, metrics, comparisons = [], [], []
    async with Client(create_server(Catalog(ROOT / "data/catalog.sqlite"))) as client:
        for index, call in enumerate(transcript["calls"]):
            response = await client.call_tool(call["tool"], {"request": call["request"]})
            assert not response.is_error, index
            result = response.structured_content
            results.append(result)
            metrics.append({"call": index, "scenario": call["scenario"], "tool": call["tool"],
                "request_tokens": tokens({"request": call["request"]}),
                "before_text_tokens": tokens(call["result"]),
                "after_text_tokens": tokens(response.content[0].text),
                "after_full_result_tokens": tokens(response.model_dump_json(by_alias=True))})
        verify(results)
        # Compare exactly the same selected engineering rows with an unfiltered,
        # full-column variant page. Retain context, notes and source in both paths.
        for index in [28, 29, 30, 31]:
            request = copy.deepcopy(transcript["calls"][index]["request"])
            for table in request["tables"]:
                for key in ["columns", "filters", "limit"]:
                    table.pop(key, None)
            response = await client.call_tool("get_products", {"request": request})
            assert not response.is_error
            broad = response.structured_content["products"][0]["data"]
            projected = results[index]["products"][0]["data"]
            for compact, full in zip(projected, broad, strict=True):
                assert all(compact[k] == full[k] for k in ["context", "notes", "source"])
                for selected in compact["rows"]:
                    original = next(r for r in full["rows"] if r["id"] == selected["id"])
                    values = dict(zip([c["code"] for c in full["columns"]], original["values"], strict=True))
                    assert selected["values"] == [values[c["code"]] for c in compact["columns"]]
            comparisons.append({"scenario": transcript["calls"][index]["scenario"],
                "projected_text_tokens": metrics[index]["after_text_tokens"],
                "unfiltered_variant_page_text_tokens": tokens(response.content[0].text),
                "unfiltered_has_more_pages": any(t["next_cursor"] is not None for t in broad),
                "identical_context_notes_sources_and_selected_cells": True})
    report = {"method": transcript["method"], "catalog_version": results[0]["catalog_version"],
        "measurement": "cl100k_base; actual SDK text and full CallToolResult measured separately. Baseline native results normalized to compact JSON. Client model-context/billing tokens may differ. No latency claim.",
        "scenario_checks_passed": 7, "calls": metrics, "projection_comparisons": comparisons,
        "discovery_text_tokens": sum(m["after_text_tokens"] for m in metrics if m["tool"] == "discover_catalog"),
        "warm_successful_searches": {"ceiling": metrics[17], "flowbar_70lps": metrics[23]},
        "rating_diagnostic_before": {"calls": 2, "text_tokens": metrics[26]["before_text_tokens"] + metrics[31]["before_text_tokens"]},
        "rating_diagnostic_after": {"calls": 1, "text_tokens": metrics[26]["after_text_tokens"]},
        "limitations": ["Guided agent had implementation context; no independent agent or other-client qualification.",
            "Seven scoped engineering tasks, not complete HVAC design or universal source validation.",
            "Qualified bounds still require inspection; no interpolation, certification verification or source conflict repair.",
            "Projection reduction is against bounded unfiltered variant pages, not full catalogs. Discovery/schema cache is tied to catalog version."]}
    (ROOT / "docs/SELECTION_EVALUATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "calls"}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
