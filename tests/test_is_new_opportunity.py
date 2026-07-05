import unittest
from datetime import datetime, timezone

from api import is_new_opportunity, NEW_WINDOW_DAYS


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


if __name__ == "__main__":
    unittest.main()
