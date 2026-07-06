import unittest
from datetime import date

import api


TODAY = date(2026, 7, 6)  # the day the ライフウィズアート助成 leak was reported


class DeadlinePassedFormatCoverageTests(unittest.TestCase):
    """Regression tests: _deadline_passed must parse every date format that
    actually occurs in compact_opportunities.json. On 2026-07-06 the live
    Stretch Goal slot served ライフウィズアート助成 whose deadline field read
    '29-Jun-2026' — a week past — because no regex handled hyphenated
    DD-Mon-YYYY. A dataset scan found sibling holes: ordinal-suffix English
    dates, day-first slash dates, and day-less English month-years."""

    def _passed(self, deadline):
        return api._deadline_passed({"deadline": deadline, "category": "grant"}, today=TODAY)

    # ── the live bug and its siblings ──────────────────────────────────────
    def test_hyphenated_dd_mon_yyyy_past(self):
        self.assertTrue(self._passed("29-Jun-2026"))
        self.assertTrue(self._passed("16-Jun-2026"))

    def test_hyphenated_dd_mon_yyyy_future(self):
        self.assertFalse(self._passed("29-Dec-2026"))

    def test_ordinal_suffix_english_date_past(self):
        self.assertTrue(self._passed("19th December 2025"))

    def test_ordinal_suffix_english_date_future(self):
        self.assertFalse(self._passed("1st August 2026"))

    def test_day_first_slash_date_past(self):
        self.assertTrue(self._passed("31/3/2026"))  # 31 March 2026 (d/m/y)

    def test_english_month_year_dayless_past(self):
        self.assertTrue(self._passed("April 2025"))
        self.assertTrue(self._passed("March 2026"))
        self.assertTrue(self._passed("May 2026"))

    def test_english_month_year_dayless_current_month_is_lenient(self):
        # Same leniency as the Japanese 2026年7月 rule: not past until the
        # month is over.
        self.assertFalse(self._passed("July 2026"))
        self.assertFalse(self._passed("December 2026"))

    # ── year-less dates resolve to the cycle they were discovered in ──────
    def test_yearless_range_resolved_against_added_at(self):
        # The second live leak (2026-07-06): a duplicate ライフウィズアート助成
        # added 2026-07-05 with deadline '5/25 – 6/29' — no year, so the
        # "year-less can never expire" leniency let it into the Stretch slot.
        self.assertTrue(api._deadline_passed(
            {"deadline": "5/25 – 6/29", "added_at": "2026-07-05", "category": "grant"},
            today=TODAY))

    def test_yearless_single_date_resolved_against_added_at(self):
        self.assertTrue(api._deadline_passed(
            {"deadline": "4/30", "added_at": "2026-07-05", "category": "grant"},
            today=TODAY))

    def test_yearless_date_near_year_boundary_rolls_forward(self):
        # Scraped in December, deadline '1/15' means NEXT January, not last.
        self.assertFalse(api._deadline_passed(
            {"deadline": "1/15", "added_at": "2026-12-01", "category": "grant"},
            today=date(2026, 12, 5)))

    def test_yearless_jp_month_day_resolved(self):
        self.assertTrue(api._deadline_passed(
            {"deadline": "6月29日", "added_at": "2026-07-05", "category": "grant"},
            today=TODAY))

    def test_unparseable_year_present_stays_lenient(self):
        # A 4-digit year we couldn't attribute → can't place the m/d in a
        # cycle → keep the old leniency (never hide a possibly-open call).
        self.assertFalse(self._passed("2026 edition: watch 10/1 for next call"))

    # ── formats that already worked must keep working ─────────────────────
    def test_existing_formats_unbroken(self):
        self.assertTrue(self._passed("2026年5月25日"))
        self.assertTrue(self._passed("2026-05-25"))
        self.assertTrue(self._passed("May 25, 2026"))
        self.assertTrue(self._passed("25 May 2026"))
        self.assertFalse(self._passed("2026年12月25日"))
        self.assertFalse(self._passed("Rolling"))
        self.assertFalse(self._passed(""))

    def test_range_judged_by_latest_date(self):
        self.assertFalse(self._passed("Oct 31 2025 or Aug 25 2026"))

    def test_relationship_venues_stay_exempt(self):
        self.assertFalse(api._deadline_passed(
            {"deadline": "29-Jun-2026", "category": "cafe_gallery"}, today=TODAY))


class NoExpiredCardInTodaysFocusTests(unittest.TestCase):
    """End-to-end guard over the real dataset: no slot in get_today() may
    serve a card whose deadline field contains a concrete, non-recurring
    date that is clearly in the past."""

    def test_live_dataset_serves_no_expired_focus_cards(self):
        result = api.get_today()
        for slot in ("quick_win", "high_impact", "stretch_goal"):
            card = result.get(slot)
            if not card:
                continue
            self.assertFalse(
                api._deadline_passed(card),
                f"{slot} serves expired card {card.get('name')!r} "
                f"(deadline={card.get('deadline')!r})",
            )


if __name__ == "__main__":
    unittest.main()
