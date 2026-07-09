import unittest

from engines.visit_tracking import describe_event, action_detail


class ReturnEventTests(unittest.TestCase):
    """A tab-return must be a first-class event. Without it the log shows a
    `leave` with no `open` before it, which reads as impossible behaviour."""

    def test_return_event_reports_time_away(self):
        text, status = describe_event(
            {"type": "return", "page": "discover", "away_ms": 192000})
        self.assertIn("3m 12s", text)
        self.assertEqual(status, "info")

    def test_return_event_is_not_the_generic_fallback(self):
        text, _ = describe_event({"type": "return", "page": "observe", "away_ms": 5000})
        self.assertNotEqual(text, "👀 activity")

    def test_malformed_away_ms_does_not_raise(self):
        text, _ = describe_event({"type": "return", "page": "discover", "away_ms": None})
        self.assertIn("a moment", text)

    def test_unknown_type_still_falls_back(self):
        self.assertEqual(describe_event({"type": "wat"})[0], "👀 activity")


class ActionDetailTests(unittest.TestCase):
    """The Discord feed must say WHICH opportunity and on WHICH surface she
    clicked — 'open_card (cafe_gallery)' was ambiguous between Today's Focus
    and the browse list."""

    def test_names_opportunity_category_and_surface(self):
        detail = action_detail({"action": "external_link_click", "name": "Mograg Gallery",
                                "category": "cafe_gallery", "surface": "today_focus",
                                "role": "quick_win"})
        self.assertIn("Mograg Gallery", detail)
        self.assertIn("cafe_gallery", detail)
        self.assertIn("Today's Focus", detail)
        self.assertIn("Quick Win", detail)

    def test_browse_surface_is_distinguishable_from_todays_focus(self):
        tf = action_detail({"action": "open_card", "name": "X", "surface": "today_focus"})
        br = action_detail({"action": "open_card", "name": "X", "surface": "browse:institutional"})
        self.assertNotEqual(tf, br)
        self.assertIn("Today's Focus", tf)

    def test_no_surface_degrades_quietly(self):
        detail = action_detail({"action": "open_card", "name": "X", "category": "zine"})
        self.assertIn("X", detail)
        self.assertNotIn("None", detail)

    def test_empty_event_does_not_raise(self):
        self.assertEqual(action_detail({}), "")


if __name__ == "__main__":
    unittest.main()
