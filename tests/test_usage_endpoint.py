import json
import unittest
from pathlib import Path
import tempfile

import api


class AppendUsageEventTests(unittest.TestCase):
    def test_appends_one_json_line_with_ts(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "usage_events.jsonl"
            api._append_usage_event({"type": "nav", "page": "observe"}, path=path)
            api._append_usage_event({"type": "action", "action": "follow"}, path=path)
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 2)
            rec = json.loads(lines[0])
            self.assertEqual(rec["type"], "nav")
            self.assertIn("ts", rec)          # server-stamped

    def test_bad_path_does_not_raise(self):
        # A failed append must never propagate (tracking is best-effort).
        api._append_usage_event({"type": "nav"}, path=Path("/nonexistent-dir/x/y.jsonl"))

    def test_read_round_trips(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "usage_events.jsonl"
            api._append_usage_event({"type": "open", "page": "discover"}, path=path)
            api._append_usage_event({"type": "nav", "page": "observe"}, path=path)
            events = api._read_usage_events(path=path)
            self.assertEqual([e["type"] for e in events], ["open", "nav"])

    def test_read_missing_file_is_empty(self):
        self.assertEqual(api._read_usage_events(path=Path("/no/such/file.jsonl")), [])


if __name__ == "__main__":
    unittest.main()
