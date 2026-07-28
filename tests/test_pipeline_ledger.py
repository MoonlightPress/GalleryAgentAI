"""Pipeline ledger + resume.

smart_pipeline_runner was a bare subprocess loop: no record of which steps ran,
no timings, and no way to resume — the 2026-07-27 run died on Tavily quota at
step 39-ish and the only options were "restart all 101 steps" or hand-surgery.
Scott's ask (system audit, 2026-07-06): "know when something goes wrong and
where."

Every run now writes memory/pipeline_ledger.json — per-step status, return
code, duration — and run_pipeline(resume=True) skips the steps the last
INCOMPLETE run already finished. A completed prior run is not resumed-over:
a fresh invocation after success runs everything again.

Tests use tiny real scripts in a temp dir (the runner spawns real
subprocesses; mocking subprocess would test the mock).
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from smart_pipeline_runner import run_pipeline


class LedgerTests(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ledger = self.tmp / "ledger.json"
        self.marker = self.tmp / "marker.txt"
        # ok.py appends its argv marker; boom.py exits 1
        (self.tmp / "ok.py").write_text(
            "import sys\n"
            f"open(r'{self.marker}', 'a').write('ok:' + (sys.argv[1] if len(sys.argv) > 1 else '-') + '\\n')\n",
            encoding="utf-8")
        (self.tmp / "boom.py").write_text("import sys; sys.exit(1)\n", encoding="utf-8")
        self._old_cwd = Path.cwd()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_steps(self, steps, **kw):
        return run_pipeline(steps, search_dirs=[self.tmp],
                            ledger_path=self.ledger, **kw)

    def runs(self):
        return self.marker.read_text(encoding="utf-8").splitlines() if self.marker.exists() else []

    def test_successful_run_writes_a_completed_ledger_with_one_entry_per_step(self):
        self.run_steps(["ok.py a", "ok.py b"])
        led = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertTrue(led["completed"])
        self.assertEqual([e["step"] for e in led["steps"]], ["ok.py a", "ok.py b"])
        self.assertEqual([e["status"] for e in led["steps"]], ["ok", "ok"])
        for e in led["steps"]:
            self.assertIsInstance(e["duration_s"], float)

    def test_failed_step_is_recorded_and_the_ledger_is_not_completed(self):
        with self.assertRaises(SystemExit):
            self.run_steps(["ok.py a", "boom.py", "ok.py b"])
        led = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertFalse(led["completed"])
        self.assertEqual(led["steps"][-1]["step"], "boom.py")
        self.assertEqual(led["steps"][-1]["status"], "failed")
        self.assertEqual(led["steps"][-1]["returncode"], 1)
        # step after the failure never ran
        self.assertEqual(self.runs(), ["ok:a"])

    def test_resume_skips_steps_the_incomplete_run_finished(self):
        with self.assertRaises(SystemExit):
            self.run_steps(["ok.py a", "boom.py", "ok.py b"])
        (self.tmp / "boom.py").write_text("pass\n", encoding="utf-8")  # "fix" the step
        self.run_steps(["ok.py a", "boom.py", "ok.py b"], resume=True)
        # ok.py a ran exactly once — the resume did not repeat it
        self.assertEqual(self.runs(), ["ok:a", "ok:b"])
        led = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertTrue(led["completed"])
        self.assertEqual([e["status"] for e in led["steps"]],
                         ["skipped_resume", "ok", "ok"])

    def test_resume_after_a_completed_run_runs_everything(self):
        """Resume must never skip based on a run that FINISHED — that would
        turn 'python pipeline --resume' into a silent no-op forever."""
        self.run_steps(["ok.py a"])
        self.run_steps(["ok.py a"], resume=True)
        self.assertEqual(self.runs(), ["ok:a", "ok:a"])

    def test_resume_without_a_ledger_is_a_fresh_run(self):
        self.run_steps(["ok.py a"], resume=True)
        self.assertEqual(self.runs(), ["ok:a"])


if __name__ == "__main__":
    unittest.main()
