import unittest

from engines import geoip
from engines.geoip import geo_label, geo_hosting, _flag, _is_public


class RecordingFetcher:
    """Stand-in for the HTTP lookup that records calls instead of doing I/O."""

    def __init__(self, data=None, boom=False):
        self.calls = []
        self._data = data or {}
        self._boom = boom

    def __call__(self, url, timeout=None):
        self.calls.append({"url": url, "timeout": timeout})
        if self._boom:
            raise RuntimeError("network down")
        return self._data


class FlagTests(unittest.TestCase):
    def test_two_letter_code_becomes_flag(self):
        self.assertEqual(_flag("TW"), "🇹🇼")

    def test_lowercase_is_handled(self):
        self.assertEqual(_flag("jp"), "🇯🇵")

    def test_bad_code_is_empty(self):
        self.assertEqual(_flag(""), "")
        self.assertEqual(_flag("USA"), "")
        self.assertEqual(_flag("1"), "")


class IsPublicTests(unittest.TestCase):
    def test_private_and_loopback_are_not_public(self):
        for ip in ("127.0.0.1", "192.168.1.5", "10.0.0.3", "::1"):
            self.assertFalse(_is_public(ip), ip)

    def test_garbage_is_not_public(self):
        self.assertFalse(_is_public("?"))
        self.assertFalse(_is_public("not-an-ip"))

    def test_public_ip_is_public(self):
        self.assertTrue(_is_public("8.8.8.8"))


class GeoLabelTests(unittest.TestCase):
    def setUp(self):
        geoip._CACHE.clear()

    def test_unknown_and_private_are_empty_noops(self):
        f = RecordingFetcher(boom=True)
        self.assertEqual(geo_label("", fetcher=f), "")
        self.assertEqual(geo_label("?", fetcher=f), "")
        self.assertEqual(geo_label("192.168.0.1", fetcher=f), "")
        self.assertEqual(f.calls, [])  # never reaches the network

    def test_successful_lookup_formats_flag_city_country(self):
        f = RecordingFetcher({"status": "success", "countryCode": "TW",
                              "city": "Taipei", "country": "Taiwan"})
        self.assertEqual(geo_label("8.8.8.8", fetcher=f), "🇹🇼 Taipei, Taiwan")

    def test_missing_city_still_gives_flag_and_country(self):
        f = RecordingFetcher({"status": "success", "countryCode": "JP",
                              "city": "", "country": "Japan"})
        self.assertEqual(geo_label("1.1.1.1", fetcher=f), "🇯🇵 Japan")

    def test_confirmed_lookup_is_cached(self):
        f = RecordingFetcher({"status": "success", "countryCode": "US",
                              "city": "Seattle", "country": "United States"})
        first = geo_label("9.9.9.9", fetcher=f)
        second = geo_label("9.9.9.9", fetcher=f)
        self.assertEqual(first, second)
        self.assertEqual(len(f.calls), 1)  # second call served from cache

    def test_network_failure_is_empty_and_not_cached(self):
        boom = RecordingFetcher(boom=True)
        self.assertEqual(geo_label("4.4.4.4", fetcher=boom), "")
        # A later good fetch for the same IP must still be attempted (not cached).
        good = RecordingFetcher({"status": "success", "countryCode": "FR",
                                 "city": "Paris", "country": "France"})
        self.assertEqual(geo_label("4.4.4.4", fetcher=good), "🇫🇷 Paris, France")

    def test_api_failure_status_is_empty(self):
        f = RecordingFetcher({"status": "fail", "message": "reserved range"})
        self.assertEqual(geo_label("208.67.222.222", fetcher=f), "")


class GeoHostingTests(unittest.TestCase):
    def setUp(self):
        geoip._CACHE.clear()

    def test_private_ip_is_not_hosting(self):
        f = RecordingFetcher(boom=True)
        self.assertFalse(geo_hosting("192.168.0.1", fetcher=f))
        self.assertEqual(f.calls, [])

    def test_flagged_proxy_is_hosting(self):
        f = RecordingFetcher({"status": "success", "countryCode": "US",
                              "city": "Ashburn", "country": "United States",
                              "proxy": True, "hosting": False})
        self.assertTrue(geo_hosting("3.3.3.3", fetcher=f))

    def test_flagged_hosting_is_hosting(self):
        f = RecordingFetcher({"status": "success", "countryCode": "DE",
                              "city": "Frankfurt", "country": "Germany",
                              "proxy": False, "hosting": True})
        self.assertTrue(geo_hosting("5.5.5.5", fetcher=f))

    def test_plain_residential_ip_is_not_hosting(self):
        f = RecordingFetcher({"status": "success", "countryCode": "JP",
                              "city": "Tokyo", "country": "Japan",
                              "proxy": False, "hosting": False})
        self.assertFalse(geo_hosting("6.6.6.6", fetcher=f))

    def test_network_failure_is_not_hosting(self):
        self.assertFalse(geo_hosting("7.7.7.7", fetcher=RecordingFetcher(boom=True)))

    def test_label_and_hosting_share_one_network_call(self):
        f = RecordingFetcher({"status": "success", "countryCode": "TW",
                              "city": "Taipei", "country": "Taiwan",
                              "proxy": False, "hosting": False})
        geo_label("8.8.4.4", fetcher=f)
        geo_hosting("8.8.4.4", fetcher=f)
        self.assertEqual(len(f.calls), 1)  # second lookup served from the shared cache


if __name__ == "__main__":
    unittest.main()
