"""Tests for the Saffron hybrid reframe ranking wiring.

The contract:
  - Nothing is hidden — opportunities are RE-RANKED by fit to her current level.
  - Tier 1–2 (her foundation) are always fully in reach.
  - Tier 3/4 fit RISES with her readiness, so those opps climb on their own as
    she levels up.
  - Raw quality still dominates: a genuinely better stretch opp stays above a
    mediocre level-appropriate one. Level-fit only nudges + breaks ties.
"""
import unittest
from unittest import mock

import api
from engines.career_strategy_engine import _career_level


def _opp(tier, score=10.0):
    return {"career_tier": tier, "overall_score": score, "name": f"t{tier}-{score}"}


class LevelFitTests(unittest.TestCase):
    def test_tier_1_2_always_fully_fit(self):
        r = {"tier_3": 0.0, "tier_4": 0.0}
        self.assertEqual(api._level_fit(_opp(1), r), 1.0)
        self.assertEqual(api._level_fit(_opp(2), r), 1.0)

    def test_tier3_fit_rises_with_readiness(self):
        low  = api._level_fit(_opp(3), {"tier_3": 0.10, "tier_4": 0.0})
        high = api._level_fit(_opp(3), {"tier_3": 0.80, "tier_4": 0.0})
        self.assertAlmostEqual(low, 0.55, places=3)
        self.assertAlmostEqual(high, 0.90, places=3)
        self.assertGreater(high, low)

    def test_tier4_fit_rises_with_readiness(self):
        none = api._level_fit(_opp(4), {"tier_3": 1.0, "tier_4": 0.0})
        full = api._level_fit(_opp(4), {"tier_3": 1.0, "tier_4": 1.0})
        self.assertAlmostEqual(none, 0.40, places=3)
        self.assertAlmostEqual(full, 1.00, places=3)
        self.assertGreater(full, none)

    def test_multiplier_band_is_gentle(self):
        r = {"tier_3": 0.0, "tier_4": 0.0}
        # tier 1 (fit 1.0) -> 1.15 ; tier 4 (fit 0.40) -> 0.97
        self.assertAlmostEqual(api._level_fit_multiplier(_opp(1), r), 1.15, places=3)
        self.assertAlmostEqual(api._level_fit_multiplier(_opp(4), r), 0.97, places=3)

    def test_fit_band_labels(self):
        self.assertEqual(api._fit_band(_opp(1), {"tier_3": 0.0, "tier_4": 0.0}), "in_reach")
        self.assertEqual(api._fit_band(_opp(3), {"tier_3": 0.10, "tier_4": 0.0}), "stretch")
        self.assertEqual(api._fit_band(_opp(3), {"tier_3": 0.50, "tier_4": 0.0}), "near")
        self.assertEqual(api._fit_band(_opp(3), {"tier_3": 1.0, "tier_4": 0.0}), "in_reach")

    def test_ranking_orders_level_appropriate_above_stretch_at_equal_quality(self):
        with mock.patch.object(api, "_career_readiness",
                               return_value={"tier_3": 0.10, "tier_4": 0.0}):
            opps = [_opp(4), _opp(3), _opp(1)]  # all score 10
            ranked = sorted(opps, key=api._ranked_score, reverse=True)
            self.assertEqual([o["career_tier"] for o in ranked], [1, 3, 4])

    def test_quality_still_dominates(self):
        # A strong tier-3 (10) must outrank a weak tier-1 (7) even at low readiness.
        with mock.patch.object(api, "_career_readiness",
                               return_value={"tier_3": 0.10, "tier_4": 0.0}):
            self.assertGreater(api._ranked_score(_opp(3, 10.0)),
                               api._ranked_score(_opp(1, 7.0)))

    def test_tier3_opp_rises_as_she_levels(self):
        opp = _opp(3, 10.0)
        with mock.patch.object(api, "_career_readiness",
                               return_value={"tier_3": 0.10, "tier_4": 0.0}):
            low = api._ranked_score(opp)
        with mock.patch.object(api, "_career_readiness",
                               return_value={"tier_3": 0.90, "tier_4": 0.0}):
            high = api._ranked_score(opp)
        self.assertGreater(high, low)


class CareerLevelTests(unittest.TestCase):
    def test_foundation_level_when_readiness_low(self):
        lv = _career_level(0.10, 0.0)
        self.assertEqual(lv["current"], 2)
        self.assertEqual(lv["next"], 3)
        self.assertAlmostEqual(lv["progress_to_next"], round(0.10 / 0.60, 2), places=2)

    def test_rises_to_tier3_when_crossed(self):
        self.assertEqual(_career_level(0.70, 0.0)["current"], 3)

    def test_tops_out_at_tier4(self):
        lv = _career_level(0.80, 0.70)
        self.assertEqual(lv["current"], 4)
        self.assertIsNone(lv["next"])
        self.assertEqual(lv["progress_to_next"], 1.0)


if __name__ == "__main__":
    unittest.main()
