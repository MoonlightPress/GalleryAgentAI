import unittest

from engines.visit_tracking import register_visit, describe_event, mark_visitor


class RegisterVisitTests(unittest.TestCase):
    """Coarse, privacy-respecting usage signal: notify at most once per day the
    first time she opens the app. We track day-count and total visits, but
    nothing about WHAT she looks at."""

    def test_first_ever_visit_notifies_day_one(self):
        log, notify, day = register_visit({}, today="2026-06-25")
        self.assertTrue(notify)
        self.assertEqual(day, 1)
        self.assertEqual(log["total_visits"], 1)
        self.assertEqual(log["last_notified_date"], "2026-06-25")

    def test_second_visit_same_day_does_not_notify(self):
        log, _, _ = register_visit({}, today="2026-06-25")
        log, notify, day = register_visit(log, today="2026-06-25")
        self.assertFalse(notify)
        self.assertEqual(day, 1)               # still day one
        self.assertEqual(log["total_visits"], 2)  # but the visit is counted

    def test_next_day_notifies_day_two(self):
        log, _, _ = register_visit({}, today="2026-06-25")
        log, notify, day = register_visit(log, today="2026-06-26")
        self.assertTrue(notify)
        self.assertEqual(day, 2)
        self.assertEqual(log["total_visits"], 2)

    def test_first_seen_is_recorded_once(self):
        log, _, _ = register_visit({}, today="2026-06-25")
        log, _, _ = register_visit(log, today="2026-06-30")
        self.assertEqual(log["first_seen"], "2026-06-25")

    def test_malformed_log_is_tolerated(self):
        # A partially-written / garbage log must not crash the visit endpoint.
        log, notify, day = register_visit({"total_visits": "oops"}, today="2026-06-25")
        self.assertTrue(notify)
        self.assertEqual(log["total_visits"], 1)


class MarkVisitorTests(unittest.TestCase):
    """Anonymous returning-vs-new detection — tells a real repeat visitor from a
    scattered one-off hit, without storing anything about her."""

    def test_first_time_visitor_is_new(self):
        log, returning = mark_visitor({}, "abc")
        self.assertFalse(returning)
        self.assertEqual(log["visitor_ids"], ["abc"])

    def test_same_id_again_is_returning(self):
        log, _ = mark_visitor({}, "abc")
        log, returning = mark_visitor(log, "abc")
        self.assertTrue(returning)
        self.assertEqual(log["visitor_ids"], ["abc"])  # not duplicated

    def test_missing_id_is_new_and_untracked(self):
        log, returning = mark_visitor({}, None)
        self.assertFalse(returning)
        self.assertNotIn("visitor_ids", log)


class DescribeEventTests(unittest.TestCase):
    """Human-readable, friendly-page-name messages for the live Discord feed."""

    def test_open_event_mentions_opened_and_day(self):
        text, status = describe_event({"type": "open", "page": "discover"}, day=3)
        self.assertIn("opened", text.lower())
        self.assertIn("3", text)
        self.assertIn("Home", text)  # 'discover' -> friendly label

    def test_nav_with_from_shows_arrow_between_labels(self):
        text, _ = describe_event({"type": "nav", "from": "discover", "page": "observe"})
        self.assertEqual(text, "Home → Saffron")

    def test_nav_without_from_shows_arrow_to_label(self):
        text, _ = describe_event({"type": "nav", "page": "refine"})
        self.assertEqual(text, "→ Peppercorn")

    def test_unknown_page_falls_back_to_titlecase(self):
        text, _ = describe_event({"type": "nav", "page": "mystery"})
        self.assertIn("Mystery", text)

    def test_open_says_returning_or_new_when_known(self):
        ret, _ = describe_event({"type": "open", "page": "observe", "visitor_id": "abcdef12"}, day=2, returning=True)
        self.assertIn("returning", ret.lower())
        self.assertIn("opened", ret.lower())
        self.assertIn("Saffron", ret)
        self.assertIn("abcdef", ret)  # short id surfaced
        new, _ = describe_event({"type": "open", "page": "discover"}, day=1, returning=False)
        self.assertIn("new visitor", new.lower())

    def test_action_event_is_described(self):
        text, _ = describe_event({"type": "action", "action": "edited her statement"})
        self.assertIn("edited her statement", text)

    def test_nav_with_section_shows_subarrow_label(self):
        text, _ = describe_event({"type": "nav", "page": "discover", "section": "people"})
        self.assertEqual(text, "↳ People")

    def test_nav_with_unknown_section_titlecases(self):
        text, _ = describe_event({"type": "nav", "page": "observe", "section": "money_runway"})
        self.assertIn("Money Runway", text)

    def test_unknown_type_does_not_crash(self):
        text, status = describe_event({"type": "weird"})
        self.assertIsInstance(text, str)
        self.assertTrue(text)


if __name__ == "__main__":
    unittest.main()
