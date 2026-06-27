"""
geoip.py

Turn a raw client IP into a short, glanceable location label (flag + city,
country) for the Discord visit feed — so a known visitor can be told apart from
Scott's own connection at a glance, instead of memorising bare IP numbers.

Dependency-light, never raises (a tracking nicety must never crash the request
it decorates), and a safe no-op for private/local/unknown addresses. Successful
lookups are cached per-IP so the outbound HTTP call is paid once per address,
not once per event.

Uses the free, keyless ip-api.com endpoint (~45 req/min, plenty for one app).
"""
from __future__ import annotations

import ipaddress

# Confirmed lookups (and deterministic no-ops like private IPs) cached per-IP.
# A transient network miss is intentionally NOT cached, so it retries next event.
_CACHE: dict[str, str] = {}


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


def geo_label(ip, *, fetcher=None, timeout: float = 2.5) -> str:
    """Return a short ``"🇹🇼 Taipei, Taiwan"`` label for ``ip``, or ``""`` when
    the location is private, unknown, or can't be fetched.

    Cached per IP for confirmed lookups. Never raises — any error degrades to an
    empty string so the visit feed still posts. ``fetcher`` is injectable for
    testing; it takes ``(url, timeout)`` and returns the parsed JSON dict.
    """
    if not ip or ip == "?":
        return ""
    if ip in _CACHE:
        return _CACHE[ip]
    if not _is_public(ip):
        _CACHE[ip] = ""  # deterministic — safe to cache the no-op
        return ""

    try:
        if fetcher is None:
            import requests  # local import keeps the module import-cheap

            def fetcher(url, timeout):
                return requests.get(url, timeout=timeout).json()

        url = (f"http://ip-api.com/json/{ip}"
               "?fields=status,country,countryCode,city")
        data = fetcher(url, timeout=timeout) or {}
        if data.get("status") == "success":
            flag = _flag(data.get("countryCode", ""))
            city = (data.get("city") or "").strip()
            country = (data.get("country") or "").strip()
            place = ", ".join(p for p in (city, country) if p)
            label = f"{flag} {place}".strip() if place else flag
            _CACHE[ip] = label  # cache only confirmed lookups
            return label
    except Exception:
        pass
    return ""  # transient miss — not cached, retries on the next event
