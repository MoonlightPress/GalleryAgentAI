"""
geoip.py

Turn a raw client IP into a short, glanceable location label (flag + city,
country) for the Discord visit feed — so a known visitor can be told apart from
Scott's own connection at a glance, instead of memorising bare IP numbers. Also
exposes a hosting/proxy/datacenter flag for bot detection that doesn't rely on
the User-Agent string, which a scraper can simply not send or fake.

Dependency-light, never raises (a tracking nicety must never crash the request
it decorates), and a safe no-op for private/local/unknown addresses. Successful
lookups are cached per-IP so the outbound HTTP call is paid once per address,
not once per event — geo_label and geo_hosting share the same cached lookup.

Uses the free, keyless ip-api.com endpoint (~45 req/min, plenty for one app).
"""
from __future__ import annotations

import ipaddress

# Confirmed lookups (and deterministic no-ops like private IPs) cached per-IP,
# keyed to the raw parsed response dict so geo_label/geo_hosting can each pull
# out what they need without a second network call.
_CACHE: dict[str, dict] = {}


def _is_public(ip: str) -> bool:
    """True only for a routable public address. Private/loopback/link-local/
    reserved IPs (and anything unparseable) return False — no point geolocating
    a LAN address, and ip-api would just reflect the server's own location."""
    try:
        return ipaddress.ip_address(ip).is_global
    except ValueError:
        return False


def _flag(country_code: str) -> str:
    """Two-letter ISO country code -> regional-indicator flag emoji, or '' if
    the code isn't a clean pair of letters."""
    cc = (country_code or "").upper()
    if len(cc) != 2 or not cc.isalpha():
        return ""
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in cc)


def _lookup(ip, *, fetcher=None, timeout: float = 2.5) -> dict:
    """Shared cached ip-api.com lookup backing geo_label and geo_hosting.
    Returns the parsed response dict, or {} for private/unknown/failed
    lookups. Never raises. ``fetcher`` is injectable for testing; it takes
    ``(url, timeout)`` and returns the parsed JSON dict."""
    if not ip or ip == "?":
        return {}
    if ip in _CACHE:
        return _CACHE[ip]
    if not _is_public(ip):
        _CACHE[ip] = {}  # deterministic — safe to cache the no-op
        return {}

    try:
        if fetcher is None:
            import requests  # local import keeps the module import-cheap

            def fetcher(url, timeout):
                return requests.get(url, timeout=timeout).json()

        url = (f"http://ip-api.com/json/{ip}"
               "?fields=status,country,countryCode,city,proxy,hosting")
        data = fetcher(url, timeout=timeout) or {}
        if data.get("status") == "success":
            _CACHE[ip] = data  # cache only confirmed lookups
            return data
    except Exception:
        pass
    return {}  # transient miss or API-reported failure — not cached, retries next event


def geo_label(ip, *, fetcher=None, timeout: float = 2.5) -> str:
    """Return a short ``"🇹🇼 Taipei, Taiwan"`` label for ``ip``, or ``""`` when
    the location is private, unknown, or can't be fetched."""
    data = _lookup(ip, fetcher=fetcher, timeout=timeout)
    if not data:
        return ""
    flag = _flag(data.get("countryCode", ""))
    city = (data.get("city") or "").strip()
    country = (data.get("country") or "").strip()
    place = ", ".join(p for p in (city, country) if p)
    return f"{flag} {place}".strip() if place else flag


def geo_hosting(ip, *, fetcher=None, timeout: float = 2.5) -> bool:
    """True when ip-api flags the address as a known proxy/VPN or a
    datacenter/hosting IP — a signal a plain-UA bot/scraper can't fake by
    simply omitting or spoofing its User-Agent string. False for private,
    unknown, or failed lookups (never raises)."""
    data = _lookup(ip, fetcher=fetcher, timeout=timeout)
    return bool(data.get("proxy") or data.get("hosting"))
