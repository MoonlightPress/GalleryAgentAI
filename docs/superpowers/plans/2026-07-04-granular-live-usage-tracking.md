# Granular Live Usage Tracking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing live Discord usage-tracking pipeline with a real `leave`/dwell event, persisted bot/hosting classification, and a handful of new curated click actions, so "what she clicks, how long, and is it really her" is visible without adding a dashboard or any identity infrastructure.

**Architecture:** Backend (`api.py`, `engines/geoip.py`, `engines/visit_tracking.py`) already logs every event to `usage_events.jsonl` and posts `open`/`nav`/`action` live to Discord. This plan adds a fourth event type (`leave`, fired by the frontend on tab-hide/close with a client-measured `dwell_ms`), persists the existing bot/device classification onto the log record instead of discarding it, adds a hosting/proxy signal from the geo lookup, and wires ~7 new `track()` call sites across 4 React components that aren't tracked today.

**Tech Stack:** FastAPI (`api.py`), plain-function "engines" modules (`engines/*.py`), Python `unittest`/`pytest`, React (`frontend/src`), Node's built-in test runner (`node --test`).

## Global Constraints

- Never log or Discord-post a specific opportunity name — category/type only (existing posture, unchanged).
- Every tracking call is best-effort: swallow errors, never block the UI or fail `/api/event` (existing posture, unchanged).
- `IDLE_MINUTES = 10`, `TICK_SECONDS = 60` (existing constants in `api.py:55-56`) are unchanged by this work.
- No dashboard, no cross-session geo-change auto-flagging, no login/identity system — out of scope per `docs/superpowers/specs/2026-07-04-granular-live-usage-tracking-design.md`.

---

## Task 1: Persist bot/device classification onto every logged event

**Files:**
- Modify: `api.py:3417-3436` (`_classify_client`), `api.py:3461-3468` (`track_event`, IP/UA/append block)
- Test: Create `tests/test_classify_client.py`

**Interfaces:**
- Produces: `_classify_client(ua: str) -> tuple[str, bool]` — `(display_label, is_bot)`. Task 3's `track_event` edits build on the same call site, so the return-type change must land first.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_classify_client.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_classify_client.py -v`
Expected: FAIL — `_classify_client` currently returns a plain `str`, so unpacking into `(label, is_bot)` raises (`ValueError: too many values to unpack` or similar).

- [ ] **Step 3: Change `_classify_client` to return `(label, is_bot)`**

Replace `api.py:3417-3436`:

```python
def _classify_client(ua: str) -> tuple[str, bool]:
    """Compact who-is-this from the User-Agent: a bot flag (so a link-preview /
    crawler is obvious at a glance) or a rough device + browser for a real visitor.
    Returns (display_label, is_bot) — the label is for the Discord suffix, the
    bool is what gets persisted onto the logged event record."""
    u = (ua or "").lower()
    if not u:
        return "❓ no user-agent", False
    for b in ("bot", "crawl", "spider", "facebookexternalhit", "discordbot",
              "slackbot", "telegrambot", "whatsapp", "embedly", "preview",
              "headless", "python-requests", "curl", "wget", "go-http", "httpx",
              "node-fetch", "axios", "lighthouse", "bingpreview"):
        if b in u:
            return f"🤖 bot ({b})", True
    dev = ("📱 iPhone" if "iphone" in u else "📱 iPad" if "ipad" in u
           else "📱 Android" if "android" in u else "💻 Mac" if ("macintosh" in u or "mac os" in u)
           else "💻 Windows" if "windows" in u else "🖥 other")
    br = ("Chrome" if ("crios" in u or ("chrome" in u and "edg" not in u and "opr" not in u))
          else "Firefox" if ("fxios" in u or "firefox" in u) else "Edge" if "edg" in u
          else "Safari" if "safari" in u else "?")
    return f"{dev} · {br}", False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_classify_client.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Update the call site and persist the classification**

Replace `api.py:3461-3468`:

```python
    ip = _client_ip(request)
    ua = request.headers.get("user-agent", "")
    geo = geo_label(ip)
    device_label, is_bot = _classify_client(ua)
    geo_part = f" · {geo}" if geo else ""
    suffix = f"\n`{ip}`{geo_part} · {device_label}"

    # Durable record for the idle digest — every event, now carrying attribution
    # AND the classification itself (previously computed only for the Discord
    # text and thrown away).
    _append_usage_event({**(event or {}), "ip": ip, "ua": ua,
                          "device": device_label, "is_bot": is_bot})
