"""A why-line must say something that could only be about her.

2026-09-04: the three Today's Focus cards — the first thing she reads — were
carrying the opportunity's own catalog summary as the reason it fitted her.
"以AQYLA水性丙烯颜料为指定媒材的绘画比赛，适合水彩及插画艺术家参与" describes a paint
competition; nothing in it has ever been true of her in particular.

The rule these tests hold: every why-line that reaches the card face contains
at least one clause anchored in her practice, her record or her situation.
Two places enforce it — the generator (engines/why_it_fits_engine.is_weak)
rewrites lines that lack the clause, and the serve-time guard (api.shape_card)
keeps one off the card face if it is shipped anyway.
"""
import unittest

from engines.why_hook import has_personal_hook, is_boilerplate, why_line_problem
from engines.why_it_fits_engine import MAX_WHY_CHARS, is_weak, meta_problem, sanitize


class HookDetectionTests(unittest.TestCase):
    def test_catalog_sentences_have_no_hook(self):
        """The three lines the review caught, in the language she reads."""
        for line in (
            "Water-based paint competition specifically for AQYLA acrylic paint, "
            "relevant for watercolor and illustration artists",
            "以AQYLA水性丙烯颜料为指定媒材的绘画比赛，适合水彩及插画艺术家参与。",
            "面向国际视觉艺术家，覆盖绘画、素描及综合媒介等类别，资金使用不受限制。",
            "A Tokyo gallery showing emerging artists in painting and drawing.",
        ):
            self.assertFalse(has_personal_hook(line), line)

    def test_category_word_alone_is_not_a_hook(self):
        """水彩 / watercolor describing the CONTEST is not a clause about her."""
        self.assertFalse(has_personal_hook("An open call for watercolor painters in Tokyo."))
        self.assertFalse(has_personal_hook("面向东京水彩画家的公开征集。"))

    def test_her_practice_beside_a_possessive_is_a_hook(self):
        for line in (
            "Consignment is free — your daily watercolor diary fits their shelf.",
            "你从 2020 年起的每日水彩日记直接符合投稿格式。",
            "2020年から続くあなたの毎日の水彩日記が応募形式に合う。",
        ):
            self.assertTrue(has_personal_hook(line), line)

    def test_her_record_is_a_hook_without_a_possessive(self):
        for line in (
            "Colour Diary already exists in artist-book format.",
            "ACC accepts Chinese nationals for its Mainland China track.",
            "明确接受学生申请，随时可投。",
        ):
            self.assertTrue(has_personal_hook(line), line)

    def test_boilerplate_is_caught_even_with_an_anchor_word(self):
        self.assertTrue(is_boilerplate("适合水彩及插画艺术家参与"))
        self.assertTrue(is_boilerplate("Open to all artists, relevant for watercolor and "
                                       "illustration artists."))

    def test_empty_line_is_a_problem_not_a_pass(self):
        self.assertEqual(why_line_problem(""), "empty")
        self.assertEqual(why_line_problem("你的水彩日记正好合适。"), "")


class GeneratorWeaknessTests(unittest.TestCase):
    def test_summary_echo_is_weak(self):
        opp = {"one_sentence": "A juried watercolor open call in Tokyo.",
               "why_this_fits_short": "A juried watercolor open call in Tokyo."}
        self.assertTrue(is_weak(opp)[0])

    def test_line_without_her_is_weak(self):
        opp = {"one_sentence": "A juried open call.",
               "why_this_fits_short": "An international juried exhibition open to painters "
                                      "working in any medium, with a modest entry fee and a "
                                      "September deadline."}
        weak, reason = is_weak(opp)
        self.assertTrue(weak)
        self.assertIn("her-specific", reason)

    def test_line_with_her_in_it_is_kept(self):
        opp = {"one_sentence": "A juried open call.",
               "why_this_fits_short": "Free to enter and open to un-represented painters — "
                                      "send 4-6 pages straight from your daily watercolor diary."}
        self.assertEqual(is_weak(opp), (False, ""))

    def test_english_hook_does_not_excuse_a_generic_chinese_line(self):
        """Chinese is the language she reads; a hook only she never sees is none."""
        opp = {"one_sentence": "A juried open call.",
               "why_this_fits_short": "Send 4-6 pages from your daily watercolor diary.",
               "why_it_fits_zh": "面向国际视觉艺术家的公开征集，涵盖绘画与综合媒介。"}
        weak, reason = is_weak(opp)
        self.assertTrue(weak)
        self.assertIn("zh", reason)

    def test_a_line_too_long_for_the_card_is_weak(self):
        opp = {"one_sentence": "A juried open call.",
               "why_this_fits_short": "Your daily watercolor diary fits this. " +
                                      "Padding sentence. " * 30}
        weak, reason = is_weak(opp)
        self.assertTrue(weak)
        self.assertIn("too long", reason)
        self.assertGreater(len(opp["why_this_fits_short"]), MAX_WHY_CHARS)


