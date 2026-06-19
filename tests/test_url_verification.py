import unittest

from engines.url_verification_engine import decide_url_status


class DecideUrlStatusTests(unittest.TestCase):
    """Pure, network-free tests for the url_verification_status decision.

    Bug: an opportunity with no official_website AND no submission_page was
    being marked url_verification_status == "ok" because the engine fell back
    to a discovery-trail source_url and live-checked that instead. You cannot
    verify a URL that (for the purposes of the opportunity) does not exist.
    """

    def test_no_url_is_not_ok(self):
        # The core contradiction: no official_website, no submission_page.
        opp = {
            "name": "Royal Watercolour Society Open Exhibition",
            "official_website": None,
            "submission_page": "",
            # A discovery-trail URL must NOT make this "ok".
            "source_url": "https://royalwatercoloursociety.co.uk/",
        }
        status = decide_url_status(opp)
        self.assertNotEqual(status, "ok")
        self.assertEqual(status, "no_url")

    def test_both_fields_missing_keys_is_no_url(self):
        opp = {"name": "Asian Cultural Council"}
        self.assertEqual(decide_url_status(opp), "no_url")

    def test_empty_strings_are_no_url(self):
        opp = {"official_website": "", "submission_page": ""}
        self.assertEqual(decide_url_status(opp), "no_url")

    def test_empty_list_is_no_url(self):
        # submission_page is occasionally stored as a list.
        opp = {"official_website": None, "submission_page": []}
        self.assertEqual(decide_url_status(opp), "no_url")

    def test_official_website_present_is_checkable(self):
        # A real site is present -> the engine is allowed to perform a live
        # check; the decision function should report it as "has_url" (not
        # short-circuited to no_url). It must never be "no_url" here.
        opp = {"official_website": "https://example.org/", "submission_page": ""}
        self.assertNotEqual(decide_url_status(opp), "no_url")

    def test_submission_page_present_is_checkable(self):
        opp = {"official_website": "", "submission_page": "https://example.org/apply"}
        self.assertNotEqual(decide_url_status(opp), "no_url")

    def test_submission_page_list_with_value_is_checkable(self):
        opp = {"official_website": None, "submission_page": ["https://example.org/apply"]}
        self.assertNotEqual(decide_url_status(opp), "no_url")


if __name__ == "__main__":
    unittest.main()
