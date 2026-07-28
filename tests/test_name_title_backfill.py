"""name/title backfill — the split-field pair at the identity level.

Found 2026-07-28: 41 live entries have `title` but no `name` (they predate the
name field) — among them National Watercolor Society International Open and
Japan International Watercolor Institute, i.e. real, valuable calls. Serving
paths mostly fall back (`name or title`), but every diff, dedup, or engine that
keys on one spelling silently drops them — same class as added_at/imported_at
and fee/fees. Backfilling both spellings at clean time kills the class instead
of patching each reader.
"""

import unittest

from recommendation_trust_cleaner import backfill_identity


class BackfillIdentityTests(unittest.TestCase):

    def test_title_only_entry_gains_name(self):
        opp = {"title": "National Watercolor Society International Open Exhibition"}
        changed = backfill_identity(opp)
        self.assertTrue(changed)
        self.assertEqual(opp["name"], opp["title"])

    def test_name_only_entry_gains_title(self):
        opp = {"name": "Some Call"}
        self.assertTrue(backfill_identity(opp))
        self.assertEqual(opp["title"], "Some Call")

    def test_entry_with_both_is_untouched(self):
        opp = {"name": "A", "title": "B — long form"}
        self.assertFalse(backfill_identity(opp))
        self.assertEqual(opp["name"], "A")
        self.assertEqual(opp["title"], "B — long form")

    def test_entry_with_neither_is_left_alone(self):
        opp = {"category": "x"}
        self.assertFalse(backfill_identity(opp))
        self.assertNotIn("name", opp)

    def test_empty_string_counts_as_missing(self):
        opp = {"name": "", "title": "Real Title"}
        self.assertTrue(backfill_identity(opp))
        self.assertEqual(opp["name"], "Real Title")


if __name__ == "__main__":
    unittest.main()