```

- [ ] **Step 6: Run the full existing usage-event test file to confirm no regression**

Run: `python -m pytest tests/test_usage_endpoint.py tests/test_visit_tracking.py -v`
Expected: PASS (all existing tests unaffected — this task didn't touch `_append_usage_event`'s signature, only what's passed into it)

- [ ] **Step 7: Commit**

```bash
git add api.py tests/test_classify_client.py
git commit -m "$(cat <<'EOF'
webhooks: persist bot/device classification onto logged events

_classify_client was computed only for the Discord message text and
discarded. Now returns (label, is_bot) so both are usable — the label
still decorates the live ping, and is_bot lands on the durable record
for later querying.
EOF
)"
```

---

## Task 2: Add hosting/proxy detection to geoip.py and wire it into the event log

**Files:**
- Modify: `engines/geoip.py` (whole file — refactors the cache to hold the raw lookup dict instead of just the label string)
- Modify: `api.py:20` (import), `api.py:3461-3470` (append call, building on Task 1's edit)
- Test: Modify `tests/test_geoip.py` (add new test class; existing tests must keep passing unchanged)

**Interfaces:**
- Consumes: nothing new from Task 1 besides the same edit location in `api.py`.
- Produces: `geo_hosting(ip, *, fetcher=None, timeout=2.5) -> bool`, alongside the existing `geo_label(ip, ...) -> str` (signature unchanged).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_geoip.py` (after the existing `GeoLabelTests` class, before `if __name__ == "__main__":`):

```python
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
```

Add `geo_hosting` to the existing import line (`tests/test_geoip.py:4`):

```python
from engines.geoip import geo_label, geo_hosting, _flag, _is_public
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_geoip.py -v`
Expected: FAIL — `ImportError: cannot import name 'geo_hosting'`

- [ ] **Step 3: Refactor geoip.py to share one cached lookup between `geo_label` and the new `geo_hosting`**

Replace the whole file `engines/geoip.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_geoip.py -v`
Expected: PASS — all original `GeoLabelTests`/`FlagTests`/`IsPublicTests` cases plus the new `GeoHostingTests` (18 total).

- [ ] **Step 5: Wire `geo_hosting` into the persisted event record**

Update the import at `api.py:20`:

```python
from engines.geoip import geo_label, geo_hosting
```

Replace the block from Task 1 Step 5 (`api.py:3461-3470`) with:

```python
    ip = _client_ip(request)
    ua = request.headers.get("user-agent", "")
    geo = geo_label(ip)
    hosting = geo_hosting(ip)
    device_label, is_bot = _classify_client(ua)
    geo_part = f" · {geo}" if geo else ""
    suffix = f"\n`{ip}`{geo_part} · {device_label}"

    # Durable record for the idle digest — every event, now carrying attribution,
    # the UA-based classification, AND a hosting/proxy signal that catches bots
    # which don't self-identify via User-Agent at all.
    _append_usage_event({**(event or {}), "ip": ip, "ua": ua,
                          "device": device_label, "is_bot": is_bot,
                          "likely_bot_hosting": hosting})
```

- [ ] **Step 6: Run the full backend usage/geoip test suite**

Run: `python -m pytest tests/test_geoip.py tests/test_classify_client.py tests/test_usage_endpoint.py tests/test_visit_tracking.py -v`
Expected: PASS (all)

- [ ] **Step 7: Commit**

```bash
git add engines/geoip.py api.py tests/test_geoip.py
git commit -m "$(cat <<'EOF'
geoip: add hosting/proxy signal, persist onto logged events

geo_label and the new geo_hosting() now share one cached ip-api lookup
(adds proxy/hosting to the requested fields) instead of a second network
call. likely_bot_hosting lands on every logged usage event so a bot/
scraper running from a datacenter IP is catchable even with a plain,
non-self-identifying User-Agent.
EOF
)"
```

