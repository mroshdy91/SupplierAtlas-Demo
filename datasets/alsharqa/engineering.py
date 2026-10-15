"""Package reviewed engineering transcriptions; never read OCR drafts at build time."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


def cell(value):
    if value is None:
        return {"status": "not_supplied"}
    if isinstance(value, str) and value.startswith(("<", ">")):
        return {"value": float(value[1:]), "qualifier": "lt" if value[0] == "<" else "gt"}
    return value


class Engineering:
    def __init__(self, data):
        self.data = data
        self.inventory = json.loads((ROOT / "source_inventory.json").read_text(encoding="utf-8"))
        self.docs = {}
        for document in self.inventory["documents"]:
            name = document["file"]
            identity = "alsharqa-ceiling" if name == "ceiling-diffusers.pdf" else "alsharqa-" + slug(Path(name).stem)
            self.docs[name] = identity
            if not any(d["id"] == identity for d in data["documents"]):
                data["documents"].append({"id": identity, "title": "Alsharqa " + Path(name).stem,
                    "published_date": None, "revision_label": None, "sha256": document["sha256"],
                    "local_path": "alsharqa/" + name, "url": document["url"]})

    def source(self, file, page, printed=None):
        identity = f"{self.docs[file]}-pdf{page}"
        existing = next((s for s in self.data["sources"] if s["id"] == identity), None)
        if existing is not None and printed is not None:
            existing["printed_page"] = printed
        if not any(s["id"] == identity for s in self.data["sources"]):
            self.data["sources"].append({"id": identity, "document_id": self.docs[file],
                "pdf_page": page, "printed_page": printed,
                "label": f"Alsharqa {Path(file).stem}, PDF p.{page}"})
        return identity

    def model(self, key, code, label, category, file, page):
        identity = "alsharqa." + key
        if not any(c["id"] == category for c in self.data["categories"]):
            self.data["categories"].append({"id": category, "label": category.split(".")[-1].replace("_", " ").title()})
        if not any(p["id"] == identity for p in self.data["products"]):
            self.data["products"].append({"id": identity, "kind": "model", "category_id": category,
                "brand_key": "alsharqa", "model_code": code, "label": "Alsharqa " + label,
                "values": {}, "source_ref": self.source(file, page)})
        return identity

    def variant(self, model, key, label, source):
        identity = model + "." + slug(str(key).replace(" x ", "x"))
        parent = next(p for p in self.data["products"] if p["id"] == model)
        if not any(p["id"] == identity for p in self.data["products"]):
            self.data["products"].append({"id": identity, "kind": "variant", "parent_id": model,
                "category_id": parent["category_id"], "brand_key": "alsharqa", "model_code": parent["model_code"],
                "label": parent["label"] + " " + label, "values": {}, "source_ref": source})
        return identity

    def table(self, model, key, label, columns, rows, file, page, *, context=None, notes=None,
              row_key=None, variant_columns=None, printed=None, row_pages=None):
        """Rows are published cells in column order. No interpolation or inferred cells."""
        source = self.source(file, page, printed)
        category = next(p["category_id"] for p in self.data["products"] if p["id"] == model)
        tid = model + "." + key
        definitions = []
        for definition in columns:
            code, unit, *rest = definition
            definitions.append({"code": code, "label": code.replace("_", " ").capitalize(),
                "type": rest[0] if rest else "number", "unit": unit})
        codes = [c["code"] for c in definitions]
        self.data["schemas"].append({"id": tid + ".v1", "category_id": category, "version": 1,
            "label": label, "columns": definitions, "row_key": row_key or [codes[0]],
            "context_schema": {"type": "object"}})
        table = {"id": tid, "product_id": model, "schema_id": tid + ".v1", "context": context or {},
            "notes": notes or [], "source_ref": source, "rows": []}
        for index, values in enumerate(rows):
            row_source = self.source(file, row_pages[index]) if row_pages else source
            if len(values) != len(columns):
                raise ValueError(f"Wrong column count: {tid} row {index + 1}")
            mapping = dict(zip(codes, map(cell, values), strict=True))
            vkeys = [codes[0]] if variant_columns is None else variant_columns
            vlabel = " x ".join(str(mapping[c]) for c in vkeys) if vkeys else "published reference"
            variant = self.variant(model, vlabel, vlabel, row_source)
            table["rows"].append({"id": f"{tid}.r{index + 1}", "variant_id": variant, "values": mapping,
                "source_ref": row_source, "review_status": "accepted"})
        self.data["tables"].append(table)
        return table


def expand(data):
    builder = Engineering(data)
    from reviewed_balljet import add_balljet
    from reviewed_ceiling import add_ceiling
    from reviewed_dimensions import add_dimensions
    from reviewed_disc import add_disc
    from reviewed_drum import add_drum
    from reviewed_duct import add_duct
    from reviewed_fire import add_fire
    from reviewed_flowbar import add_flowbar
    from reviewed_grilles import add_grilles
    from reviewed_jet import add_jet
    from reviewed_linearbar import add_linearbar
    from reviewed_louvers import add_louvers
    from reviewed_round import add_round
    from reviewed_slot import add_slot
    from reviewed_sound import add_sound
    from reviewed_swirl import add_swirl
    from reviewed_troffer import add_troffer
    add_dimensions(builder)
    add_flowbar(builder)
    add_balljet(builder)
    add_disc(builder)
    add_swirl(builder)
    add_round(builder)
    add_drum(builder)
    add_jet(builder)
    add_louvers(builder)
    add_slot(builder)
    add_sound(builder)
    add_troffer(builder)
    add_linearbar(builder)
    add_fire(builder)
    add_duct(builder)
    add_grilles(builder)
    add_ceiling(builder)
    data["release"] = "alsharqa-engineering-002"
    data["coverage"] = {
        "scope": "Engineering data across all 22 Alsharqa catalogs inventoried 2026-10-15.",
        "exceptions": "Source defects/unknown units are disclosed in table notes; obscured cells and the unlabeled VCD matrix are withheld. Curves are not digitized. No interpolation.",
        "content": "37 models, 76 tables, 3707 rows. Advertising and generic guidance excluded; publication dates unknown.",
    }
    return data
