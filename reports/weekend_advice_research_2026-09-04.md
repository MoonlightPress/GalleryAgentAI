# Weekend advice research — named targets for `_next_tier_levers()`

**Date:** 2026-09-04
**Scope:** research only, for `engines/career_strategy_engine.py::_next_tier_levers()` (line 472). No code changed.
**Method:** five parallel web-research passes (galleries, residencies, grants, press, fairs + solo venues), ~150 searches and ~250 page fetches against official pages where possible. Every item below carries a confidence tag: **direct** = read on the organisation's own page; **inferred** = pattern/secondary source; **unverified** = could not confirm, do not surface as fact.

---

## 0. Things the engine gets wrong today (read this first)

These came out of reading the function and the profile against the research; they matter more than any single venue name.

1. **`solo_venue_quality` never fires for her any more.** The gate is `if solo_shows < 3:` (line 506). `memory/career_strategy_report.json` says `solo_shows: 3` (77ART Shanghai 2025, Moon Gallery April 2026, Le Monde Sept 2026). So the lever that is *most* relevant right now is the one she can't see. The research below shows the gate is also measuring the wrong thing: all three solos were **pay-to-exhibit** venues (see §2), so the real question is "has she had a solo that the venue paid for" — not the count. Suggest gating on venue tier (e.g. `has_curated_solo`) rather than `solo_shows < 3`, or dropping the gate entirely.

2. **Nationality is not an open question — it's in the profile.** `artist_master_profile.json` → `visual_profile.nationality: "Chinese"`, hometown Changsha, `is_student: true`, JLPT N2, based "Tokyo / Beijing". This is the single largest filter on grants and residencies: every classic Japanese overseas-study grant (Pola, Yoshino Gypsum, almost certainly 文化庁) requires 日本国籍 or 永住. The `grant` action ("open to your nationality") should be replaced with the actual eligible list in §5. Corollary: she is a Chinese citizen, so **ACC's Mainland-China track is open to her by citizenship** regardless of living in Tokyo.

3. **`career_strategy.current_phase` in `artist_master_profile.json` still says `"Tier 1-2"`** (line 473 of the JSON). The report file says Tier 3. CLAUDE.md says don't hardcode the tier, and the engine reads the report, so this is a documentation stale rather than a bug — but anything else reading the profile directly will get the wrong phase.

4. **Foundation-tier text names venues that are closed.** Not in `_next_tier_levers` but in the same file's foundation ladder and in the profile's `tier_2`/`tier_3` examples: **3331 Arts Chiyoda closed March 2023**; **BankART Station / KAIKO ceased March 31, 2025** (Yokohama City contract ended; the "Under 35" program is gone — verify what BankART1929 still operates before naming it anywhere); **Youkobo Art Space discontinued its residency**. She's past that ladder so it doesn't reach her, but tests and future artists will hit it.

5. **The `residency` action says "Tokyo–Beijing"** — consistent with the profile, fine. But the *detail* text frames residency as "abroad"; the two best-fit programs are in Tokyo and Fukuoka and are nationality-unrestricted. Don't push her overseas for a first residency when TOKAS is a train ride away.

6. **Time-sensitive as of today:** Arts Council Tokyo Startup Grant Round 2 closes **2026-09-24**; TOKAS 2027 residency calls expected to open **mid-September 2026** (six-week window); HB Gallery FILE competition vol.37 likely closes **mid-October**; Nomura **Oct 1–30**; Asahi **Oct 25**; ACC **Oct 1–Nov 10**. If any of this lands in Today's Focus, it should land this month.

---

## 1. `gallery_representation` — commercial galleries that fit

