"""A recurring event whose CURRENT edition is over must not read as open.

2026-08-21: Today's Focus offered 第113回 日本水彩展 as her High Impact move of
the day. Its deadline field read:

    "Annual — 113th edition June 2026; 114th expected spring 2027
     (check nihonsuisai.or.jp)"

The 113th closed in June. The 114th is *expected*, not open. But "annual" is in
_RECURRING_HINTS, and that check short-circuited _deadline_passed() before it
ever looked at the dates — so a finished exhibition became the most important
thing she could do today.

The recurring exemption exists so a rolling/undated call is never hidden, and
that is right. What it must not do is override a concrete date that has already
passed. Recurrence says the thing will come back; it does not say it is open
now.

Rule: apply the recurring exemption only when the field carries no concrete
date. If every concrete date in it is in the past, this edition is over.
"""
import unittest
from datetime import date

import api


TODAY = date(2026, 8, 21)


class RecurringWithPastEditionTests(unittest.TestCase):
    def test_annual_with_finished_edition_is_past(self):
        item = {"deadline": "Annual — 113th edition June 2026; 114th expected "
                            "spring 2027 (check nihonsuisai.or.jp)"}
        self.assertTrue(api._deadline_passed(item, today=TODAY))

    def test_annual_with_future_edition_is_not_past(self):
        item = {"deadline": "Annual — next edition closes June 2027"}
        self.assertFalse(api._deadline_passed(item, today=TODAY))

    def test_undated_rolling_still_exempt(self):
        """The case the exemption was built for — never hide these."""
        for raw in ("Rolling — check website for details",
                    "Ongoing, no fixed deadline",
                    "Annual, dates not yet announced",
                    "Year-round submissions"):
            self.assertFalse(api._deadline_passed({"deadline": raw}, today=TODAY), raw)

    def test_relationship_venues_never_archived_on_a_date(self):
        """Consignment venues keep event notes in the deadline field."""
        for cat in api.RELATIONSHIP_CATEGORIES:
            item = {"category": cat, "deadline": "Annual — spring 2026 market"}
            self.assertFalse(api._deadline_passed(item, today=TODAY), cat)
            break

    def test_recurring_with_a_still_open_date_stays_open(self):
        item = {"deadline": "毎年開催 — 2026年9月30日締切"}
        self.assertFalse(api._deadline_passed(item, today=TODAY))

    def test_recurring_month_only_uses_month_leniency(self):
        """Day-less months stay open until the month is over, recurring or not."""
        self.assertFalse(api._deadline_passed({"deadline": "Annual — August 2026"}, today=TODAY))
        self.assertTrue(api._deadline_passed({"deadline": "Annual — June 2026"}, today=TODAY))


if __name__ == "__main__":
    unittest.main()


class DatedCallInARelationshipCategoryTests(unittest.TestCase):
    """2026-08-21: Today's Focus offered "Call for Entry: Showcase your art in
    Tokyo, Japan" as her Quick Win. Its deadline (1 August 2026) was three weeks
    past and its own link pointed at the 2025 edition.

    It survived because its category is `gallery`, and relationship categories
    are exempt from deadline checks — correctly, because a consignment venue's
    deadline field holds an event note, not a binding cutoff.

    But a thing whose NAME says "Call for Entry" is a dated call that was filed
    in a venue category, not an evergreen venue. The exemption should turn on
    what the entry IS, not only on how it was categorised.
    """

    DATED = ("call for entry: showcase your art in tokyo, japan",
             "open call for artists 2026", "公募展 2026", "call for submissions")

    def test_dated_call_in_a_gallery_category_still_expires(self):
        for name in self.DATED:
            item = {"category": "gallery", "name": name, "deadline": "1st August 2026"}
            self.assertTrue(api._deadline_passed(item, today=TODAY), name)

    def test_real_consignment_venue_keeps_its_exemption(self):
        for name in ("Avancé 船橋 委託販売作家募集", "ハコミツ ハンドメイド委託作家募集",
                     "Clouds Gallery Coffee Koenji", "Nui Hostel Bar Lounge Asakusa"):
            item = {"category": "gallery", "name": name, "deadline": "1st August 2026"}
            self.assertFalse(api._deadline_passed(item, today=TODAY), name)
