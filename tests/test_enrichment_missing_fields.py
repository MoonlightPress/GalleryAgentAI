"""missing_fields / manual_review_needed — the keystone of the research loop.

Fifth confirmed instance of the split-field class, and the one that made the
needs_research backlog immortal: missing_fields() checked only submission_page,
fees, and contact/email/contact_url — never submission_url, fee, or
contact_email, which are EXACTLY the spellings rumor_mill writes on success.

Chain of the bug (measured 2026-07-28): rumor_mill answers an item ->
enrichment re-stamps manual_review_needed=True because it can't see the
answer's spellings -> differentiation's `verify <= 2 OR manual_review_needed`
refiles it into needs_research -> 713 of 714 backlog members carried the flag,
including 520 items with verification_score >= 4 (fully researched).
"""

import unittest

from opportunity_enrichment_pipeline import missing_fields, enrich_opportunity

ANSWERED = {
    # An item exactly as rumor_mill leaves it after a successful search.
    "title": "X", "source_url": "https://x.org/call",
    "deadline": "2026-12-01", "fee": "$35",
    "submission_url": "https://x.org/apply", "contact_email": "hi@x.org",
}


class MissingFieldsTests(unittest.TestCase):

    def test_submission_url_satisfies_the_submission_check(self):
        self.assertNotIn("submission process", missing_fields(ANSWERED))

    def test_fee_satisfies_the_fees_check(self):
        self.assertNotIn("fees", missing_fields(ANSWERED))

    def test_contact_email_satisfies_the_contact_check(self):
        self.assertNotIn("contact", missing_fields(ANSWERED))

    def test_fully_answered_item_has_nothing_missing(self):
        self.assertEqual(missing_fields(ANSWERED), [])

    def test_unanswered_item_still_reports_missing(self):
        bare = {"title": "X", "source_url": "https://x.org/call"}
        m = missing_fields(bare)
        self.assertIn("submission process", m)
        self.assertIn("deadline", m)

    def test_old_spellings_still_satisfy(self):
        old = {"title": "X", "source_url": "https://x.org/call",
               "deadline": "2026-12-01", "fees": "Free",
               "submission_page": "https://x.org/apply", "contact": "hi@x.org"}
        self.assertEqual(missing_fields(old), [])


class ManualReviewTests(unittest.TestCase):

    def test_answered_item_is_no_longer_flagged_for_manual_review(self):
        out = enrich_opportunity(ANSWERED, {})
        self.assertFalse(out["manual_review_needed"])

    def test_answered_item_is_verified(self):
        out = enrich_opportunity(ANSWERED, {})
        self.assertEqual(out["verification_status"], "verified")

    def test_bare_item_keeps_the_flag(self):
        out = enrich_opportunity({"title": "X", "source_url": "https://x.org/c"}, {})
        self.assertTrue(out["manual_review_needed"])


class ScoreIdempotencyTests(unittest.TestCase):
    """THE score-inflation mechanism (found 2026-07-28). upgraded_score reads
    the stored overall_score as its base and adds bumps (+0.8 ideal-type,
    +0.4 source, +0.4 submission, -0.2 unknown fee) — and enrichment runs in
    every pipeline, so every run compounded the bumps onto the previous run's
    output: 6.0 -> 6.8 -> 7.6 -> 8.4 -> ... -> 10.0. Weeks of monthly/weekly
    runs pushed everything ideal-shaped toward the cap, flattening ranking
    into the "endless 9.4 ties" differentiation complains about. CLAUDE.md:
    "Score inflation is real. The system has repeatedly grown more confident
    while growing less accurate." This was how.

    Fix: the first enrichment snapshots score_base; every later enrichment
    recomputes overall_score FROM THE BASE. Enriching twice must equal
    enriching once."""

    def opp(self):
        return {"title": "X", "overall_score": 6.0, "category": "grant",
                "source_url": "https://x.org", "submission_url": "https://x.org/a",
                "fee": "Free", "deadline": "2026-12-01", "contact_email": "a@x.org"}

    def test_enriching_twice_gives_the_same_score_as_once(self):
        once = enrich_opportunity(self.opp(), {})
        twice = enrich_opportunity(once, {})
        self.assertEqual(once["overall_score"], twice["overall_score"])

    def test_ten_passes_do_not_move_the_score(self):
        out = self.opp()
        for _ in range(10):
            out = enrich_opportunity(out, {})
        self.assertEqual(out["overall_score"],
                         enrich_opportunity(self.opp(), {})["overall_score"])

    def test_first_fixed_enrichment_does_not_move_the_stored_score(self):
        """Migration property: existing scores already contain years of bump
        passes. The first run under the fix must FREEZE them (seed base =
        stored - bump), not add yet another bump on top."""
        out = enrich_opportunity(self.opp(), {})
        self.assertEqual(out["overall_score"], 6.0)
        self.assertIn("score_base", out)

    def test_existing_base_is_respected_not_overwritten(self):
        """An entry already carrying score_base keeps it — overall_score may
        be inflated history; the base is the anchor."""
        opp = {**self.opp(), "score_base": 5.0, "overall_score": 9.4}
        out = enrich_opportunity(opp, {})
        self.assertEqual(out["score_base"], 5.0)
        self.assertLess(out["overall_score"], 9.4)


if __name__ == "__main__":
    unittest.main()