---

## Task 3: Add the `leave` event type — backend (dwell formatting + live post)

**Files:**
- Modify: `engines/visit_tracking.py:41-79` (`describe_event`)
- Modify: `api.py:3486-3496` (`track_event`, add a new `elif` branch)
- Test: Modify `tests/test_visit_tracking.py`

**Interfaces:**
- Consumes: none from Tasks 1-2 (independent section of the same files).
- Produces: `describe_event({"type": "leave", "page": ..., "section": ..., "dwell_ms": ...})` → `(text, status)`, consumed by `track_event`'s new branch. Frontend contract (Task 4): `{ "type": "leave", "page": "discover", "section": "landscape"?, "dwell_ms": 47000 }`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_visit_tracking.py`, inside `DescribeEventTests` (after `test_unknown_type_does_not_crash`):

```python
    def test_leave_event_shows_page_and_dwell_seconds(self):
        text, status = describe_event({"type": "leave", "page": "discover", "dwell_ms": 47000})
        self.assertIn("Home", text)
        self.assertIn("47s", text)
        self.assertEqual(status, "info")

    def test_leave_event_with_section_shows_both(self):
        text, _ = describe_event({"type": "leave", "page": "observe", "section": "landscape", "dwell_ms": 5000})
        self.assertIn("Saffron", text)
        self.assertIn("Landscape", text)
        self.assertIn("5s", text)

    def test_leave_event_over_a_minute_shows_minutes_and_seconds(self):
        text, _ = describe_event({"type": "leave", "page": "refine", "dwell_ms": 192000})
        self.assertIn("3m 12s", text)

    def test_leave_event_exact_minute_omits_zero_seconds(self):
        text, _ = describe_event({"type": "leave", "page": "refine", "dwell_ms": 120000})
        self.assertIn("2m", text)
        self.assertNotIn("2m 0s", text)

    def test_leave_event_missing_dwell_does_not_crash(self):
        text, status = describe_event({"type": "leave", "page": "discover"})
        self.assertIsInstance(text, str)
        self.assertTrue(text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_visit_tracking.py -v -k leave`
Expected: FAIL — `describe_event` has no `"leave"` branch, so it falls through to the generic `"👀 activity"` string and the assertions on page/dwell content fail.

- [ ] **Step 3: Add a dwell formatter and the `leave` branch**

Replace `engines/visit_tracking.py:41-79` (`describe_event` and everything above the `_as_int` helper stays; insert the new formatter just before `describe_event` and a new branch inside it):

```python
def _format_dwell(ms) -> str:
    """47000 -> '47s', 192000 -> '3m 12s', 120000 -> '2m'. Never raises —
    a malformed/missing dwell degrades to a generic word rather than crashing
    the live ping."""
    try:
        seconds = max(0, int(ms) // 1000)
    except (TypeError, ValueError):
        return "a moment"
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    return f"{minutes}m {secs}s" if secs else f"{minutes}m"


def describe_event(event: dict, day: int | None = None,
                   returning: bool | None = None) -> tuple[str, str]:
    """Turn a navigation event into ``(message, status)`` for the Discord feed.

    Event types: ``open`` (session start), ``nav`` (page change), ``action``
    (a meaningful action like a profile edit), ``leave`` (she hid/closed the
    tab — reports real, client-measured dwell time on the page she was on).
    Unknown shapes degrade to a safe generic string rather than raising.

    ``returning`` (when known) makes the open message say whether this is a
    repeat visitor or a new one — so a scattered one-off hit is distinguishable
    from someone actually coming back. ``None`` keeps the old generic wording.
    """
    event = event or {}
    etype = event.get("type")

    if etype == "open":
        who = ("A returning visitor" if returning is True
               else "A new visitor" if returning is False
               else "GEGYjiji")
        label = _page_label(event.get("page"))
        day_part = f" · day {day}" if day else ""
        vid = str(event.get("visitor_id") or "")[:6]
        vid_part = f" · id {vid}" if vid else ""
        return f"📊 {who} opened Mochi{day_part} · on {label}{vid_part}", "info"

    if etype == "nav":
        section = event.get("section")
        if section:
            return f"↳ {_section_label(section)}", "info"
        to = _page_label(event.get("page"))
        frm = event.get("from")
        if frm:
            return f"{_page_label(frm)} → {to}", "info"
        return f"→ {to}", "info"

    if etype == "action":
        return f"✏️ {event.get('action', 'did something')}", "info"

    if etype == "leave":
        label = _page_label(event.get("page"))
        section = event.get("section")
        where = f"{label} · {_section_label(section)}" if section else label
        return f"↩ left {where} · {_format_dwell(event.get('dwell_ms'))}", "info"

    return "👀 activity", "info"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_visit_tracking.py -v`
