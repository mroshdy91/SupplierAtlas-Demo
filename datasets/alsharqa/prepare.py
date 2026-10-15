"""Deterministic packaging of visually reviewed transcription, not PDF extraction.

Source: Alsharqa ceiling diffusers, printed pages 7, 9, 19, 20.
The numeric arrays below are transcribed source values, not generated performance.
Run from any directory; creates catalog.json beside this file.
"""
import json
from pathlib import Path


def prepare():
    category = "air_outlets.ceiling_diffusers"
    model = "alsharqa.scd"
    # Source columns left to right. Throw pairs correspond to 100 and 50 fpm.
    # Only the reviewed four-way supply pattern is included.
    sizes = {
        6: {"area": .25, "q": [63, 75, 100, 125, 150, 175, 200],
            "snc": ["<18", "<18", 19, 23, 27, 32, 36],
            "side": [16, 19, 25, 31, 37, 44, 50],
            "throw": [[4, 7], [5, 9], [6, 11], [8, 12], [9, 13], [10, 14], [11, 15]],
            "rnc": ["<18", 18, 20, 24, 28, 33, 37]},
        9: {"area": .56, "q": [140, 169, 225, 281, 338, 394, 450],
            "snc": ["<18", 18, 22, 27, 31, 37, 40],
            "side": [35, 42, 56, 70, 84, 98, 112],
            "throw": [[7, 12], [8, 13], [10, 14], [12, 16], [13, 17], [14, 18], [15, 19]],
            "rnc": [18, 20, 24, 29, 33, 39, 42]},
        12: {"area": 1.0, "q": [250, 300, 400, 500, 600, 700, 800],
             "snc": ["<18", "<18", 19, 23, 27, 32, 36],
             "side": [63, 75, 100, 125, 150, 175, 200],
             "throw": [[11, 15], [12, 16], [14, 16], [15, 20], [16, 22], [17, 23], [18, 24]],
             "rnc": ["<18", 23, 29, 34, 38, 43, 47]},
    }
    supply_dp = [.018, .026, .046, .072, .104, .142, .186]
    return_dp = [.021, .031, .055, .086, .125, .170, .220]
    data = {"format_version": 1, "release": "alsharqa-demo-001", "coverage": {
        "scope": "Partial catalog: SCD square necks 6, 9 and 12 inches; four-way supply and return.",
        "excluded": "Other sizes/patterns/products not imported. No interpolation. Unknown publication date.",
        "source_pages": [7, 9, 19, 20]},
        "categories": [{"id": category, "label": "Ceiling diffusers"}],
        "properties": [], "products": [], "schemas": [], "tables": [],
        "documents": [{"id": "alsharqa-ceiling", "title": "Alsharqa Ceiling Diffusers",
            "published_date": None, "revision_label": None,
            "sha256": "6548714c85b082cda1206210774a42baea2fd164b7e1a39058a977e9c50e57df",
            "local_path": "alsharqa/ceiling-diffusers.pdf",
            "url": "https://alsharqa.com/wp-content/uploads/2025/04/ceiling-diffusers.pdf"}],
        "sources": []}
    for code, label, unit in [("neck_width", "Nominal neck width", "in"),
                              ("neck_height", "Nominal neck height", "in"),
                              ("neck_area", "Published neck area", "ft2")]:
        data["properties"].append({"id": code, "code": code, "label": label, "type": "number",
            "unit": unit, "categories": [category]})
    data["products"].append({"id": model, "kind": "model", "category_id": category,
        "brand_key": "alsharqa", "model_code": "SCD", "label": "Alsharqa square ceiling diffuser",
        "values": {}, "source_ref": "alsharqa-p7"})
    for page in [7, 9, 19, 20]:
        data["sources"].append({"id": f"alsharqa-p{page}", "document_id": "alsharqa-ceiling",
            "pdf_page": page, "printed_page": str(page), "label": f"Alsharqa ceiling diffusers p.{page}"})
    for size, raw in sizes.items():
        data["products"].append({"id": f"{model}.{size}x{size}", "kind": "variant", "parent_id": model,
            "category_id": category, "brand_key": "alsharqa", "model_code": "SCD",
            "label": f"Alsharqa SCD {size} x {size} in", "values": {"neck_width": size,
            "neck_height": size, "neck_area": raw["area"]}, "source_ref": "alsharqa-p9"})
    for mode, page in [("supply", 9), ("return", 19)]:
        schema_id = f"ceiling_diffuser.{mode}.v1"
        columns = [{"code": "airflow", "label": "Total airflow", "type": "number", "unit": "cfm", "role": "input"},
            {"code": "pressure_drop", "label": f"{mode.title()} pressure drop", "type": "number", "unit": "inH2O", "role": "output"},
            {"code": "nc", "label": f"{mode.title()} room noise criterion", "type": "number", "unit": "NC", "role": "output"}]
        context = {"mode": mode, "room_effect_db": 8}
        notes = ["NC is the room noise criterion based on an 8 dB room effect; bounds are preserved."]
        if mode == "supply":
            context.update({"pattern": "4-way", "directions": "A and B have equal side airflow and throw",
                            "throw_terminal_velocities_fpm": [100, 50]})
            columns += [{"code": "side_airflow", "label": "Side airflow (A and B)", "type": "number", "unit": "cfm", "role": "output"},
                {"code": "throw_100fpm", "label": "Throw at 100 fpm terminal velocity", "type": "number", "unit": "ft", "role": "output"},
                {"code": "throw_50fpm", "label": "Throw at 50 fpm terminal velocity", "type": "number", "unit": "ft", "role": "output"}]
            notes.append("Throw values apply to the four-way pattern. Published rounding of side airflow is retained.")
        else:
            context["pattern_applicability"] = "Square/rectangular core styles with 1, 2, 3 or 4 ways (p.20)."
            notes.append("Return interpretation uses p.20 notes; its pressure symbol says s while table heading says R.")
        data["schemas"].append({"id": schema_id, "category_id": category, "version": 1,
            "label": f"{mode.title()} performance", "columns": columns, "row_key": ["airflow"],
            "context_schema": {"type": "object", "required": ["mode", "room_effect_db"]}})
        table = {"id": f"{model}.{mode}", "product_id": model, "schema_id": schema_id,
            "context": context, "notes": notes, "source_ref": f"alsharqa-p{page}", "rows": []}
        for size, raw in sizes.items():
            for n, q in enumerate(raw["q"]):
                nc = raw["snc" if mode == "supply" else "rnc"][n]
                values = {"airflow": q, "pressure_drop": (supply_dp if mode == "supply" else return_dp)[n],
                    "nc": {"value": 18, "qualifier": "lt"} if nc == "<18" else nc}
                if mode == "supply":
                    values.update({"side_airflow": raw["side"][n], "throw_100fpm": raw["throw"][n][0],
                                   "throw_50fpm": raw["throw"][n][1]})
                ref = f"alsharqa-p{page}-{size}x{size}-c{n+1}"
                data["sources"].append({"id": ref, "document_id": "alsharqa-ceiling", "pdf_page": page,
                    "printed_page": str(page), "label": f"Alsharqa p.{page}, {size}x{size}, column {n+1}",
                    "table": f"{mode} performance", "size_in": [size, size], "operating_column": n+1,
                    "notes_pages": [9] if mode == "supply" else [20]})
                table["rows"].append({"id": f"{model}.{mode}.{size}x{size}.{n+1}",
                    "variant_id": f"{model}.{size}x{size}", "values": values,
                    "source_ref": ref, "review_status": "accepted"})
        data["tables"].append(table)
    return data


if __name__ == "__main__":
    Path(__file__).with_name("catalog.json").write_text(json.dumps(prepare(), indent=2) + "\n", encoding="utf-8")

