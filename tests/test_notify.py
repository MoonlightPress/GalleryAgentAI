import os
import unittest
from unittest import mock

from engines.notify import build_discord_payload, notify_discord


class RecordingPoster:
    """Stand-in for requests.post that records the call instead of doing I/O."""

    def __init__(self, status_code=204):
        self.calls = []
        self._status = status_code

    def __call__(self, url, json=None, timeout=None):
        self.calls.append({"url": url, "json": json, "timeout": timeout})

        class _Resp:
            status_code = self._status

        return _Resp()


class BuildDiscordPayloadTests(unittest.TestCase):
    def test_message_appears_in_payload(self):
        payload = build_discord_payload("monthly pass finished", status="success")
        blob = str(payload)
        self.assertIn("monthly pass finished", blob)

    def test_success_and_failure_have_different_colors(self):
        ok = build_discord_payload("done", status="success")
        bad = build_discord_payload("broke", status="failure")
        ok_color = ok["embeds"][0]["color"]
        bad_color = bad["embeds"][0]["color"]
        self.assertNotEqual(ok_color, bad_color)

    def test_unknown_status_falls_back_to_info(self):
        # Must never KeyError on an unexpected status string.
        payload = build_discord_payload("hmm", status="banana")
        self.assertIn("embeds", payload)


class NotifyDiscordTests(unittest.TestCase):
    def test_no_webhook_is_safe_noop(self):
        poster = RecordingPoster()
        sent = notify_discord("hello", webhook_url="", poster=poster)
        self.assertFalse(sent)
        self.assertEqual(poster.calls, [])

    def test_none_webhook_is_safe_noop(self):
        # With nothing passed AND no env var configured, it must stay a no-op.
        poster = RecordingPoster()
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("MOCHI_DISCORD_WEBHOOK", None)
            sent = notify_discord("hello", webhook_url=None, poster=poster)
        self.assertFalse(sent)
        self.assertEqual(poster.calls, [])

    def test_uses_env_var_when_no_url_passed(self):
        # The live wiring: webhook comes from MOCHI_DISCORD_WEBHOOK in the env.
        poster = RecordingPoster()
        with mock.patch.dict(os.environ, {"MOCHI_DISCORD_WEBHOOK": "https://discord.test/env"}):
            sent = notify_discord("hi", webhook_url=None, poster=poster)
        self.assertTrue(sent)
        self.assertEqual(poster.calls[0]["url"], "https://discord.test/env")

    def test_posts_to_configured_webhook(self):
        poster = RecordingPoster(status_code=204)
        sent = notify_discord(
            "pipeline ok", status="success",
            webhook_url="https://discord.test/webhook", poster=poster,
        )
        self.assertTrue(sent)
        self.assertEqual(len(poster.calls), 1)
        self.assertEqual(poster.calls[0]["url"], "https://discord.test/webhook")
        self.assertIn("pipeline ok", str(poster.calls[0]["json"]))

    def test_non_2xx_response_returns_false(self):
        poster = RecordingPoster(status_code=500)
        sent = notify_discord(
            "oops", webhook_url="https://discord.test/webhook", poster=poster,
        )
        self.assertFalse(sent)

    def test_poster_exception_is_swallowed(self):
        def boom(*a, **k):
            raise RuntimeError("network down")

        # A notifier must never crash the pipeline it is reporting on.
        sent = notify_discord(
            "msg", webhook_url="https://discord.test/webhook", poster=boom,
        )
        self.assertFalse(sent)


if __name__ == "__main__":
    unittest.main()