Expected: PASS (all, including the 5 new `leave` cases)

- [ ] **Step 5: Add the `leave` branch to `track_event`**

In `api.py`, the `elif etype == "action":` block (around line 3491-3496) is followed by `return {"ok": True}`. Insert a new branch between them:

```python
    elif etype == "leave":
        # Real, client-measured dwell time — including the final page before
        # she closes the tab, which the idle-gap inference can't see at all.
        text, status = describe_event(event)
        notify_discord(text + suffix, status=status)

    return {"ok": True}
```

- [ ] **Step 6: Run the backend test suite once more**

Run: `python -m pytest tests/test_visit_tracking.py tests/test_usage_endpoint.py tests/test_geoip.py tests/test_classify_client.py -v`
Expected: PASS (all)

- [ ] **Step 7: Commit**

```bash
git add engines/visit_tracking.py api.py tests/test_visit_tracking.py
git commit -m "$(cat <<'EOF'
webhooks: add leave event — real client-measured dwell time

New etype 'leave' posts live (mirroring nav/action) with a formatted
dwell string ('left Home · 47s'). Closes the biggest blind spot in the
existing digest: the final page she was on before closing the tab had
no measurable end-time before this.
EOF
)"
```

---

## Task 4: Emit the `leave` event — frontend (`App.jsx`)

**Files:**
- Modify: `frontend/src/App.jsx:94-107` (the existing nav-beacon effect)

**Interfaces:**
- Consumes: `track(event)` from `frontend/src/utils/track.js` (unchanged signature); backend contract from Task 3 (`{type:'leave', page, section?, dwell_ms}`).
- Produces: nothing consumed by later tasks — this is a leaf.

- [ ] **Step 1: Add dwell tracking and the visibility/pagehide listeners**

Replace `frontend/src/App.jsx:94-107`:

```jsx
export default function App() {
  const [page, setPage] = useState('discover')
  const [view, setView] = useState('cards')

  // UX-research beacon: report the opening page and each page change so they
  // show up live in Discord. Best-effort; never blocks or breaks the UI.
  const prevPage = useRef(null)
  useEffect(() => {
    const from = prevPage.current
    prevPage.current = page
    // Open = first mount; subsequent changes = companion-page navigation. The
    // anonymous visitor_id is attached inside track(). Best-effort; never blocks.
    track(from === null ? { type: 'open', page } : { type: 'nav', page, from })
  }, [page])

  // Real, client-measured dwell time on the current companion page — the
  // server can only ever infer dwell from gaps between events, and has no
  // way to know how long she was on the LAST page before closing the tab.
  // A leave beacon fires on tab-hide (covers alt-tab and actual close on
  // every modern browser) and again on pagehide as a fallback; a guard
  // avoids double-posting the same dwell window when both fire back to back.
  const pageEnteredAt = useRef(Date.now())
  const leaveSentRef = useRef(false)
  useEffect(() => {
    pageEnteredAt.current = Date.now()
    leaveSentRef.current = false
  }, [page])
  useEffect(() => {
    function sendLeave() {
      if (leaveSentRef.current) return
      leaveSentRef.current = true
      track({ type: 'leave', page, dwell_ms: Date.now() - pageEnteredAt.current })
    }
    function onVisibilityChange() {
      if (document.visibilityState === 'hidden') {
        sendLeave()
      } else if (document.visibilityState === 'visible') {
        // Coming back to the tab starts a fresh dwell window on the same page.
        pageEnteredAt.current = Date.now()
        leaveSentRef.current = false
      }
    }
    document.addEventListener('visibilitychange', onVisibilityChange)
    window.addEventListener('pagehide', sendLeave)
    return () => {
      document.removeEventListener('visibilitychange', onVisibilityChange)
      window.removeEventListener('pagehide', sendLeave)
    }
  }, [page])
```

