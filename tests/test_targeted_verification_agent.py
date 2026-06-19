import unittest
from datetime import date

from engines.targeted_verification_agent import _deadline_is_real

TODAY = date(2026, 6, 19)


class DeadlineIsRealTests(unittest.TestCase):
    def test_past_deadline_is_not_real(self):
        # A past deadline must not be treated as a real, actionable deadline,
        # or step 83 will re-promote what step 42 corrected.
        self.assertFalse(_deadline_is_real({"deadline": "1 July 2025"}, today=TODAY))

    def test_future_deadline_is_real(self):
        self.assertTrue(_deadline_is_real({"deadline": "March 15, 2027"}, today=TODAY))

    def test_rolling_is_real(self):
        self.assertTrue(_deadline_is_real({"deadline": "Rolling — proposal-based"}, today=TODAY))


if __name__ == "__main__":
    unittest.main()
