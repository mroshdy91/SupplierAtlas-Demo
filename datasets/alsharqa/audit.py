"""Produce review coverage from the reviewed package, not from OCR guesses."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent


def main():
    data=json.loads((HERE / "catalog.json").read_text(encoding="utf-8"))
    inventory=json.loads((HERE / "source_inventory.json").read_text(encoding="utf-8"))
    sources={s["id"]:s for s in data["sources"]}
    docs={Path(d["local_path"]).name:d for d in data["documents"]}
    duplicate={
        ("Grilles-_-registers.pdf",12):"Same performance table as p.11; imported once.",
        ("Jet-diffusers.pdf",7):"Same drum performance as Drum-Diffuser.pdf p.3; imported under SDL once.",
        ("Round-Volume-Damper.pdf",4):"Same ACVD diameter schedule as G.S.V.D-Cat.pdf p.9; imported once.",
    }
    withheld={("VOLUM-DAMPER-_PRESSURE-DROP.pdf",4):
        "Unlabeled numeric matrix: no reliable quantity/unit definition or connection to the adjacent curves. Not exposed as area or correction factors."}
    coverage=["# Alsharqa engineering coverage", "",
        "Review scope: all 22 official catalogs listed on the supplier's products page on 2026-10-15 (248 PDF pages).",
        "37 model records, 758 variant/reference records, 76 technical tables, 3,707 rows. These counts include dimensional schedules, construction facts and performance points; they are not counts of certified/orderable products.",
        "", "All identified engineering-table pages were reviewed. Exceptions below are explicit; this is not a claim that every source value is correct or every graph was digitized.", "",
        "| Catalog | PDF pages with imported rows | Tables | Rows | Table-page disposition |",
        "|---|---|---:|---:|---|"]
    issues=["# Published-source qualifications", "",
        "These are source limitations and interpretation notes retained with the data. Manufacturer clarification remains necessary for ambiguous or contradictory values. No guessed corrections or interpolation were substituted.",
        "", "Unreadable/ill-typed cells are unknown; genuine blanks are not supplied; absent directions are not applicable. Readable suspect numbers remain literal with notes. Units are unspecified where the source does not establish them.", ""]
    for entry in inventory["documents"]:
        file=entry["file"]
        doc=docs[file]
        tables=[t for t in data["tables"] if sources[t["source_ref"]]["document_id"] == doc["id"]]
        rows=[r for t in tables for r in t["rows"]]
        pages=sorted({sources[r["source_ref"]]["pdf_page"] for r in rows})
        entry["status"]="reviewed; engineering data packaged with disclosed source exceptions"
        entry["imported_row_pages"]=pages
        entry["table_count"]=len(tables)
        entry["row_count"]=len(rows)
        dispositions=[]
        for page in entry["table_pages"]:
            key=(file,page)
            if key in withheld:
                state,reason="withheld",withheld[key]
            elif key in duplicate:
                state,reason="duplicate",duplicate[key]
            elif page in pages:
                state,reason="imported","Readable engineering cells reviewed; see table notes for cell-level qualifications."
            else:
                raise AssertionError(f"Unaccounted engineering table: {file} p.{page}")
            dispositions.append({"pdf_page":page,"status":state,"reason":reason})
        entry["table_review"]=dispositions
        special=[f"p.{d['pdf_page']} {d['status']}" for d in dispositions if d["status"] != "imported"]
        coverage.append(f"| [{file}]({entry['url']}) | {', '.join(map(str,pages))} | {len(tables)} | {len(rows)} | {'; '.join(special) or 'Imported'} |")
        notes=[(t["id"],t["notes"]) for t in tables if t["notes"]]
        if notes or special:
            issues.extend([f"## {file}",""])
            for d in dispositions:
                if d["status"] != "imported":
                    issues.extend([f"- PDF p.{d['pdf_page']}: {d['reason']}",""])
            for tid,table_notes in notes:
                issues.append(f"**{tid}**")
                issues.append("")
                issues.extend(f"- {note}" for note in table_notes)
                issues.append("")
    coverage.extend(["", "Curves without numeric tables, wiring diagrams and general design advice are not digitized into invented numerical rows. Concise conditions and construction facts needed to interpret tables are retained; promotional material is excluded.",
        "", "The original 42 SCD reference rows and IDs remain unchanged. Some new rows contain conflicting published values: see [source qualifications](SOURCE_ISSUES.md). The unlabeled VCD matrix and blue-obscured ACVD cells remain unresolved, explicitly outside usable numeric coverage.",
        "", "Original PDFs remain private verification material. URLs, page locators and SHA-256 fingerprints are in `datasets/alsharqa/source_inventory.json`. Printed publication dates/revisions are unknown; URL directory dates were not used as revisions."])
    (HERE / "source_inventory.json").write_text(json.dumps(inventory,indent=2)+"\n",encoding="utf-8")
    (ROOT / "docs/ALSHARQA_COVERAGE.md").write_text("\n".join(coverage)+"\n",encoding="utf-8")
    (ROOT / "docs/SOURCE_ISSUES.md").write_text("\n".join(issues)+"\n",encoding="utf-8")
    print(json.dumps({"documents":len(docs),"tables":len(data["tables"]),"rows":sum(len(t["rows"]) for t in data["tables"]),
                      "table_pages":dict(Counter(d["status"] for e in inventory["documents"] for d in e["table_review"]))}))


if __name__ == "__main__":
    main()
