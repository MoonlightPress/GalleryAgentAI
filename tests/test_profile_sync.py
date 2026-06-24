import unittest

from engines.profile_sync import (
    apply_peppercorn_edits,
    select_email_targets,
    clear_drafts_stale,
)


class ApplyPeppercornEditsTests(unittest.TestCase):
    """When the artist edits her statement in Peppercorn, that edit must reach
    the canonical artist_master_profile.json (the file the email-draft writer
    reads) and mark the existing drafts stale so a regen knows to refresh."""

    def test_statement_edit_propagates_to_master(self):
        master = {"artist_statement": {"synthesized_en": "old statement"}}
        pepper = {"artist_statement": "a brand new statement"}
        out, changed = apply_peppercorn_edits(master, pepper)
        self.assertTrue(changed)
        self.assertEqual(out["artist_statement"]["synthesized_en"], "a brand new statement")

    def test_statement_edit_marks_drafts_stale(self):
        master = {"artist_statement": {"synthesized_en": "old"}}
        out, _ = apply_peppercorn_edits(master, {"artist_statement": "new"})
        self.assertTrue(out.get("email_drafts_stale"))

    def test_unchanged_statement_is_noop(self):
        master = {"artist_statement": {"synthesized_en": "same"}}
        out, changed = apply_peppercorn_edits(master, {"artist_statement": "same"})
        self.assertFalse(changed)
        self.assertFalse(out.get("email_drafts_stale"))

    def test_empty_statement_does_not_wipe_master(self):
        # Clearing the box in the UI must not erase her real statement.
        master = {"artist_statement": {"synthesized_en": "real statement"}}
        out, changed = apply_peppercorn_edits(master, {"artist_statement": "   "})
        self.assertFalse(changed)
        self.assertEqual(out["artist_statement"]["synthesized_en"], "real statement")

    def test_missing_statement_block_is_created(self):
        master = {}
        out, changed = apply_peppercorn_edits(master, {"artist_statement": "first ever"})
        self.assertTrue(changed)
        self.assertEqual(out["artist_statement"]["synthesized_en"], "first ever")

    def test_peppercorn_without_statement_is_noop(self):
        master = {"artist_statement": {"synthesized_en": "keep"}}
        out, changed = apply_peppercorn_edits(master, {"goals": ["x"]})
        self.assertFalse(changed)
        self.assertEqual(out["artist_statement"]["synthesized_en"], "keep")


class SelectEmailTargetsTests(unittest.TestCase):
    """Target selection for the draft writer. Normally only opps MISSING drafts
    are written (cheap, idempotent). But when the profile changed
    (email_drafts_stale), every eligible opp must be re-targeted so the stale
    drafts actually refresh."""

    def _opp(self, tier=1, bucket=None, score=1.0, ja="", en=""):
        return {
            "career_tier": tier,
            "exclusive_primary_bucket": bucket,
            "overall_score": score,
            "email_ja": ja,
            "email_en": en,
        }

    def test_normal_run_targets_only_missing_drafts(self):
        opps = [
            self._opp(score=2, ja="have", en="have"),   # already has drafts
            self._opp(score=1, ja="", en=""),            # missing
        ]
        targets = select_email_targets(opps, master={}, limit=10)
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0]["overall_score"], 1)

    def test_stale_run_targets_all_eligible(self):
        opps = [
            self._opp(score=2, ja="have", en="have"),
            self._opp(score=1, ja="", en=""),
        ]
        targets = select_email_targets(opps, master={"email_drafts_stale": True}, limit=10)
        self.assertEqual(len(targets), 2)

    def test_eligibility_includes_immediate_best_moves_off_tier(self):
        opps = [self._opp(tier=4, bucket="immediate_best_moves", ja="", en="")]
        targets = select_email_targets(opps, master={}, limit=10)
        self.assertEqual(len(targets), 1)

    def test_ineligible_opp_is_excluded(self):
        opps = [self._opp(tier=4, bucket=None, ja="", en="")]
        targets = select_email_targets(opps, master={}, limit=10)
        self.assertEqual(targets, [])

    def test_limit_is_respected_and_sorted_by_score(self):
        opps = [
            self._opp(score=1, ja="", en=""),
            self._opp(score=3, ja="", en=""),
            self._opp(score=2, ja="", en=""),
        ]
        targets = select_email_targets(opps, master={}, limit=2)
        self.assertEqual([t["overall_score"] for t in targets], [3, 2])


class ClearDraftsStaleTests(unittest.TestCase):
    def test_clears_flag(self):
        out = clear_drafts_stale({"email_drafts_stale": True})
        self.assertFalse(out.get("email_drafts_stale"))


if __name__ == "__main__":
    unittest.main()
