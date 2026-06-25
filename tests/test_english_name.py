"""The English display-name extractor must not surface junk fragments (bare
years, generic category words) as a card's title — those showed up as cards
literally titled "2026" / "Zine" in the English UI."""
import unittest
import api


class ExtractEnglishNameTests(unittest.TestCase):
    def test_rejects_bare_year(self):
        # leading Latin run is just a year -> no usable English name; show the real one
        self.assertEqual(api._extract_english_name("2026年 日本の絵画展"), "")

    def test_rejects_generic_category_word(self):
        self.assertEqual(api._extract_english_name("ZINEフェス東京"), "")

    def test_keeps_real_latin_prefix(self):
        self.assertEqual(api._extract_english_name("TOKAS レジデンシー"), "TOKAS")

    def test_keeps_parenthetical_english(self):
        self.assertEqual(
            api._extract_english_name("日本水彩展（Japan Watercolor Exhibition）"),
            "Japan Watercolor Exhibition",
        )

    def test_pure_latin_needs_no_extraction(self):
        self.assertEqual(api._extract_english_name("Tokyo Art Book Fair"), "")

    def test_degenerate_helper(self):
        self.assertTrue(api._degenerate_en_name("2026"))
        self.assertTrue(api._degenerate_en_name("219"))
        self.assertTrue(api._degenerate_en_name("Zine"))
        self.assertFalse(api._degenerate_en_name("TOKAS"))
        self.assertFalse(api._degenerate_en_name("Japan Watercolor Society"))


if __name__ == "__main__":
    unittest.main()