(The rest of the `App` function — the warm-cache effect, `nav`, and the JSX return — is unchanged; only the two effects above are new, inserted right after the existing nav-beacon effect.)

- [ ] **Step 2: Manually verify in the running dev server**

There's no jsdom/component test harness in this repo (`frontend/src/**/*.test.js` only covers plain utility functions, per `frontend/package.json:10`), so this browser-event wiring is verified by hand, same as the existing `TrackedSection.jsx` IntersectionObserver logic was:

1. Run `start_mochi.bat` (or `npm run dev` in `frontend/` with `python api.py` running).
2. Open http://localhost:5177, open DevTools → Network, filter on `event`.
3. Switch to another browser tab for a couple of seconds, then back.
4. Confirm a `POST /api/event` fired with `{"type":"leave","page":"discover","dwell_ms": <plausible ms>}`, and that returning to the tab doesn't immediately fire a second one.
5. Close the tab entirely (a fresh dwell window open) and, if `MOCHI_DISCORD_WEBHOOK` is set, confirm exactly one "↩ left Home · Ns" line appears in Discord (not two).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.jsx
git commit -m "$(cat <<'EOF'
webhooks: fire leave event on tab-hide/close with real dwell time

Client-measured dwell (Date.now() delta) posted via the existing
track() beacon on visibilitychange-to-hidden, with pagehide as a
fallback and a guard so both firing back-to-back doesn't double-post.
EOF
)"
```

---

## Task 5: Track the external "open" link on opportunity cards

**Files:**
- Modify: `frontend/src/components/OppCard.jsx:267-287`

**Interfaces:**
- Consumes: `track` (already imported at `OppCard.jsx:9`).

- [ ] **Step 1: Add the tracking call to the external link**

Replace `frontend/src/components/OppCard.jsx:266-287`:

```jsx
        {/* Primary action */}
        <div className="opp-card-actions">
          <button
            className={`opp-btn-details${isOpen ? ' opp-btn-details--active' : ''}`}
            onClick={() => {
              if (!isOpen) track({ type: 'action', action: 'open_card', category: opp.category })
              onDetails()
            }}
          >
            {isOpen ? t('card.close') : t('card.details')}
          </button>
          {(opp.submission_page || opp.official_website) && (
            <a
              className="opp-btn-open"
              href={opp.submission_page || opp.official_website}
              target="_blank"
              rel="noreferrer"
              onClick={() => track({ type: 'action', action: 'external_link_click', category: opp.category })}
            >
              {t('tf.open')}
            </a>
          )}
        </div>
```

- [ ] **Step 2: Manually verify**

Run the dev server, open any opportunity card's "Open" link, confirm (DevTools Network or Discord) a `👆 external_link_click · <category>` ping fires alongside the normal navigation.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/OppCard.jsx
git commit -m "$(cat <<'EOF'
webhooks: track external link click-through on opportunity cards

The 'Open' link to the actual submission page/site was the single
biggest untracked signal on the card — she clicking through to apply
is stronger intent than opening details ever was.
EOF
)"
```

---

## Task 6: Track contact "reached" and "not for me" in RelationshipTargets

**Files:**
- Modify: `frontend/src/components/RelationshipTargets.jsx:1-8` (imports), `:143-151` (`markReached`), `:295-297` (`hide`)

**Interfaces:**
- Consumes: `track` from `frontend/src/utils/track.js` (newly imported — not currently imported in this file).

- [ ] **Step 1: Import `track`**

Replace `frontend/src/components/RelationshipTargets.jsx:1-8`:

```jsx
import { useState, useEffect, useRef } from 'react'
import './RelationshipTargets.css'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb } from '../i18n/translations'
import { prepareRelationshipTargets } from '../utils/relationshipTargets'
import { cardsPerBatch } from '../utils/layout'
import { getCache, setCache } from '../utils/apiCache'
import { SectionHeader } from './OpportunitiesSection'
import { track } from '../utils/track'
```

