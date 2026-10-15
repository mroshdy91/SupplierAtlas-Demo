"""Generic, bounded SQL queries against a read-only catalog snapshot."""
import base64
import hashlib
import hmac
import json
import secrets
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path

from .ingestion import encoded
from .models import DiscoverRequest, GetRequest, SearchRequest


class QueryError(ValueError):
    pass


UNITS = {
    "in": ("length", .0254), "mm": ("length", .001), "m": ("length", 1), "ft": ("length", .3048),
    "ft2": ("area", .09290304), "m2": ("area", 1),
    "cfm": ("flow", 1.69901079552), "L/s": ("flow", 3.6), "m3/s": ("flow", 3600),
    "m3/h": ("flow", 1),
    "inH2O": ("pressure", 249.08891), "Pa": ("pressure", 1), "NC": ("NC", 1),
    "mmH2O": ("pressure", 9.80665),
    "fpm": ("velocity", .00508), "m/s": ("velocity", 1),
    "cfm/ft": ("flow_per_length", .001548384), "L/s/m": ("flow_per_length", .001),
    "ft2/ft": ("area_per_length", .3048), "m2/m": ("area_per_length", 1),
    "h": ("time", 3600), "min": ("time", 60), "s": ("time", 1),
}
OPS = {"eq": "=", "lt": "<", "lte": "<=", "gt": ">", "gte": ">="}
EMPTY_NUMERIC_HINT = (
    "No matching published scalar row. Numeric filters exclude qualified bounds and missing cells; "
    "no interpolation. Relax a filter to inspect nearby points or bounds; an empty result is not a suitability verdict."
)


def comparison(expression, predicate, definition):
    value = predicate.value
    numeric = definition["type"] in ("number", "integer")
    if numeric:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise QueryError(f"{predicate.field} requires a numeric value")
        native = definition.get("unit")
        if predicate.unit and predicate.unit != native:
            source, target = UNITS.get(predicate.unit), UNITS.get(native)
            if not source or not target or source[0] != target[0]:
                raise QueryError(f"Incompatible unit for {predicate.field}; expected {native}")
            value = float(Decimal(str(value)) * Decimal(str(source[1])) / Decimal(str(target[1])))
        # Qualified values and explicit missing states are JSON objects, excluded here.
        return f"json_type({expression}) IN ('integer','real') AND json_extract({expression},'$') {OPS[predicate.op]} ?", [value]
    if predicate.unit or predicate.op != "eq":
        raise QueryError("Non-numeric fields support eq without units")
    expected = bool if definition["type"] == "boolean" else str
    if type(value) is not expected:
        raise QueryError(f"{predicate.field} requires {definition['type']}")
    return f"json_extract({expression},'$') = ?", [value]


