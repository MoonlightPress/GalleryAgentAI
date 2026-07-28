"""Fee extraction regressions found 2026-07-27.

Live bug: "The Homiens Art Prize ($12,000 Annually)" was served to the artist
with `fee: "$12"`. The real entry fee is $35. Two independent defects combined:

  1. The USD pattern is \\$[\\d]+ — no comma — so "$12,000" matched as "$12".
     The yen pattern already used [\\d,]+, so this was USD/EUR only.
  2. $12,000 is the PRIZE, not an entry fee. build_text_blob() includes the
     title, so an award amount advertised in the title got read as a cost.

Defect 2 is the dangerous one: it invents a fee where the source states none,
and a wrong fee is worse than a missing one — she budgets against it.
"""

import unittest

from engines.fee_text_extractor import extract_fee


class UsdCommaTests(unittest.TestCase):

    def test_usd_amount_with_thousands_separator_is_not_truncated(self):
        fee, matched = extract_fee("Entry fee is $1,200 per submission")
        self.assertTrue(matched)
        self.assertEqual(fee, "$1,200")

    def test_plain_usd_amount_still_works(self):
        fee, matched = extract_fee("Entry fee is $35 per submission")
        self.assertEqual(fee, "$35")

    def test_euro_amount_with_separator_is_not_truncated(self):
        fee, matched = extract_fee("Fee: €1,500 to enter")
        self.assertEqual(fee, "€1,500")


class AmountBoundaryTests(unittest.TestCase):
    """Allowing commas inside amounts must not let sentence punctuation in.
    Regression: "submission via Google Form, ¥500, deadline Aug 31" yielded
    the malformed "¥500," once [\\d,]+ was introduced."""

    def test_trailing_comma_from_the_sentence_is_not_part_of_the_amount(self):
        fee, _ = extract_fee("submission via Google Form, ¥500, deadline Aug 31, 2026")
        self.assertEqual(fee, "¥500")

    def test_thousands_separator_inside_an_amount_is_kept(self):
        fee, _ = extract_fee("Entry fee: ¥13,200 per work")
        self.assertEqual(fee, "¥13,200")

    def test_usd_trailing_comma_is_not_captured(self):
        fee, _ = extract_fee("Entry fee: $35, due at submission")
        self.assertEqual(fee, "$35")


class AdmissionIsNotAFeeTests(unittest.TestCase):
    """Second live case found 2026-07-28, same class as the prize bug: listing
    pages for 公募展 quote the VISITOR admission price, and it was stored as her
    entry fee. 第110回二科美術展覧会 was served as "一般 1,400円" — that is a
    ticket to walk in and look at the show. Real submission fees for these
    society exhibitions run 10,000 yen and up, so the number is not merely
    wrong, it is wrong in the direction that makes her under-budget."""

    def test_general_admission_price_is_not_an_entry_fee(self):
        for text in ("一般 1,400円", "一般 1,500円 / 学生 800円", "大人 700円"):
            fee, matched = extract_fee(text)
            self.assertFalse(matched, f"read admission {fee!r} as an entry fee from: {text}")

    def test_explicit_admission_labels_are_not_entry_fees(self):
        for text in ("入場料 500円", "観覧料 700円", "当日 1,000円 前売 800円"):
            fee, matched = extract_fee(text)
            self.assertFalse(matched, f"read {fee!r} as an entry fee from: {text}")

    def test_english_admission_is_not_an_entry_fee(self):
        fee, matched = extract_fee("Admission: 700 yen (adults)")
        self.assertFalse(matched, f"read {fee!r} as an entry fee")

    def test_a_real_submission_fee_still_survives(self):
        """Must not over-correct — 出品料/参加費 are genuine costs to her."""
        self.assertEqual(extract_fee("出品料 10,000円")[0], "10,000円")
        self.assertEqual(extract_fee("参加費 3,000円")[0], "3,000円")

    def test_real_entry_fee_quoted_alongside_admission(self):
        fee, matched = extract_fee("一般 1,400円（入場）。出品料 12,000円。")
        self.assertTrue(matched)
        self.assertEqual(fee, "12,000円")


class PrizeIsNotAFeeTests(unittest.TestCase):

    def test_prize_amount_in_title_is_not_reported_as_a_fee(self):
        """The exact live failure."""
        fee, matched = extract_fee("The Homiens Art Prize ($12,000 Annually)")
        self.assertFalse(matched, f"invented a fee of {fee!r} from a prize amount")
        self.assertIsNone(fee)

    def test_award_and_grant_amounts_are_not_fees(self):
        for text in (
            "Winner receives a $5,000 award",
            "Grant of ¥500,000 to individual artists",
            "Three winners receive $1,000 cash prizes",
        ):
            fee, matched = extract_fee(text)
            self.assertFalse(matched, f"read {fee!r} as an entry fee from: {text}")

    def test_a_real_fee_alongside_a_prize_is_still_found(self):
        """Must not over-correct into reporting nothing when a fee is stated."""
        fee, matched = extract_fee("$12,000 annual prize. Entry fee: $35 per work.")
        self.assertTrue(matched)
        self.assertEqual(fee, "$35")

    def test_free_to_enter_still_wins(self):
        fee, matched = extract_fee("$10,000 prize. Free to enter.")
        self.assertEqual(fee, "Free")


if __name__ == "__main__":
    unittest.main()
