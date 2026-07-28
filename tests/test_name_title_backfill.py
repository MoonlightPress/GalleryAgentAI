"""name/title backfill — the split-field pair at the identity level.

Found 2026-07-28: 41 live entries have `title` but no `name` (they predate the
name field) — among them National Watercolor Society International Open and
Japan International Watercolor Institute, i.e. real, valuable calls. Serving
paths mostly fall back (`name or title`), but every diff, dedup, or engine that
keys on one spelling silently drops them — same class as added_at/imported_at
and fee/fees. Backfilling both spellings at clean time kills the class instead
of patching each reader.
"""

import unittest

from recommendation_trust_cleaner import backfill_identity


class BackfillIdentityTests(unittest.TestCase):

    def test_title_only_entry_gains_name(self):
        opp = {"title": "National Watercolor Society International Open Exhibition"}
        changed = backfill_identity(opp)
        self.assertTrue(changed)
        self.assertEqual(opp["name"], opp["title"])

    def test_name_only_entry_gains_title(self):
        opp = {"name": "Some Call"}
        self.assertTrue(backfill_identity(opp))
        self.assertEqual(opp["title"], "Some Call")

    def test_entry_with_both_is_untouched(self):
        opp = {"name": "A", "title": "B — long form"}
        self.assertFalse(backfill_identity(opp))
        self.assertEqual(opp["name"], "A")
        self.assertEqual(opp["title"], "B — long form")

    def test_entry_with_neither_is_left_alone(self):
        opp = {"category": "x"}
        self.assertFalse(backfill_identity(opp))
        self.assertNotIn("name", opp)

    def test_empty_string_counts_as_missing(self):
        opp = {"name": "", "title": "Real Title"}
        self.assertTrue(backfill_identity(opp))
        self.assertEqual(opp["name"], "Real Title")


from recommendation_trust_cleaner import is_junk, refresh_visibility


class SocialSourcedGrantTests(unittest.TestCase):
    """Found 2026-07-28: the junk gate hides any entry whose SOURCE is
    instagram/facebook — which was hiding ACC Hong Kong Anniversary
    Fellowships and a Japan Foundation fellowship, discovered via the orgs'
    own official accounts. ACC is a named Tier-4 prestige target (CLAUDE.md).
    A real-looking grant announced on social media is UNVERIFIED, not junk —
    the bucket engine's grant gate already routes unverified grants to
    research_needed, which is where these belong. Non-grant social scrapes
    stay junk: that part of the gate exists for a reason."""

    ACC = {"title": "ACC Hong Kong Anniversary Fellowships 2026",
           "category": "grant",
           "source_url": "https://www.facebook.com/asianculturalcouncil/posts/x"}

    def test_social_sourced_grant_is_not_junk(self):
        self.assertFalse(is_junk(self.ACC))

    def test_social_sourced_non_grant_is_still_junk(self):
        opp = {"title": "cool art reel", "category": "gallery_event",
               "source_url": "https://www.instagram.com/reel/abc"}
        self.assertTrue(is_junk(opp))

    def test_grant_with_genuinely_junk_title_is_still_junk(self):
        """The exemption is for the SOURCE bits only — a grant whose title
        itself trips the junk list stays hidden."""
        opp = {"title": "login to view this page", "category": "grant",
               "source_url": "https://www.facebook.com/x"}
        self.assertTrue(is_junk(opp))

    def test_previously_hidden_entry_is_unhidden_once_no_longer_junk(self):
        """Sticky-flag regression: after the is_junk fix, ACC's fellowships
        stayed hidden because the old verdict was stamped on the data and the
        cleaner only ever setdefault'd. The gate must re-evaluate: junk status
        comes from the CURRENT rules, not from whatever an older rule decided.
        (dead_url_pruner runs after this in the pipeline and re-hides dead
        entries, so restoring show here cannot resurrect dead URLs.)"""
        opp = {**self.ACC, "recommendation_visibility": "hidden"}
        refresh_visibility(opp)
        self.assertEqual(opp["recommendation_visibility"], "show")

    def test_junk_entry_gets_hidden_by_refresh(self):
        opp = {"title": "cool art reel", "category": "gallery_event",
               "source_url": "https://www.instagram.com/reel/abc",
               "recommendation_visibility": "show"}
        refresh_visibility(opp)
        self.assertEqual(opp["recommendation_visibility"], "hidden")


if __name__ == "__main__":
    unittest.main()
