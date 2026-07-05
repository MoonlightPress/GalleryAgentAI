import unittest

from api import _contact_value, _has_email_contact, _fees_value, _submission_url


class FieldAccessorTests(unittest.TestCase):
    """Regression (audit 2026-07-06): same-concept-different-key field pairs
    written by different-era engines. A reader checking only one key silently
    dropped entries carrying the other — 51 live venues store their address in
    contact_email only and were invisible to Quick Win eligibility."""

    def test_contact_prefers_contact_then_contact_email(self):
        self.assertEqual(_contact_value({"contact": "a@x.com"}), "a@x.com")
        self.assertEqual(_contact_value({"contact_email": "b@y.com"}), "b@y.com")
        self.assertEqual(_contact_value({"contact": "a@x.com", "contact_email": "b@y.com"}), "a@x.com")
        self.assertEqual(_contact_value({}), "")

    def test_has_email_contact_sees_contact_email_only_entries(self):
        # The core fix: a venue with ONLY contact_email is now reachable
        # (was silently invisible to Quick Win when only "contact" was checked).
        self.assertTrue(_has_email_contact({"contact_email": "hi@gallery.jp"}))
        self.assertTrue(_has_email_contact({"contact": "reach us at hi@x.com"}))
        # Pre-existing (preserved) behavior: an IG handle counts as reachable —
        # a DM is a legitimate reach channel for these café/shop venues.
        self.assertTrue(_has_email_contact({"contact": "@bookandsons (Instagram)"}))
        self.assertFalse(_has_email_contact({"contact": "call 03-1234-5678"}))
        self.assertFalse(_has_email_contact({}))

    def test_fees_falls_back_to_singular_fee(self):
        self.assertEqual(_fees_value({"fees": "Free"}), "Free")
        self.assertEqual(_fees_value({"fee": "$25"}), "$25")
        self.assertEqual(_fees_value({"fees": "Free", "fee": "$25"}), "Free")
        self.assertEqual(_fees_value({}), "")

    def test_submission_url_falls_back_to_submission_url_key(self):
        self.assertEqual(_submission_url({"submission_page": "https://a"}), "https://a")
        self.assertEqual(_submission_url({"submission_url": "https://b"}), "https://b")
        self.assertEqual(_submission_url({"submission_page": "https://a", "submission_url": "https://b"}), "https://a")
        self.assertEqual(_submission_url({}), "")


if __name__ == "__main__":
    unittest.main()
