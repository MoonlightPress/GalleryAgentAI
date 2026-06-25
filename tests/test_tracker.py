import unittest

from api import _followed_opps


class FollowedOppsTests(unittest.TestCase):
    """Join the 'follow' feedback signals to opportunity data so the tracker can
    show name + link, not just an opaque id."""

    OPPS = [
        {"title": "Open Call A", "name": "Gallery A Open Call",
         "official_website": "https://a.test", "deadline": "2026-09-01"},
        {"title": "Open Call B", "name": "Gallery B", "official_website": "https://b.test"},
    ]

    def test_returns_followed_joined_with_opp_data(self):
        fb = [{"opp_id": "Open Call A", "action": "follow"}]
        out = _followed_opps(fb, self.OPPS)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["name"], "Gallery A Open Call")
        self.assertEqual(out[0]["website"], "https://a.test")
        self.assertEqual(out[0]["deadline"], "2026-09-01")

    def test_ignores_non_follow_actions(self):
        fb = [{"opp_id": "Open Call A", "action": "applied"},
              {"opp_id": "Open Call B", "action": "not_for_me"}]
        self.assertEqual(_followed_opps(fb, self.OPPS), [])

    def test_followed_opp_missing_from_dataset_still_shows(self):
        fb = [{"opp_id": "Gone Show", "action": "follow"}]
        out = _followed_opps(fb, self.OPPS)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["name"], "Gone Show")   # falls back to the id
        self.assertEqual(out[0]["website"], "")

    def test_matches_by_name_too(self):
        fb = [{"opp_id": "Gallery B", "action": "follow"}]
        out = _followed_opps(fb, self.OPPS)
        self.assertEqual(out[0]["website"], "https://b.test")


if __name__ == "__main__":
    unittest.main()
