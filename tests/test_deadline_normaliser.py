import unittest
from datetime import date

from engines.deadline_normaliser import classify_deadline, parse_deadline_date

TODAY = date(2026, 6, 19)


class DeadlinePastDetectionTests(unittest.TestCase):
    def test_past_month_year_deadline_is_not_verified(self):
        # "1 July 2025" is well in the past relative to 2026-06-19.
        result = classify_deadline("", "1 July 2025", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "passed")

    def test_past_iso_full_date_is_not_verified(self):
        result = classify_deadline("", "2026-05-05", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "passed")

    def test_future_date_stays_verified(self):
        # Over-flagging is the danger — a clearly future date must stay verified.
        result = classify_deadline("", "March 15, 2027", today=TODAY)
        self.assertEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "confirmed_date")

    def test_current_month_is_not_past(self):
        # Leniency: a month-year deadline isn't "past" until the month is over.
        # June 2026 with today 2026-06-19 must NOT be flagged passed.
        result = classify_deadline("", "June 2026", today=TODAY)
        self.assertNotEqual(result.get("deadline_type"), "passed")
        self.assertEqual(result.get("deadline_verified"), True)

    def test_last_month_is_past(self):
        result = classify_deadline("", "May 2026", today=TODAY)
        self.assertEqual(result.get("deadline_type"), "passed")

    def test_rolling_is_unaffected_by_past_check(self):
        result = classify_deadline("open year-round, rolling", "", today=TODAY)
        self.assertEqual(result.get("deadline_type"), "rolling")
        self.assertEqual(result.get("deadline_verified"), True)

    def test_parse_returns_none_for_undatable(self):
        self.assertIsNone(parse_deadline_date("check website"))
        self.assertIsNone(parse_deadline_date(""))


if __name__ == "__main__":
    unittest.main()
