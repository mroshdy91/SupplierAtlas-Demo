"""Validate reviewed import packages and atomically build immutable SQLite snapshots."""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


DDL = """
PRAGMA foreign_keys=ON;
CREATE TABLE catalog_release(id TEXT PRIMARY KEY, schema_version INTEGER, manifest_hash TEXT, coverage TEXT);
CREATE TABLE categories(id TEXT PRIMARY KEY, label TEXT NOT NULL);
CREATE TABLE properties(id TEXT PRIMARY KEY, definition TEXT NOT NULL);
CREATE TABLE category_properties(category_id TEXT REFERENCES categories, property_id TEXT REFERENCES properties,
    PRIMARY KEY(category_id,property_id));
CREATE TABLE products(id TEXT PRIMARY KEY, kind TEXT CHECK(kind IN ('model','variant')), parent_id TEXT REFERENCES
    products, category_id TEXT REFERENCES categories, brand_key TEXT, model_code TEXT, label TEXT);
CREATE TABLE documents(id TEXT PRIMARY KEY, metadata TEXT NOT NULL);
CREATE TABLE source_refs(id TEXT PRIMARY KEY, document_id TEXT REFERENCES documents, locator TEXT NOT NULL);
CREATE TABLE product_values(product_id TEXT REFERENCES products, property_id TEXT REFERENCES properties,
    value_json TEXT, source_ref_id TEXT REFERENCES source_refs, PRIMARY KEY(product_id,property_id));
CREATE TABLE table_schemas(id TEXT PRIMARY KEY, category_id TEXT REFERENCES categories, definition TEXT NOT NULL);
CREATE TABLE product_tables(id TEXT PRIMARY KEY, product_id TEXT REFERENCES products, schema_id TEXT REFERENCES
    table_schemas, context_json TEXT, notes_json TEXT, source_ref_id TEXT REFERENCES source_refs);
CREATE TABLE table_rows(id TEXT PRIMARY KEY, table_id TEXT REFERENCES product_tables, variant_id TEXT REFERENCES
    products, sequence INTEGER, values_json TEXT, source_ref_id TEXT REFERENCES source_refs,
    UNIQUE(table_id,sequence));
CREATE INDEX products_category ON products(category_id,parent_id,id);
CREATE INDEX row_table_variant ON table_rows(table_id,variant_id,sequence);
CREATE INDEX tables_owner_schema ON product_tables(product_id,schema_id);
"""


def cell_schema(column):
    base = {"type": column["type"]}
    if "enum" in column:
        base["enum"] = column["enum"]
    choices = [base, {"type": "object", "properties": {"status": {"enum":
        ["unknown", "not_supplied", "not_applicable"]}}, "required": ["status"], "additionalProperties": False}]
    if column["type"] in ("number", "integer"):
        choices.append({"type": "object", "properties": {"value": base,
            "qualifier": {"enum": ["lt", "lte", "gt", "gte"]}},
            "required": ["value", "qualifier"], "additionalProperties": False})
    return {"oneOf": choices}


