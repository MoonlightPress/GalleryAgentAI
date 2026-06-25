"""Tests for the failed-run Discord alert in scripts/check_attention.py.

A failed pipeline run (last_run.json status="failed") went unnoticed on 2026-06-23
and let her data go stale. check_attention.py now fires a best-effort Discord alert
on a failed run. These tests pin that wiring without doing any network I/O.
"""
import unittest

from scripts.check_attention import build_failure_message, alert_on_failed_run


class RecordingNotifier:
    """Stand-in for engines.notify.notify_discord that records calls."""

    def __init__(self, returns=True):
        self.calls = []
        self._returns = returns

    def __call__(self, message, status="info"):
        self.calls.append({"message": message, "status": status})
        return self._returns


class BuildFailureMessageTests(unittest.TestCase):
    def test_message_mentions_failure_and_timestamp(self):
        msg = build_failure_message({"status": "failed", "last_run": "2026-06-23T09:00:01"})
        self.assertIn("FAILED", msg)
        self.assertIn("2026-06-23T09:00:01", msg)

    def test_message_includes_host_when_present(self):
        msg = build_failure_message({"status": "failed", "last_run": "t", "host": "server"})
        self.assertIn("server", msg)

    def test_message_tolerates_missing_timestamp(self):
        msg = build_failure_message({"status": "failed"})
        self.assertIn("unknown time", msg)


class AlertOnFailedRunTests(unittest.TestCase):
    def test_failed_run_fires_failure_alert(self):
        notifier = RecordingNotifier()
        sent = alert_on_failed_run(
            {"status": "failed", "last_run": "2026-06-23T09:00:01"}, notifier=notifier
        )
        self.assertTrue(sent)
        self.assertEqual(len(notifier.calls), 1)
        self.assertEqual(notifier.calls[0]["status"], "failure")
        self.assertIn("FAILED", notifier.calls[0]["message"])

    def test_ok_run_does_not_alert(self):
        notifier = RecordingNotifier()
        sent = alert_on_failed_run({"status": "ok", "last_run": "t"}, notifier=notifier)
        self.assertFalse(sent)
        self.assertEqual(notifier.calls, [])

    def test_empty_last_run_does_not_alert(self):
        notifier = RecordingNotifier()
        self.assertFalse(alert_on_failed_run({}, notifier=notifier))
        self.assertEqual(notifier.calls, [])

    def test_notifier_exception_is_swallowed(self):
        def boom(*a, **k):
            raise RuntimeError("network down")

        # A monitoring hook must never crash the thing it monitors.
        self.assertFalse(
            alert_on_failed_run({"status": "failed", "last_run": "t"}, notifier=boom)
        )

    def test_notifier_noop_returns_false(self):
        # notifier returning False (e.g. no webhook configured) -> alert reports not-sent.
        notifier = RecordingNotifier(returns=False)
        self.assertFalse(
            alert_on_failed_run({"status": "failed", "last_run": "t"}, notifier=notifier)
        )


if __name__ == "__main__":
    unittest.main()
