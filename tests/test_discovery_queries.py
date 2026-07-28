"""Integrity of the hardcoded discovery query lists.

These lists are the ONLY thing that finds new opportunities. On 2026-07-27 they
were 43 + 10 entries and produced all 148 of the run's new opportunities at
~2.7 per query, while ~1,650 credits of re-milling produced none. Expanding
them is the highest-yield lever in the system — which makes their correctness
worth pinning, because a duplicate id silently overwrites a cache entry and a
duplicate query string spends a credit to learn nothing.
"""

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VALID_GROUPS = {
    "JP", "CN", "DIASPORA",
    "JP_EDITORIAL", "JP_COMPETITION",
    "CN_EDITORIAL", "CN_COMPETITION",
    "JP_RESIDENCY", "JP_GRANT", "JP_BOOK", "CN_BOOK",
}


def load_list(filename, varname):
    tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == varname:
            return ast.literal_eval(node.value)
    raise AssertionError(f"{varname} not found in {filename}")


class QueryListIntegrityTests(unittest.TestCase):

    def setUp(self):
        self.jc = load_list("engines/japanese_chinese_discovery_engine.py", "QUERIES")
        self.gr = load_list("engines/grant_discovery_engine.py", "GRANT_QUERIES")

    def test_every_query_id_is_unique(self):
        """A duplicate id collides in the per-query cache — one silently
        suppresses the other on every subsequent run."""
        for name, qs in (("QUERIES", self.jc), ("GRANT_QUERIES", self.gr)):
            ids = [q["id"] for q in qs]
            dupes = {i for i in ids if ids.count(i) > 1}
            self.assertEqual(dupes, set(), f"{name} has duplicate ids: {dupes}")

    def test_no_duplicate_query_strings(self):
        """Two identical searches spend two credits to learn one thing."""
        for name, qs in (("QUERIES", self.jc), ("GRANT_QUERIES", self.gr)):
            strings = [q["q"].strip() for q in qs]
            dupes = {s for s in strings if strings.count(s) > 1}
            self.assertEqual(dupes, set(), f"{name} has duplicate queries: {dupes}")

    def test_every_entry_has_the_required_shape(self):
        for q in self.jc:
            self.assertTrue(q.get("id"), f"missing id: {q}")
            self.assertTrue(q.get("q", "").strip(), f"empty query: {q}")
            self.assertIn(q.get("group"), VALID_GROUPS, f"bad group: {q}")
            self.assertIn(q.get("lang"), ("ja", "zh", "en", "mixed"), f"bad lang: {q}")
            if "domains" in q:
                self.assertIsInstance(q["domains"], list)

    def test_grant_entries_have_the_required_shape(self):
        for q in self.gr:
            self.assertTrue(q.get("id"), f"missing id: {q}")
            self.assertTrue(q.get("q", "").strip(), f"empty query: {q}")

    def test_discovery_breadth_has_not_regressed(self):
        """The whole point of the 2026-07-28 expansion. If someone trims these
        lists back, the system quietly stops finding new things — which is the
        failure mode that prompted the change."""
        self.assertGreaterEqual(len(self.jc), 150,
                                "JP/CN discovery breadth regressed")
        self.assertGreaterEqual(len(self.gr), 35,
                                "grant discovery breadth regressed")


if __name__ == "__main__":
    unittest.main()