def validate_package(data):
    """Reject unsupported, ambiguous and internally inconsistent imports before any write."""
    if data["format_version"] != 1:
        raise ValueError("Unsupported import format")
    encoded(data)  # rejects NaN/infinity
    for collection in ("categories", "properties", "products", "documents", "sources", "schemas", "tables"):
        ids = [x["id"] for x in data[collection]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate {collection} IDs")
    schemas = {s["id"]: s for s in data["schemas"]}
    products = {p["id"]: p for p in data["products"]}
    props = {p["id"]: p for p in data["properties"]}
    for p in products.values():
        if p["kind"] == "model" and p.get("parent_id") is not None:
            raise ValueError("Models cannot have parents")
        if p["kind"] == "variant":
            parent = products[p["parent_id"]]
            if parent["kind"] != "model" or parent["category_id"] != p["category_id"]:
                raise ValueError("Variant must belong to a model in the same category")
        for code, value in p.get("values", {}).items():
            Draft202012Validator(cell_schema(props[code])).validate(value)
    row_ids = set()
    for s in schemas.values():
        codes = [c["code"] for c in s["columns"]]
        if len(codes) != len(set(codes)) or any(not re.fullmatch(r"[a-z][a-z0-9_]*", c) for c in codes):
            raise ValueError("Invalid or duplicate column codes")
        if not s["row_key"] or not set(s["row_key"]) <= set(codes):
            raise ValueError("Invalid row key")
        Draft202012Validator.check_schema(s["context_schema"])
    for table in data["tables"]:
        schema = schemas[table["schema_id"]]
        owner = products[table["product_id"]]
        if owner["category_id"] != schema["category_id"]:
            raise ValueError("Table/category mismatch")
        Draft202012Validator(schema["context_schema"]).validate(table["context"])
        validator = Draft202012Validator({"type": "object", "properties":
            {c["code"]: cell_schema(c) for c in schema["columns"]},
            "required": [c["code"] for c in schema["columns"] if c.get("required", True)],
            "additionalProperties": False})
        points = set()
        for row in table["rows"]:
            if row.get("review_status") != "accepted":
                raise ValueError("Only reviewed accepted rows can be published")
            if row["id"] in row_ids:
                raise ValueError("Duplicate row ID")
            row_ids.add(row["id"])
            variant = products[row["variant_id"]]
            if variant["kind"] != "variant" or (variant["parent_id"] != owner["id"]
                    if owner["kind"] == "model" else variant["id"] != owner["id"]):
                raise ValueError("Row variant does not belong to table owner")
            validator.validate(row["values"])
            point = encoded([row["variant_id"], *[row["values"][k] for k in schema["row_key"]]])
            if point in points:
                raise ValueError("Duplicate operating point")
            points.add(point)


def build(package: Path, output: Path, source_root: Path | None = None):
    data = json.loads(package.read_text(encoding="utf-8"))
    validate_package(data)
    if source_root:
        for doc in data["documents"]:
            source = (source_root / doc["local_path"]).resolve()
            if not source.is_relative_to(source_root.resolve()):
                raise ValueError("Source path escapes source root")
            if hashlib.sha256(source.read_bytes()).hexdigest() != doc["sha256"]:
                raise ValueError("Source document fingerprint mismatch")
    digest = hashlib.sha256(encoded(data).encode()).hexdigest()
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(suffix=".sqlite", dir=output.parent)
    os.close(fd)
    db = None
    try:
        with sqlite3.connect(temp) as db:
            db.executescript(DDL)
            db.execute("INSERT INTO catalog_release VALUES(?,?,?,?)", (
                data["release"] + "+" + digest[:12], 1, digest, encoded(data["coverage"])))
            db.executemany("INSERT INTO categories VALUES(?,?)", [(x["id"], x["label"]) for x in data["categories"]])
            for p in data["properties"]:
                db.execute("INSERT INTO properties VALUES(?,?)", (p["id"], encoded(p)))
                for category in p["categories"]:
                    db.execute("INSERT INTO category_properties VALUES(?,?)", (category, p["id"]))
            for doc in data["documents"]:
                db.execute("INSERT INTO documents VALUES(?,?)", (doc["id"], encoded(doc)))
            for src in data["sources"]:
                db.execute("INSERT INTO source_refs VALUES(?,?,?)", (src["id"], src["document_id"], encoded(src)))
            for p in sorted(data["products"], key=lambda x: x["kind"] != "model"):
                db.execute("INSERT INTO products VALUES(?,?,?,?,?,?,?)", (p["id"], p["kind"], p.get("parent_id"),
                    p["category_id"], p["brand_key"], p["model_code"], p["label"]))
                for code, value in p.get("values", {}).items():
                    db.execute("INSERT INTO product_values VALUES(?,?,?,?)", (p["id"], code, encoded(value), p["source_ref"]))
            for s in data["schemas"]:
                db.execute("INSERT INTO table_schemas VALUES(?,?,?)", (s["id"], s["category_id"], encoded(s)))
            for table in data["tables"]:
                db.execute("INSERT INTO product_tables VALUES(?,?,?,?,?,?)", (table["id"], table["product_id"],
                    table["schema_id"], encoded(table["context"]), encoded(table["notes"]), table["source_ref"]))
                for n, row in enumerate(table["rows"]):
                    db.execute("INSERT INTO table_rows VALUES(?,?,?,?,?,?)", (row["id"], table["id"],
                        row["variant_id"], n, encoded(row["values"]), row["source_ref"]))
            if db.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Invalid catalog references")
        db.close()
        os.replace(temp, output)
    finally:
        if db is not None:
            db.close()
        if os.path.exists(temp):
            os.unlink(temp)
    return {"catalog": str(output), "version": data["release"] + "+" + digest[:12],
            "models": sum(p["kind"] == "model" for p in data["products"]),
            "variants": sum(p["kind"] == "variant" for p in data["products"]),
            "tables": len(data["tables"]), "rows": sum(len(t["rows"]) for t in data["tables"]),
            "source_hashes_verified": source_root is not None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    print(encoded(build(args.package, args.output, args.source_root)))


if __name__ == "__main__":
    main()
