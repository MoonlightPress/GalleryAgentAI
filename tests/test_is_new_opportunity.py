import unittest
from datetime import datetime, timezone

from api import is_new_opportunity, shape_card, NEW_WINDOW_DAYS


class IsNewOpportunityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 7, 5, 12, 0, 0, tzinfo=timezone.utc)

    def test_fresh_date_is_new(self):
        self.assertTrue(is_new_opportunity("2026-07-05", now=self.now))

    def test_eight_days_old_is_not_new(self):
        self.assertFalse(is_new_opportunity("2026-06-27", now=self.now))

    def test_exactly_seven_days_old_is_new(self):
        self.assertTrue(is_new_opportunity("2026-06-28", now=self.now))

    def test_missing_imported_at_is_not_new(self):
        self.assertFalse(is_new_opportunity(None, now=self.now))
        self.assertFalse(is_new_opportunity("", now=self.now))

    def test_malformed_imported_at_is_not_new(self):
        self.assertFalse(is_new_opportunity("not-a-date", now=self.now))
        self.assertFalse(is_new_opportunity("2026-13-99", now=self.now))

    def test_future_date_is_not_new(self):
        # A data glitch (imported_at after "now") must never be flagged new.
        self.assertFalse(is_new_opportunity("2026-07-10", now=self.now))

    def test_default_window_constant_is_seven(self):
        self.assertEqual(NEW_WINDOW_DAYS, 7)


class ShapeCardIsNewFieldTests(unittest.TestCase):
    """Regression coverage for the added_at/imported_at field mismatch: the
    active discovery engines (japanese_chinese_discovery_engine.py,
    grant_discovery_engine.py, global_opportunity_expander.py) stamp
    "added_at" on new entries, not "imported_at" - a real pipeline run on
    2026-07-05 produced 126 new opportunities that were silently never
    flagged is_new until shape_card() was fixed to check both fields."""

    def _today(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def test_added_at_from_discovery_engines_is_recognized(self):
        card = shape_card({"title": "Test", "added_at": self._today()})
        self.assertTrue(card["is_new"])

    def test_imported_at_from_legacy_scripts_still_works(self):
        card = shape_card({"title": "Test", "imported_at": self._today()})
        self.assertTrue(card["is_new"])

    def test_added_at_takes_precedence_when_both_present(self):
        card = shape_card({"title": "Test", "added_at": self._today(), "imported_at": "2020-01-01"})
        self.assertTrue(card["is_new"])

    def test_neither_field_present_is_not_new(self):
        card = shape_card({"title": "Test"})
        self.assertFalse(card["is_new"])


if __name__ == "__main__":
    unittest.main()
