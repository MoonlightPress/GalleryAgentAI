import sys
import unittest

from engines.regen import build_regen_command, spawn_draft_regen


class RecordingRunner:
    """Stand-in for subprocess.Popen that records the call instead of spawning."""

    def __init__(self, raises=None):
        self.calls = []
        self._raises = raises

    def __call__(self, cmd, **kwargs):
        if self._raises:
            raise self._raises
        self.calls.append({"cmd": cmd, "kwargs": kwargs})
        return object()  # a fake process handle


class BuildRegenCommandTests(unittest.TestCase):
    def test_command_runs_the_writer_with_current_interpreter(self):
        cmd = build_regen_command()
        self.assertEqual(cmd[0], sys.executable)
        self.assertIn("engines/ibm_email_writer.py", cmd)

    def test_limit_is_passed_through_when_given(self):
        cmd = build_regen_command(limit=5)
        self.assertIn("--limit", cmd)
        self.assertIn("5", cmd)

    def test_no_limit_flag_when_omitted(self):
        self.assertNotIn("--limit", build_regen_command())


class SpawnDraftRegenTests(unittest.TestCase):
    def test_spawns_the_writer_and_reports_success(self):
        runner = RecordingRunner()
        ok = spawn_draft_regen(runner=runner)
        self.assertTrue(ok)
        self.assertEqual(len(runner.calls), 1)
        self.assertIn("engines/ibm_email_writer.py", runner.calls[0]["cmd"])

    def test_passes_cwd_through(self):
        runner = RecordingRunner()
        spawn_draft_regen(runner=runner, cwd="/some/repo")
        self.assertEqual(runner.calls[0]["kwargs"].get("cwd"), "/some/repo")

    def test_spawn_failure_is_swallowed(self):
        # A failed background launch must never bubble up into the save request.
        runner = RecordingRunner(raises=OSError("no such file"))
        ok = spawn_draft_regen(runner=runner)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
