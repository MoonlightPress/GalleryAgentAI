"""The opportunity dedup must collapse the same event listed under variant
titles (Tokyo Art Book Fair appeared 4x: TOKIO/TOKYO, with/without year, with
an 'Exhibitor Call' suffix) WITHOUT merging genuinely different fairs."""
import unittest

import api


class DedupKeyTests(unittest.TestCase):
    def test_tabf_variants_collapse(self):
        variants = [
            "Tokyo Art Book Fair",
            "TOKIO ART BOOK FAIR 2026",
            "TOKYO ART BOOK FAIR 2026",
            "TOKYO ART BOOK FAIR 2026 Exhibitor Call",
        ]
        keys = {api._dedup_key(v) for v in variants}
        self.assertEqual(len(keys), 1, f"TABF variants did not collapse: {keys}")

    def test_different_fairs_stay_distinct(self):
        tabf     = api._dedup_key("TOKYO ART BOOK FAIR 2026")
        fukuoka  = api._dedup_key("Fukuoka Art Book Fair 2026")
        potluck  = api._dedup_key("Potluck Art Book Fair 2026 Exhibitor Call")
        bologna  = api._dedup_key("Bologna Children's Book Fair Illustrators Exhibition")
        self.assertEqual(len({tabf, fukuoka, potluck, bologna}), 4)

    def test_live_data_shows_one_tabf(self):
        # Integration: after dedup, the live set has a single Tokyo Art Book Fair.
        items = api.load_opportunities()
        tabf = [o for o in items
                if "tokyo art book fair" in (api._opp_name(o) or "").lower()
                or "tokio art book fair" in (api._opp_name(o) or "").lower()]
        self.assertLessEqual(len(tabf), 1, f"TABF still duplicated: {[api._opp_name(o) for o in tabf]}")


if __name__ == "__main__":
    unittest.main()