- [ ] **Step 2: Track `markReached`**

Replace `frontend/src/components/RelationshipTargets.jsx:143-151`:

```jsx
  function markReached() {
    setReached(true)
    patchContact(c.name, {
      last_contacted: new Date().toISOString().slice(0, 10),
      status: 'in_contact',
    })
    track({ type: 'action', action: 'contact_reached', category: c.type })
    setToast(t('people.toast.reached'))
    setTimeout(() => setToast(null), 2500)
  }
```

- [ ] **Step 3: Track `hide`**

Replace `frontend/src/components/RelationshipTargets.jsx:295-297`:

```jsx
  function hide(name, type) {
    setHidden(prev => new Set([...prev, name]))
    track({ type: 'action', action: 'contact_hide', category: type })
  }
```

This changes `hide`'s signature from one argument to two. Update its only call site — `onHide?.(c.name)` at `frontend/src/components/RelationshipTargets.jsx:214-216` — to pass the type through:

```jsx
        <button className="rt-fb-btn rt-fb-btn--hide" onClick={() => onHide?.(c.name, c.type)}>
          ✕ {t('people.act.notForMe')}
        </button>
```

- [ ] **Step 4: Manually verify**

Run the dev server, open the People section, click "Reached" and "Not for me" on a contact card, confirm both actions ping (`contact_reached`, `contact_hide`) with the contact's `type` as category.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/RelationshipTargets.jsx
git commit -m "$(cat <<'EOF'
webhooks: track contact reached/hide actions in People section

Both were silent before — reached only patched the CRM record, hide
only updated local state. Now both post the same way follow/apply/hide
already do on opportunity cards.
EOF
)"
```

---

## Task 7: Track email draft copy and contact-log save in OppDetailPanel

**Files:**
- Modify: `frontend/src/components/OppDetailPanel.jsx:1-7` (imports), `:166-190` (log-contact save button), `:300-305` (copy-draft button)

**Interfaces:**
- Consumes: `track` (newly imported — not currently imported in this file).

- [ ] **Step 1: Import `track`**

Replace `frontend/src/components/OppDetailPanel.jsx:1-7`:

```jsx
import { useState, useEffect } from 'react'
import './OppDetailPanel.css'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb, translatePhrase } from '../i18n/translations'
import { isDistinct } from '../utils/textGuards.js'
import { locF, localizeDeadline } from '../utils/localize.js'
import { track } from '../utils/track'
```

- [ ] **Step 2: Track the "log contact" save**

Replace `frontend/src/components/OppDetailPanel.jsx:166-190`:

```jsx
            <button
              className="detail-log-btn"
              onClick={async () => {
                // If contact exists, update; otherwise create new
                const endpoint = crmContact ? '/api/contacts/update' : '/api/contacts'
                const method = crmContact ? 'PATCH' : 'POST'
                const body = crmContact
                  ? { name: opp.name, status: logForm.status, notes: logForm.notes, last_contacted: logForm.last_contacted }
                  : { name: opp.name, type: opp.category || '', city: opp.city || 'Tokyo', status: logForm.status, notes: logForm.notes, last_contacted: logForm.last_contacted, last_visited: '' }
                const r = await fetch(endpoint, {
                  method,
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(body),
                })
                if (r.ok) {
                  const result = await r.json()
                  setCrmContact(crmContact ? result.contact : { ...body })
                  setShowLogForm(false)
                  setLogSaved(true)
                  track({ type: 'action', action: 'contact_log_save', category: opp.category })
                  setTimeout(() => setLogSaved(false), 2000)
                }
              }}
            >
              {logSaved ? t('detail.savedCheck') : (crmContact ? t('detail.update') : t('detail.addToCrm'))}
            </button>
```

- [ ] **Step 3: Track the copy-draft button**

Replace `frontend/src/components/OppDetailPanel.jsx:300-305`:

```jsx
                  <button
                    className="detail-copy-btn"
                    onClick={() => {
                      navigator.clipboard?.writeText(draft)
                      track({ type: 'action', action: 'email_draft_copy', category: opp.category })
                    }}
                  >
                    {t('detail.copyDraft')}
                  </button>
