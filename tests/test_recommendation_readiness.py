import unittest

from recommendation_readiness import assess_actionability


class RecommendationReadinessTests(unittest.TestCase):
    def test_ready_when_deadline_fee_and_submission_path_are_verified(self):
        result = assess_actionability({
            "category": "japan_watercolor_open_call",
            "native_medium": "painting",
            "deadline_verified": True,
            "fees_verified": True,
            "submission_page": "https://example.test/apply",
            "url_verification_status": "ok",
        })

        self.assertEqual(result["actionability_status"], "ready")
        self.assertEqual(result["review_flags"], [])
        self.assertIn("Submission path is clear", result["recommendation_reasons"])

    def test_relationship_target_can_be_check_before_acting_with_unknown_fee(self):
        result = assess_actionability({
            "category": "cafe_gallery",
            "native_medium": "painting",
            "deadline": "",
            "fees": "Unknown — confirm with venue",
            "contact_verified": True,
            "url_verification_status": "error",
            "status": "needs_reverification",
        })

        self.assertEqual(result["actionability_status"], "check_before_acting")
        self.assertIn("fee_unknown", result["review_flags"])
        self.assertIn("source_needs_reverification", result["review_flags"])
        self.assertIn("Relationship contact route exists", result["recommendation_reasons"])

    def test_unclear_submission_or_contact_route_is_review_not_deleted(self):
        result = assess_actionability({
            "category": "fair_popup",
            "native_medium": "mixed",
            "deadline_verified": True,
            "fees_verified": True,
            "url_verification_status": "ok",
        })

        self.assertEqual(result["actionability_status"], "review")
        self.assertIn("submission_or_contact_missing", result["review_flags"])

    def test_closed_or_stale_wins_over_other_signals(self):
        result = assess_actionability({
            "category": "global_open_call",
            "native_medium": "painting",
            "status": "closed_this_cycle",
            "deadline_verified": True,
            "fees_verified": True,
            "submission_page": "https://example.test/apply",
            "url_verification_status": "ok",
        })

        self.assertEqual(result["actionability_status"], "closed_or_stale")
        self.assertIn("closed_this_cycle", result["review_flags"])

    def test_student_only_calls_need_review_unless_eligible(self):
        result = assess_actionability({
            "category": "competition_award",
            "native_medium": "painting",
            "student_call": True,
            "deadline_verified": True,
            "fees_verified": True,
            "submission_page": "https://example.test/apply",
            "url_verification_status": "ok",
        })

        self.assertEqual(result["actionability_status"], "review")
        self.assertIn("student_only", result["review_flags"])

    def test_photography_only_is_closed_or_stale_for_this_artist_surface(self):
        result = assess_actionability({
            "category": "photo_open_call",
            "native_medium": "photography",
            "deadline_verified": True,
            "fees_verified": True,
            "submission_page": "https://example.test/apply",
            "url_verification_status": "ok",
        })

        self.assertEqual(result["actionability_status"], "closed_or_stale")
        self.assertIn("photography_only", result["review_flags"])


if __name__ == "__main__":
    unittest.main()