class Catalog:
    def __init__(self, path, cursor_key=None, max_bytes=32768):
        self.path = Path(path).resolve()
        if not self.path.is_file():
            raise FileNotFoundError(f"Build the catalog first: {self.path}")
        self.cursor_key = (cursor_key or secrets.token_hex(32)).encode()
        self.max_bytes = max_bytes

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path.as_uri() + "?mode=ro&immutable=1", uri=True)
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    def release(self, db):
        row = db.execute("SELECT * FROM catalog_release").fetchone()
        return row["id"], json.loads(row["coverage"])

    def bounded(self, value):
        if len(encoded(value).encode()) > self.max_bytes:
            raise QueryError("Response exceeds byte budget; request fewer fields, tables, IDs or rows")
        return value

    def offset(self, cursor, query, version):
        if not cursor:
            return 0
        try:
            raw = base64.urlsafe_b64decode(cursor.encode())
            signature, body = raw[:32], raw[32:]
            if not hmac.compare_digest(signature, hmac.digest(self.cursor_key, body, "sha256")):
                raise ValueError()
            payload = json.loads(body)
            if payload["version"] != version or payload["query"] != hashlib.sha256(encoded(query).encode()).hexdigest():
                raise ValueError()
            if type(payload["offset"]) is not int or payload["offset"] < 0:
                raise ValueError()
            return payload["offset"]
        except (ValueError, KeyError, TypeError):
            raise QueryError("Invalid cursor: query, catalog version or server cursor key changed") from None

    def cursor(self, offset, query, version):
        body = encoded({"offset": offset, "query": hashlib.sha256(encoded(query).encode()).hexdigest(),
                        "version": version}).encode()
        return base64.urlsafe_b64encode(hmac.digest(self.cursor_key, body, "sha256") + body).decode()

    def page(self, rows, limit, offset, query, version):
        return {"returned": min(len(rows), limit), "next_cursor":
                self.cursor(offset + limit, query, version) if len(rows) > limit else None}

    def schema(self, db, schema_id):
        row = db.execute("SELECT definition FROM table_schemas WHERE id=?", (schema_id,)).fetchone()
        if not row:
            raise QueryError(f"Unknown schema: {schema_id}; use discover_catalog")
        return json.loads(row[0])

    def properties(self, db, category):
        return {r["id"]: json.loads(r["definition"]) for r in db.execute(
            "SELECT p.* FROM properties p JOIN category_properties cp ON cp.property_id=p.id WHERE cp.category_id=?",
            (category,))}

    def source(self, db, ref, expanded=False):
        row = db.execute("SELECT s.locator,d.metadata FROM source_refs s JOIN documents d ON d.id=s.document_id WHERE s.id=?",
                         (ref,)).fetchone()
        locator, doc = json.loads(row[0]), json.loads(row[1])
        value = {"id": ref, "label": locator["label"], "url": doc["url"]}
        if expanded:
            value.update({"locator": locator, "document": {k: v for k, v in doc.items() if k != "local_path"}})
        return value

    def discover(self, request: DiscoverRequest):
        with self.connect() as db:
            version, coverage = self.release(db)
            query = {"tool": "discover", **request.model_dump(exclude={"cursor"})}
            offset = self.offset(request.cursor, query, version)
            result = {"catalog_version": version, "coverage": coverage,
                      "numeric_filters": "Exact numeric cells only; qualified bounds excluded. Units default to schema units."}
            if request.schema_id:
                schema = self.schema(db, request.schema_id)
                if request.category and schema["category_id"] != request.category:
                    raise QueryError("Schema does not belong to category")
                if request.cursor:
                    raise QueryError("Schema detail is not paginated")
                result["schema"] = schema
            elif request.category:
                if not db.execute("SELECT 1 FROM categories WHERE id=?", (request.category,)).fetchone():
                    raise QueryError("Unknown category")
                result["properties"] = list(self.properties(db, request.category).values())
                rows = db.execute("SELECT id,definition FROM table_schemas WHERE category_id=? ORDER BY id LIMIT ? OFFSET ?",
                                  (request.category, request.limit+1, offset)).fetchall()
                result["schemas"] = [{"id": r["id"], "label": json.loads(r["definition"])["label"]} for r in rows[:request.limit]]
                result.update(self.page(rows, request.limit, offset, query, version))
            else:
                rows = db.execute("SELECT c.*, (SELECT COUNT(*) FROM products p WHERE p.category_id=c.id AND p.kind='model') models FROM categories c ORDER BY id LIMIT ? OFFSET ?",
                                  (request.limit+1, offset)).fetchall()
                result["categories"] = [dict(r) for r in rows[:request.limit]]
                result.update(self.page(rows, request.limit, offset, query, version))
            result["operators"] = list(OPS)
            return self.bounded(result)

    def row_filters(self, schema, predicates, alias="r"):
        columns = {c["code"]: c for c in schema["columns"]}
        clauses, params = [], []
        for predicate in predicates:
            if predicate.field not in columns:
                raise QueryError(f"Unknown table field: {predicate.field}")
            # Column codes were validated at import, never taken directly as SQL from the request.
            expression = f"json_quote(json_extract({alias}.values_json,'$.{predicate.field}'))"
            clause, values = comparison(expression, predicate, columns[predicate.field])
            clauses.append(clause)
            params.extend(values)
        return " AND ".join(clauses) or "1", params

    def values(self, db, product, fields, definitions):
        if fields is None:
            fields = list(definitions)
        unknown = set(fields) - definitions.keys()
        if unknown:
            raise QueryError(f"Unknown properties: {', '.join(sorted(unknown))}")
        rows = db.execute("SELECT * FROM product_values WHERE product_id IN (?,?) ORDER BY product_id=?",
                          (product["parent_id"], product["id"], product["id"])).fetchall()
        resolved = {r["property_id"]: r for r in rows}
        return {field: {"value": json.loads(resolved[field]["value_json"]),
                        "unit": definitions[field].get("unit"), "source_ref": resolved[field]["source_ref_id"]}
                if field in resolved else {"status": "not_supplied"} for field in fields}

    def search(self, request: SearchRequest):
        with self.connect() as db:
            version, coverage = self.release(db)
            defs = self.properties(db, request.category)
            if not db.execute("SELECT 1 FROM categories WHERE id=?", (request.category,)).fetchone():
                raise QueryError("Unknown category; use discover_catalog")
            if set(request.fields) - defs.keys():
                raise QueryError("Unknown requested summary properties")
            clauses, params = [], []
            if request.text:
                clauses.append("instr(lower(v.label || ' ' || v.model_code || ' ' || v.brand_key), lower(?)) > 0")
                params.append(request.text)
            for predicate in request.properties:
                if predicate.field not in defs:
                    raise QueryError(f"Unknown property: {predicate.field}")
                # Correlated lookup with explicit child values overriding parent, including unknown.
                code = predicate.field.replace("'", "''")
                expression = f"COALESCE((SELECT value_json FROM product_values WHERE product_id=v.id AND property_id='{code}'), (SELECT value_json FROM product_values WHERE product_id=v.parent_id AND property_id='{code}'))"
                clause, values = comparison(expression, predicate, defs[predicate.field])
                clauses.append(clause)
                params.extend(values)
            row_where, row_params, schema = "1", [], None
            if request.table:
                schema = self.schema(db, request.table.schema_id)
                if schema["category_id"] != request.category:
                    raise QueryError("Table schema/category mismatch")
                row_where, row_params = self.row_filters(schema, request.table.filters)
                clauses.append("EXISTS(SELECT 1 FROM table_rows r JOIN product_tables t ON t.id=r.table_id "
                               f"WHERE r.variant_id=v.id AND t.schema_id=? AND ({row_where}))")
                params.extend([request.table.schema_id, *row_params])
            where = " AND ".join(clauses) or "1"
            query = {"tool": "search", **request.model_dump(exclude={"cursor"})}
            offset = self.offset(request.cursor, query, version)
            sql = f"""SELECT * FROM (SELECT m.*, (SELECT v.id FROM products v
                WHERE (v.parent_id=m.id OR v.id=m.id) AND ({where}) ORDER BY v.id LIMIT 1) match_id
                FROM products m WHERE m.kind='model' AND m.category_id=?)
                WHERE match_id IS NOT NULL ORDER BY id LIMIT ? OFFSET ?"""
            rows = db.execute(sql, [*params, request.category, request.limit+1, offset]).fetchall()
            results = []
            for row in rows[:request.limit]:
                product = db.execute("SELECT * FROM products WHERE id=?", (row["match_id"],)).fetchone()
                item = {"id": row["id"], "label": row["label"]}
                if product["kind"] == "variant":
                    item["matching_variant"] = product["id"]
                if request.fields:
                    item["properties"] = self.values(db, product, request.fields, defs)
                if request.table:
                    evidence = db.execute("SELECT r.* FROM table_rows r JOIN product_tables t ON t.id=r.table_id "
                        f"WHERE r.variant_id=? AND t.schema_id=? AND ({row_where}) ORDER BY t.id,r.sequence LIMIT 1",
                        [product["id"], request.table.schema_id, *row_params]).fetchone()
                    table = db.execute("SELECT * FROM product_tables WHERE id=?", (evidence["table_id"],)).fetchone()
                    selected = list(dict.fromkeys(p.field for p in request.table.filters))
                    item["evidence"] = self.format_rows(db, table, schema, [evidence], selected or None)
                    item["evidence"]["scope"] = "One matching published operating point; other matches may exist."
                results.append(item)
            result = {"catalog_version": version, "coverage": coverage, "products": results,
                      **self.page(rows, request.limit, offset, query, version)}
            predicates = [*request.properties, *(request.table.filters if request.table else [])]
            if not results and offset == 0 and any(type(p.value) in (int, float) for p in predicates):
                result["empty_result_hint"] = EMPTY_NUMERIC_HINT
            return self.bounded(result)

    def format_rows(self, db, table, schema, rows, selected=None):
        available = {c["code"]: c for c in schema["columns"]}
        if selected is not None and set(selected) - available.keys():
            raise QueryError("Unknown table columns")
        # Include operating coordinates even when the caller projects outputs only.
        codes = list(dict.fromkeys([*schema["row_key"], *schema.get("context_columns", []),
                                   *(selected if selected is not None else available)]))
        return {"id": table["id"], "schema_id": schema["id"], "columns": [available[c] for c in codes],
            "context": json.loads(table["context_json"]), "notes": json.loads(table["notes_json"]),
            "source": self.source(db, table["source_ref_id"]),
            "rows": [{"id": r["id"], "variant_id": r["variant_id"],
                      "values": [json.loads(r["values_json"]).get(c, {"status": "not_supplied"}) for c in codes],
                      "source_ref": r["source_ref_id"]} for r in rows]}

    def get(self, request: GetRequest):
        with self.connect() as db:
            version, coverage = self.release(db)
            results = []
            for product_id in dict.fromkeys(request.ids):
                try:
                    product = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
                    if not product:
                        raise QueryError("Product not found")
                    item = dict(product)
                    item["properties"] = self.values(db, product, request.fields, self.properties(db, product["category_id"]))
                    tables = db.execute("SELECT * FROM product_tables WHERE product_id IN (?,?) ORDER BY id",
                                        (product_id, product["parent_id"])).fetchall()
                    item["tables"] = []
                    table_map = {t["id"]: t for t in tables}
                    if any(r.table_id not in table_map for r in request.tables):
                        raise QueryError("Requested table does not belong to this product")
                    for table in tables:
                        if request.tables and table["id"] not in {r.table_id for r in request.tables}:
                            continue
                        count = db.execute("SELECT COUNT(*) FROM table_rows WHERE table_id=? AND (?='model' OR variant_id=?)",
                                           (table["id"], product["kind"], product_id)).fetchone()[0]
                        item["tables"].append({"id": table["id"], "schema_id": table["schema_id"], "row_count": count})
                    variants = [] if request.tables else db.execute(
                        "SELECT id,label FROM products WHERE parent_id=? ORDER BY id LIMIT 21", (product_id,)).fetchall()
                    if variants:
                        item["variants"] = [dict(v) for v in variants[:20]]
                        item["variants_complete"] = len(variants) <= 20
                        if len(variants) > 20:
                            item["variant_hint"] = "Filter using search_products; this is a partial variant overview."
                    item["data"] = []
                    for table_request in request.tables:
                        table = table_map[table_request.table_id]
                        schema = self.schema(db, table["schema_id"])
                        where, params = self.row_filters(schema, table_request.filters)
                        query = {"tool": "get", "product_id": product_id, **table_request.model_dump(exclude={"cursor"})}
                        offset = self.offset(table_request.cursor, query, version)
                        rows = db.execute(f"SELECT r.* FROM table_rows r WHERE table_id=? AND (?='model' OR variant_id=?) AND ({where}) ORDER BY sequence LIMIT ? OFFSET ?",
                            [table["id"], product["kind"], product_id, *params, table_request.limit+1, offset]).fetchall()
                        formatted = self.format_rows(db, table, schema, rows[:table_request.limit], table_request.columns)
                        formatted.update(self.page(rows, table_request.limit, offset, query, version))
                        if not rows and offset == 0 and any(type(p.value) in (int, float) for p in table_request.filters):
                            formatted["empty_result_hint"] = EMPTY_NUMERIC_HINT
                        if request.include_sources:
                            refs = dict.fromkeys(r["source_ref_id"] for r in rows[:table_request.limit])
                            formatted["row_sources"] = [self.source(db, ref, True) for ref in refs]
                        item["data"].append(formatted)
                    if request.include_sources:
                        refs = {v["source_ref"] for v in item["properties"].values() if "source_ref" in v}
                        refs.update(t["source_ref_id"] for t in tables
                                    if not request.tables or t["id"] in {r.table_id for r in request.tables})
                        item["sources"] = [self.source(db, ref, True) for ref in sorted(refs)]
                    results.append(item)
                except QueryError as exc:
                    results.append({"id": product_id, "error": str(exc)})
            return self.bounded({"catalog_version": version, "coverage": coverage, "products": results})
