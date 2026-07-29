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


class TokyoGrantVariantTests(unittest.TestCase):
    """2026-07-28/29: the Tokyo Grant Program appeared as FIVE simultaneous
    cards for Category I and three for Category II — the July run's discovery
    scraped every title spelling as a separate entry, and _dedup_key kept them
    apart because it didn't strip fullwidth square brackets ［］, didn't fold
    Unicode roman numerals (Ⅲ vs III), and treated period/qualifier tokens
    (第2期, 単年助成, 年度) as distinguishing. Categories must still stay
    distinct — I vs II vs III are genuinely different grants."""

    CAT1 = [
        "2026年度 東京芸術文化創造発信助成 カテゴリーI（芸術創造活動）",
        "2026年度 東京芸術文化創造発信助成 カテゴリーI（単年助成）芸術創造活動",
        "2026年度 東京芸術文化創造発信助成 カテゴリーI［単年助成］芸術創造活動",
        "2026年度 第1期 東京芸術文化創造発信助成 カテゴリーI［単年助成］芸術創造活動",
        "2026年度 第2期 東京芸術文化創造発信助成 カテゴリーI［単年助成］芸術創造活動",
    ]
    CAT2 = [
        "2026年度 東京芸術文化創造発信助成 カテゴリーII（芸術創造活動）",
        "2026年度 東京芸術文化創造発信助成 カテゴリーII（長期助成）芸術創造活動",
        "2026年度 東京芸術文化創造発信助成 カテゴリーII［長期助成］芸術創造活動",
    ]

    def test_category_one_variants_collapse(self):
        keys = {api._dedup_key(t) for t in self.CAT1}
        self.assertEqual(len(keys), 1, keys)

    def test_category_two_variants_collapse(self):
        keys = {api._dedup_key(t) for t in self.CAT2}
        self.assertEqual(len(keys), 1, keys)

    def test_categories_stay_distinct(self):
        k1 = api._dedup_key(self.CAT1[0])
        k2 = api._dedup_key(self.CAT2[0])
        k3 = api._dedup_key("2026年度 東京芸術文化創造発信助成 カテゴリーⅢ［長期助成］創造環境向上活動")
        self.assertEqual(len({k1, k2, k3}), 3)

    def test_unicode_roman_numerals_fold_to_ascii(self):
        a = api._dedup_key("カテゴリーⅢ 創造環境向上活動")
        b = api._dedup_key("カテゴリーIII 創造環境向上活動")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
