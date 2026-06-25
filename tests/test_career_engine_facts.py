import unittest

from engines.career_strategy_engine import (
    _count_group_shows,
    _has_solo_show,
    _has_institutional_show,
    _blocking_gaps,
)

EMPTY_PROFILE = {"career_history": {"exhibitions": []}}


class ConfidenceGatingTests(unittest.TestCase):
    """Evidence over prediction: a logged show marked 'mentioned' (unconfirmed,
    e.g. a featured collab nobody documented) must NOT inflate the counts."""

    def test_confirmed_group_show_counts(self):
        # base is 1 (Tide from China); one confirmed group show -> 2
        self.assertEqual(
            _count_group_shows(EMPTY_PROFILE, [{"type": "group"}]), 2
        )

    def test_mentioned_group_show_does_not_count(self):
        self.assertEqual(
            _count_group_shows(EMPTY_PROFILE, [{"type": "group", "confidence": "mentioned"}]),
            1,
        )

    def test_mentioned_solo_show_does_not_count(self):
        self.assertFalse(
            _has_solo_show(EMPTY_PROFILE, [{"type": "solo", "confidence": "mentioned"}])
        )

    def test_confirmed_solo_show_counts(self):
        self.assertTrue(_has_solo_show(EMPTY_PROFILE, [{"type": "solo"}]))


class InstitutionalTypeTests(unittest.TestCase):
    """An explicit institutional-type entry should count even if its venue name
    doesn't happen to match a keyword."""

    def test_explicit_institutional_type_counts(self):
        self.assertTrue(
            _has_institutional_show(EMPTY_PROFILE, [{"type": "institutional", "venue": "Some Hall"}])
        )

    def test_mentioned_institutional_does_not_count(self):
        self.assertFalse(
            _has_institutional_show(
                EMPTY_PROFILE, [{"type": "institutional", "venue": "Hall", "confidence": "mentioned"}]
            )
        )


class GapIdTests(unittest.TestCase):
    """Every blocking gap needs a stable id so the UI can attach the right
    'I already did this' form to it."""

    def test_all_gaps_have_ids(self):
        gaps = _blocking_gaps(0, False, False, False, False)
        ids = {g.get("gap_id") for g in gaps}
        self.assertEqual(
            ids,
            {"group_shows", "solo_show", "institutional_show", "international_show", "jws"},
        )


if __name__ == "__main__":
    unittest.main()
