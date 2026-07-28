"""Organizations-only eligibility — detection and routing.

Found 2026-07-27 while hand-verifying the Tokyo Grant Program: Category II
(deadline 3 days out, surfaced near the top of her digest) is open to 団体
(organizations) only — individual Tokyo residents are ineligible. The system
had no way to represent that, so a grant she can never apply to was presented
as actionable. This is the exact failure CLAUDE.md warns about: recommending
the impossible wastes attention and sets the wrong expectation.

Three pieces:
  1. prerequisite_detection_engine gains an `organizations_only` signal
     (ja + en phrasings, plus the `eligibility` field in its text blob).
  2. exclusive_strategy_bucket_engine routes organizations_only -> reject.
     Unlike exhibition-credit prerequisites (meetable in time — stretch),
     org-only is structural: she is an individual, full stop.
  3. manual_research records may assert `eligibility`, so a hand-verified
     restriction flows in through the sanctioned source file.
"""

import unittest

from engines.prerequisite_detection_engine import detect_from_text, build_text_blob
from engines.exclusive_strategy_bucket_engine import choose_bucket
from engines.manual_research_engine import validate_record


class DetectionTests(unittest.TestCase):

    def test_japanese_organizations_only_phrasings_are_detected(self):
        for text in (
            "応募資格：東京都内に活動拠点を置く団体のみ",
            "対象は団体に限る（個人は応募できません）",
            "個人での応募は不可。アートnpo法人・実行委員会が対象",
        ):
            self.assertIn("organizations_only", detect_from_text(text.lower()), text)

    def test_english_organizations_only_phrasings_are_detected(self):
        for text in (
            "applicants must be organizations based in tokyo",
            "individuals are ineligible; groups only",
            "open to arts organizations only",
        ):
            self.assertIn("organizations_only", detect_from_text(text), text)

    def test_individual_friendly_text_is_not_flagged(self):
        for text in (
            "open to individual artists and groups",
            "個人・団体を問わず応募可能",
            "individuals welcome to apply",
        ):
            self.assertNotIn("organizations_only", detect_from_text(text.lower()), text)

    def test_eligibility_field_feeds_the_text_blob(self):
        """A hand-verified eligibility note must reach detection even when the
        scraped prose never mentioned the restriction."""
        opp = {"title": "Some Grant", "eligibility": "団体のみ（個人不可）"}
        self.assertIn("団体のみ", build_text_blob(opp))


class RoutingTests(unittest.TestCase):

    BASE = {"title": "X Grant", "category": "grant", "overall_score": 9.0,
            "verification_status": "verified"}

    def test_organizations_only_routes_to_reject(self):
        opp = {**self.BASE, "prerequisites": ["organizations_only"]}
        self.assertEqual(choose_bucket(opp), "reject")

    def test_reject_beats_the_grant_stretch_gate(self):
        """A verified, high-scoring org-only grant is still un-actionable for
        an individual — the score must not rescue it into stretch_targets."""
        opp = {**self.BASE, "verification_bucket": "stretch_targets",
               "prerequisites": ["organizations_only"]}
        self.assertEqual(choose_bucket(opp), "reject")

    def test_bucket_override_still_wins(self):
        """bucket_override is the sanctioned manual pin — it outranks
        everything, including this gate."""
        opp = {**self.BASE, "prerequisites": ["organizations_only"],
               "bucket_override": "stretch_targets"}
        self.assertEqual(choose_bucket(opp), "stretch_targets")

    def test_other_prerequisites_do_not_reject(self):
        """Meetable-in-time prerequisites (exhibition credits etc.) keep their
        existing routing — only the structural one rejects."""
        opp = {**self.BASE, "prerequisites": ["exhibition_credits_3"]}
        self.assertNotEqual(choose_bucket(opp), "reject")


class ManualResearchEligibilityTests(unittest.TestCase):

    def test_record_may_assert_eligibility(self):
        rec = {"title": "X", "source_url": "https://example.org/call",
               "verified_at": "2026-07-28",
               "found": {"eligibility": "団体のみ — individual artists ineligible"}}
        ok, why = validate_record(rec)
        self.assertTrue(ok, why)

    def test_placeholder_eligibility_is_still_rejected(self):
        rec = {"title": "X", "source_url": "https://example.org/call",
               "verified_at": "2026-07-28", "found": {"eligibility": "unknown"}}
        ok, _ = validate_record(rec)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