```

- [ ] **Step 4: Manually verify**

Run the dev server, open an opportunity's detail panel, click "Log contact" → save, and separately copy an email draft. Confirm both `contact_log_save` and `email_draft_copy` actions ping.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/OppDetailPanel.jsx
git commit -m "$(cat <<'EOF'
webhooks: track contact-log save and email-draft copy in detail panel

Copying a draft is a stronger "about to actually send this" signal
than opening the card ever was; logging a contact was previously
silent even though it writes to the CRM.
EOF
)"
```

---

## Task 8: Track goal-add and exhibition-log save in PeppercornPage

**Files:**
- Modify: `frontend/src/components/PeppercornPage.jsx:357-365` (`addGoal`), `:811-832` (`submitShow`)

**Interfaces:**
- Consumes: `track` (already imported at `PeppercornPage.jsx:7`).

- [ ] **Step 1: Track `addGoal`**

Replace `frontend/src/components/PeppercornPage.jsx:357-365`:

```jsx
  function addGoal() {
    const trimmed = input.trim()
    if (!trimmed) return
    const isFirst = goals.length === 0
    const next = [...goals, { id: Date.now(), text: trimmed, done: false }]
    setGoals(next); setInput('')
    if (isFirst) setShownFirstNote(true)
    onSave(next); flash()
    track({ type: 'action', action: 'goal_add' })
  }
```

- [ ] **Step 2: Track `submitShow`**

Replace `frontend/src/components/PeppercornPage.jsx:811-832`:

```jsx
  async function submitShow() {
    if (!form.name.trim() && !form.venue.trim()) return
    const wasEditing = !!editingId
    setSaving(true)
    try {
      // PATCH an existing entry when editing, POST a new one otherwise.
      const url = editingId ? `/api/exhibition_log/${editingId}` : '/api/exhibition_log'
      const r = await fetch(url, {
        method: editingId ? 'PATCH' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form }),
      })
      if (r.ok) {
        const updated = await fetch('/api/exhibition_log').then(r2 => r2.json())
        setShows(Array.isArray(updated) ? updated : [])
        resetForm()
        flash()
        onCountsChanged?.()  // refresh the canonical group-show count (shared with Saffron)
        track({ type: 'action', action: wasEditing ? 'exhibition_log_edit' : 'exhibition_log_add' })
      }
    } finally {
      setSaving(false)
    }
  }
```

- [ ] **Step 3: Manually verify**

Run the dev server, open Peppercorn, add a career goal, then add and edit an exhibition-log entry. Confirm `goal_add`, `exhibition_log_add`, and `exhibition_log_edit` each ping once, at the right moment (not on every keystroke).

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/PeppercornPage.jsx
git commit -m "$(cat <<'EOF'
webhooks: track goal-add and exhibition-log save in Peppercorn

Both write real data (career_goals, exhibition_log) but were silent
before — rounds out curated-action coverage into Peppercorn, which had
only profile_save/saffron_answer until now.
EOF
)"
```

---

## Self-Review Notes

- **Spec coverage:** Expanded curated actions (Task 5-8, 7 new action types across 4 files), `leave`/real-dwell event (Tasks 3-4), persisted bot classification (Task 1), hosting/proxy signal (Task 2). All four goals in the design doc have a task. Non-goals (dashboard, geo auto-flag, identity system) have no task, correctly.
- **Placeholder scan:** none — every step has literal code, exact commands, and expected output.
- **Type consistency:** `_classify_client` returns `(str, bool)` from Task 1 onward; Task 2's edit to the same call site is written against that already-changed signature, not the original. `hide(name)` → `hide(name, type)` signature change in Task 6 updates its one call site in the same task.
- **Note on design-doc §1 accuracy:** `filter_change`/`sort_change`/`watchlist_add`/`watchlist_remove` from the earlier design draft don't correspond to real UI (no filter/sort controls or watchlist toggle exist in the current frontend — `watch_list` is a static section, not a togglable state). Tasks 5-8 substitute confirmed, real, currently-untracked interactions instead: external link click-through, contact reached/hide, email draft copy, contact-log save, goal add, exhibition-log add/edit.
