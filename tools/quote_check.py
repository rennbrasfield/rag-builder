#!/usr/bin/env python3
"""Quote checker for RAG Builder build workspaces (Organizational Rules §8, rule 5).

Confirms that every active evidence entry's quote appears word for word in its source:
  - document evidence: the file in inputs/, whose SHA-256 must match build.yaml and the entry;
  - person evidence: the logged response file in correspondence/responses/, if one is given.

Read-only: it never changes build records. It prints a report and exits with status 1 if any
quote fails, so Claude can propose updates for the user to approve.

Usage:
    .venv/bin/python tools/quote_check.py <path-to-build-workspace>
"""

import hashlib
import html
import re
import sys
import zipfile
from pathlib import Path

import yaml

TEXT_SUFFIXES = {".txt", ".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".eml"}
HTML_SUFFIXES = {".html", ".htm"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_text(path):
    """Return (text, note). text is None when the format can't be read automatically."""
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return path.read_text(encoding="utf-8", errors="replace"), None
    if suffix in HTML_SUFFIXES:
        raw = path.read_text(encoding="utf-8", errors="replace")
        return html.unescape(re.sub(r"<[^>]+>", " ", raw)), None
    if suffix == ".docx":
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        xml = re.sub(r"</w:p>", "\n", xml)
        return html.unescape(re.sub(r"<[^>]+>", "", xml)), None
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # optional dependency
        except ImportError:
            return None, "PDF text extraction needs the optional 'pypdf' package; check this quote manually"
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if len(text.strip()) < 20:
            return None, "PDF has no readable text (likely a scan); needs OCR or a manual check"
        return text, None
    return None, f"unsupported file type '{suffix}'; check this quote manually"


def normalize_whitespace(text):
    """Collapse runs of whitespace (line breaks, tabs, spaces) only. Words are never changed."""
    return re.sub(r"\s+", " ", text).strip()


def check_quote(quote, text):
    """Return 'exact', 'whitespace', or None."""
    if quote in text:
        return "exact"
    if normalize_whitespace(quote) in normalize_whitespace(text):
        return "whitespace"
    return None


def load_yaml(path, key):
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get(key)


def catalog_ids(build):
    """Variable IDs from the catalog version recorded in build.yaml, if it can be found."""
    tool = (build or {}).get("tool") or {}
    tool_path, version = tool.get("path"), tool.get("variable_catalog")
    if not tool_path or not version or "{{" in str(tool_path):
        return None
    version_id = str(version).split("|")[-1].strip()
    for folder in ("custom-design", "archive"):
        candidate = Path(tool_path) / folder / f"Custom__RAG_Variable_Catalog__{version_id}.yaml"
        if candidate.exists():
            data = yaml.safe_load(candidate.read_text(encoding="utf-8"))
            return {v["id"] for v in data.get("variables", [])}
    return None


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    ws = Path(argv[1]).expanduser().resolve()
    if not (ws / "build.yaml").exists():
        print(f"ERROR: {ws} is not a build workspace (no build.yaml).")
        return 2

    build = yaml.safe_load((ws / "build.yaml").read_text(encoding="utf-8")) or {}
    inputs = {i.get("file"): i for i in (build.get("inputs") or [])}
    evidence = load_yaml(ws / "evidence.yaml", "evidence") or []
    known_ids = catalog_ids(build)

    results = {"PASS": [], "PASS (whitespace only)": [], "FAIL": [], "MANUAL CHECK": []}
    for ev in evidence:
        if ev.get("status", "active") != "active":
            continue
        eid, quote, src = ev.get("id", "?"), ev.get("quote") or "", ev.get("source") or {}
        problems = []

        if known_ids is not None:
            unknown = [v for v in (ev.get("supports") or []) if v not in known_ids]
            if unknown:
                problems.append(f"supports unknown variable IDs {unknown}")

        if src.get("type") == "document":
            rel = src.get("file")
            path = ws / rel if rel else None
            if not path or not path.exists():
                results["FAIL"].append((eid, f"source file not found: {rel}"))
                continue
            actual = sha256(path)
            recorded = (inputs.get(rel) or {}).get("sha256")
            if recorded is None:
                problems.append(f"{rel} has no fingerprint in build.yaml")
            elif recorded != actual:
                problems.append(f"{rel} has changed since intake (fingerprint mismatch)")
            if src.get("sha256") and src.get("sha256") != actual:
                problems.append("entry's fingerprint doesn't match the file")
        elif src.get("type") == "person":
            rel = src.get("response_file")
            if not rel:
                results["MANUAL CHECK"].append((eid, "statement has no logged response file to check against"))
                continue
            path = ws / rel
            if not path.exists():
                results["FAIL"].append((eid, f"response file not found: {rel}"))
                continue
        else:
            results["FAIL"].append((eid, f"unknown source type '{src.get('type')}'"))
            continue

        text, note = extract_text(path)
        if text is None:
            results["MANUAL CHECK"].append((eid, note))
            continue
        match = check_quote(quote, text)
        if match is None:
            problems.insert(0, f"quote not found in {rel}")
        if problems:
            results["FAIL"].append((eid, "; ".join(problems)))
        elif match == "exact":
            results["PASS"].append((eid, rel))
        else:
            results["PASS (whitespace only)"].append((eid, f"{rel} — line breaks/spacing differ; words match"))

    total = sum(len(v) for v in results.values())
    print(f"Quote check — {ws.name} — {total} active evidence entries")
    if known_ids is None:
        print("  (variable IDs not checked: catalog not found from build.yaml)")
    for label, items in results.items():
        if items:
            print(f"\n{label}: {len(items)}")
            for eid, detail in items:
                print(f"  {eid}: {detail}")
    return 1 if results["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
