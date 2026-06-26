# Squire — Outreach Email Draft Review (Mochi / GEGYjiji)

Date: 2026-06-26
Reviewer: Squire (content / fact-check lead)
Batch reviewed: the 20 most recent drafts in `reports/inquiry_drafts/`, generated 2026-06-26 12:23–12:25 (files `ibm_01_*` through `ibm_20_*`). Older same-numbered files from earlier runs (6/24, 6/22, etc.) were ignored.
Sources: `Memory/artist_master_profile.json` (artist truth), `deploy_data/compact_opportunities.json` (522 opportunities; matched each draft to its entry by name/slug), `engines/ibm_email_writer.py` (generator + TONE_MAP).

Scott's bar applied: when GEGYjiji opens a draft she should feel RELIEF — send it after, at most, dropping in her real name or portfolio link. A draft only passes if it is true to her, fits what the venue actually is, is in the right language, and has nowhere left to fix.

---

## Section 1 — Per-draft verdict table

| # | venue (file) | category (opp) | lang | verdict | single most important issue |
|---|---|---|---|---|---|
| 01 | アートオリンピア2026 (`ibm_01`) | japan_watercolor_open_call | EN | EDIT | English inquiry to a Tokyo-based online-entry competition; no email contact, and it asks for the deadline/fees that are already public (July 31 2026; ¥6k student / ¥12k). |
| 02 | Route Books (`ibm_02`) | bookstore_gallery | JA | READY | — |
| 03 | 第113回 日本水彩展 (`ibm_03`) | japan_watercolor_open_call | EN | PROBLEM | Written in English to a Japanese national watercolour society that lists TEL/FAX only (no email); subject says "113th", body asks about the "114th". |
| 04 | Canadian Society of Painters in Water Colour (`ibm_04`) | global_watercolor_open_call | EN | READY | — |
| 05 | Book and Sons (`ibm_05`) | bookstore_gallery | JA | READY | — |
| 06 | SUZURI (`ibm_06`) | zine_shop_consignment | JA | PROBLEM | SUZURI is a self-serve print-on-demand platform (contact: None) — you upload designs, you do not email a consignment request. Wrong action entirely. |
| 07 | mona records (`ibm_07`) | zine_shop_consignment | JA | PROBLEM | Garbled term "コンスメント" in BOTH subject and body (should be コンサインメント / 委託販売) — not sendable as written. |
| 08 | Blooming Stories 2026 (`ibm_08`) | japan_watercolor_open_call | EN | PROBLEM | English email to a Japanese-language note.com call, and it ignores the imminent deadline (2026年6月29日 — 3 days out). |
| 09 | Tokyo Art Book Fair (`ibm_09`) | fair_popup | EN | READY | — |
| 10 | Kamome Roastery Tokyo (`ibm_10`) | cafe_gallery | JA | READY | — |
| 11 | Mograg Gallery (`ibm_11`) | cafe_gallery | JA | EDIT | Claims Mograg's space is "静かで親密" (quiet/intimate); the opp explicitly warns it is contemporary/outsider, "not polished or quiet." Mischaracterises the venue. |
| 12 | biscuit gallery「grid next : Emerging」 (`ibm_12`) | gallery | JA | PROBLEM | Applying to an expired call — opp deadline is January 1, 2024 (closed ~2.5 years). |
| 13 | Gallery and Links81 group-show call (`ibm_13`) | gallery | JA | READY | — |
| 14 | grid next : 2025 Emerging Artists Showcase (`ibm_14`) | gallery | JA | PROBLEM | Expired call (opp deadline August 10, 2024) AND a duplicate of #12 (same gallery, same programme). |
| 15 | Osaka Open Call — ARRIVAL (`ibm_15`) | gallery_event | EN | EDIT | Invents a venue aesthetic ("the quiet, atmospheric visual language your gallery tends to champion") with no supporting data; opp `why_it_fits` is empty and contact is None. |
| 16 | Village Vanguard Shimokitazawa (`ibm_16`) | bookstore_gallery | JA | READY | — |
| 17 | Antenna Books (`ibm_17`) | bookstore_gallery | JA | READY | — |
| 18 | SPBS (Shibuya Publishing Booksellers) (`ibm_18`) | bookstore_gallery | JA | READY | — |
| 19 | SHIBUYA CAST. Gallery (`ibm_19`) | cafe_gallery | JA | EDIT | Invents a venue character ("日常の中にある美しさを大切にされている貴ギャラリー"); opp describes a proposal-based mixed-use event complex, not a curatorial gallery with that ethos. |
| 20 | Tokyo Gendai 2026 (`ibm_20`) | fair_popup | EN | PROBLEM | A gallery-booth international art fair — only galleries exhibit, not individual artists. She has no representation, so the "exhibitor inquiry" ask is structurally impossible; contact is None. |