class SanitizeTests(unittest.TestCase):
    """The card prints the model's text verbatim — so the model's asides print too."""

    def test_a_trailing_character_count_is_stripped(self):
        """Asking the model to count characters gets the count back in the answer."""
        self.assertEqual(
            sanitize("Your daily watercolor diary fits their shelf.\n\n(174 characters)"),
            "Your daily watercolor diary fits their shelf.")
        self.assertEqual(
            sanitize("你的每日水彩日记正合适。（86字）"), "你的每日水彩日记正合适。")

    def test_markdown_emphasis_is_stripped(self):
        """The card renders plain text, so *Colour Diary* arrives with its asterisks."""
        self.assertEqual(
            sanitize("Your *Colour Diary* grew out of the daily pages."),
            "Your Colour Diary grew out of the daily pages.")

    def test_a_wrapping_quote_is_stripped(self):
        self.assertEqual(sanitize('"Send 4-6 diary pages."'), "Send 4-6 diary pages.")

    def test_a_clean_line_is_left_alone(self):
        line = "Free to enter — send 4-6 pages from your daily watercolor diary."
        self.assertEqual(sanitize(line), line)


class MetaLineTests(unittest.TestCase):
    """The line is advice from her app, never the app discussing its own data."""

    def test_a_first_person_refusal_is_caught(self):
        self.assertTrue(meta_problem(
            "I cannot recommend this opportunity because the recorded deadline has passed "
            "and I lack confirmation of a current cycle."))

    def test_a_dead_deadline_lead_is_caught(self):
        self.assertTrue(meta_problem(
            "The deadline has already passed; contact them about the next cycle."))

    def test_a_reviewer_note_is_caught(self):
        self.assertTrue(meta_problem("Needs verification before recommendation."))
        self.assertTrue(meta_problem("建议在推荐前进行核实。"))

    def test_ordinary_advice_passes(self):
        self.assertFalse(meta_problem(
            "They take works on paper on consignment — email them a dummy from your daily "
            "watercolor diary."))


class CatsAreNotAnAnchorTests(unittest.TestCase):
    """Her subject is architecture and space; cats wander through it incidentally."""

    def test_a_cat_line_is_not_a_hook(self):
        self.assertFalse(has_personal_hook("A cat-themed group show in Tokyo open to painters."))
        self.assertFalse(has_personal_hook("面向猫主题绘画作品的公开征集。"))

    def test_architecture_beside_a_possessive_still_is(self):
        self.assertTrue(has_personal_hook(
            "They show works on paper — your watercolors of quiet Tokyo architecture fit."))


class ServeTimeGuardTests(unittest.TestCase):
    """api.shape_card is the last line of defence before her page."""

    @staticmethod
    def _card(**kw):
        import api
        base = {"name": "Some Open Call", "category": "competition",
                "one_sentence": "A juried open call for painters."}
        return api.shape_card({**base, **kw})

    def test_generic_why_never_reaches_the_card_face(self):
        card = self._card(
            why_this_fits_short="An international juried exhibition for visual artists "
                                "working in painting, drawing and mixed media.",
            why_it_fits_zh="面向国际视觉艺术家，覆盖绘画、素描及综合媒介等类别。",
        )
        self.assertEqual(card["why_card"], "")
        self.assertEqual(card["why_card_zh"], "")

    def test_a_line_about_her_survives(self):
        why_en = ("Free to enter and open to un-represented painters — send 4-6 pages "
                  "straight from your daily watercolor diary.")
        why_zh = "免费投稿，不要求画廊代理——直接从你的每日水彩日记里挑 4-6 页寄出。"
        card = self._card(why_this_fits_short=why_en, why_it_fits_zh=why_zh)
        self.assertEqual(card["why_card"], why_en)
        self.assertEqual(card["why_card_zh"], why_zh)

    def test_a_weak_chinese_line_blanks_english_too(self):
        """locF falls back to English when the zh field is empty, so blanking one
        language alone would leak English onto her Chinese card."""
        card = self._card(
            why_this_fits_short="Send 4-6 pages from your daily watercolor diary.",
            why_it_fits_zh="面向国际视觉艺术家的公开征集。",
        )
        self.assertEqual(card["why_card"], "")
        self.assertEqual(card["why_card_zh"], "")

    def test_the_detail_panel_still_receives_the_full_line(self):
        """Blanking is a card-face decision — the long form stays available."""
        why = ("An international juried exhibition for visual artists working in "
               "painting, drawing and mixed media.")
        card = self._card(why_this_fits_short=why)
        self.assertEqual(card["why_card"], "")
        self.assertEqual(card["why_it_fits"], why)


if __name__ == "__main__":
    unittest.main()
