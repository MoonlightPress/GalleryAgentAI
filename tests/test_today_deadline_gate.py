import unittest
from unittest.mock import patch

import api


def _stretch_opp(id_, score, deadline_past):
    return {
        "id": id_,
        "title": f"Test Opp {id_}",
        "name": f"Test Opp {id_}",
        "category": "grant",
        "exclusive_primary_bucket": "stretch_targets",
        "career_tier": 3,
        "overall_score": score,
        "deadline_past": deadline_past,
    }


class TodayStretchGoalDeadlineGateTests(unittest.TestCase):
    """Regression test: get_today()'s stretch-goal selection (and its
    fallbacks) must honor the already-computed deadline_past field from
    load_opportunities(), not re-derive it with the older, lenient
    _deadline_past() helper (which has a 7-day grace period and missed a
    real deadline only 6 days past - the exact bug that put a June 29
    opportunity into the live Stretch Goal slot on 2026-07-05)."""

    def test_past_deadline_stretch_target_is_never_selected(self):
        past = _stretch_opp("past1", score=9.9, deadline_past=True)
        open_ = _stretch_opp("open1", score=1.0, deadline_past=False)
        with patch("api.load_opportunities", return_value=[past, open_]):
            result = api.get_today()
        self.assertIsNotNone(result["stretch_goal"])
        self.assertEqual(result["stretch_goal"]["name"], "Test Opp open1")

    def test_all_past_deadline_stretch_targets_yields_no_pick_from_that_bucket(self):
        # Every stretch_targets candidate is past-deadline; the function must
        # not fall back to picking one of them just because nothing else
        # qualifies in that bucket - it should fall through to a later
        # fallback (watch_list/research_needed) or return None, never a
        # stale item.
        past1 = _stretch_opp("past1", score=9.9, deadline_past=True)
        past2 = _stretch_opp("past2", score=8.0, deadline_past=True)
        with patch("api.load_opportunities", return_value=[past1, past2]):
            result = api.get_today()
        if result["stretch_goal"] is not None:
            self.assertNotIn(
                result["stretch_goal"]["name"], ("Test Opp past1", "Test Opp past2")
            )


if __name__ == "__main__":
    unittest.main()
