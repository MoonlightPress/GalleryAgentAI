import unittest

from api import _classify_client


class ClassifyClientTests(unittest.TestCase):
    def test_empty_ua_is_unknown_not_bot(self):
        label, is_bot = _classify_client("")
        self.assertEqual(label, "❓ no user-agent")
        self.assertFalse(is_bot)

    def test_known_bot_substring_is_flagged(self):
        label, is_bot = _classify_client("Mozilla/5.0 (compatible; Discordbot/2.0)")
        self.assertIn("bot", label.lower())
        self.assertTrue(is_bot)

    def test_iphone_safari_is_not_a_bot(self):
        ua = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
              "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/604.1")
        label, is_bot = _classify_client(ua)
        self.assertIn("iPhone", label)
        self.assertIn("Safari", label)
        self.assertFalse(is_bot)

    def test_windows_chrome_is_not_a_bot(self):
        ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
        label, is_bot = _classify_client(ua)
        self.assertIn("Windows", label)
        self.assertIn("Chrome", label)
        self.assertFalse(is_bot)


if __name__ == "__main__":
    unittest.main()
