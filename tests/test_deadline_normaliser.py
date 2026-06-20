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


class TwoDigitYearTests(unittest.TestCase):
    def test_two_digit_year_past_date_parses(self):
        # "5/26/26" -> 2026-05-26, past relative to 2026-06-19.
        self.assertEqual(parse_deadline_date("5/26/26"), date(2026, 5, 26))

    def test_two_digit_year_past_date_with_time_parses(self):
        # "1/15/25, 6:52 PM" -> 2025-01-15; must not mis-match the time.
        self.assertEqual(parse_deadline_date("1/15/25, 6:52 PM"), date(2025, 1, 15))

    def test_two_digit_year_past_date_not_verified(self):
        result = classify_deadline("", "5/26/26", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "passed")

    def test_two_digit_year_with_time_not_verified(self):
        result = classify_deadline("", "1/15/25, 6:52 PM", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "passed")

    def test_four_digit_year_still_parses(self):
        # Guard: existing 4-digit date handling is untouched.
        self.assertEqual(parse_deadline_date("06/15/2026"), date(2026, 6, 15))


class YearlessDateTests(unittest.TestCase):
    def test_yearless_month_day_is_unconfirmed(self):
        result = classify_deadline("", "April 30", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "unconfirmed_year")

    def test_yearless_month_day_with_suffix_is_unconfirmed(self):
        result = classify_deadline("", "January 31st", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "unconfirmed_year")

    def test_yearless_japanese_month_day_is_unconfirmed(self):
        result = classify_deadline("", "2月26日 (February 26)", today=TODAY)
        self.assertNotEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "unconfirmed_year")

    def test_four_digit_year_date_stays_verified_guard(self):
        # Guard: a dated deadline WITH a 4-digit year is unaffected.
        result = classify_deadline("", "March 15, 2027", today=TODAY)
        self.assertEqual(result.get("deadline_verified"), True)
        self.assertEqual(result.get("deadline_type"), "confirmed_date")

    def test_rolling_stays_rolling_guard(self):
        # Guard: a rolling deadline is not downgraded to unconfirmed_year.
        result = classify_deadline("submissions accepted anytime", "anytime", today=TODAY)
        self.assertEqual(result.get("deadline_type"), "rolling")
        self.assertEqual(result.get("deadline_verified"), True)


class VenueExemptionTests(unittest.TestCase):
    def test_venue_with_past_date_is_not_flagged_passed(self):
        # A bookshop/gallery is an evergreen venue — a stale date must NOT mark it expired.
        result = classify_deadline("", "1 July 2025", today=TODAY, category="bookstore_gallery")
        self.assertNotEqual(result.get("deadline_type"), "passed")
        self.assertNotEqual(result.get("deadline_past"), True)

    def test_non_venue_past_date_still_flagged_passed(self):
        # A dated open call is still flagged past — the exemption is venue-only.
        result = classify_deadline("", "1 July 2025", today=TODAY, category="global_open_call")
        self.assertEqual(result.get("deadline_type"), "passed")

    def test_no_category_behaves_as_before(self):
        result = classify_deadline("", "1 July 2025", today=TODAY)
        self.assertEqual(result.get("deadline_type"), "passed")


if __name__ == "__main__":
    unittest.main()
