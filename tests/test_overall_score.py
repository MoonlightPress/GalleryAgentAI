import unittest

from api import _overall_score


class OverallScoreTests(unittest.TestCase):
    """Regression for the score-shadowing bug (audit 2026-07-06):
    truth_aligned_score used to WIN the priority order outright, so a stale
    truth-checker value silently replaced a fresher overall_score in 635/653
    live entries (only 69 were intentional caps). New semantics: the fresh
    score chain is the base; truth_aligned_score only ever LOWERS it (a cap),
    never raises it."""

    def test_truth_aligned_caps_a_higher_fresh_score(self):
        # Intentional cap: truth checker knocked an inflated 10.0 down.
        opp = {"overall_score": 10.0, "truth_aligned_score": 6.4}
        self.assertEqual(_overall_score(opp), 6.4)

    def test_stale_truth_aligned_never_inflates(self):
        # Staleness: overall_score was re-computed lower after the truth
        # checker ran; the old higher truth_aligned must NOT win.
        opp = {"overall_score": 7.2, "truth_aligned_score": 8.9}
        self.assertEqual(_overall_score(opp), 7.2)

    def test_no_truth_aligned_uses_fresh_chain(self):
        self.assertEqual(_overall_score({"overall_score": 5.5}), 5.5)

    def test_fresh_chain_priority_without_overall(self):
        opp = {"differentiated_score": 6.0, "dna_adjusted_score": 9.0}
        self.assertEqual(_overall_score(opp), 6.0)

    def test_truth_aligned_caps_fallback_chain_too(self):
        opp = {"differentiated_score": 8.0, "truth_aligned_score": 2.5}
        self.assertEqual(_overall_score(opp), 2.5)

    def test_truth_aligned_alone_still_counts(self):
        # Only the truth field exists (old-era entry): use it rather than 0.
        self.assertEqual(_overall_score({"truth_aligned_score": 4.2}), 4.2)

    def test_empty_is_zero(self):
        self.assertEqual(_overall_score({}), 0.0)


if __name__ == "__main__":
    unittest.main()
