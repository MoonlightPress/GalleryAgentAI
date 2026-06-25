import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fastapi.testclient import TestClient


class CareerStrategyRefreshTests(unittest.TestCase):
    """Adding/removing a show must re-run the (deterministic, free) career
    strategy report so the advice + readiness reflect it immediately. Before
    the fix the report was a frozen file — counts moved, advice didn't."""

    def setUp(self):
        import api
        import engines.career_strategy_engine as cse
        self.api, self.cse = api, cse

        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        (d / "memory").mkdir()
        (d / "deploy_data").mkdir()
        (d / "memory" / "artist_master_profile.json").write_text(
            json.dumps({"career_history": {"exhibitions": []}}), encoding="utf-8")
        (d / "memory" / "exhibition_log.json").write_text("[]", encoding="utf-8")
        (d / "deploy_data" / "compact_opportunities.json").write_text("[]", encoding="utf-8")

        self._patches = [
            mock.patch.object(api, "DATA_DIR", d / "memory"),
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

    def test_adding_group_shows_raises_readiness(self):
        self.cse.build_career_strategy_report()  # initial report
        before = self.client.get("/api/career_strategy").json()
        t3_before = before["readiness_scores"]["tier_3_readiness"]

        # base group-show count is 1; adding two confirmed group shows -> 3,
        # which crosses a readiness threshold.
        for i in range(2):
            r = self.client.post(
                "/api/exhibition_log",
                json={"date": "2026-06-25", "venue": f"Gallery {i}", "type": "group"},
            )
            self.assertEqual(r.status_code, 200)

        after = self.client.get("/api/career_strategy").json()
        t3_after = after["readiness_scores"]["tier_3_readiness"]
        self.assertGreater(t3_after, t3_before)


if __name__ == "__main__":
    unittest.main()