**Baseline fact for the copy:** neither of her Tokyo venues is a representing gallery. Both are rental:
- **月画廊 / Moon Gallery & Studio (合同会社新月芸術)**, Kita-Ueno — Chinese-run rental, ¥100,000 / 5 days minimum, no commission, Google-Form booking. Program is Chinese ceramicists/illustrators and zines. [moon-gallery-studio.com](https://www.moon-gallery-studio.com/) · [rental-gallery.jp listing](https://rental-gallery.jp/moon-gallery-studio/) — **direct**
- **Galerie LE MONDE**, Harajuku — curated-but-paid illustration gallery (Yoshinobu Tajima, since 2015). Apply by email, they vet, you pay: from ¥180,000 / 6 days; 12-day solo ≈ ¥374,000 incl. tax. Her current solo is on their front page. [galerielemonde.com/about](https://www.galerielemonde.com/about) — **direct**
- **ACG_Labo** (her 2023 debut) is a Chinese-illustration merchandising company's gallery — same tier. — **direct**

So "a step up" means: *a gallery that pays for the show and takes commission only, or a juried route to a free solo.* Say that plainly.

### Ranked targets

**1. GALLERY KOGURE (ギャラリー小暮)** — Kanda-Jimbocho (+ Kyoto)
- Why it fits: best roster match found. Works-on-paper and illustration-to-fine-art crossovers — Yuko Soi (colour pencil/pen drawing), Atsuko Goto (pigment/ink on cotton), Noriyuki Haraguchi (pencil/pastel on paper), Takato Yamamoto — plus Asian artists (Xueyang Wang, Teng-Yuan Chang, Filipino illustration-adjacent painters Valerie Chua, Dexter Sy). Group shows like "A Little Gem" and "Summer of Ghosts" (Jul–Aug 2026) are small paper works — her format. Shows at ART021 Shanghai, JINGART Beijing, Enter Art Fair Copenhagen.
- How they take artists: **no submissions page, no "no unsolicited" notice** — only works@gallerykogure.com. Cold approach after visiting a show is the realistic route.
- Source: [gallerykogure.com/artists](https://gallerykogure.com/artists/) · [exhibitions](https://gallerykogure.com/exhibitions/)
- Confidence: fit **direct**; intake **unverified**.

**2. biscuit gallery** — nudge field, Shinjuku 3-32-10 (moved June 2025)
- Why it fits: founded 2021, "emerging artists from Japan and abroad", 181 artists incl. young Korean painters. **The only Tokyo commercial gallery found with a formal, free open call — "grid next"** (with AWASE gallery): free entry, free exhibition, ~age ≤40, students OK, ~25 artists shown in August, **one gets a solo show**. 2025 winner (Momoka Ota) then appeared in Kaikai Kiki's Instagram-scouted show — the pipeline is real.
- Window: 2026 call ran Dec 25 2025 – Apr 30 2026 (closed). **Expect 2027 call ~late Dec 2026.**
- Source: [biscuitgallery.com/gridnext-2026](https://biscuitgallery.com/gridnext-2026/) · [about](https://biscuitgallery.com/about/)
- Confidence: **direct**.

**3. Kaikai Kiki Gallery / Hidari Zingaro** — Nakano Broadway
- Why it fits: their current show **"Artists Met on SNS" (Aug 14–Sep 13, 2026)** is 12 artists scouted via Instagram, with gallery text saying artists discovered on Instagram have joined the roster. For a 26k-follower daily-diary account this is the one blue-chip-adjacent door that is openly Instagram-driven. Fit is on the Zingaro side (illustration/kawaii → contemporary), not the main gallery. GEISAI (the old open call) last ran April 2023 — do not cite it as live.
- Source: [gallery-kaikaikiki.com](https://gallery-kaikaikiki.com/) · [zingarokk.com/news](https://zingarokk.com/news/) · [geisai.net](https://www.geisai.net/)
- Confidence: SNS scouting **direct**; any route for her **inferred**.

**4. Tokyo Gallery + BTAP (東京画廊+BTAP)** — Ginza + Beijing 798
- Why it fits: the one genuine China–Japan crossover gallery (BTAP since 2002, "young promising Asian artists"). Roster includes Chinese ink/watercolor-on-paper painters Tian Wei, Wu Qiang, Zhu Jianzhong. **Caveat:** those are mid/senior figures and the 2026 program is historical (Sui Jianguo, Sekine). Strong on identity, weak on career level — a 3–5 year target, not a cold-approach now.
- Source: [tokyo-gallery.com/en/artists](https://www.tokyo-gallery.com/en/artists)
- Confidence: **inferred**.

**5. GALLERY MoMo** — Ryogoku + Roppongi Projects
- Why it fits: since 2003, "primarily introduces young artists"; recurring young-painter showcase "New-laid eggs" (invitation, not open call). Figurative young painters — plausible.
- Source: [gallery-momo.com](https://www.gallery-momo.com/) · [newlaideggs3](https://www.gallery-momo.com/newlaideggs3)
- Confidence: **inferred**; no intake path found.

**Evidence that Chinese artists in Tokyo do get picked up:** Yutaka Kikutake Gallery represents **Yang Bo** (Chinese, TOKAS-Emerging 2026). Program is conceptual/media so she'd be an outlier there — cite as proof-of-pattern, not as a target. [yutakakikutakegallery.com/artists](https://www.yutakakikutakegallery.com/artists/) — **inferred**.

**Thematic-analogue note for copy:** KOTARO NUKAGA represents **Keita Morimoto** (nocturnal Tokyo street painter) — the closest artist to her subject in any Tokyo blue-chip roster. No intake route; note only. [kotaronukaga.com/en/artist](https://kotaronukaga.com/en/artist/)

### Illustration-side juried routes to a free solo (matches her actual roots)

**HB Gallery (HBギャラリー)** — Omotesando. **HB FILE COMPETITION vol.37 is open now.** Vol.36 terms: no eligibility restriction, ¥7,000, 15–20 works, judged by five art directors, **5 grand-prize winners each get a one-week solo at HB Gallery**. Vol.36 closed Oct 17, 2025 → vol.37 likely mid-October 2026; read the PDF now. [hbgallery.com/compe.html](https://hbgallery.com/compe.html) · [entry form](https://ws.formzu.net/dist/S20484972/) — **direct**.

**Pinpoint Gallery** picture-book competition — only relevant if she makes a picture book. [pinpointgallery.com](https://pinpointgallery.com/) — **direct**, low fit.

### General finding on how Tokyo galleries take artists
Consistent across Japanese-language sources: Tokyo commercial galleries do not run portfolio drop-boxes. The standard path is visit as a viewer → meet the gallerist at openings → get introduced. Tokyo portfolio reviews in 2026 are photography-only (IMA, KYOTOGRAPHIE). The action text should say this rather than "build relationships."

---

## 2. `solo_venue_quality` — venues that are a clear step up and reachable without a gallery

(Remember: this lever is currently gated off — see §0.1.)

**1. TOKAS-Emerging (Tokyo Arts and Space Hongo)**
- Why it fits: Tokyo Metropolitan institution; free venue + **¥150,000 production grant** + install/transport/PR/catalogue; 4–6 solo shows per cycle. Eligibility: **resident in Japan, age ≤35, nationality not restricted** — two of the 2026 picks (Yang Bo, Yuan Shuohan) are Chinese. 186 applied for 6 slots in 2026.
- Window: 2027 cycle closed Jul 31, 2026. **Next call Jun–Jul 2027** (for 2028). Caveat: TOKAS Hongo has facility maintenance and OPEN SITE recruitment is shifted "from FY2027"; confirm Emerging 2028 is unaffected when the call opens.
- Source: [2027 guidelines](https://www.tokyoartsandspace.jp/archive/application/2026/20260616-331.html) · [2026 exhibition](https://www.tokyoartsandspace.jp/en/archive/exhibition/2026/20260404-7535.html)
- Confidence: **direct**.

**2. TOKAS OPEN SITE**
- Why it fits: same institution, no age limit, solo proposals allowed, exhibition grant **¥400,000**. Very competitive (~570 proposals for 8 slots).
- Window: OPEN SITE 11 closed Mar 17, 2026. **Next call Feb–Mar 2027**, subject to the maintenance note.
- Source: [tokyoartsandspace.jp/application/schedule.html](https://www.tokyoartsandspace.jp/application/schedule.html)
- Confidence: **direct**.

**3. Art Center NEW, Yokohama — "NEW New Artists" (<35)**
- Why it fits: run by Ongoing (Ozawa Nobuo), co-hosted by Yokohama City; free to apply; 2 Grand Prix → gallery exhibition + ¥200,000 fee + up to ¥200,000 costs. The de-facto successor to BankART Under 35. Japanese communication required (she has N2).
- Window: 2026 closed Jul 15. **Next ~Jun 2027.**
- Source: [artcenter-new.jp/event/newnewbackbone2026](https://artcenter-new.jp/event/newnewbackbone2026/)
- Confidence: **direct**.

**4. Spiral Atrium / Spiral Garden via SICF Grand Prix** — see §4. The single highest-profile Aoyama solo reachable by an unrepresented artist; only via SICF. **direct**.

**5. Kyoto Art Center Co-program, Category B (exhibition)**
- Why it fits: institutional Kyoto venue; Gallery North/South free, **up to ¥1,000,000 production**, 6 weeks' studio, documentation. Best-funded open call found. Not Tokyo.
- Window: last call Oct 17 – Nov 15, 2025 (covered summer 2026 and 2027). **Expect next call Oct–Nov 2026** — check [kac.or.jp/open_call](https://www.kac.or.jp/open_call/) in October.
- Source: [kac.or.jp/news/20251016](https://www.kac.or.jp/news/20251016/)
- Confidence: structure **direct**; 2027 timing **inferred**.

**6. Shibuya Hikarie 8/CUBE**
- Why it fits: paid rental but **committee-screened**, 107 m², station-direct footfall — visibly above a Harajuku rental, and the screening gives it standing. Fee not extracted (rate-table PDF).
- Window: **call for Apr 2027–Mar 2028 use planned for autumn 2026** (last cycle closed Oct 31, 2025). Timely.
- Source: [hikarie8.com/cube](https://www.hikarie8.com/cube/)
- Confidence: model/window **direct**; fee **unverified**.

**7. Tokyo Metropolitan Art Museum 都美セレクション グループ展** — museum gallery, open call, **groups of 3+ only**; 2027 deadline was May 9, 2026; next ~spring 2027. A museum CV line if she forms a group. [tobikan.jp](https://www.tobikan.jp/information/20250220_1.html) — **direct**.

**Checked and not viable — do not surface:** BankART Station/KAIKO (closed Mar 2025); 3331 (closed 2023; replacement "ちよだアートスクエア" status unverified); Art Center Ongoing (2026 call is student-only "mirai" — she IS a student, so this one may actually apply: verify); Roppongi Art Night (painting ineligible); Ueno Artist Project (selected from 公募団体 members, route = JWS membership, not application); OIL by 美術手帖, Park Hotel Artist Room, Ginza Tsutaya ATRIUM, department-store galleries — curated/gallery-fed, no open route found.

---

## 3. `residency`

Assumed: Chinese national, Tokyo resident, currently a student. Several programs bar students at residency time (not application time) — flagged.

**1. TOKAS Local Emerging Creator Residency (国内若手クリエーター滞在プログラム)**
- Why it fits: 60–90 days at TOKAS Residency (Sumida), production fee + living expenses + domestic travel; visual art, architecture, design named. **"日本国内在住（国籍不問）"** — Japan-resident, nationality unrestricted; 3+ years activity; no age limit; student status not mentioned in the 2026 guidelines (verify in 2027's). Her exact profile.
- Window: 2026 call ran Sept 17 – Nov 3, 2025. **2027 call expected to open mid-September 2026 — i.e. within two weeks of this report.** Watch [tokyoartsandspace.jp/application](https://www.tokyoartsandspace.jp/application/index.html).
- Source: [2026 guidelines](https://www.tokyoartsandspace.jp/archive/application/2025/20250912-312.html)
- Confidence: terms **direct**; 2027 window **inferred**.

**2. TOKAS Exchange Residency — outbound (二都市間交流事業／派遣)**
- Why it fits: ~3 months abroad, fully funded (airfare, production, living, housing, studio). 2026 destinations, 1 slot each: **Taipei (Treasure Hill), Seoul (SeMA Nanji), Helsinki (HIAP)**, Basel, Berlin, Brussels, Dublin, Montreal. Japan-resident with 住民登録, nationality unrestricted. This is the realistic path to HIAP/Taipei/Seoul — all of which otherwise require applying via a partner.
- Window: same as #1; **2027 call expected mid-Sept 2026.**
- Source: [2026 guidelines](https://www.tokyoartsandspace.jp/archive/application/2025/20250912-313.html)
- Confidence: terms **direct**; window **inferred**.

**3. Fukuoka Asian Art Museum (FAAM) Residency**
- Why it fits: FAAM's whole mission is Asian contemporary art; a China–Japan practice with Chinese museum credits is its audience. ~70–90 days, museum-hosted with exhibition. **"応募する者の居住地および国籍は問いません"**; 2025 guidelines had a domestic slot "日本在住者で国籍は問わない". Strongest institutional credential on this list.
- Window: 2026 cycle closed Jan 25, 2026. **Expect late Dec 2026 – late Jan 2027.**
- Source: [faam.city.fukuoka.lg.jp/residence/requirement](https://faam.city.fukuoka.lg.jp/residence/requirement/)
- Confidence: eligibility **direct**; next window **inferred**; stipend amounts **unverified**.

**4. Swatch Art Peace Hotel — Shanghai**
- Why it fits: she had a Shanghai solo in 2025 and a Chinese exhibition network; a Bund studio is a natural base to re-enter it. 3–6 months, apartment + studio, one round-trip flight, **no stipend**. All nationalities, painting included, student status not a stated barrier.
- Window: **rolling, no deadline**; CHF 30 fee; 12+ weeks review.
- Source: [swatch-art-peace-hotel.com/en/apply](https://www.swatch-art-peace-hotel.com/en/apply)
- Confidence: **direct**.

**5. A4 Residency Art Center — Chengdu (International Residency Fellowship)**
- Why it fits: fully funded ≥8 weeks, studio + accommodation, airfare, **RMB 10,000 production budget**, presentation. Museum-attached AIR in China she hasn't exhibited in; application in English and Chinese.
- Window: **2028 full-year recruitment deadline Dec 31, 2026** (2027 sessions closed June 30).
- Source: [a4artmuseum.com … latest-recruitment](https://www.a4artmuseum.com/en/a4-residencyartcenter/residing/latest-recruitment/)
- Confidence: **direct**.

**6. Kamiyama Artist in Residence (KAIR) — Tokushima**
- Why it fits: one of the few funded Japanese AIRs that names **painting, drawing** first. 2026: 69 days, ¥200,000 stipend + ¥250,000 materials + travel, ends in exhibition. English required; Japan-based applicants accepted. Rural — frame as a memory/absence body rather than cityscape.
- Window: 2026 call Jan 8 – Feb 27, 2026. **Expect Jan–Feb 2027.**
- Source: [air-j.info/en/program/kamiyama2026air](https://air-j.info/en/program/kamiyama2026air/) · [guidelines PDF](https://www.in-kamiyama.jp/images/sites/2/2026/01/KAIR2026_Application-GuidelinesProcedure_Payment-Instructions.pdf)
- Confidence: 2026 terms **direct**; 2027 **inferred**.

**Self-funded, open now (to break the "never done one" barrier cheaply):** Sapporo Tenjinyama Art Studio (¥430–860/day, rolling) [tenjinyamastudio.jp](https://tenjinyamastudio.jp/en/apartment/); Inside-Out Art Museum Beijing (RMB 3,000/month, rolling) [ioam.org.cn](https://www.ioam.org.cn/en/residency/); Vermont Studio Center (**deadline Sept 30, 2026**, partial fellowships for all) [vermontstudiocenter.org/apply](https://vermontstudiocenter.org/apply). All **direct**.

**Ruled out (so nobody re-researches):** TOKAS International Creator (must live outside Japan); TOKAS Research Residency (bars students, no studio); ARCUS (outside-Japan only, no students); AIR Taipei direct (students ineligible unless MA/PhD — go via TOKAS Exchange); Institut français × Cité (Kansai residents only); Cité main program (partner-only, no Tokyo partner found); Akiyoshidai AIAV (needs existing grant/recommendation); Kyoto Art Center AIR (visual arts even years only; next 2028); Pola overseas (Japanese nationality/PR); **Youkobo (residency discontinued)**; **Awagami (explicitly excludes non-Japanese living in Japan; page 404s)**.

---

## 4. `art_fairs` — how an unrepresented artist actually gets in

**Confirmed gallery-only (the current lever text is right about these):** Art Fair Tokyo (Galleries, Crossing = non-commercial orgs, new Projects section = galleries presenting emerging artists — all gallery-applied) [artfair.tokyo guideline](https://artfair.tokyo/gallery/applicants/guideline?fair_id=27); Tokyo Gendai (US$250 gallery application) [tokyogendai.com/apply](https://tokyogendai.com/apply/); ACK, Art Osaka, AFA Fukuoka, ART TAIPEI (individuals explicitly excluded), Art Central HK. All **direct**. Affordable Art Fair HK/SG young-talent sections are local-artist only — she does not qualify. No fair called "Tokyo Independent", "Art Fair Tokyo Future Artists", "Shibuya Art Fair" or "ART in PARK HOTEL TOKYO" exists in 2026.

**The artist-direct ladder that does exist:**

**1. SICF (Spiral Independent Creators Festival)** — Spiral, Aoyama
- Why it fits: artist-direct, juried, no age/nationality limit. EXHIBITION booth ¥48,400 / MARKET ¥55,000 (3 days). **Grand Prix = solo show in Spiral's Atrium + ¥500,000 production budget**; runner-up = winners' group show. Serves both the fair goal and the solo-venue goal at once. A new SICF Fukuoka also exists (Sept 2026).
- Window: SICF27 ran Nov 10, 2025 – Feb 5, 2026 (fair May 2026). **SICF28 call expected ~Nov 2026, deadline ~early Feb 2027.**
- Source: [spiral.co.jp/artcat/sicf](https://www.spiral.co.jp/artcat/sicf) · [SICF27 call](https://www.spiral.co.jp/topics/call-for-artists-for-sicf27)
- Confidence: **direct**.

**2. Independent Tokyo (tagboat)** — Takeshiba
- Why it fits: ~400 artists / 388 booths, screened by organiser; **20–30 gallerist judges on the floor** (Koyama Tomio listed); prizes include a free-booth Taipei group show and possible tagboat representation. Low selectivity, but it's the recognised 登竜門 and the one place gallerists are contractually there to look.
- Window: 2026 call Oct 6, 2025 – Jan/Mar 2026. **2027 call expected ~Oct 2026.** Fee historically ¥45k–89k by panel count (told on acceptance).
- Source: [tagboat.com/artevent/independenttokyo2026](https://www.tagboat.com/artevent/independenttokyo2026/index.php)
- Confidence: **direct** (fee **inferred**).

**3. Art Fair Beppu Spring (HAPS × Art Fair Beppu)**
- Why it fits: artist-direct, **curated by HAPS (serious Kyoto org), free entry, 30% commission, travel/transport/accommodation subsidised**; open to anyone 18+ based in East/SE/South Asia. Strongest fit-per-yen found; must be present.
- Window: Spring 2027 call closed Aug 21, 2026. **Next call likely Jul–Aug 2027.**
- Source: [haps-kyoto.com/art-fair-beppu-spring-2027](https://haps-kyoto.com/art-fair-beppu-spring-2027/)
- Confidence: **direct**.

**4. UNKNOWN ASIA (Osaka)** — artist-direct, 150+ industry "reviewers" award prizes at a VIP preview. Booth ¥99,000–132,000 single. 2026 closed Aug 16; **2027 call ~Jul 2027**. [unknownasia.net](https://unknownasia.net/artist/artist_entry.php) — **direct** (commission **unverified**).

**5. ARTISTS' FAIR KYOTO** — the most prestigious artist-direct fair in Japan (museum venue, ~40 artists), **but the public call requires Kyoto Prefecture residence and age 18–39** per the prefecture's FAQ. Only route = recommendation from an advisory-board artist. Do not surface as an open call. [artists-fair.kyoto](https://artists-fair.kyoto/) · [Kyoto Pref 2025 公募](https://www.pref.kyoto.jp/bungei/artistsfair/news/afk2025_artist_public_offering.html) — dates **direct**, residency rule **medium-high**.

**Tokyo Art Book Fair** (Jan 2027 edition, applications closed Jun 7, 2026; next call ~spring 2027) — right venue for her paper/zine side; she may already do it. [tokyoartbookfair.com](https://tokyoartbookfair.com/en/about/) — **direct**.

**Suggested rewrite of the action:** "Fair access for an unrepresented artist runs through the juried artist-direct fairs — SICF (Nov call), Independent Tokyo (Oct call), Art Fair Beppu (summer call) — where gallerists scout; Art Fair Tokyo and Tokyo Gendai follow representation."

---

## 5. `grant` — what a Chinese national resident in Tokyo can actually apply for

**Filter that decides everything:** Pola, Yoshino Gypsum, and (unverified but historically) 文化庁 overseas-study grants require 日本国籍 or 永住. Kuma Foundation is ≤25 (she's 26). Pollock-Krasner excludes students and wants 10 shows in 10 years (she's close — revisit when not enrolled). Gottlieb needs 20 years.

**1. アーツカウンシル東京 スタートアップ助成 (Arts Council Tokyo Startup Grant) — Round 2 OPEN NOW**
- Why it fits: up to **¥300,000** for an individual's public activity in Tokyo (exhibition) or an international activity. Eligibility is **residence in Tokyo, no nationality clause**, and "新進" = <3 years since first self-organised Tokyo activity or ≤5 such activities — her 2026 solos put her squarely inside. Funds exactly what she already does and starts her grant record.
- Window: **2026-08-25 → 2026-09-24 18:00.** Three rounds/year.
- Source: [artscouncil-tokyo.jp/grants/startup-grant-program](https://www.artscouncil-tokyo.jp/grants/startup-grant-program/) · [Round 1 rules](https://www.artscouncil-tokyo.jp/grants/startup-grant-program/26679/)
- Confidence: **direct**.

**2. Elizabeth Greenshields Foundation Grant (Canada)**
- Why it fits: built for exactly her — age 18–41, early-stage/student or emerging, **representational painting/drawing**, **no geographic, citizenship or residency requirement**, students explicitly eligible. First grant ~CAD 17,000 (secondary sources; older pages say 15k). Rolling; online form then **mailed** to Montreal.
- Source: [elizabethgreenshieldsfoundation.org](https://www.elizabethgreenshieldsfoundation.org/) (403'd to fetcher; verified via [printscholars](https://printscholars.org/elizabeth-greenshields-foundation-grants/))
- Confidence: rules **direct** (secondary); amounts **inferred**.

**3. 野村財団 芸術文化助成 美術部門 個人 (Nomura Foundation)**
- Why it fits: up to **¥1,000,000** per project for 若手芸術家の育成 or 芸術文化の国際交流; an individual's own solo/art event is explicitly eligible; **no nationality, residency, age or career clause stated**. A China–Japan exchange show is a textbook 国際交流 project. Overseas variant needs a host invitation.
- Window: **2027年度上期: 2026-10-01 → 2026-10-30 17:00** (activities Apr–Sep 2027).
- Source: [国内](https://www.nomurafoundation.or.jp/culture/art_ov01.html) · [海外](https://www.nomurafoundation.or.jp/culture/cu_koubo/art_ov02.html)
- Confidence: **direct**.

**4. 朝日新聞文化財団 芸術活動助成金 (Asahi Shimbun Foundation) — OPEN NOW**
- Why it fits: ¥数十万–1,000,000 for a non-profit exhibition; **individuals eligible**, needs Japanese address/bank, no nationality clause. Favours organised shows over commercial-gallery solos — pitch a self-organised or artist-run-space show.
- Window: **2026-07-01 → 2026-10-25** (activities FY2027).
- Source: [asahizaidan.or.jp/grant/grant01.html](https://www.asahizaidan.or.jp/grant/grant01.html)
- Confidence: **direct** (individual-applicant nuance from HTML summary; PDF wouldn't parse).

**5. ホルベイン・スカラシップ (Holbein Scholarship)**
- Why it fits: ¥300,000 of Holbein materials over a year for up to 7 artists; age 18–45, **residence in Japan, no nationality clause**, works in colour media. Holbein is a watercolor manufacturer — near-perfect medium match and a recognised CV line.
- Window: Round 39 closed Jul 31, 2026. **Expect Round 40 April–July 2027.**
- Source: [holbein.co.jp/scholarship.html](https://www.holbein.co.jp/scholarship.html)
- Confidence: rules **direct**; timing **inferred**.

**6. Asian Cultural Council (ACC) Individual Fellowship**
- Why it fits: 1–6 month exchange fellowship, up to US$35,000. Open to citizens or PRs of eligible countries — **China (Mainland) and Japan both listed** — so she qualifies **by Chinese citizenship** regardless of living in Tokyo; a Mainland applicant may submit in Chinese. Needs ≥21 and **5 years of professional experience** — borderline (first shows 2021); no coursework during fellowship. Already named in her Tier 4 list — this is the eligibility detail that makes it real.
- Window: **2026-10-01 → 2026-11-10**; references Nov 16.
- Source: [asianculturalcouncil.org/grant-opportunities](https://www.asianculturalcouncil.org/grant-opportunities)
- Confidence: rules **direct**; citizenship-vs-residence handling **inferred** — confirm with ACC.

**Secondary:** アイスタイル芸術文化財団 (≤¥1M, individuals ≥2 yrs, no nationality clause; expect Dec 2026–Jan 2027) [istyle-found.org](https://istyle-found.org/support/art2026/); 小笠原敏晶記念財団 travel grant (≤¥500k, **open Sept 1 – Oct 15, 2026**, only with a residency/symposium invitation) [ogasawarazaidan.or.jp](https://ogasawarazaidan.or.jp/artculture/travel/); Hopper Prize (worldwide, $40 fee, **Nov 17, 2026**) [hopperprize.org](https://hopperprize.org/); 国家艺术基金 青年艺术创作人才 (needs mainland hukou — she has it — but assumes a domestic work-unit; next ~Apr–Jun 2027) [cnaf.cn](https://www.cnaf.cn/guide_detail/4482.html); Tokyo Artist Accelerator Program (needs 3–10 yrs in Tokyo + N1 — **not yet**) [artscouncil-tokyo.jp](https://www.artscouncil-tokyo.jp/en/news/22469/). All **direct**.

---

## 6. `critical_press`

**Honest verdict:** the named-critic route (Maerkle/ART iT dormant since 2023; Darryl Wee now in tech; Emily Wakeling in Australia; TAB's 2026 reviewers are museum/biennale level) is not where her first writeup comes from. It comes from illustration-adjacent international sites with open submissions, Tokyo English lifestyle press that already covers foreign-born painters' Tokyo debuts, and the Japanese illustration industry's own magazine.

**1. Colossal (thisiscolossal.com)**
- Why it fits: their watercolor tag is active and runs precisely her kind of work — "Felicia Chiao's Domestic Scenes Reflect the Emotional Structures of Daily Life" (Jul 24, 2026), "kelogsloops" (Sep 1, 2026). A 6-year daily watercolor diary of Tokyo interiors is a Colossal-shaped story, and a Colossal feature is what Japanese/Chinese outlets cite later.
- Pitch: **submissions@thisiscolossal.com** — short description + hi-res images/link; pitch the body of work, not the show (they won't run exhibitions without individual images).
- Source: [submissions](https://www.thisiscolossal.com/submissions/) · [watercolor tag](https://www.thisiscolossal.com/tags/watercolor/)
- Confidence: **direct**.

**2. Tokyo Weekender — Eugenie Shin**
- Why it fits: bylines the monthly "Best Art Exhibitions in Tokyo" (mixes commercial galleries with museums, notes watercolor) and TW ran a Chinese painter's *first solo exhibition in Japan* in Harajuku (Zigsen Liu) and a Rwandan painter's Tokyo debut — "foreign-born painter's first Tokyo solo" is a story shape they already publish. Story-driven, not theory-driven.
- Pitch: editorial email on the contact page (obfuscated to the fetcher; open in browser). Pitch 3–4 weeks before the next solo.
- Source: [Sept 2026 list](https://www.tokyoweekender.com/art_and_culture/best-art-exhibitions-in-tokyo-september-2026/) · [contact](https://www.tokyoweekender.com/contact-us/)
- Confidence: coverage **direct**; address **exists but unread**.

**3. Time Out Tokyo — 吉岡ちかる (Chikaru Yoshioka)**
- Why it fits: writes the monthly "東京、◯月に行くべき**無料の**アート展10選" — free shows = gallery shows, exactly where an unrepresented solo can land; profile says she values artists' backgrounds.
- Pitch: **unverified** — no press address found before budget ran out.
- Source: [timeout.com/profile/chikaru-yoshioka](https://www.timeout.com/profile/chikaru-yoshioka)
- Confidence: coverage **direct**; path **unverified**.

**4. イラストレーション magazine (Genkosha) — The Choice (ザ・チョイス)**
- Why it fits: the Japanese illustration industry's magazine of record; quarterly juried competition since 1979, one guest judge per round, ~190 entrants/700 works, watercolor explicitly among accepted media; selected works printed, winners interviewed. A Choice selection is a CV line Japanese galleries recognise, and it's the one Japanese print outlet where watercolor is normal. Matches her actual roots.
- Source: [illustration-mag.jp/choice](https://illustration-mag.jp/choice) (403'd to fetcher — read 応募要項 in browser)
- Confidence: active + accepts watercolor **direct**; fee/format **unverified**.

**5. Tokyo Art Beat — listing, not review**
- Path (**direct**): event@tokyoartbeat.com, subject "◯月◯日, venue, イベント掲載依頼", ≥2 weeks before opening, JP overview + vertical JPGs. **Approval is near-certain only if the venue is already on TAB** — check before booking a solo; new venues go to venue-pr@tokyoartbeat.com. Editorial reviews in 2026 are museum-level; the only emerging-scale review was 北出栞 (Feb 2026).
- Source: [tokyoartbeat.com/FAQ](https://www.tokyoartbeat.com/FAQ)

**6. ARTnews JAPAN** — press-release address on [contact page](https://artnewsjapan.com/contact) (obfuscated). Proof of fit: their "30 young artists" piece included 川内理香子, "紙に鉛筆と水彩絵具で描いたシンプルなドローイング." Realistic use = press-release pickup for a well-produced show. Path **direct**; coverage **inferred**.

**7. 美術手帖 web** — [contact form](https://bijutsutecho.com/contact) → "情報のご提供"; listing realistic, editorial long shot. **direct** path, **low** likelihood.

**8. Chinese-language:** 艺术新闻／中文版 TANC (theartjournal@modernmedia.com.cn — active Sept 2026, though ownership churn; verify who answers) [theartjournal.cn](https://theartjournal.cn) — path **direct**; Hi艺术 (info@hiart.cn / 展讯 zhanxun@126.com from snippets; site refused connection) — **inferred**. Pitch as 海外华人青年艺术家 with the Shanghai solo and museum group shows. ARTFORUM 中文网 has no Japan coverage and no submission route; Randian dormant since 2022.

**9. Other international with open submissions (all direct):** It's Nice That (submit@itsnicethat.com; "Ones to Watch" is <12 months pro — she's past it); Creative Boom ([/submit/](https://www.creativeboom.com/submit/)); Hi-Fructose (info@hifructose.com, subject "Submissions" — pop-surrealist, medium fit); Booooooom (paid membership; runs a Book Award — "Colour Diary"-shaped).

**アートコレクターズ** (the young-painter/完売作家 issues) is gallery-fed — realistic only once a gallery is selling her. Note as a *consequence* of representation, not a press target now.

---

## 7. What I'd recommend NOT including

- **Any named critic from the original brief as a pitch target.** They are dormant (Maerkle/ART iT), relocated (Wakeling), out of the field (Wee), or museum-tier (TAB's 2026 reviewers). Naming them would be the exact false-confidence failure we're fixing.
- **Nanzuka, KOTARO NUKAGA, Tomio Koyama, MISAKO & ROSEN, ANOMALY, Yumiko Chiba, Takuro Someya, WAITINGROOM, Tokyo International Gallery** as representation targets. Either no intake route exists, or the program is market-tier/conceptual and she'd be an outlier, or (the last five) I simply couldn't verify the roster before the search budget ran out. Fine to mention Morimoto at NUKAGA as a thematic analogue in prose; not as a door.
- **Whitestone.** Its "YOUTH" open call was Seoul-only, Korea-based, 2024, non-recurring. Do not surface as an open call.
- **ARTISTS' FAIR KYOTO as an open call.** Kyoto-resident rule.
- **GEISAI** (last held April 2023), **BankART Under 35 / BankART Station** (closed 2025), **3331** (closed 2023), **Youkobo residency** (discontinued), **Awagami** (excludes foreigners living in Japan), **Shiseido art egg** (2026 suspended, no 2027 announced), **Terrada Art Award** (no 2026 edition posted — watch list only).
- **Pola / Yoshino Gypsum / 文化庁 overseas study grants** — she is not eligible on a student visa. Listing them would send her down a dead application.
- **Pollock-Krasner** until she's not a student; **Gottlieb** for ~15 years.
- **Casa Brutus / Pen / Brutus / &Premium / Ginza / MOE** — no evidence of small-gallery watercolor coverage and no pitch path checked. Generic to name.
- **Department-store galleries (Isetan, Mitsukoshi, Seibu), Ginza Tsutaya ATRIUM, OIL by 美術手帖, Park Hotel Artist Room** as solo targets — all curated/gallery-fed with no application route found.
- **The phrase "portfolio review"** — Tokyo's 2026 portfolio reviews are photography-only.

**Search-budget caveats:** all five passes ran out of web-search quota near the end. Specifically unverified and worth a second look before naming: Time Out Tokyo press address; Hi艺术 addresses; 8/CUBE fee table; FAAM stipend amounts; Shanghai fairs (ART021/West Bund — assumed gallery-only); Art Center Ongoing's student-only "mirai" call (she IS a student — it may fit); the 文化庁 nationality clause (PDF unretrievable); whether ちよだアートスクエア has opened.

---

## 8. Suggested data shape (for Scott, optional)

Saffron renders `gap`, `detail`, `action` via `locF()` in `SaffronPage.jsx` (line 1503: `_zh` and `_ja` siblings, else raw). Named targets could go in a new `targets: [{name, why, url, window, confidence}]` list per lever so the page can render them as links without stuffing URLs into `action` prose, and so `test_career_graduated_ladder.py::test_every_graduated_lever_is_localized` keeps passing (it only checks `gap_zh`/`detail_zh`/`action_zh`). Anything with a real deadline (Arts Council Tokyo Sept 24; TOKAS mid-Sept; HB mid-Oct; Nomura Oct 30; Asahi Oct 25; ACC Nov 10) is a candidate for Today's Focus, not just the Saffron career page.
