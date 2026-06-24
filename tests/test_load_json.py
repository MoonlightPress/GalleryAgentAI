import tempfile
import unittest
from pathlib import Path

from api import _load_json


class LoadJsonTests(unittest.TestCase):
    """A hot GET reader must degrade gracefully: a file that exists but is
    malformed (e.g. an interrupted self-write) should return the default, not
    raise a JSONDecodeError that becomes an HTTP 500 on every page load."""

    def test_valid_json_is_returned(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text('{"a": 1}', encoding="utf-8")
            self.assertEqual(_load_json(p, {}), {"a": 1})

    def test_missing_file_returns_default(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(_load_json(Path(d) / "nope.json", []), [])

    def test_corrupt_json_returns_default_without_raising(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "broken.json"
            p.write_text('{"a": 1', encoding="utf-8")  # truncated write
            self.assertEqual(_load_json(p, {"fallback": True}), {"fallback": True})

    def test_empty_file_returns_default(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "empty.json"
            p.write_text("", encoding="utf-8")
            self.assertEqual(_load_json(p, []), [])

    def test_default_defaults_to_none(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(_load_json(Path(d) / "nope.json"))


if __name__ == "__main__":
    unittest.main()
