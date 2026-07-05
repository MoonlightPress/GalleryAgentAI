import unittest

from opportunity_truth_checker import truth_check


class TruthCheckTests(unittest.TestCase):
    def test_negative_explanation_caps_at_6_4(self):
        opp = {"overall_score": 10.0, "why_this_fits_short": "honestly unclear fit"}
        current, corrected, verdict, _ = truth_check(opp)
        self.assertEqual(corrected, 6.4)
        self.assertTrue(opp["score_capped_by_truth_checker"])

    def test_clean_entry_not_capped(self):
        opp = {"overall_score": 8.0, "why_this_fits_short": "strong watercolor venue fit"}
        _, corrected, verdict, _ = truth_check(opp)
        self.assertEqual(corrected, 8.0)
        self.assertEqual(verdict, "ok")
        self.assertFalse(opp["score_capped_by_truth_checker"])

    def test_photography_only_capped_even_when_native_medium_is_photography(self):
        # Regression: an exemption based on the FALSE claim "the artist is a
        # photographer" let photography-native entries escape this cap. She is
        # a watercolor painter; photography opportunities are blocked by
        # Scott's 2026-06-19 decision. The cap must apply regardless of the
        # entry's native_medium.
        opp = {
            "overall_score": 9.0,
            "native_medium": "photography",
            "one_sentence": "annual photo contest for street photography portfolios",
        }
        _, corrected, verdict, _ = truth_check(opp)
        self.assertLessEqual(corrected, 5.8)
        self.assertEqual(verdict, "capped_wrong_medium")

    def test_watercolor_terms_defuse_photography_cap(self):
        # Mixed-media calls that genuinely welcome watercolor are not
        # photography-only — the existing watercolor-term escape stays.
        opp = {
            "overall_score": 9.0,
            "one_sentence": "photography and watercolor artists welcome",
        }
        _, corrected, verdict, _ = truth_check(opp)
        self.assertEqual(corrected, 9.0)


if __name__ == "__main__":
    unittest.main()
