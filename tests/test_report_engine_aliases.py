"""upgraded_score / confidence_level — sixth split-field instance.

Both functions read only submission_page and fees. An entry rumor_mill
answered (submission_url + fee) misses the +0.4 score bump, EATS a -0.2
"unknown fee" penalty despite having a known fee, and reads as lower
confidence than an identical entry with the older spellings. Researched
entries were being ranked below their unresearched twins.
"""

import unittest

from engines.opportunity_report_engine import upgraded_score, confidence_level


class UpgradedScoreAliasTests(unittest.TestCase):

    OLD = {"overall_score": 6.0, "source_url": "https://x.org",
           "submission_page": "https://x.org/apply", "fees": "$35"}
    NEW = {"overall_score": 6.0, "source_url": "https://x.org",
           "submission_url": "https://x.org/apply", "fee": "$35"}

    def test_new_spellings_score_the_same_as_old(self):
        self.assertEqual(upgraded_score(self.OLD, {}), upgraded_score(self.NEW, {}))

    def test_known_fee_under_new_spelling_avoids_the_unknown_fee_penalty(self):
        no_fee = {"overall_score": 6.0, "source_url": "https://x.org"}
        with_fee = {**no_fee, "fee": "$35"}
        self.assertGreater(upgraded_score(with_fee, {}), upgraded_score(no_fee, {}))


class ConfidenceAliasTests(unittest.TestCase):

    def test_new_spellings_yield_the_same_confidence(self):
        old = {"source_url": "https://x.org", "submission_page": "https://x.org/a",
               "deadline": "2026-12-01", "fees": "Free"}
        new = {"source_url": "https://x.org", "submission_url": "https://x.org/a",
               "deadline": "2026-12-01", "fee": "Free"}
        self.assertEqual(confidence_level(old), confidence_level(new))


if __name__ == "__main__":
    unittest.main()
