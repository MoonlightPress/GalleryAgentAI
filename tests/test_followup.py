import unittest
from datetime import datetime, timezone

from api import is_overdue_followup


# A fixed "now" so the tests are deterministic regardless of when they run.
NOW = datetime(2026, 6, 19, 12, 0, 0, tzinfo=timezone.utc)


class IsOverdueFollowupTests(unittest.TestCase):
    """Pure, network-free tests for the CRM follow-up staleness decision.

    Bug: a malformed / non-ISO ``last_contacted`` used to be treated as an
    overdue follow-up (the ``except`` branch defaulted to surfacing the
    contact). A date we cannot parse is *unknown*, not *overdue* — it must
    never spam the Quick Win slot on the strength of a parse failure alone.
    """

    # ── Malformed / unparseable dates: UNKNOWN, never surfaced ──────────────
    def test_malformed_date_is_not_overdue(self):
        self.assertFalse(is_overdue_followup("not-a-date", now=NOW))

    def test_garbage_string_is_not_overdue(self):
        self.assertFalse(is_overdue_followup("yesterday-ish", now=NOW))

    def test_partial_nonsense_is_not_overdue(self):
        # Looks date-ish but is not valid ISO and not parseable.
        self.assertFalse(is_overdue_followup("2026-13-99", now=NOW))

    def test_none_is_not_overdue(self):
        # A None value is missing, not stale — do not surface on a parse error.
        self.assertFalse(is_overdue_followup(None, now=NOW))

    # ── Empty / missing: treated as "no contact date known", not overdue ────
    def test_empty_string_is_not_overdue(self):
        self.assertFalse(is_overdue_followup("", now=NOW))

    # ── Genuinely old valid ISO date: SURFACED ─────────────────────────────
    def test_old_valid_iso_date_is_overdue(self):
        # 60 days before NOW — comfortably past the 30-day threshold.
        old = "2026-04-20T09:00:00+00:00"
        self.assertTrue(is_overdue_followup(old, now=NOW))

    def test_old_valid_date_only_is_overdue(self):
        # Date-only ISO, no time component, well past the threshold.
        self.assertTrue(is_overdue_followup("2026-01-01", now=NOW))

    def test_old_valid_zulu_date_is_overdue(self):
        # Trailing "Z" must be accepted as UTC.
        self.assertTrue(is_overdue_followup("2026-04-20T09:00:00Z", now=NOW))

    # ── Recent valid date: NOT surfaced ────────────────────────────────────
    def test_recent_valid_date_is_not_overdue(self):
        # 5 days before NOW — inside the 30-day window.
        recent = "2026-06-14T09:00:00+00:00"
        self.assertFalse(is_overdue_followup(recent, now=NOW))

    def test_exactly_at_threshold_is_overdue(self):
        # 30 days before NOW — the boundary is inclusive (>= 30).
        boundary = "2026-05-20T12:00:00+00:00"
        self.assertTrue(is_overdue_followup(boundary, now=NOW))

    def test_just_under_threshold_is_not_overdue(self):
        # 29 days before NOW — just inside the window.
        under = "2026-05-21T13:00:00+00:00"
        self.assertFalse(is_overdue_followup(under, now=NOW))


if __name__ == "__main__":
    unittest.main()
