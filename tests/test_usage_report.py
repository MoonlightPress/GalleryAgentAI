import unittest
from datetime import datetime, timezone, timedelta

from engines.usage_report import (
    split_sessions, sessions_to_flush, dwell_by_page, most_time_on,
    interaction_counts, format_flow, build_digest, duration_minutes,
    run_flush,
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


class InteractionCountsTests(unittest.TestCase):
    def test_counts_by_action_and_category(self):
        evs = [
            _ev(0, type="action", action="follow", category="zine"),
            _ev(1, type="action", action="follow", category="gallery"),
            _ev(2, type="action", action="applied", category="fair_popup"),
            _ev(3, type="nav", page="observe"),  # ignored
        ]
        c = interaction_counts(evs)
        self.assertEqual(c["follow"]["total"], 2)
        self.assertEqual(c["follow"]["by_category"], {"zine": 1, "gallery": 1})
        self.assertEqual(c["applied"]["total"], 1)
        self.assertNotIn("nav", c)


class FlowTests(unittest.TestCase):
    def test_flow_dedupes_consecutive_and_uses_labels(self):
        evs = [
            _ev(0, type="open", page="discover"),
            _ev(1, type="nav", page="discover", section="people"),
            _ev(2, type="nav", page="discover", section="people"),  # dup
            _ev(3, type="nav", page="observe"),
        ]
        self.assertEqual(format_flow(evs), "Home → People → Saffron")


class BuildDigestTests(unittest.TestCase):
    def test_digest_has_header_dwell_counts_flow(self):
        evs = [
            _ev(0, type="open", page="discover"),
            _ev(1, type="nav", page="observe"),
            _ev(8, type="action", action="follow", category="zine"),
        ]
        text = build_digest(evs)
        self.assertIn("Session wrap-up", text)
        self.assertIn("most time on: Saffron", text)
        self.assertIn("followed 1 (1 zine)", text)
        self.assertIn("flow:", text)

    def test_digest_with_no_interactions_omits_counts_line(self):
        evs = [_ev(0, type="open", page="discover"), _ev(2, type="nav", page="observe")]
        text = build_digest(evs)
        self.assertIn("Session wrap-up", text)
        self.assertNotIn("followed", text)

    def test_empty_events_degrade_safely(self):
        self.assertIsInstance(build_digest([]), str)


class RunFlushTests(unittest.TestCase):
    def _events(self):
        return [
            _ev(0, type="open", page="discover", visitor_id="v1"),
            _ev(3, type="action", action="follow", category="zine", visitor_id="v1"),
        ]

    def test_posts_one_digest_for_idle_session(self):
        posted = []
        now = T0 + timedelta(minutes=20)
        state, count = run_flush(self._events(), now, {}, notifier=posted.append)
        self.assertEqual(count, 1)
        self.assertEqual(len(posted), 1)
        self.assertIn("Session wrap-up", posted[0])
        self.assertIn("v1", state)

    def test_second_run_does_not_repost(self):
        now = T0 + timedelta(minutes=20)
        state, _ = run_flush(self._events(), now, {}, notifier=lambda m: None)
        posted = []
        state2, count = run_flush(self._events(), now, state, notifier=posted.append)
        self.assertEqual(count, 0)
        self.assertEqual(posted, [])


if __name__ == "__main__":
    unittest.main()