Counts: READY 9 · EDIT 4 · PROBLEM 7.

---

## Section 2 — PROBLEMS, detail

For each EDIT/PROBLEM: the draft, the exact issue, the fix, and the opportunity field that proves the mismatch.

### 01 — アートオリンピア2026 — EDIT
- Issue: The email is in English and is framed as a "share details on the submission process, deadline, and any associated fees" inquiry. Art Olympia is a Tokyo-based juried competition with online entry; the deadline and fee structure are already published, and there is no email address to receive an inquiry.
- Fix: Switch to Japanese (Japan-based call). Drop the request for deadline/fees — state instead that she intends to enter the watercolour category by the July 31 deadline and is confirming the entry route, or simply repurpose this as portfolio framing for the online submission rather than an "inquiry email." Naming Tide from China (an ACG illustration group show) to a fine-art prize is acceptable but Colour Diary + the diary practice carry more weight here.
- Proof: opp `category: japan_watercolor_open_call`, `city: Tokyo / country: Japan`, `deadline: 2026-07-31`, `contact: "Online submission: compe.japandesign.ne.jp/artolympia-2026"` (no email), `why_this_fits_short` already states the fees ("¥6,000 for one work vs ¥12,000").

### 03 — 第113回 日本水彩展 — PROBLEM
- Issue 1 (language/fit): English email to 日本水彩展 — a Japanese national watercolour institution shown at the Tokyo Metropolitan Art Museum. It must be Japanese.
- Issue 2 (deliverability): the opp lists `contact: TEL: 03-5828-1616 / FAX: 03-5828-1619` — there is no email address, so an email draft has nowhere to go.
- Issue 3 (internal consistency): subject line reads "113th Japan Watercolor Exhibition" while the body asks about "the upcoming 114th edition." Pick one. (Timing-wise the 114th is the live target — the 113th ran June 2026 and is over — so the body's intent is right and the subject is stale.)
- Fix: Rewrite in Japanese; correct the subject to the 114th / next open call; route it to phone or the society's site contact, not email. Note this is a Tier-3 "prepare-and-watch" target, not a today action.
- Proof: opp `deadline: "Annual — 113th edition June 2026; 114th expected spring 2027"`, `contact: TEL/FAX only`, `city: Tokyo / country: Japan`, `category: japan_watercolor_open_call`.

### 06 — SUZURI — PROBLEM
- Issue: The draft is a consignment-style outreach asking SUZURI to consider featuring her work ("ご興味をもっていただけましたら幸いです"). SUZURI is a print-on-demand platform — the artist signs up and uploads designs; the platform prints and ships on sale. There is no one to email and nothing to "inquire" about.
- Fix: Do not generate an outreach email for this opportunity at all. The correct user action is "make an account and upload a few diary pieces if it appeals." If Mochi wants to surface it, it should be an action card, not a draft email.
- Proof: opp `contact: None`, `one_sentence: "Japanese print-on-demand platform where artists upload designs and the platform produces and ships any sales… entirely optional"`, `why_this_fits_short: "nothing you need to set up unless it appeals."` (The `category: zine_shop_consignment` label is itself wrong for a POD platform and is what produced the bad draft.)

### 07 — mona records — PROBLEM
- Issue: The word "コンスメント" appears in the subject (件名: 水彩作品のコンスメントについてのご相談) and again in the body ("ジンや印刷物のコンスメント"). It is a garbled rendering of コンサインメント (consignment); the natural Japanese is 委託販売. A native reader sees a broken loanword immediately — this fails ready-to-send on its own. Secondary: the opp's `deadline: "March 30th at 5pm"` is already past, and `contact: None`.
- Fix: Replace コンスメント with 委託販売 (or コンサインメント) in both places. Confirm whether mona records currently takes consigned printed matter before sending.
- Proof: opp `name: Mona Records`, `category: zine_shop_consignment`, `deadline: "March 30th at 5pm"`, `contact: None`.

### 08 — Blooming Stories 2026 — PROBLEM
- Issue 1 (language): English email to a Japanese-language open call hosted via note.com (公募展 hashtag). Should be Japanese.
- Issue 2 (deadline-blind): the deadline is 2026年6月29日 — three days from this review — and the draft never mentions it. A deadline-aware draft would lead with it.
- Issue 3 (fit, handled honestly): it is a flower-themed call and flowers are not her core subject; the draft hedges this gracefully ("flowers appear often… not as a subject in themselves"). Acceptable, but combined with 1+2 the draft is not sendable.
- Fix: Rewrite in Japanese, lead with the June 29 deadline, and confirm watercolour is accepted (the listing is thin). If it cannot be confirmed and turned around in three days, deprioritise.
- Proof: opp `category: japan_watercolor_open_call`, `country: Japan`, `deadline: 2026年6月29日（月）`, `official_website` = a note.com 公募展 hashtag page, `one_sentence: "confirm whether watercolour entries are accepted before you invest time."`

### 11 — Mograg Gallery — EDIT
- Issue: The draft asserts "Mogragさんの空間に漂う、静かで親密な雰囲気が自分の作品と近いものを感じ" — i.e. it claims the gallery's atmosphere is quiet and intimate, matching her work. The opportunity research says the opposite.
- Fix: Remove the "quiet/intimate atmosphere" claim. Anchor instead on the real, verifiable hook: Mograg programmes emerging, un-represented artists by direct proposal (no juried call) — that is the honest reason to approach. Send via Instagram DM (no email).
- Proof: opp `one_sentence: "contemporary/outsider-leaning, so judge the fit yourself"`, `why_this_fits_short: "The work it shows leans contemporary/outsider, not polished or quiet, so don't take a 'fit' on trust"`, `contact: @mograggallery`.

### 12 — biscuit gallery「grid next : Emerging」 — PROBLEM
- Issue: The draft is a live application to an open call whose deadline has passed. The email itself is well-written Japanese (names Colour Diary + Tide from China, references the call by name), but the call is closed.
- Fix: Do not send. If Biscuit Gallery runs a current grid next cycle, retarget the draft to that edition's deadline. Also see #14 — these two drafts are the same gallery/programme and should be deduplicated to one.
- Proof: opp `name: 【biscuit gallery】初の公募企画「grid next : Emerging …`, `deadline: January 1, 2024`.

### 14 — grid next : 2025 Emerging Artists Showcase — PROBLEM
- Issue: Same as #12 — expired (deadline August 10, 2024) — and a duplicate venue. Two near-identical application emails to Biscuit Gallery for the same "grid next" programme should never both reach the artist.
- Fix: Drop this one; keep at most a single, current grid next draft. Add venue/organisation-level deduplication upstream so one gallery does not generate two drafts.
- Proof: opp `name: 公募企画「grid next : 2025 - Emerging Artists Showcase …`, `official_website: https://biscuitgallery.com/gridnext-2025/`, `deadline: August 10, 2024`, `contact: info@biscuitgallery.com` (same address as #12).

### 15 — Osaka Open Call — ARRIVAL — EDIT
- Issue: The opener invents a venue character — "the kind of quiet, atmospheric visual language your gallery tends to champion" — with no supporting data. The opp's `why_it_fits` is empty and `one_sentence` is only "Open Calls / Contests (found through targeted research)." Fabricated-specific praise is worse than honest generic, because it claims knowledge she does not have. Secondary: submission is via an EntryThingy portal and `contact: None`, so an email has no recipient.
- Fix: Remove the invented aesthetic claim; open honestly ("I came across your Osaka 2026 open call via EntryThingy"). Route through the portal, not email. Confirm whether the call accepts international/Tokyo-based applicants and what the fee/deadline are (genuinely unlisted).
- Proof: opp `name: Osaka Open Call For Artists. - ARRIVAL`, `why_this_fits_short:` (empty), `one_sentence: "Open Calls / Contests (found through targeted research)."`, `submission_page: app.entrythingy.com/...`, `contact: None`.

### 19 — SHIBUYA CAST. Gallery — EDIT
- Issue: The draft praises "渋谷という街に根ざしたコミュニティと、日常の中にある美しさを大切にされている貴ギャラリー" — attributing a "values everyday beauty" curatorial ethos to the venue. The opp describes a central-Shibuya mixed-use complex with rentable gallery/event space, programmed by proposal — not a gallery with that stated aesthetic. It is also the thinnest draft in the batch.
- Fix: Replace the invented ethos with the real hook: a central-Shibuya, proposal-based space with strong foot traffic and community programming. Keep it honest that she is proposing an exhibition and asking about the space-use process.
- Proof: opp `one_sentence: "Central Shibuya mixed-use complex with gallery space and a cafe; programs exhibitions and community events — proposal-based."`, `why_this_fits_short: "whether the space suits your work is something to check against their current shows."`, `contact: @shibuyacast`.

### 20 — Tokyo Gendai 2026 — PROBLEM
- Issue: The draft asks "about exhibitor opportunities at Tokyo Gendai 2026" as an individual artist. Tokyo Gendai is a gallery-booth international art fair — galleries apply and bring their represented artists; individual artists cannot apply to exhibit. GEGYjiji has no gallery representation (profile: `gallery_representation: "none confirmed"`), so the ask is structurally impossible. There is also no email contact. (Note: the opp's own `why_it_fits` text is itself hallucinated — "making your a strong fit for gallery representation at this stage" — which is what produced this draft.)
- Fix: Do not generate an artist-direct outreach email for gallery-booth art fairs (Tokyo Gendai, Art SG, Frieze-class). If surfaced at all, it belongs in a long-range "stretch / via-a-gallery" note, not an immediate sendable draft.
- Proof: opp `category: fair_popup`, `one_sentence: "Fourth edition art fair in Tokyo, September 11-13, 2026, with gallery applications open."`, `deadline: "2026 (gallery applications open…)"`, `contact: None`; artist profile `career_history.gallery_representation: "none confirmed"`.

---

## Section 3 — STANDARDS: what every draft must satisfy (spec for fixing the generator)

This is the concrete pass/fail checklist a regenerated draft must meet before it reaches GEGYjiji.

### A. Truth
1. Only facts present in `artist_master_profile.json`: Colour Diary (first solo illustration collection, Oct 2021); the daily "diary" practice since 2020; Tide from China Part1 (first Japan show, group, ACG_Labo Harajuku, Feb 2023); Instagram @gegyjiji. (This batch passed truth — keep it that way.)
2. No invented awards, residencies, gallery representation, sales, or follower counts. Do not state a follower number in the body (the profile flags a 27k-Instagram vs 90k-Twitter ambiguity — omit the number, as every draft here correctly did).
3. Work-title/date accuracy: "Colour Diary, October 2021"; "Tide from China Part1, February 2023." No drift.
4. Title discipline: "watercolour illustrator" / "水彩イラストレーター" is the truest self-description (BIFT illustration roots, her own bio says イラストレーター). "画家 / painter" is tolerable but should not be the default for illustration-ecosystem venues.

### B. Fit to the opportunity (the area that failed most)
5. The ASK must match the venue's actual mechanism. Map category/overview to the correct action and refuse to email when email is not the mechanism:
   - print-on-demand (SUZURI) → self-serve sign-up, NO email draft;
   - online juried entry (Art Olympia, CSPWC, EntryThingy calls) → submit via portal; an email is at most a narrow logistics question, not an introduction;
   - gallery-booth art fairs (Tokyo Gendai) → galleries apply, NOT individual artists → NO artist-direct draft;
   - rental/bookshop/café/zine-shop/consignment → an email/DM introduction is correct.
6. Reference the venue's REAL focus, taken from the opp's `overview` / `why_it_fits` / `one_sentence`. Never invent a venue aesthetic. If those fields are empty or thin (Osaka ARRIVAL) or warn against a fit (Mograg), the draft must NOT manufacture specific-sounding praise — open with a neutral, verifiable fact (location, format, programme type).
7. Respect explicit venue warnings in the data ("not polished or quiet," "judge the fit yourself") — do not assert the opposite.

### C. Language
8. Language follows the VENUE's operating language, not whether the category happens to be in `TONE_MAP`. Domestic Japanese venue (city Tokyo/Osaka/etc. or country Japan) → Japanese; genuinely international venue (Canada, UK, US, "International") → English.
9. Root-cause to fix in `ibm_email_writer.py`: `TONE_MAP` does not contain `japan_watercolor_open_call`, `global_watercolor_open_call`, `global_open_call`, etc., so they fall through to the default `("en", …)`. That is why three Japanese watercolour calls (Art Olympia 01, 日本水彩展 03, Blooming Stories 08) came out in English. Every category must map a language, and the `is_international()` override must be able to flip EN→JA for domestic venues, not only JA→EN.

### D. Specificity
10. Name a work that fits THIS venue: Colour Diary + the daily diary for zine/bookshop/consignment/book-fair; Tide from China for Japan exhibition/gallery contexts; either for watercolour open calls. No interchangeable boilerplate.
11. The opener must contain at least one venue-specific, data-backed detail (neighbourhood, format, programme), never "I love your space."

### E. Ready-to-send
12. No garbled or invented loanwords. "コンスメント" must never ship — use 委託販売 / コンサインメント. Add a Japanese-term lint check.
13. Subject and body must agree (the 113th-vs-114th split must not happen).
14. No `[brackets]`, placeholders, or instructions; Instagram @gegyjiji present; no Twitter/X. (This batch was clean on brackets — keep it.)
15. Deadline awareness: if the opp has a real future deadline, name it (Blooming Stories June 29; Gallery and Links81 Sept 14; CSPWC June 30). If the deadline is in the PAST, do not generate a live application at all (Biscuit grid next Jan 2024 / Aug 2024; mona records Mar 30) — filter on `deadline < today`.
16. Deliverability: if the opp has no email and the mechanism is a portal/DM, the draft must be shaped for that channel (or suppressed), not addressed as an email to nobody.
17. Deduplicate by venue/organisation: one gallery (Biscuit Gallery appeared as both #12 and #14) must not yield two drafts.

---

## Section 4 — One-line verdict

Of the 20 drafts, 9 are genuinely send-ready (02 Route Books, 04 CSPWC, 05 Book and Sons, 09 Tokyo Art Book Fair, 10 Kamome, 13 Gallery and Links81, 16 Village Vanguard, 17 Antenna Books, 18 SPBS); 11 need work (4 EDIT, 7 PROBLEM) — driven by wrong language on Japanese calls, expired/duplicate calls, wrong-action drafts for self-serve or gallery-only venues, one garbled word, and invented venue praise.
