"""verification_score — the function that decides needs_research membership.

Root cause of the needs_research refill loop (714-item backlog, 2026-07-28):
rumor_mill answers an item by writing `deadline`, `fee`, `submission_url` —
but verification_score counted only `submission_page` and `fees`, the OTHER
spellings of those split-field pairs. An answered item scored <= 2, was
refiled into needs_research on the next differentiation pass, and re-searched
forever. The drain (rumor_mill moves items out) lost to the refill every
cycle, which is why the backlog only ever grew.

Fourth confirmed instance of the split-field class (added_at/imported_at,
fee/fees at serve time, name/title, now fee/fees + submission_page/url at
scoring time).
"""

import unittest

from engines.opportunity_differentiation_engine import verification_score


class VerificationScoreTests(unittest.TestCase):

    def test_submission_url_counts_like_submission_page(self):
        self.assertEqual(verification_score({"submission_page": "https://x.org/apply"}),
                         verification_score({"submission_url": "https://x.org/apply"}))

    def test_fee_counts_like_fees(self):
        self.assertEqual(verification_score({"fees": "Free"}),
                         verification_score({"fee": "Free"}))

    def test_an_item_rumor_mill_answered_scores_above_the_research_gate(self):
        """rumor_mill writes exactly these three fields on success. The result
        must clear the needs_research threshold (verify <= 2), or the item
        cycles back into the bucket it was just researched out of."""
        answered = {"deadline": "2026-12-01", "fee": "$35",
                    "submission_url": "https://x.org/apply"}
        self.assertGreater(verification_score(answered), 2)

    def test_unresearched_item_still_gates_into_research(self):
        self.assertLessEqual(verification_score({"deadline": "2026-12-01"}), 2)
        self.assertLessEqual(verification_score({}), 2)

    def test_both_spellings_together_do_not_double_count(self):
        one = verification_score({"submission_page": "https://x.org/a"})
        both = verification_score({"submission_page": "https://x.org/a",
                                   "submission_url": "https://x.org/a"})
        self.assertEqual(one, both)


if __name__ == "__main__":
    unittest.main()
