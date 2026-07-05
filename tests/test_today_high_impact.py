import unittest
from unittest.mock import patch

import api


def _opp(id_, score, cat="global_watercolor_open_call", tier=3, deadline_past=False,
         bucket="research_needed", deadline="2099-12-31", submission="https://x/apply"):
    return {
        "id": id_, "title": f"Opp {id_}", "name": f"Opp {id_}",
        "category": cat, "career_tier": tier, "overall_score": score,
        "exclusive_primary_bucket": bucket, "deadline_past": deadline_past,
        "deadline": deadline, "submission_page": submission,
        "url_verification_status": "ok",
    }


class TodayHighImpactFallbackTests(unittest.TestCase):
    """Regression (audit 2026-07-06): the immediate_best_moves bucket is
    structurally near-unreachable, so the High Impact slot was always null and
    Today's Focus showed 2 items, not the spec's 3. A fallback now fills it
    from the strongest actionable, open, non-Tier-4, non-relationship call."""

    def test_high_impact_fills_when_ibm_bucket_empty(self):
        pool = [
            _opp("open_call_hi", 9.0),
            _opp("cafe", 8.0, cat="cafe_gallery", tier=1),  # relationship -> QW territory
        ]
        with patch("api.load_opportunities", return_value=pool):
            t = api.get_today()
        self.assertIsNotNone(t["high_impact"])
        self.assertEqual(t["high_impact"]["name"], "Opp open_call_hi")

    def test_high_impact_excludes_tier4_and_past_deadline(self):
        pool = [
            _opp("tier4", 10.0, tier=4),
            _opp("stale", 9.5, deadline_past=True),
            _opp("good", 7.0),
        ]
        with patch("api.load_opportunities", return_value=pool):
            t = api.get_today()
        self.assertIsNotNone(t["high_impact"])
        self.assertEqual(t["high_impact"]["name"], "Opp good")

    def test_high_impact_and_quick_win_are_distinct(self):
        pool = [
            _opp("call", 9.0),
            _opp("cafe", 8.5, cat="cafe_gallery", tier=1),
        ]
        pool[1]["contact"] = "hi@cafe.jp"
        with patch("api.load_opportunities", return_value=pool):
            t = api.get_today()
        if t["high_impact"] and t["quick_win"]:
            self.assertNotEqual(t["high_impact"]["id"], t["quick_win"]["id"])


if __name__ == "__main__":
    unittest.main()
