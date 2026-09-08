# Saffron authored-content audit — 2026-09-08

**Scope:** every factual claim in `frontend/src/data/saffron_insights.js` (1,332 lines,
9 exports), plus `peer_artists.json`. Six parallel agents, each checking one block
against live external sources. Nothing in this file is my opinion about tone — it
is claims that are checkably true or checkably false.

**Why it happened:** on 2026-09-08 three fabrications surfaced in the parts of
Saffron that happened to be touched for unrelated reasons — an invented
`editorial@bijutsutecho.com`, an invented pricing band set *above* her real
prices, and `a_series` asserting a false absence. None was found by looking. The
question was whether the rest was any better.

**It is not.**

---

## The one-line summary

Across the four blocks measured precisely, **roughly a quarter of claims are
checkable and true, and most of that quarter is "this company exists."** The rest
splits between wrong specifics and unfalsifiable filler. The filler is the reason
the wrong facts survived: it reads as expertise while asserting nothing, so
nobody audits it.

| Block | Verified | Wrong | Unverifiable | Unfalsifiable filler |
|---|---|---|---|---|
| `LICENSING_LANDSCAPE` | ~24% | ~12% | ~26% | ~38% |
| `GRANT_LANDSCAPE` | 4 of ~30 claims | high | high | all 5 `competition` fields |
| `PRESS_PITCH_MAP` | 1 outlet clean | 3 of 5 routes broken | 1 outlet may not exist | every `how_discovered`, every `timeline` |
| `COLLECTOR_ECOSYSTEM` / `REVENUE_STREAMS` | platforms exist | 1 claim about her record | — | conversion/demographic claims |

---

## TIME-CRITICAL — perishable, verify then act

1. **Arts Council Tokyo Startup Grant, ¥300,000 — closes 24 Sep 2026, 18:00 JST.**
   Individual-eligible; no nationality clause found; Tokyo residence required.
   The only individual-eligible Arts Council Tokyo grant currently open. **Not
   mentioned anywhere in the app.** Open question: whether a 留学 visa satisfies
   「東京都内に居住する個人」 is *not* addressed on any published page — needs the
   募集要項 PDF or a call to 03-6256-8431. Do not present as settled.
2. **ACC Individual Fellowship — 2027 cycle open 1 Oct – 10 Nov 2026.** The app
   says "typically March". But see the student bar below before surfacing it.

---

## Ranked findings

### 1. Bunka-cho — the app tells her to apply to something she is legally barred from
`GRANT_LANDSCAPE` says *"Foreign residents may apply if they meet career stage
criteria."* The FY2027 募集案内 §2.5(1) reads
「日本国籍又は日本の永住資格を有すること」, and the form requires documentary proof
of permanent residency from non-nationals. Her `residence_status` is a student
visa. **There is no career-stage route around it.** The entry's own tip pushes her
to secure a host-institution 受入承諾書 first — months of work against a closed
door. The FY2027 window also closed 31 Jul 2026.

### 2. `acc.org` is the American College of Cardiology
The only contact URL in the grants block. Correct domain:
`asianculturalcouncil.org`.

### 3. Two organisations that could not be shown to exist
- **"China Arts Foundation International"** — zero registered nonprofits under
  that name; "apply via the Chinese embassy cultural attaché" is an invented
  route; the Tokyo embassy's notice index carries nothing about arts funding.
- **"ILOVETOYS / neuprint"** (press) — eight searches across English and Chinese
  found nothing. Its contact field names no account on a platform
  (**Weibo**) she does not use, while Xiaohongshu (44k), where she does, goes
  unmentioned. Its `_zh` also invents "Beijing" as her origin; the English does
  not say it.

Note the two failure shapes. Bijutsu Techo was dangerous because it was
**specific and false**. These are dangerous because they are **vague enough never
to be caught**.

### 4. A second Bijutsu Techo, in licensing
Midori/Designphil: *"Send a licensing lookbook PDF directly to the creative
director (not info@)."* No creative director is named; Designphil publishes no
individual contact. The instruction actively pushes her to guess an address.

### 5. Press routes — three of five are broken
- **Casa Brutus** — "email editorial" does not exist. Magazine House accepts
  press **by post only** (〒104-8003 東京都中央区銀座3-13-10, per-title). The one
  email a determined person will find is **ad sales**.
- **Pen** — no contact form on `pen-online.jp`. Real: form.run/@cccmh-1668417933
  (print). No editorial email is published anywhere; "cold email" should go.
