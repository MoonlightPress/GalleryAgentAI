"""T0.6 + T4.2 — cross-tab count unification and derived-field hygiene.

T0.6: Saffron and Peppercorn must read ONE shared group-show count so the two
tabs can never show her different versions of her own record.

T4.2: the GET-injected derived `live_counts` must never be persisted back into
peppercorn_profile.json on a POST, and the statement is one canonical field whose
stale localized siblings are dropped when the canonical text changes.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fastapi.testclient import TestClient


class ConsistencyTests(unittest.TestCase):
    def setUp(self):
        import api
        import engines.career_strategy_engine as cse
        self.api, self.cse = api, cse

        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        (d / "memory").mkdir()
        (d / "deploy_data").mkdir()
        # Two confirmed group shows + a solo in the profile.
        profile = {
            "career_history": {
                "exhibitions": [
                    {"title": "G1", "type": "group show", "city": "Shanghai, China",
                     "confidence": "confirmed (artist's own exhibition history)"},
                    {"title": "G2", "type": "group show (museum)", "city": "Tianjin, China",
                     "venue": "Mian Art Museum", "confidence": "confirmed"},
                    {"title": "S1", "type": "solo show", "city": "Tokyo, Japan",
                     "confidence": "confirmed"},
                ],
                "publications": [{"title": "Colour Diary"}],
                "gallery_representation": "none confirmed",
                "residencies": "none found",
                "awards": "none found",
            },
            "social_presence": {"instagram": {"followers": "26k", "followers_approx": 26000}},
        }
        (d / "memory" / "artist_master_profile.json").write_text(
            json.dumps(profile), encoding="utf-8")
        (d / "memory" / "exhibition_log.json").write_text("[]", encoding="utf-8")
        (d / "memory" / "peppercorn_profile.json").write_text(
            json.dumps({"artist_statement": "Old statement."}), encoding="utf-8")
        (d / "deploy_data" / "compact_opportunities.json").write_text("[]", encoding="utf-8")

        self._patches = [
            mock.patch.object(api, "DATA_DIR", d / "memory"),
            mock.patch.object(api, "DEPLOY_DIR", d / "deploy_data"),
            mock.patch.object(api, "_OPP_CACHE", None),
            mock.patch.object(cse, "EX_LOG", d / "memory" / "exhibition_log.json"),
            mock.patch.object(cse, "PROFILE", d / "memory" / "artist_master_profile.json"),
            mock.patch.object(cse, "OPP_PATH", d / "deploy_data" / "compact_opportunities.json"),
            mock.patch.object(cse, "OUT_PATH", d / "memory" / "career_strategy_report.json"),
        ]
        for p in self._patches:
            p.start()
        self.client = TestClient(api.app)

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self.tmp.cleanup()

    def test_saffron_and_peppercorn_agree_on_group_count(self):
        saffron_count = self.client.get("/api/saffron").json()["career_benchmarks"]["artist_record"]["exhibitions"]
        pepper_count = self.client.get("/api/peppercorn").json()["live_counts"]["group_shows"]
        self.assertEqual(saffron_count, pepper_count)

    def test_logging_a_show_keeps_both_tabs_in_sync(self):
        before = self.client.get("/api/peppercorn").json()["live_counts"]["group_shows"]
        r = self.client.post("/api/exhibition_log",
                             json={"date": "2026-06-25", "venue": "New", "type": "group"})
        self.assertEqual(r.status_code, 200)
        s = self.client.get("/api/saffron").json()["career_benchmarks"]["artist_record"]["exhibitions"]
        p = self.client.get("/api/peppercorn").json()["live_counts"]["group_shows"]
        self.assertEqual(s, p)
        self.assertEqual(p, before + 1)

    def test_live_counts_not_persisted(self):
        # GET injects live_counts; a POST of the whole doc must not write it back.
        got = self.client.get("/api/peppercorn").json()
        self.assertIn("live_counts", got)
        self.client.post("/api/peppercorn", json=got)
        on_disk = json.loads((Path(self.tmp.name) / "memory" / "peppercorn_profile.json").read_text(encoding="utf-8"))
        self.assertNotIn("live_counts", on_disk)

    def test_changed_statement_drops_stale_localized_siblings(self):
        self.client.post("/api/peppercorn", json={
            "artist_statement": "A brand new statement.",
            "artist_statement_zh": "stale zh", "artist_statement_ja": "stale ja",
        })
        on_disk = json.loads((Path(self.tmp.name) / "memory" / "peppercorn_profile.json").read_text(encoding="utf-8"))
        self.assertIsNone(on_disk.get("artist_statement_zh"))
        self.assertIsNone(on_disk.get("artist_statement_ja"))
        self.assertTrue(on_disk.get("artist_statement_translation_stale"))

    def test_pathway_graduates_past_first_solo(self):
        pw = self.client.get("/api/saffron").json()["pathway"]
        self.assertNotEqual(pw["goal"], "First Solo Show in Tokyo")
        self.assertNotIn("more group shows needed", pw["blocking_now"].lower())


if __name__ == "__main__":
    unittest.main()
