"""Integrity tests for the active Variable Catalog and Role Map in custom-design/.

These catch formatting slips that a person reading the file would miss but every tool would
inherit, such as a comma inside brackets splitting one option into two, or "yes"/"no"
silently becoming true/false.

Run from the repository root:
    .venv/bin/python -m unittest discover -s tests -v
"""

import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DESIGN = REPO / "custom-design"
BOOLEAN_FIELDS = {"one_way"}  # the only fields allowed to be true/false


def active(prefix):
    files = sorted(DESIGN.glob(f"{prefix}__v*.yaml"))
    if len(files) != 1:
        raise AssertionError(f"expected exactly one active {prefix} file, found {[f.name for f in files]}")
    return files[0], yaml.safe_load(files[0].read_text(encoding="utf-8"))


def walk(node, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk(value, path + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, path + (str(index),))
    else:
        yield path, node


class CatalogIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog_file, cls.catalog = active("Custom__RAG_Variable_Catalog")
        cls.rolemap_file, cls.rolemap = active("Custom__Role_Map")
        cls.variables = cls.catalog["variables"]
        cls.ids = [v["id"] for v in cls.variables]

    def test_metadata_matches_filename(self):
        version = self.catalog["metadata"]["version"]
        self.assertTrue(self.catalog_file.name.endswith(f"__{version}.yaml"))
        self.assertTrue(self.catalog["metadata"]["title"].endswith(f"| {version}"))

    def test_ids_are_unique(self):
        self.assertEqual(len(self.ids), len(set(self.ids)))

    def test_no_text_became_true_or_false(self):
        bad = [
            (v["id"], ".".join(p), val)
            for v in self.variables
            for p, val in walk(v)
            if isinstance(val, bool) and p[-1] not in BOOLEAN_FIELDS
        ]
        self.assertEqual(bad, [], "quote yes/no values so YAML keeps them as text")

    def test_no_text_was_split_at_a_comma(self):
        bad = [
            (v["id"], ".".join(p), val)
            for v in self.variables
            for p, val in walk(v)
            if isinstance(val, str) and val.count("(") != val.count(")")
        ]
        self.assertEqual(bad, [], "quote list items that contain commas")

    def test_required_fields_present(self):
        required = {
            "id", "name", "analysis", "one_way", "question", "plain_question", "plain_explanation",
            "why_it_matters", "answer_form", "where_to_find", "typical_authority",
            "typical_informants", "sufficient_answer", "default", "drives",
        }
        missing = {v["id"]: sorted(required - v.keys()) for v in self.variables if required - v.keys()}
        self.assertEqual(missing, {})

    def test_analysis_levels_in_range(self):
        bad = [v["id"] for v in self.variables if not (isinstance(v["analysis"], int) and 0 <= v["analysis"] <= 10)]
        self.assertEqual(bad, [])

    def test_cross_references_resolve(self):
        refs = {r for v in self.variables for key in ("related", "conflicts_with", "feeds") for r in v.get(key) or []}
        self.assertEqual(sorted(refs - set(self.ids)), [])

    def test_every_variable_has_an_authority(self):
        self.assertEqual([v["id"] for v in self.variables if not v["typical_authority"]], [])

    def test_roles_used_are_defined_in_role_map(self):
        defined = {r["id"] for r in self.rolemap["roles"]}
        used = {r for v in self.variables for r in v["typical_authority"] + v["typical_informants"]}
        used |= {o["role"] for v in self.variables for o in v.get("fallback_overrides") or []}
        self.assertEqual(sorted(used - defined), [])

    def test_role_map_lists_match_catalog(self):
        for role in self.rolemap["roles"]:
            rid = role["id"]
            with self.subTest(role=rid):
                self.assertEqual(role["typical_authority_for"],
                                 [v["id"] for v in self.variables if rid in v["typical_authority"]])
                self.assertEqual(role["typical_informant_for"],
                                 [v["id"] for v in self.variables if rid in v["typical_informants"]])


if __name__ == "__main__":
    unittest.main()
