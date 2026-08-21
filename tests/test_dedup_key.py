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


class DedupKeeperTests(unittest.TestCase):
    """Which duplicate survives matters as much as collapsing them. Found
    2026-07-29 live: the Tokyo Cat I variants collapsed correctly, but the
    score-only keeper chose 第1期 (February deadline, PASSED) over 第2期
    (August 4, open) because the dead edition happened to score higher — the
    only actionable window disappeared from the site. Openness must outrank
    score; score breaks ties among equally-open entries."""

    def test_open_entry_beats_higher_scored_passed_entry(self):
        passed = {"name": "第1期 東京芸術文化創造発信助成 カテゴリーI",
                  "overall_score": 9.4, "deadline_past": True}
        open_  = {"name": "第2期 東京芸術文化創造発信助成 カテゴリーI",
                  "overall_score": 8.6, "deadline_past": False}
        kept = api._dedup_keep([passed, open_])
        self.assertEqual(len(kept), 1)
        self.assertFalse(kept[0]["deadline_past"])

    def test_score_still_breaks_ties_between_open_entries(self):
        a = {"name": "Some Call A-Edition", "overall_score": 7.0, "deadline_past": False}
        b = {"name": "Some Call B-Edition", "overall_score": 9.0, "deadline_past": False}
        b["name"] = a["name"]  # same key
        kept = api._dedup_keep([a, b])
        self.assertEqual(kept[0]["overall_score"], 9.0)

    def test_unkeyed_entries_are_never_merged(self):
        kept = api._dedup_keep([{"name": ""}, {"name": ""}])
        self.assertEqual(len(kept), 2)


if __name__ == "__main__":
    unittest.main()


class JapaneseTitleVariantTests(unittest.TestCase):
    """2026-08-21: the August pass put EIGHT cards on her banner that were
    really TWO competitions. 絵の現在 選抜展 appeared 3x and 公募―日本の絵画 5x,
    all with identical deadlines and fees. Three causes, all in _dedup_key:

      1. A parenthesised romanisation gloss survived, and the extractor
         transliterated the same name differently each time — "(Ienoima
         Selection Exhibition)" vs "(Enoteimu Selection Exhibition)".
      2. CJK dash variants were not stripped. Only ASCII '-' was; the real
         titles use ― (U+2015) and － (U+FF0D), so 公募―日本の絵画,
         公募－日本の絵画－ and 公募 日本の絵画 were three keys.
      3. The 公募 ("open call") qualifier and the 第N回 edition ordinal were
         kept, so 日本の絵画2026 / 公募―日本の絵画―2026 and 都展 / 第61回「都展」
         did not meet.
    """

    def test_romanisation_gloss_variants_collapse(self):
        variants = [
            "絵の現在 選抜展",
            "絵の現在 選抜展（Ienoima Selection Exhibition）",
            "絵の現在 選抜展 (Enoteimu Selection Exhibition)",
        ]
        keys = {api._dedup_key(v) for v in variants}
        self.assertEqual(len(keys), 1, f"did not collapse: {keys}")

    def test_nihon_no_kaiga_variants_collapse(self):
        variants = [
            "公募―日本の絵画 2026",
            "公募 日本の絵画 2026 (Japan Painting Open Call 2026)",
            "公募－日本の絵画 2026－ (Public Recruitment - Japanese Painting 2026)",
            "公募―日本の絵画―2026",
            "日本の絵画2026",
        ]
        keys = {api._dedup_key(v) for v in variants}
        self.assertEqual(len(keys), 1, f"did not collapse: {keys}")

    def test_edition_ordinal_folds(self):
        """第N回 is the edition number. Folding it is what lets an annual event
        be ONE thing across years instead of a new card every edition."""
        self.assertEqual(api._dedup_key("第61回「都展」"), api._dedup_key("都展"))
        self.assertEqual(api._dedup_key("第113回 日本水彩展"),
                         api._dedup_key("第114回 日本水彩展"))

    def test_single_word_paren_gloss_is_kept(self):
        """A one-word parenthetical is usually a CITY, not a romanisation —
        merging those would fuse genuinely different regional events."""
        self.assertNotEqual(api._dedup_key("水彩展（東京）"),
                            api._dedup_key("水彩展（大阪）"))
        self.assertNotEqual(api._dedup_key("水彩展 (Tokyo)"),
                            api._dedup_key("水彩展 (Osaka)"))

    def test_genuinely_different_japanese_calls_stay_apart(self):
        keys = {api._dedup_key(n) for n in (
            "公募―日本の絵画 2026",
            "絵の現在 選抜展",
            "第61回「都展」",
            "関西アートコンペ2026",
            "第36回 全日本アートサロン絵画大賞展",
        )}
        self.assertEqual(len(keys), 5, f"over-merged: {keys}")


class EditionAndAttributionTests(unittest.TestCase):
    """The English half of the same problem, still live on 2026-08-21 with THREE
    TABF cards. '16th edition' is the Latin twin of 第N回, and 'X 2026 by X' is
    an attribution clause the extractor appends when a listing page names its
    own organiser."""

    def test_ordinal_edition_folds(self):
        self.assertEqual(api._dedup_key("TOKYO ART BOOK FAIR 16th edition (2027)"),
                         api._dedup_key("Tokyo Art Book Fair"))
        self.assertEqual(api._dedup_key("3rd Edition Watercolour Open"),
                         api._dedup_key("Watercolour Open"))

    def test_by_organiser_clause_folds(self):
        self.assertEqual(api._dedup_key("TOKIO ART BOOK FAIR 2026 by TOKYO ART BOOK FAIR"),
                         api._dedup_key("Tokyo Art Book Fair"))

    def test_by_is_only_stripped_as_a_trailing_clause(self):
        """'Blessed by Fire' is a title, not an attribution — only fold 'by'
        when it introduces a trailing organiser clause."""
        self.assertNotEqual(api._dedup_key("Blessed by Fire"),
                            api._dedup_key("Blessed"))
