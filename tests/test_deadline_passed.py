import unittest
from datetime import date

from api import _deadline_passed, shape_card
from recommendation_readiness import RELATIONSHIP_CATEGORIES

TODAY = date(2026, 6, 25)


class ShapeCardServesStrictDeadlineTests(unittest.TestCase):
    """Regression (audit 2026-07-06): shape_card used to recompute its served
    deadline_past with the lenient _deadline_past (7-day grace, no evergreen
    exemption), silently discarding the strict value load_opportunities()
    stamps. Now it uses the same strict _deadline_passed everywhere."""

    def test_served_deadline_past_matches_strict_check(self):
        # A hard-past dated open call: served flag must be True.
        card = shape_card({"title": "X", "category": "grant", "deadline": "2020-01-01"})
        self.assertTrue(card["deadline_past"])

    def test_evergreen_venue_never_served_as_past(self):
        # A café gallery with an old date is evergreen — must NOT be flagged
        # past (the strict check exempts relationship categories).
        cat = next(iter(RELATIONSHIP_CATEGORIES))
        card = shape_card({"title": "Y", "category": cat, "deadline": "2020-01-01"})
        self.assertFalse(card["deadline_past"])


class DeadlinePassedTests(unittest.TestCase):
    """Serve-time past-deadline check. The cardinal rule: never wrongly hide a
    still-open call. New: numeric m/d/y and 2-digit-year formats are now caught
    (previously missed, so genuinely-past calls in that format stayed visible)."""

    def test_iso_past_still_detected(self):
        self.assertTrue(_deadline_passed({"deadline": "2020-01-01"}, today=TODAY))

    def test_numeric_mdy_4digit_past(self):
        self.assertTrue(_deadline_passed({"deadline": "Apply by 5/26/2026"}, today=TODAY))

    def test_numeric_mdy_2digit_past(self):
        self.assertTrue(_deadline_passed({"deadline": "deadline 5/26/26"}, today=TODAY))

    def test_numeric_mdy_future_not_past(self):
        self.assertFalse(_deadline_passed({"deadline": "12/31/2099"}, today=TODAY))

    def test_multi_date_judged_by_latest(self):
        # one past, one future -> still open (judge by the last option)
        self.assertFalse(
            _deadline_passed({"deadline": "5/26/2020 or 12/1/2099"}, today=TODAY)
        )

    def test_no_parseable_date_is_not_past(self):
        self.assertFalse(_deadline_passed({"deadline": "rolling / open"}, today=TODAY))

    def test_relationship_category_is_never_past(self):
        cat = next(iter(RELATIONSHIP_CATEGORIES))
        self.assertFalse(
            _deadline_passed({"category": cat, "deadline": "1/1/2000"}, today=TODAY)
        )

    def test_empty_deadline_is_not_past(self):
        self.assertFalse(_deadline_passed({"deadline": ""}, today=TODAY))

    def test_explicit_closure_phrase_with_no_date_is_past(self):
        # A one-time call whose deadline field is pure prose ("Submissions now
        # closed", as rumor-mill sometimes finds) with no attached date at all.
        self.assertTrue(
            _deadline_passed({"deadline": "Submissions now closed"}, today=TODAY)
        )
        self.assertTrue(
            _deadline_passed({"deadline": "Applications closed"}, today=TODAY)
        )

    def test_closure_phrase_does_not_override_recurring_exemption(self):
        # "annual" already exempts this via _RECURRING_HINTS - the closure
        # phrase must never override that (a recurring call's THIS cycle being
        # closed doesn't mean the opportunity itself is dead).
        self.assertFalse(
            _deadline_passed(
                {"deadline": "Annual — 2026 cycle closed May 22. Watch January 2027."},
                today=TODAY,
            )
        )

    def test_closure_phrase_does_not_override_relationship_category_exemption(self):
        cat = next(iter(RELATIONSHIP_CATEGORIES))
        self.assertFalse(
            _deadline_passed(
                {"category": cat, "deadline": "Submissions now closed"}, today=TODAY
            )
        )

    def test_closure_phrase_with_a_parseable_date_uses_the_date(self):
        # A real date takes precedence over the closure phrase entirely
        # (dates are checked first) - a future date still means open.
        self.assertFalse(
            _deadline_passed(
                {"deadline": "Submissions closed, reopens 12/31/2099"}, today=TODAY
            )
        )


if __name__ == "__main__":
    unittest.main()
