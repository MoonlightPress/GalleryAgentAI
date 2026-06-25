"""Tests for the graduated career ladder (Scott, 2026-06-25).

Her corrected record shows solo shows, museum/institutional group shows, and an
international (London) showing. The advice MUST graduate past foundation-building:
no "needs a first solo" / "needs more group shows before a solo" framing, and the
real next levers (representation, bigger solo venues, fairs, residencies, grants,
press, a second book) must surface instead.
"""
import unittest

from engines.career_strategy_engine import (
    _is_solo_type,
    _is_group_type,
    _has_international_show,
    _has_representation,
    _has_residency,
    _has_grant,
    _count_solo_shows,
    _count_group_shows,
    _blocking_gaps,
    _next_tier_levers,
)


class TypeMatchingTests(unittest.TestCase):
    """The 'group/solo not specified on source' disclaimer must not be mistaken
    for either a group or a solo credit."""

    def test_not_specified_is_neither_group_nor_solo(self):
        t = "exhibition (group/solo not specified on source)"
        self.assertFalse(_is_solo_type(t))
        self.assertFalse(_is_group_type(t))

    def test_real_solo_matches(self):
        self.assertTrue(_is_solo_type("solo show"))

    def test_real_group_matches(self):
        self.assertTrue(_is_group_type("group show (6 illustrators)"))


class InternationalDetectionTests(unittest.TestCase):
    """A confirmed showing in a non-China/Japan city counts as international even
    when the venue name is blank and the title says nothing about 'international'."""

    def _profile(self, city, venue="—", title="Some Show"):
        return {"career_history": {"exhibitions": [
            {"title": title, "venue": venue, "city": city, "confidence": "confirmed"}
        ]}}

    def test_london_city_counts(self):
        self.assertTrue(_has_international_show(self._profile("London, UK"), []))

    def test_tokyo_city_does_not_count(self):
        self.assertFalse(_has_international_show(self._profile("Tokyo, Japan"), []))

    def test_shanghai_city_does_not_count(self):
        self.assertFalse(_has_international_show(self._profile("Shanghai, China"), []))


class NextTierSignalTests(unittest.TestCase):
    def test_representation_none_confirmed_reads_false(self):
        self.assertFalse(_has_representation(
            {"career_history": {"gallery_representation": "none confirmed"}}))

    def test_representation_named_reads_true(self):
        self.assertTrue(_has_representation(
            {"career_history": {"gallery_representation": "Tsuki Gallery"}}))

    def test_residency_none_found_reads_false(self):
        self.assertFalse(_has_residency(
            {"career_history": {"residencies": "none found"}}, []))

    def test_grant_none_found_reads_false(self):
        self.assertFalse(_has_grant({"career_history": {"awards": "none found"}}))


class GraduatedLadderTests(unittest.TestCase):
    """An artist past foundation gets the next-tier ladder, never the foundation
    'first solo / more group shows' gaps."""

    def _graduated_gaps(self):
        # group_shows>=3, has_solo, has_institutional -> foundation complete
        return _blocking_gaps(
            8, True, True, has_international=True, has_jws=False,
            solo_shows=2, has_representation=False, has_residency=False,
            has_grant=False, publications=2,
        )

    def test_no_foundation_gaps_when_graduated(self):
        ids = {g["gap_id"] for g in self._graduated_gaps()}
        for forbidden in ("group_shows", "solo_show", "institutional_show"):
            self.assertNotIn(forbidden, ids)

    def test_representation_is_first_and_highest(self):
        gaps = self._graduated_gaps()
        self.assertEqual(gaps[0]["gap_id"], "gallery_representation")
        self.assertEqual(gaps[0]["priority"], "high")

    def test_real_levers_present(self):
        ids = {g["gap_id"] for g in self._graduated_gaps()}
        self.assertEqual(
            ids,
            {"gallery_representation", "solo_venue_quality", "art_fairs",
             "residency", "grant", "critical_press", "monograph"},
        )

    def test_no_text_claims_she_lacks_a_solo(self):
        # The deficit framing — telling an artist who has solos that she needs a
        # first one, or more group shows before a gallery will discuss a solo —
        # must never appear. (Mentioning her real "first solo collection" is fine.)
        blob = " ".join(
            (g.get("detail", "") + g.get("gap", "")) for g in self._graduated_gaps()
        ).lower()
        self.assertNotIn("a first solo show", blob)
        self.assertNotIn("within reach", blob)
        self.assertNotIn("before a gallery will discuss a solo", blob)
        self.assertNotIn("more group shows", blob)

    def test_every_graduated_lever_is_localized(self):
        for g in _next_tier_levers(2, False, False, False, False, False, 2):
            self.assertIn("gap_zh", g)
            self.assertIn("detail_zh", g)
            self.assertIn("action_zh", g)

    def test_foundation_ladder_still_fires_for_a_beginner(self):
        # group_shows<3 & no solo & no institutional -> still foundation stage.
        ids = {g["gap_id"] for g in _blocking_gaps(1, False, False, False, False)}
        self.assertIn("group_shows", ids)
        self.assertIn("solo_show", ids)


if __name__ == "__main__":
    unittest.main()