- **It's Nice That** — `/submit` 302s to `/contact`. Real: `/submissions` and
  `submit@itsnicethat.com`. They *do* take unsolicited work, so the block's core
  advice is right and only the URL is stale.
- **Apartamento** — correct. "Not pitch-based" holds up.
- Handles that ARE verified: `@casabrutus`, `@apartamentomagazine`.

### 6. Licensing — a quarter true, and one brand is simply wrong
- **Stalogy is Nitoms (Nitto Group), art-directed by good design company — not
  Nakabayashi.** It has no illustration line and no external design route, and it
  is named in the lead as one of four "natural partners."
- **Osaji does not collab with illustrators** (makeup artists, chefs, musicians).
  HACCI does. Wrong name in the sentence.
- **Mark's "open to submissions from Japanese-resident artists"** — invented
  eligibility rule; no submissions route is published. It is the only green light
  in the block and the least supported.
- **All six yen figures unsourced.** The royalty band (3–8%) is defensible but
  sourced entirely from US/UK practice; Japanese stationery deals are commonly
  flat-fee 買い取り, so it sets the wrong negotiating posture.
- **"Get a press feature first, then publishers come to you"** displaces the real,
  dated, nationality-open routes: ザ・チョイス, 装画コンペ/GALLERY HOUSE MAYA
  (check hiatus status), and agency representation (CWC Tokyo).

### 7. A wrong claim about her own record
`COLLECTOR_ECOSYSTEM`: *"three originals at your top price have sold."* Her shop
shows **two** at ¥115,500 sold out (9 listed, 4 sold out). Overstates top-price
revenue by ¥115,500. Worse, it treats BASE's `SOLD OUT` stock flag as a completed
sale, and it violates the profile's own `_volume_caveat`, which forbids deriving
demand from shop history in exactly these words.

### 8. No platform economics anywhere
Neither revenue block states a single fee. Current real rates: **BASE 6.6% + ¥40**,
**BOOTH 5.6% + ¥45** (raised 28 Oct 2025), **Creema 10.67%** (changed 5 Nov 2025 —
now charged on shipping too), **minne 10.56–10.89%** (incl. shipping). The fixed
per-order component is regressive: her ¥1,100 postcard pack carries ~10% cost on
both platforms the page recommends for it. Any "11% Creema" elsewhere in the repo
is stale.

### 9. TABF is presented as an open door with no window
2026 applications **closed 7 Jun 2026**; the fair runs 21–24 & 29–31 Jan 2027;
next window ~mid-2027. Also: a *different* event, TOKIO ART BOOK FAIR, exists and
is separately in the pipeline — easy to conflate.

### 10. Press kit — overstated to editors
- `long_bio` cites **Bored Panda ×2** as her press record. Both are unsigned
  listicles with zero artist quotes. This is her entire press credential line in
  a bio destined for 美術手帖 / Apartamento / Casa Brutus.
- **"based between Tokyo and Beijing"** — unsourced, and it opens every bio in
  all three languages. The profile's own sourced synthesis says "based in Tokyo."
- **Cats foregrounded throughout** — contradicts the dated `subject_correction`
  (2026-09-05): cats are *not* her subject, architecture and space is, and the
  correction names Bored Panda as the contamination source. The kit propagates
  the exact error into copy telling editors what to cover.
- **Missing her third solo show** (Light and Shadows and Cats, Lemonde Tokyo,
  25 Aug–6 Sep 2026). `long_bio` still says "a solo exhibition" singular.
- The first-person `statement` is machine-authored; the profile explicitly warns
  against attributing synthesized text to her.
- **Clean and worth protecting:** no age, no birth year, no follower number, no
  "90k Instagram", and **no invented representation, residency or award.**

### 11. Collaboration map — no handle sends her to a stranger
The good news first: every link resolves to the right person. Remaining issues:
- **Liz Climo "cats are her whole language"** — false, and it is the stated
  reason for the pairing.
- **富大貴 "a cats series"** — unsupported; the works are 「四季」 and
  「蜥蜴と猫」 (one work). Line 1033 leans on it.
- **Kiuchi mischaracterised** — an ADC judge with NYT/New Yorker/Penguin credits,
  framed as "bookshop ecosystem."
