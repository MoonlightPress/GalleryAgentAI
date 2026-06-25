"""Tests for the free-discovery scraper engine. All offline — the only piece
that touches the network (fetch_source) is mocked."""
import unittest
from unittest import mock

from engines import free_discovery_engine as fd


JP_SOURCE = {"name": "Test JP", "region": "JP", "lang": "ja", "locality": "global",
             "url": "https://example.jp/calls/"}

FIXTURE_HTML = """
<html><body>
  <nav><a href="/">ホーム</a><a href="/about">About</a></nav>
  <ul>
    <li><a href="/calls/123">第113回 日本水彩展 作品募集</a></li>
    <li><a href="https://other.jp/comp">2026 International Watercolor Competition</a></li>
    <li><a href="/news/weather">今日の天気</a></li>
    <li><a href="/calls/123#section">第113回 日本水彩展 作品募集</a></li>
  </ul>
</body></html>
"""


class ExtractTests(unittest.TestCase):
    def test_extracts_only_opportunity_links(self):
        cands = fd.extract_candidates(FIXTURE_HTML, JP_SOURCE)
        names = [c["name"] for c in cands]
        self.assertIn("第113回 日本水彩展 作品募集", names)
        self.assertIn("2026 International Watercolor Competition", names)
        self.assertNotIn("今日の天気", names)          # no keyword
        self.assertNotIn("About", names)               # nav noise

    def test_resolves_relative_urls_and_dedupes_fragments(self):
        cands = fd.extract_candidates(FIXTURE_HTML, JP_SOURCE)
        urls = [c["url"] for c in cands]
        self.assertIn("https://example.jp/calls/123", urls)
        # the #section duplicate collapses to the same candidate
        self.assertEqual(sum(u == "https://example.jp/calls/123" for u in urls), 1)

    def test_carries_source_provenance(self):
        c = fd.extract_candidates(FIXTURE_HTML, JP_SOURCE)[0]
        self.assertEqual(c["region"], "JP")
        self.assertEqual(c["locality"], "global")
        self.assertEqual(c["source_name"], "Test JP")

    def test_empty_html_is_safe(self):
        self.assertEqual(fd.extract_candidates("", JP_SOURCE), [])


class KeywordTests(unittest.TestCase):
    def test_lang_specific_and_english_always(self):
        self.assertTrue(fd._matches_keyword("作品募集", "ja"))
        self.assertTrue(fd._matches_keyword("作品征集", "zh"))
        self.assertTrue(fd._matches_keyword("Open Call for Artists", "ja"))  # EN always
        self.assertFalse(fd._matches_keyword("今日の天気", "ja"))


class RecordTests(unittest.TestCase):
    def test_compact_record_is_quarantined(self):
        rec = fd.to_compact_record({"name": "X", "url": "https://x.jp/c", "region": "JP"})
        self.assertEqual(rec["exclusive_primary_bucket"], "research_needed")
        self.assertEqual(rec["verification_status"], "unverified")
        self.assertEqual(rec["recommendation_visibility"], "hidden")
        self.assertEqual(rec["overall_score"], 0)
        self.assertEqual(rec["discovery_source"], "free_scraper")


class DedupeTests(unittest.TestCase):
    def test_drops_existing_by_name(self):
        recs = [fd.to_compact_record({"name": "日本水彩展", "url": "https://a.jp/1"})]
        existing = [{"name": "日本水彩展 (Japan Watercolour)", "official_website": "https://z.jp"}]
        # _norm_name strips the parenthetical/spaces so the cores collide
        self.assertEqual(len(fd.dedupe(recs, existing)), 1)  # different core -> kept
        recs2 = [fd.to_compact_record({"name": "日本水彩展", "url": "https://a.jp/1"})]
        existing2 = [{"name": "日本水彩展", "official_website": "https://z.jp"}]
        self.assertEqual(fd.dedupe(recs2, existing2), [])

    def test_drops_existing_by_url(self):
        recs = [fd.to_compact_record({"name": "New Call", "url": "https://a.jp/calls/1"})]
        existing = [{"name": "Totally Different", "source_url": "https://a.jp/calls/1/"}]
        self.assertEqual(fd.dedupe(recs, existing), [])

    def test_survives_messy_existing_fields(self):
        # Live data is messy: a url field can be a list or None. Must not crash.
        recs = [fd.to_compact_record({"name": "Brand New", "url": "https://a.jp/new"})]
        existing = [
            {"name": ["weird", "list"], "source_url": ["https://x.jp/a", "https://x.jp/b"]},
            {"name": None, "official_website": None},
        ]
        self.assertEqual(len(fd.dedupe(recs, existing)), 1)

    def test_drops_internal_duplicates(self):
        recs = [
            fd.to_compact_record({"name": "Call", "url": "https://a.jp/1"}),
            fd.to_compact_record({"name": "Call", "url": "https://a.jp/1"}),
        ]
        self.assertEqual(len(fd.dedupe(recs, [])), 1)


class RunTests(unittest.TestCase):
    def test_run_offline_with_mocked_fetch(self):
        with mock.patch.object(fd, "fetch_source", return_value=FIXTURE_HTML), \
             mock.patch.object(fd, "_load_json", return_value=[]):
            summary = fd.run([JP_SOURCE], write=False)
        self.assertEqual(summary["sources_total"], 1)
        self.assertEqual(summary["sources_reached"], 1)
        self.assertGreaterEqual(summary["candidates_new"], 2)

    def test_run_survives_unreachable_source(self):
        with mock.patch.object(fd, "fetch_source", return_value=None), \
             mock.patch.object(fd, "_load_json", return_value=[]):
            summary = fd.run([JP_SOURCE], write=False)
        self.assertEqual(summary["sources_reached"], 0)
        self.assertEqual(summary["candidates_new"], 0)


if __name__ == "__main__":
    unittest.main()
