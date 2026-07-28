"""The free maintenance pipeline must never run a paid step.

run_maintenance_pipeline builds itself as [s for s in PIPELINE if s not in
PAID_STEPS]. That comparison is on the raw PIPELINE entry, so the moment an
entry carries arguments — "rumor_mill_engine.py --max 300" — it stops matching
the bare name in PAID_STEPS and silently leaks into the pipeline that is
scheduled weekly, unattended, on the assumption it spends nothing.

This is the same class of bug as the added_at/imported_at split: two spellings
of one identity, and a reader that only knows one of them.
"""

import unittest

from run_full_mochi_pipeline import PIPELINE, PAID_STEPS
from run_maintenance_pipeline import MAINTENANCE
from smart_pipeline_runner import parse_step


class MaintenanceExclusionTests(unittest.TestCase):

    def test_no_paid_step_appears_in_the_maintenance_pipeline(self):
        leaked = [s for s in MAINTENANCE if parse_step(s)[0] in PAID_STEPS]
        self.assertEqual(leaked, [], f"paid steps leaked into free pipeline: {leaked}")

    def test_every_paid_step_is_still_present_in_the_full_pipeline(self):
        names = {parse_step(s)[0] for s in PIPELINE}
        missing = [p for p in PAID_STEPS if p not in names]
        self.assertEqual(missing, [], f"PAID_STEPS names nothing in PIPELINE: {missing}")

    def test_maintenance_is_strictly_smaller_than_the_full_pipeline(self):
        self.assertLess(len(MAINTENANCE), len(PIPELINE))


if __name__ == "__main__":
    unittest.main()