- **Urbanowicz "runs an art-book fair"** — false credit; it is Ogaki Bookstore's.
- **Puuung "soft-watercolor"** — pencil + Photoshop.
- **HJL is missing** from the Tide from China roster (6 artists, 5 co-exhibitors —
  the copy's "five" is correct; the map is short one person). Title is
  "Tide from China **Part1**".
- Prefer `x.com/kuribulb` (live, ~16.6K) over the 2022-vintage Instagram; same for
  `bangjoy1992` (5K IG vs 118K X).
- `x.com/tuoer_sg` is **verified** — "_sg" is a username, not Singapore. Do not
  let anyone "correct" it.

### 12. Unflagged legal risk
She is a student. Both revenue blocks push her toward opening storefronts without
mentioning 資格外活動 individual permission. Lowest arithmetic risk, highest
consequence if wrong.

---

## Already fixed today

- **`peer_artists.json` — a shipped fix had been silently reverted.**
  `08dea050` (2026-09-05) edited the *output*; `engines/peer_artist_engine.py`
  regenerates it from `artist_intelligence_seed_data.json`, so the next pipeline
  run wiped it and resurrected the "Japan Watercolor Society exhibitors"
  pseudo-person. Textbook Data Patch Rule violation. Fixed **at the seed**;
  10 peers live.
- **`score_peer` had never worked** — whole-phrase set intersection between two
  independently authored vocabularies, so every peer scored 0.0 forever and the
  "sorted by fit" comment described nothing. Now word-level.
- Bijutsu Techo contact, pricing band, `a_series` (earlier in the session).

---

## Recommended order

1. **Surface the ¥300k Startup Grant** (16 days) — after checking the 留学
   residence question. This is the only item with a clock on it.
2. **Rewrite `GRANT_LANDSCAPE`.** Highest harm: a legal bar presented as an open
   door, a cardiology URL, and an organisation that may not exist. Verified
   replacements exist for most of it, including TOKAS-Emerging (solo show +
   ¥150k, nationality-blind) which is the best fit on the page and absent.
3. **Fix the four broken press routes.** Small, bounded, all replacements known.
4. **Decide what to do with `LICENSING_LANDSCAPE.`** At ~38% unfalsifiable filler
   and ~12% wrong, repairing it in place may cost more than cutting it to the
   verified core (Hobonichi and Mark's do license illustrators) plus the real
   entry routes.
5. **Press kit:** drop the Bored Panda credential line, fix "Tokyo and Beijing",
   add the third solo show, and resolve cats-vs-architecture against the
   2026-09-05 correction.
6. **Add platform fees** to the revenue blocks, or stop recommending platforms.
7. Collaboration map corrections — lowest risk, all small.

## The rule this suggests

Every claim in authored content should carry a source and a date, or be cut. The
blocks that survived audit best are the ones that already did (`PRESS_PITCH_MAP`
has `contact_url`; `PRICING_INTELLIGENCE` now reads from the profile). The blocks
that failed worst have neither — `LICENSING_LANDSCAPE` contains zero URLs and zero
dates in 114 lines.

---

## STATUS: acted on, same day (commits 7245f7ea, d1978cbf, 3c70a595)

Everything ranked above has been fixed and deployed, verified against the served
bundle. Two corrections from Scott changed what the fixes should say:

- **Sales.** Four originals have sold, ever — Scott bought **three**; one had
  already sold. So finding 7 was wrong on the count *and* wrong in kind: it
  credited the market with what a friend did. The claim was **removed**, not
  corrected, and `market_presence._sales_known` now carries the rule.
- **Cats.** The 2026-09-05 `subject_correction` overcorrected. Scott: *"she does
  paint cats… she does paint a lot of cats. I just don't think it's really what
  she is the best at."* Cats are **reordered below architecture, not erased.**

Deliberately NOT done: surfacing the ¥300k Arts Council Tokyo grant to her
(Scott: "don't worry about the art council thing. she probably won't even look
at it"). The grants block itself was still corrected.

One fix declined on principle: the audit noted `bangjoy1992` has 118K on X
versus 5K on Instagram, but it verified only the follower count, never the
handle. Switching the link would have meant guessing a URL — the exact failure
this audit exists to catch — so the verified Instagram link stayed.

Two things this exposed about the toolchain, both worth keeping:

1. **Six of my own edits added `_zh` keys that already existed further down the
   same object.** In JS the last key wins, so every corrected English string
   would have rendered beside its stale Chinese. `eslint no-dupe-keys` caught
   all six — lint is load-bearing for correctness here, not just style.
2. **`git add memory/...` silently matched nothing** (the tree is `Memory/`), so
   the profile changes missed their commit and were only noticed because the
   commit reported two files instead of three.
