"""Rumor Mill search gate — decide WHETHER to spend a search, and in what order.

Problem this solves (2026-07-27): the only gate was a 7-day clock, so every
monthly run re-interrogated the entire needs_research backlog from scratch —
including the 425 items it had already answered and the 149 that have never
once answered. One full run cost 3,042 Tavily credits and exhausted the monthly
quota at item 558/577, so the items at the tail (which included the newest
discoveries) never got searched at all.

Two behaviours fix that:
  * should_search() — skip items whose facts we already have; back off items
    that repeatedly yield nothing; keep asking about ones that might change.
  * search_priority() — put never-searched items FIRST, so a run that dies on
    quota dies having spent its budget on new opportunities rather than on
    re-grinding old ones.
"""

import unittest
from datetime import datetime, timedelta

from engines.rumor_mill_engine import should_search, search_priority

TODAY = datetime(2026, 8, 3, 10, 0, 0)


def ago(days):
    return (TODAY - timedelta(days=days)).isoformat()


class ShouldSearchTests(unittest.TestCase):

    def test_never_searched_item_is_always_searched(self):
        ok, why = should_search({"title": "New Call"}, None, TODAY)
        self.assertTrue(ok, why)

    def test_item_with_complete_future_facts_is_not_re_searched(self):
        """The core saving: we already know the deadline and how to apply.
        Asking again buys nothing."""
        item = {"title": "X", "deadline": "2026-12-01",
                "submission_url": "https://example.org/apply"}
        entry = {"searched_at": ago(400), "data_found": True}
        ok, why = should_search(item, entry, TODAY)
        self.assertFalse(ok)
        self.assertIn("already", why)

    def test_item_with_passed_deadline_is_searched_again(self):
        """A closed call may have reopened — this is what "updated over time" means."""
        item = {"title": "X", "deadline": "2026-01-01",
                "submission_url": "https://example.org/apply"}
        entry = {"searched_at": ago(400), "data_found": True}
        ok, why = should_search(item, entry, TODAY)
        self.assertTrue(ok, why)

    def test_item_missing_submission_url_is_still_searched(self):
        item = {"title": "X", "deadline": "2026-12-01"}
        entry = {"searched_at": ago(60), "data_found": True}
        ok, why = should_search(item, entry, TODAY)
        self.assertTrue(ok, why)

    def test_recently_searched_item_is_skipped(self):
        item = {"title": "X"}
        entry = {"searched_at": ago(2), "data_found": False, "attempts": 1}
        ok, why = should_search(item, entry, TODAY)
        self.assertFalse(ok)

    def test_repeatedly_barren_item_backs_off(self):
        """Three strikes and it stops being asked every cycle."""
        item = {"title": "X"}
        entry = {"searched_at": ago(35), "data_found": False, "attempts": 3}
        ok, why = should_search(item, entry, TODAY)
        self.assertFalse(ok)
        self.assertIn("barren", why)

    def test_barren_item_is_retried_after_a_long_enough_gap(self):
        """Back off, don't give up forever — sites do eventually publish."""
        item = {"title": "X"}
        entry = {"searched_at": ago(200), "data_found": False, "attempts": 3}
        ok, why = should_search(item, entry, TODAY)
        self.assertTrue(ok, why)

    def test_backoff_grows_with_attempts(self):
        item = {"title": "X"}
        nine_attempts = {"searched_at": ago(100), "data_found": False, "attempts": 9}
        three_attempts = {"searched_at": ago(100), "data_found": False, "attempts": 3}
        self.assertTrue(should_search(item, three_attempts, TODAY)[0])
        self.assertFalse(should_search(item, nine_attempts, TODAY)[0])


class SearchPriorityTests(unittest.TestCase):

    def test_never_searched_sorts_before_previously_searched(self):
        never = search_priority({"title": "A"}, None)
        seen = search_priority({"title": "B"}, {"searched_at": ago(90), "attempts": 1})
        self.assertLess(never, seen)

    def test_queue_puts_new_items_first(self):
        """A quota death must not consume the budget on old items."""
        items = [{"title": "old"}, {"title": "new"}]
        log = {"old": {"searched_at": ago(90), "attempts": 2}}
        ordered = sorted(items, key=lambda i: search_priority(i, log.get(i["title"])))
        self.assertEqual([i["title"] for i in ordered], ["new", "old"])

    def test_fewer_past_attempts_sorts_earlier_among_seen_items(self):
        one = search_priority({"title": "A"}, {"searched_at": ago(90), "attempts": 1})
        five = search_priority({"title": "B"}, {"searched_at": ago(90), "attempts": 5})
        self.assertLess(one, five)


if __name__ == "__main__":
    unittest.main()
