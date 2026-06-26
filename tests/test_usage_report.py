import unittest
from datetime import datetime, timezone, timedelta

from engines.usage_report import (
    split_sessions, sessions_to_flush, dwell_by_page, most_time_on,
)

T0 = datetime(2026, 6, 26, 10, 0, 0, tzinfo=timezone.utc)


def _ev(mins, **kw):
    """Event helper: ts = T0 + mins minutes."""
    e = {"ts": (T0 + timedelta(minutes=mins)).isoformat()}
    e.update(kw)
    return e


class SplitSessionsTests(unittest.TestCase):
    def test_single_run_is_one_session(self):
        evs = [_ev(0, type="open", page="discover"), _ev(2, type="nav", page="observe")]
        self.assertEqual(len(split_sessions(evs, idle_minutes=10)), 1)

    def test_gap_over_idle_splits(self):
        evs = [_ev(0, type="open"), _ev(2, type="nav"), _ev(20, type="nav")]
        sessions = split_sessions(evs, idle_minutes=10)
        self.assertEqual(len(sessions), 2)
        self.assertEqual(len(sessions[0]), 2)

    def test_unparseable_ts_dropped(self):
        evs = [_ev(0, type="open"), {"type": "nav", "ts": "garbage"}]
        self.assertEqual(len(split_sessions(evs)[0]), 1)

    def test_empty(self):
        self.assertEqual(split_sessions([]), [])


class SessionsToFlushTests(unittest.TestCase):
    def test_idle_session_is_flushed(self):
        evs = [_ev(0, type="open"), _ev(3, type="nav")]
        now = T0 + timedelta(minutes=20)        # 17 min after last event
        out = sessions_to_flush(evs, now, None, idle_minutes=10)
        self.assertEqual(len(out), 1)

    def test_active_session_not_flushed(self):
        evs = [_ev(0, type="open"), _ev(3, type="nav")]
        now = T0 + timedelta(minutes=5)         # only 2 min idle
        self.assertEqual(sessions_to_flush(evs, now, None, idle_minutes=10), [])

    def test_already_flushed_session_skipped(self):
        evs = [_ev(0, type="open"), _ev(3, type="nav")]
        now = T0 + timedelta(minutes=20)
        end_iso = (T0 + timedelta(minutes=3)).isoformat()
        self.assertEqual(sessions_to_flush(evs, now, end_iso, idle_minutes=10), [])


class DwellTests(unittest.TestCase):
    def test_most_time_on_picks_longest_page(self):
        evs = [_ev(0, type="open", page="discover"),
               _ev(1, type="nav", page="observe"),
               _ev(9, type="nav", page="discover")]  # 8 min on Saffron
        self.assertEqual(most_time_on(evs), "Saffron")

    def test_most_time_on_empty_is_none(self):
        self.assertIsNone(most_time_on([]))


if __name__ == "__main__":
    unittest.main()
