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
from engines.career_strategy_engine import _career_level, _blocking_gaps


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
    """Level is gated on ATTAINMENT, not on a readiness score. She rises to
    Tier 3 once the foundation (solo + institutional + group shows) is built,
    and to Tier 4 only once she holds an actual Tier-4 credit (representation,
    residency, grant, or watercolor-society membership). High readiness alone
    must NOT overshoot to Tier 4 — that was the bug."""

    NO_CREDITS = dict(has_representation=False, has_residency=False,
                      has_grant=False, has_jws=False)

    def test_foundation_level_when_not_complete(self):
        lv = _career_level(0.10, 0.0, foundation_complete=False, **self.NO_CREDITS)
        self.assertEqual(lv["current"], 2)
        self.assertEqual(lv["next"], 3)
        self.assertAlmostEqual(lv["progress_to_next"], round(0.10 / 0.60, 2), places=2)

    def test_rises_to_tier3_when_foundation_complete(self):
        lv = _career_level(0.85, 0.85, foundation_complete=True, **self.NO_CREDITS)
        self.assertEqual(lv["current"], 3)
        self.assertEqual(lv["next"], 4)

    def test_no_overshoot_to_tier4_on_readiness_alone(self):
        # Her real state today: foundation complete, tier-4 readiness high (0.85),
        # but NO Tier-4 credit yet -> she stays at Tier 3, progress driven by
        # tier-4 readiness (0.85), not promoted to Tier 4.
        lv = _career_level(0.85, 0.85, foundation_complete=True, **self.NO_CREDITS)
        self.assertEqual(lv["current"], 3)
        self.assertEqual(lv["current_label"], "Credibility")
        self.assertEqual(lv["next_label"], "Prestige")
        self.assertAlmostEqual(lv["progress_to_next"], 0.85, places=2)

    def test_tier4_only_when_a_real_credit_exists(self):
        # A single Tier-4 credit (here: representation) promotes her to Tier 4.
        lv = _career_level(0.85, 0.85, foundation_complete=True,
                           has_representation=True, has_residency=False,
                           has_grant=False, has_jws=False)
        self.assertEqual(lv["current"], 4)
        self.assertIsNone(lv["next"])
        self.assertEqual(lv["progress_to_next"], 1.0)

    def test_any_tier4_credit_suffices(self):
        for credit in ("has_representation", "has_residency", "has_grant", "has_jws"):
            creds = dict(self.NO_CREDITS)
            creds[credit] = True
            lv = _career_level(0.85, 0.85, foundation_complete=True, **creds)
            self.assertEqual(lv["current"], 4, f"{credit} should reach Tier 4")


class GapLocalizationTests(unittest.TestCase):
    """The leak fix: count-bearing readiness strings carry a _zh sibling built
    with the SAME live count, so zh never falls back to an English baked sentence
    when the count changes."""

    def _group_gap(self, group_shows):
        gaps = _blocking_gaps(group_shows, has_solo=False, has_institutional=False,
                              has_international=False, has_jws=False)
        return next(g for g in gaps if g["gap_id"] == "group_shows")

    def test_every_gap_has_zh_siblings(self):
        for g in _blocking_gaps(1, False, False, False, False):
            self.assertIn("gap_zh", g)
            self.assertIn("detail_zh", g)
            self.assertIn("action_zh", g)

    def test_count_tracks_in_both_languages(self):
        g1 = self._group_gap(1)
        self.assertIn("1", g1["detail"]); self.assertIn("2 more", g1["detail"])
        self.assertIn("1", g1["detail_zh"]); self.assertIn("再来 2 场", g1["detail_zh"])

        g2 = self._group_gap(2)
        self.assertIn("2 confirmed", g2["detail"]); self.assertIn("1 more", g2["detail"])
        # The zh moves in lockstep — this is exactly what used to leak.
        self.assertIn("2 场已确认", g2["detail_zh"]); self.assertIn("再来 1 场", g2["detail_zh"])


if __name__ == "__main__":
    unittest.main()
