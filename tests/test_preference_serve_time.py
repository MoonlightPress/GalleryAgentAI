"""The preference loop must work at serve time: a profile edit takes effect on
the next request, both ADDING and REMOVING effects, idempotently. These guard
the restore-baseline-then-reapply design that makes that safe."""
import copy
import json
import unittest
from pathlib import Path

from engines import peppercorn_preference_engine as pe


def _opp(**kw):
    base = {"category": "", "overall_score": 8.0, "exclusive_primary_bucket": "immediate_best_moves"}
    base.update(kw)
    return base


LOW_FEE_PROFILE = {
    "priorities":  {"primary_track": "hybrid", "active_tiers": [1, 2], "avoid": []},
    "preferences": {"fee_tolerance": "low", "geo_focus": ["tokyo", "international"],
                    "surface_more": ["zines_books"], "surface_less": []},
}


class IdempotencyTests(unittest.TestCase):
    def test_apply_twice_equals_once(self):
        opps = [
            _opp(category="zine", fees="¥8000"),                 # high fee -> suppressed
            _opp(category="zine_print", fees="free"),            # surface_more -> nudged
            _opp(category="gallery", country="france", fees="free", exclusive_primary_bucket="immediate_best_moves"),
        ]
        once  = pe.apply_preferences(copy.deepcopy(opps), LOW_FEE_PROFILE)
        twice = pe.apply_preferences(once, LOW_FEE_PROFILE)
        self.assertEqual(
            [(o["exclusive_primary_bucket"], o["overall_score"]) for o in once],
            [(o["exclusive_primary_bucket"], o["overall_score"]) for o in twice],
        )

    def test_high_fee_suppressed_then_restored_when_pref_changes(self):
        opp = _opp(category="zine", fees="¥8000")
        suppressed = pe.apply_preferences([copy.deepcopy(opp)], LOW_FEE_PROFILE)[0]
        self.assertEqual(suppressed["exclusive_primary_bucket"], "research_needed")
        self.assertTrue(suppressed["peppercorn_suppressed"])

        # She raises her fee tolerance — the suppression must LIFT, not linger.
        relaxed = dict(LOW_FEE_PROFILE)
        relaxed["preferences"] = dict(LOW_FEE_PROFILE["preferences"], fee_tolerance="high")
        restored = pe.apply_preferences([suppressed], relaxed)[0]
        self.assertEqual(restored["exclusive_primary_bucket"], "immediate_best_moves")
        self.assertNotIn("peppercorn_suppressed", restored)

    def test_empty_profile_is_noop(self):
        opps = [_opp()]
        self.assertIs(pe.apply_preferences(opps, {}), opps)

    def test_restore_baseline_reverses_old_delta_markers(self):
        # Data from an older pipeline run: nudge delta + suppression, no base fields.
        old = _opp(category="zine", overall_score=8.8,
                   exclusive_primary_bucket="research_needed",
                   peppercorn_surface_nudge=0.8, peppercorn_suppressed="high_fee_8000")
        base = pe.restore_baseline(old)
        self.assertAlmostEqual(base["overall_score"], 8.0, places=2)   # 8.8 - 0.8
        self.assertEqual(base["exclusive_primary_bucket"], "immediate_best_moves")
        self.assertNotIn("peppercorn_suppressed", base)
        self.assertNotIn("peppercorn_surface_nudge", base)

    def test_surface_more_boosts_score(self):
        out = pe.apply_preferences([_opp(category="zine_print", overall_score=5.0)], LOW_FEE_PROFILE)[0]
        self.assertGreater(out["overall_score"], 5.0)
        self.assertIn("peppercorn_base_score", out)


class RealDataStabilityTests(unittest.TestCase):
    def test_idempotent_on_live_data_with_current_profile(self):
        root = Path(pe.__file__).resolve().parent.parent
        opp_path = root / "deploy_data" / "compact_opportunities.json"
        prof_path = root / "memory" / "peppercorn_profile.json"
        if not (opp_path.exists() and prof_path.exists()):
            self.skipTest("live data not present")
        opps = json.loads(opp_path.read_text(encoding="utf-8"))
        profile = json.loads(prof_path.read_text(encoding="utf-8"))
        once  = pe.apply_preferences(opps, profile)
        twice = pe.apply_preferences(once, profile)
        self.assertEqual(
            [o.get("exclusive_primary_bucket") for o in once],
            [o.get("exclusive_primary_bucket") for o in twice],
        )
        self.assertEqual(
            [o.get("overall_score") for o in once],
            [o.get("overall_score") for o in twice],
        )


if __name__ == "__main__":
    unittest.main()
