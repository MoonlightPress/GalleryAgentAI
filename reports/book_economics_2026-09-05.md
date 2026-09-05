# Self-Published Art Book — Real Economics

**Prepared 2026-09-05 for GEGYjiji (Nin), Tokyo.**
Research only. No advice, no strategy — figures and their sources.

**Spec priced throughout:** A4 (210×297mm) or square (~210×210mm), **128 pages** (100–150 band), full colour throughout, **hardcover / 上製本**, coated art paper (157gsm class). Where a source priced a different spec, the actual spec is stated.

**FX used throughout:** **USD 1 = ¥156.25**, **CNY 1 = ¥23.28**, USD 1 = CNY 6.71.
Source: [frankfurter.dev ECB feed, 2026-09-04](https://api.frankfurter.dev/v1/latest?from=USD&to=JPY,CNY,EUR). Cross-checked against [Google Finance USD-JPY](https://www.google.com/finance/quote/USD-JPY) = 156.265 (2026-09-05 00:25 UTC). Agreement within 0.02%. **DIRECT.**

**Confidence tags:** **DIRECT** = read off a price page or official table · **INFERRED** = derived, interpolated or converted (method stated) · **UNVERIFIED** = could not confirm · **ANECDOTE** = single self-report, n=1, source named.

---

## 1. THE CENTREPIECE — Cost per unit and total, by run size and printing origin

### 1.1 Headline table

All figures **per copy in JPY**, for a **128pp full-colour hardcover**. Totals in brackets.

| Route | 100 copies | 300 copies | 500 copies |
|---|---|---|---|
| **China — EXW factory** (excl. freight/tax) | **¥2,422** (¥242,200) | **¥956** (¥286,800) | **¥684** (¥342,000) |
| **China — landed Tokyo, all-in** | **¥3,360–4,010** (¥336k–401k) | **¥1,230–1,400** (¥369k–420k) | **¥860–920** (¥430k–460k) |
| **Japan — digital hardcover** (栄光, B5, **96pp max**) | **¥3,204** (¥320,390) | — caps at 200 copies — | — not offered — |
| **Japan — offset sewn hardcover** (緑陽社, **B5**, 128pp body) | **¥16,419** (¥1,641,860) | **¥6,005** (¥1,801,590) | **¥3,927** (¥1,963,510) |
| **Japan — offset sewn hardcover** (緑陽社, **A4**, 128pp body) | **¥24,283** (¥2,428,290) | **¥8,514** (¥2,554,300) | **¥5,386** (¥2,693,120) |
| **POD — Blurb** (18×18cm square, 150pp) | ¥7,706 @ 50+ (25% vol. disc.) · ¥10,275 @ 1 | same unit price, no run commitment | same |
| **POD — Amazon KDP hardcover** (8.25×11in, 150pp, US/EU print) | ¥2,756 print cost, any quantity | same | same |

**The shape of the curve — where scale actually bites:**

- **China: the collapse is between 100 and 300.** Per-copy EXW falls **2.5×** from 100→300, then only **1.4×** from 300→500. That is the offset-vs-digital transition, not a smooth curve. Below ~250 copies she is buying digital economics at any Chinese printer.
- **Freight does not scale at all below 500 copies.** All three runs fit under **1 CBM**, and LCL sea freight bills a **1 CBM minimum**. Ocean cost is therefore effectively *flat* from 100 to 500 copies (~¥47,000–70,000 either way), which is exactly why the 100-copy run lands so badly.
- **Japan splits into two different processes that must not be averaged together.** *Digital* hardcover is cheap at 100 copies but page- and quantity-capped (栄光: 96 body pages, 200 copies max). *Offset sewn* hardcover has no caps and much better paper and binding — but carries ~¥2.36M of fixed plate/setup cost, so at 100 copies **you are paying almost entirely for plates**. 緑陽社 A4: ¥79,245/copy at 30 → ¥24,283 at 100 → ¥8,514 at 300 → ¥5,386 at 500 → **¥3,257 at 1,000**.
- **The China-vs-Japan gap is far wider than a first pass suggests.** Against Japanese *offset* (the like-for-like quality comparison — sewn binding, art paper): China is **~6× cheaper at 500 copies** (¥890 vs ¥5,386 A4) and **~7× at 100**. Against Japanese *digital* at 100 copies it is roughly a wash (¥3,360–4,010 vs ¥3,204) — but the digital route cannot do 128 pages.
- **B5 is ~33% cheaper than A4** at every page count and every tier at 緑陽社. That is the single largest lever available on the Japanese side.
- **POD has no curve at all** — that is its entire proposition (zero upfront) and its entire weakness.

### 1.2 China — the evidence behind those numbers

**QinPrinting (Shanghai) is the only printer found that publishes full quantity ladders.** All EXW Shanghai.

Hardcover photo book, 8.5"×11", 157gsm interior on 2.5mm greyboard — [qinprinting.com/photo-book-printing/](https://www.qinprinting.com/photo-book-printing/) — **DIRECT**

| Pages | 100 | 500 | 1,000 | 2,000 |
|---|---|---|---|---|
| 80pp | $11.27 | $3.17 | $2.33 | $1.96 |
| 112pp | $14.09 | $3.98 | $2.85 | $2.34 |
| 192pp | $21.15 | $6.00 | $4.14 | $3.31 |

Hardcover coffee-table book — the only published table carrying a **300 column** — [qinprinting.com/coffee-table-book-printing/](https://www.qinprinting.com/coffee-table-book-printing/) — **DIRECT**

| Size / pages | 100 | 300 | 500 | 1,000 |
|---|---|---|---|---|
| 8.5"×11", 200pp | $21.94 | $8.69 | $6.22 | $4.28 |
| 8.5"×11", 300pp | $31.18 | $12.31 | $8.88 | $5.97 |
| 11"×11", 200pp | $29.88 | $11.85 | $8.61 | $5.91 |

**Derivation of the 128pp figures:**
- **500 copies = $4.38 — DIRECT.** Published for exactly 128pp on [qinprinting.com/art-book-printing/](https://www.qinprinting.com/art-book-printing/).
- **100 copies = $15.50 — INFERRED.** Linear interpolation between the published 112pp ($14.09) and 192pp ($21.15) rows. *Method validated:* the same interpolation at 500 copies returns $4.38, matching the published 128pp figure exactly.
- **300 copies = $6.12 — INFERRED.** The 300:500 ratio from the coffee-table 200pp row (8.69 ÷ 6.22 = 1.397) applied to $4.38. Cross-check via the 100:500 ratio gives $15.45 — within 0.3% of the interpolated 100-copy figure.

**If she chooses 210×210mm square instead of A4 — roughly a third cheaper. INFERRED, indicative only.**
QinPrinting publishes the same spec at two sizes, giving a scaling law: 93.5 in² at $6.22 vs 121 in² at $8.61 → price ∝ area^1.26. A 210mm square (68.4 in²) is 0.731× the A4 area → **≈0.67× the A4 price**: ~$10.45 / ~$4.13 / ~$2.95 per copy at 100 / 300 / 500 (**¥1,632 / ¥645 / ¥461**). Caveat: this extrapolates *below* the smallest published size and thin-book fixed costs don't scale with area. Custom sizes are confirmed available (W 95–320mm × H 95–420mm, DIRECT), so 210×210 is in range — **but get it quoted.**

**Independent corroboration** (all DIRECT reads):

| Source | Figure |
|---|---|
| [qinprinting.com/blog/art-book-printing-costs/](https://www.qinprinting.com/blog/art-book-printing-costs/) | 100pp hardcover art book **$2.21–$7.57/copy** (volume-weighted); 200pp $3.41–$12.38 |
| [xinyiprint.com](https://xinyiprint.com/how-much-does-it-cost-to-print-books/) | ~120pp full-colour art book: **100 copies $10–25; 500 copies $6.50–16** — brackets the figures above |
| [suntopprint.com](https://www.suntopprint.com/catalogs/book-printing-china) | **128pp full-colour hardcover, 1,000 copies: $4.90–5.80/copy** delivered door-to-door |
| [printninja.com](https://printninja.com/printing-resource-center/printing-options/book-printing-options/) | 6×9 casewrap hardcover 200pp coated: **$4–6/unit at 1,000** |

**Minimum order quantities — lower than commonly assumed:**

| Printer | MOQ | Source |
|---|---|---|
| QinPrinting | **100** | [FAQ](https://www.qinprinting.com/faq/) DIRECT |
| BookPrintingChina | **100** | [bookprintingchina.com](https://www.bookprintingchina.com/) DIRECT |
| SunTop Printing | **100** | [suntopprint.com](https://www.suntopprint.com/catalogs/book-printing-china) DIRECT |
| PrintNinja | **250** | [printninja.com](https://printninja.com/printing-resource-center/printing-options/book-printing-options/) DIRECT |
| ChinaPrinting4U | **500** ("flexible, case-by-case") | [chinaprinting4u.com](https://www.chinaprinting4u.com/hardcover-book-printing) DIRECT |

**Hidden costs — what is and is not bundled:**

| Cost | Finding | Confidence |
|---|---|---|
| **Plate/setup (制版费/开机费)** | **Not itemised by any Western-facing broker** — baked into per-unit price. A direct 1688/Alibaba factory *will* itemise it separately. | DIRECT (verified absence on [FAQ](https://www.qinprinting.com/faq/)) |
| **Proofing (打样费)** | Digital proof free. **Physical hardcover proof $35–$250 + courier.** Foil +$100–180, gilded edges +$180–220, spot UV/emboss +$50 each | DIRECT — [blog/book-printing-costs](https://www.qinprinting.com/blog/book-printing-costs/) |
| **Payment terms** | 50% deposit before printing, balance before shipping. **PayPal adds 5%, paid by customer** | DIRECT — FAQ |
| **Incoterm** | ⚠️ **Nearly all published prices are EXW Shanghai** — freight, insurance and tax excluded. Decisive at 100 copies | DIRECT |
| **Packing** | Double-walled cartons, palletised for larger runs. Included | DIRECT |
| **Cloth/faux-leather cover upgrade** | 100 copies $23.69/unit · 200 $13.22 · 500 $6.73–6.86 | DIRECT |

⚠️ **QinPrinting's own pages contradict each other.** The hardcover page's table is headed "DDP to US" while the same page states "EXW Shanghai. Shipping and duties not included." Their blog attaches $6.21@500 to a 200-page book; the product page attaches it to 100 pages. **Published ladders are indicative, not contractual. Insist on a written quote stating page count, trim, paper and incoterm.**

**Marketplace listings** (made-in-china.com — DIRECT for what the listing says; these are **opening asks**, negotiable, and typically exclude plate/setup and freight):

| Listing | Price | MOQ |
|---|---|---|
| Shenzhen Caimei — "Hard cover art books" | **US$5.10–10.60** | **100** |
| Hangzhou Fengshuo — cloth cover, gilded edges | US$13.80–16.80 | 500 |
| Shenzhen One Net — large art offset hardcover photo book | US$1.99–5.99 | 300 |
| Fujian Juhui — case bound art book | US$0.40–2.00 | 100 |

⚠️ Treat sub-$2 listings as bait pricing anchored on thin children's board books at high volume. The Caimei and Fengshuo listings are the only ones whose spec plausibly matches, and they land in the same $5–17 band as the broker ladders — which is the useful corroboration.

🔴 **GAP — the art-book trade printers publish nothing.** Asia Pacific Offset, Everbest, 1010 Printing, C&C Offset and Regal Printing (HK) are all **quote-only** — no prices, MOQs or lead times anywhere on their sites. Shenzhen **Artron 雅昌** could not be reached (TLS certificate mismatch on artron.com.cn). **This is a market fact, not a research failure** — the art-book trade is a relationship business. For a monograph, Artron and Asia Pacific Offset are the right calls to *place*, but they will never appear in a spreadsheet.

🔴 **GAP — Chinese-language direct-factory pricing could not be obtained.** 1688 and Alibaba trade search returned empty (JS-rendered), Zhihu 403, Baidu/Sogou CAPTCHA. **This is the single largest hole in the report, and it matters most to her specifically:** a Chinese-fluent buyer negotiating direct with a Shenzhen or Shanghai factory should beat the broker prices above by a meaningful margin. The figures above are what an *English-speaking foreigner* pays. Her floor is probably lower — but by how much is **UNVERIFIED**.

### 1.3 China → Tokyo: freight, tax and the 1 CBM problem

**Weight and volume — INFERRED, calculated from gsm × sheet area; no published weight for a comparable hardcover was found (UNVERIFIED).**

| Spec | Per copy | 100 copies | 300 copies | 500 copies |
|---|---|---|---|---|
| A4, 128pp, 157gsm | **~0.90 kg** | ~85 kg / **0.16 CBM** | ~255 kg / **0.47 CBM** | ~425 kg / **0.78 CBM** |
| 210mm square, 128pp | ~0.55–0.65 kg | — | — | — |

**All three runs are under 1 CBM.** Density ~545 kg/CBM confirms **actual weight bills for air** (courier divisor 5000 = 200 kg/CBM) and **volume bills for sea**.

**Rates** (⚠️ China→Japan sources are programmatic-SEO logistics sites — DIRECT reads of published pages, but weak market evidence):

| Mode | Rate | Source |
|---|---|---|
| Express courier | $5.50–12.00/kg | [tonlexing.com](https://www.tonlexing.com/air-freight-from-china-to-japan/) |
| Consolidated air | $2.00–4.80/kg | same |
| Air DDP (双清包税) | $4.50–8.50/kg | same |
| **LCL ocean** | **$30–70/CBM, 1 CBM minimum** | [topchinalogistics.com](https://topchinalogistics.com/lcl-shipping-china-to-japan-2026-freight-cost-and-time-guide/) |

Printer-published China→US rates, as an upper bound ([qinprinting.com/book-printing-china/](https://www.qinprinting.com/book-printing-china/), DIRECT): sea $1.80–4.80/kg · air $8.80–9.50/kg · courier $10.50–12.50/kg. The same page shows the EXW→DDP delta directly: 500 copies of an 8.5×11 200pp hardcover, **EXW ~$4.30/unit vs DDP-US ~$7.10/unit**.

**Japan-side charges — the highest-confidence shipping numbers here**, from Japanese logistics reference [hunade.com/cfs](https://hunade.com/cfs) (**DIRECT**): **CFS charge ¥5,980 per R/T** · **system charge ¥2,000–12,000/m³** · doc fee ~$20/BL. **Japan-side subtotal on a 1 R/T shipment: ¥11,100–21,100** — and that is *before* THC or customs-broker fee.

A published worked case, Shenzhen→Tokyo, 2 CBM / 400 kg (DIRECT, topchinalogistics, Jul 2026): ocean $140 · origin $95 · **destination $160** · customs/duties $110 · **total $505**. **Destination charges exceed the ocean freight.**

**Freight scenarios — INFERRED, arithmetic on the rates above:**

| Mode | 100 copies (85kg) | 300 copies (255kg) | 500 copies (425kg) |
|---|---|---|---|
| Express courier | $470–1,020 | $1,400–3,060 | $2,338–5,100 |
| Air DDP | $383–723 | $1,148–2,168 | $1,913–3,613 |
| **LCL sea** (1 CBM min) | **$300–450** | **$300–450** | **$300–450** |
| LCL per book | $3.00–4.50 | $1.00–1.50 | **$0.60–0.90** |

**At 100 copies sea has no advantage** — the 1 CBM minimum plus fixed Japan-side charges cost about the same as air DDP while taking 3× longer. **Fly a 100-copy run; ship the 300 and 500.**

**Customs — books enter Japan duty-free. Verified against the live schedule.**

**HS 4901 is Free in every column**, effective 2026-08-08: [customs.go.jp/english/tariff/2026_08_08/data/e_49.htm](https://www.customs.go.jp/english/tariff/2026_08_08/data/e_49.htm) — **DIRECT, authoritative.** Code **4901.99.000 ("Other")** covers her book: General **Free**, Temporary **Free**, WTO **Free**, EPA/RCEP **Free**. Because there is no preferential margin to claim, **she does not need a certificate of origin from the Chinese printer.**

⚠️ **One trap:** shipments valued ≤¥200,000 are normally assessed under the **simplified tariff (簡易税率)**, whose residual category is **5%** — worse than the 0% books enjoy. It should not bite (the simplified tariff excludes duty-free goods, and the importer may opt for the general tariff anyway — [customs.go.jp 1001_e](https://www.customs.go.jp/english/c-answer_e/imtsukan/1001_e.htm), DIRECT), but **tell the forwarder explicitly the goods are HS 4901 and duty-free** so nobody defaults them into the 5% bucket.

**Consumption tax: 10% on CIF. The only tax she pays.** Books do **not** get the 8% reduced rate ([nta.go.jp](https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6303.htm), DIRECT). Base = customs value + duty; customs value is CIF ([customs.go.jp/english/summary/tariff.htm](https://www.customs.go.jp/english/summary/tariff.htm), DIRECT). Since duty is zero:

> **Tax owed = (printing invoice + freight + insurance) × 10%** — roughly **¥20,000 at 100 copies, ¥26,000 at 300, ¥32,000 at 500**.

**The ¥10,000 de minimis cannot help her.** The rule is real ([1006_e](https://www.customs.go.jp/english/c-answer_e/imtsukan/1006_e.htm), DIRECT) and books are not on the exclusion list, but: ¥10,000 is the total for the *shipment*, not per book; fragmented shipments from the same sender to the same recipient are **combined** for the threshold; and she has a real commercial invoice. Deliberate splitting is also a false declaration.

**A broker is convention, not law.** [customs.go.jp/english/summary/import.htm](https://www.customs.go.jp/english/summary/import.htm), DIRECT: *"Import declaration must be made, in principle, by the person who is importing the goods. Usually, a Customs broker files the declaration as a proxy."* The 通関業法 licence requirement governs acting 「他人の依頼によつて」 — at *another person's* request, as a business — not declaring one's own goods.

💡 **Hand-carry is a legitimate route for a 100-copy run** — up to ~¥300,000 as accompanied baggage, Form C-5360, tick "Commercial Goods/Samples" ([7109_e](https://www.customs.go.jp/english/c-answer_e/keitaibetsuso/7109_e.htm), DIRECT). ~85kg is the binding constraint, not the rules, so realistically a partial load.

🔴 **UNVERIFIED:** Japanese THC figures, 通関料 (broker fee) levels, whether an individual needs a NACCS importer code, and DHL/FedEx/EMS/SF Express rate tables for the China→Japan lane. A widely-repeated ¥11,800/declaration broker figure circulates but **could not be confirmed from any source actually read — deliberately not quoted as fact.**

### 1.4 Japan domestic — and a structural finding

🔴 **The cheap, famous Japanese on-demand printers do not offer 上製本 at all.** Verified against each site's own product lineup — **ラクスル, 製本直送.com, プリントパック, ちょ古っ都, しまや出版, ねこのしっぽ, 日光企画, 大陽出版, 西岡総合印刷** offer only 中綴じ / 無線綴じ / くるみ. **グラフィック says so outright:** 「グラフィックでは上製本（ハードカバー）の冊子は取り扱っていません。」 ([graphic.jp FAQ 100017](https://www.graphic.jp/customer/faq/answer/100017), **DIRECT**). **東京カラー印刷**'s 上製本 is **mono body only**. **プリントパック**'s only 上製本 is a フォトアルバム — it *does* offer 180/210/260mm **square**, but caps at **30 body pages**. The brief assumed these were candidates; they are not.

**Second structural finding: full colour + case-bound + 100–150 pages is quote-only territory almost everywhere.** Every public Japanese hardcover table found is capped on one axis — オリンピア at **30 copies**, KANBI LIVRE at **42 pages**, 絵本プレス at **32 pages**, 栄光 at **96 body pages / 200 copies**, 宅配プリント at **80 pages / 100 copies**. **Exactly one printer breaks the pattern.**

### ⭐ 緑陽社 — the only Japanese printer publishing a real price for this spec

[ryokuyou.co.jp オールカラー上製本セット](https://www.ryokuyou.co.jp/doujin/set/allcolorjyousei.html). The table is JavaScript-loaded; figures were pulled from the site's own price JSON ([admin-ajax endpoint, `allcolorjyousei-norm_2610.json`](https://www.ryokuyou.co.jp/wp2/wp-admin/admin-ajax.php?action=ryo_set_price_list_data&file=allcolorjyousei-norm_2610.json), generated 2026-08-12, applies to delivery from 2026-10-01). **DIRECT. 税込, delivery to one address included.**

**Spec:** A4 or B5 · 本文 64–400pp · **offset 4C cover *and* text** · 本文 ハイマッキンレーアート or マット **135kg art paper** · 貼り表紙 + PP · **糸かがり (sewn), ホローバック, 角背** · 見返し色上質特厚口 · 花布 · **30–10,000部**.

| Size / total pages | 100部 | 300部 | 500部 |
|---|---|---|---|
| B5 108P (104pp body) | ¥1,394,840 (**¥13,948**) | ¥1,527,320 (**¥5,091**) | ¥1,661,980 (**¥3,324**) |
| **B5 132P (128pp body)** | ¥1,641,860 (**¥16,419**) | ¥1,801,590 (**¥6,005**) | ¥1,963,510 (**¥3,927**) |
| B5 156P (152pp body) | ¥1,910,380 (**¥19,104**) | ¥2,093,350 (**¥6,978**) | ¥2,277,690 (**¥4,555**) |
| A4 108P (104pp body) | ¥2,089,430 (**¥20,894**) | ¥2,195,330 (**¥7,318**) | ¥2,314,020 (**¥4,628**) |
| **A4 132P (128pp body)** | ¥2,428,290 (**¥24,283**) | ¥2,554,300 (**¥8,514**) | ¥2,693,120 (**¥5,386**) |
| A4 156P (152pp body) | ¥2,887,570 (**¥28,876**) | ¥3,033,720 (**¥10,112**) | ¥3,192,650 (**¥6,385**) |

⚠️ Page counts are **表紙込** — subtract 4 for body pages. **Square is not in the standard set** (カスタムコース quote only). 緑陽社 does **not** offer digital hardcover — 上製本 is offset-only (「デジタルコース未対応」, [/doujin/option/hard.html](https://www.ryokuyou.co.jp/doujin/option/hard.html)). Site notice: **ハイマッキンレーアート 135kg is currently out of stock.** A cheaper table (~10–15% less) applies to delivery by 2026-09-30 (`file=allcolorjyousei-norm.json`).

**The curve is the story.** A4 132P: **¥79,245/copy at 30 → ¥24,283 at 100 → ¥8,514 at 300 → ¥5,386 at 500 → ¥3,257 at 1,000.** Roughly **¥2.36M of fixed offset setup** plus small marginal cost. Below 300 copies, offset is simply the wrong process.

| Printer | Spec | Price | Confidence |
|---|---|---|---|
| **宅配プリント** [takuhaiprint.com/price-hardcover](https://www.takuhaiprint.com/price-hardcover/) | **A4 hardcover, 80pp, colour, 100 copies** | **¥365,390 税別 = ¥3,654/copy** | **DIRECT** |
| same | B5 hardcover, 80pp, colour, 100 | ¥358,880 = ¥3,589/copy | DIRECT |
| same | A5/B6 hardcover, 80pp, colour, 100 | ¥301,370 = ¥3,014/copy | DIRECT |
| same | A5/B6 hardcover, 80pp, colour, **50** | ¥178,080 = ¥3,562/copy | DIRECT |
| **がっぷり!** [gappri.jp](https://www.gappri.jp/hardcover/cont11-1-7-6.php) | 上製本 **binding only** A4/B5 | **¥49,500 base + ¥990/copy**; 450部以上で25%割引 | DIRECT |
| same | 上製本 binding only A5/B6 | ¥36,300 + ¥880/copy | DIRECT |
| **栄光** [eikou.com](https://www.eikou.com/commodity/option/jouseihonoption/) | B5 上製本 **add-on**, 100部 | **¥79,200 = ¥792/copy**; adds **+7営業日** | DIRECT |
| **プリントオン** [print-on.jp](https://www.print-on.jp/doujin/comic/price/hard_cover_new_set.htm) | Square/B5/A5 full-colour hardcover, 100pp | 1冊 ¥26,000 · 10冊 ¥48,000 · 50冊 ¥153,900 (¥3,078/copy) | ⚠️ **CONTESTED — see below** |
| same | Square/B5/A5 full-colour hardcover, 150pp | 1冊 ¥37,500 · 10冊 ¥64,900 · 50冊 ¥215,900 (¥4,318/copy) | ⚠️ **CONTESTED** |
| **冊子印刷工房** [printsassi.com/mc44s210](https://www.printsassi.com/mc44s210) | **210×210 SQUARE**, 128pp full colour, coated — **SOFTCOVER** | ¥217,630 (¥2,176) @100 · ¥482,640 (¥1,609) @300 · ¥739,520 (¥1,479) @500 | **DIRECT** |
| same, 150pp | 210×210 square, softcover | ¥234,130 @100 · ¥518,600 @300 · ¥794,410 @500 | DIRECT |
| 冊子印刷industry [sasshi-insatsu.com](https://www.sasshi-insatsu.com/p_price/) | A4 full-colour **SOFTCOVER** | ¥2,657/copy @100 → **¥1,306/copy @500** | DIRECT |
| **東京印書館** [inshokan.co.jp](https://www.inshokan.co.jp/cost_print/) | Art-book specialist (写真集・図録・作品集) | **Quote only — no public prices** | DIRECT (verified absence) |

**The cheapest credible Japanese hardcover at ~100 copies is 栄光 at ¥3,204/copy** — B5, 96 body pages, full colour, tax **and** delivery included. Independently corroborated by two agents. Its blockers are real, though: **96 body pages max, 200 copies max, and no A4 in the hardcover option table** (A5以下/B5 only).

**オリンピア印刷** publishes the closest full-colour A4 上製本 table anyone posts — 本文 両面カラー コート紙110kg, 税込 **and 全国送料無料** — but it stops at 30 copies: **128P = 1冊 ¥71,855 / 10冊 ¥144,260 / 30冊 ¥263,531 (¥8,784/copy)** ([sasshi-insatsu.com/p_price](https://www.sasshi-insatsu.com/p_price/), section `#a03tca4`, DIRECT). Note it is **無線綴じ上製本 (glued), not sewn.** Extrapolating the falling marginal cost (¥8,344→¥7,806→¥6,642→¥5,285) forward gives **~¥633,000 at 100 copies (~¥6,335/ea) as an INFERRED *upper bound*.** Their spec page says square/変形 is possible by enquiry.

✅ **Gap now closed:** an earlier pass concluded no Japanese printer publishes a 500-copy full-colour hardcover price. **That was wrong — 緑陽社 publishes 30 through 10,000 copies.** The ceiling is not universal.

⚠️ **Sewn vs glued is a quality fork worth more than part of the price gap.** 緑陽社 and がっぷり! are **糸かがり (sewn)**; オリンピア is **無線綴じ (glued)**. For an art book that needs to open flat across a spread, that distinction matters.

⚠️ **The プリントオン figures are contested and should be re-verified before use.** One research pass read the rows above off the page; a second pass got a legacy table/image layout it could not resolve into aligned rows and **declined to report numbers**, and a third read put that product's range at **12P–76P, max 100冊** — which would make the 100pp and 150pp rows impossible. **Do not rely on them without a fresh check.** Every other DIRECT figure in this report was verified by at least one clean read; this one was not.

🔴 **A 210×210 square hardcover at 120pp has no published price anywhere in Japan.** 冊子印刷工房 does square at that page count but **softcover**; KANBI LIVRE does 210×210 hardcover but only to **42 pages**; プリントパック's square photo album caps at **30 body pages**; 緑陽社's square is カスタムコース quote-only. **オリンピア and 三景印刷 (album03.jp, 185×185) will quote square hardcover.** That version of the book is a quote-only object.

**Art-book specialists — all confirmed quote-only by verifying the absence of any price page. ⚠️ Three of the four domains in the original brief were wrong:**

| Printer | Correct domain | Evidence |
|---|---|---|
| 東京印書館 | **inshokan.co.jp** *(not tokyoinshokan.co.jp)* | Only cost page is a 見積もりフォーム |
| 藤原印刷 | **fujiwara-i.com** *(not fujiwara-printing.co.jp)* | Static sitemap: 23 URLs, no price page |
| 山田写真製版所 | **yppnet.co.jp** *(not yamada-photo.com)* | Zero 料金/価格/見積/円 on site |
| イニュニック | inuuniq.co.jp | 4 estimate *request* forms, no calculator |
| 修美社 | **syubisya.co.jp** | Has a 料金表 — but only 名刺/DM/ポスター/パンフレット; books are 「お問い合わせください」 |
| ライブアートブックス | live-art-books.jp | JS portfolio, no price page |
| 三景印刷 | album03.jp | 上製本 specialist, 185×185 square offered — quote only |

**Two further corrections worth carrying forward:** **ちょ古っ都's `/price.html` is not monochrome-only** — it carries a full-colour A4 table (100p/100部 ¥185,580 税込, 送料別) — but they do **not** offer 上製本 and the table caps at 200部. And **K.C.Print's A5 hardcover table** (144P: 100部 ¥244,000 / 300部 ¥317,000 / 500部 ¥385,000 税込) is **mono body**, colour only on the jacket — a useful floor, not a match. **三島印刷's 上製本 table** (128P: 100部 ¥577,500 / 300部 ¥619,500 / 500部 ¥661,500 税込) is verbatim-verified but **specifies neither size nor colour** (「ごくスタンダードな仕様」) and is almost certainly mono — **not a full-colour data point.**

**Useful decomposition:** the **hardcover step alone costs ¥700–1,800/copy** (栄光's B5 上製本 add-on is ¥792/copy at 100, DIRECT). A4 full-colour *softcover* runs ¥2,657/copy at 100 → ¥1,306 at 500. That brackets what the binding is actually buying.

**Print-On is the one Japanese vendor doing square + full colour + hardcover + single copies.** ¥26,000 for one copy is brutal, but it collapses to **¥3,078/copy at 50** — competitive with everything domestic and with no international shipping or customs. Max 100 copies. Lead time 12営業日 from 入稿.

⚠️ **製本直送.com surcharge worth knowing, likely a general Japanese-POD pattern** ([seichoku.com](https://www.seichoku.com/), DIRECT): 「全ページ平均で印刷面積率が50％を超える場合、本文用紙の単価が1.5倍」 — **a full-bleed watercolour book triggers a 1.5× paper surcharge.** Ask every Japanese printer whether they apply one.

### 1.5 POD floor — and two hard blockers

**The spec as written is not printable on the two cheapest platforms.**

| Platform | Can it do the spec? | Print cost, 150pp | Confidence |
|---|---|---|---|
| **Amazon KDP hardcover** | ❌ **No square trim at all.** ❌ **No hardcover in the Japan marketplace** | **¥2,756** (8.25×11in, premium colour, US print) | **DIRECT** |
| **Blurb** | ✅ 18×18cm square (not 210mm) | **¥10,275** @1 · **¥7,706** @50+ (standard paper) · ¥13,898 @1 (premium) | DIRECT tables, INFERRED arithmetic |
| **ラクスル Raksul** | ❌ **No hardcover, at all** | — | DIRECT |
| **製本直送.com** | ❌ **No hardcover, at all** | — | DIRECT |
| **MyBooks.jp** | ⚠️ Hardcover yes, but **B5 max — no A4, no square** | ~¥11,160 delivered @1 (B5 100pp) | DIRECT |
| **がっぷり!** | ✅ A4 hardcover | **Fails the "no upfront" test — ¥60,500+ before a page is printed** | DIRECT |

**The KDP finding is the most important negative in this section.** Hardcover printing costs are published for Amazon.com (USD), .co.uk (GBP), .de/.es/.fr/.it/.nl/.ie/.com.be (EUR), .pl and .se **only** — confirmed on both the English and Japanese versions of the same help page ([kdp.amazon.com hardcover cost](https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H), DIRECT). **Amazon.co.jp / JPY does not appear.** Also: **"Standard color is 'Not available' for hardcover"** — premium colour is compulsory. Page range 75–550, so 128pp is fine.

US hardcover premium colour, DIRECT verbatim: **"$5.65 USD per book" + "$0.080 USD per page"** (large trim). At 150pp = $17.65 = **¥2,756**. Cheapest number in the whole report — but it buys a **non-square, US-printed** book, with international shipping to Tokyo unpriced on top.

**What Japan *can* print on KDP is paperback only** ([kdp.amazon.co.jp](https://kdp.amazon.co.jp/ja_JP/help/topic/G201834340), DIRECT verbatim JPY): プレミアムカラー 「1冊あたり206円」+「1ページあたり5円」 (large trim) → a 150pp premium-colour **paperback** printed in Japan = **¥956**. Astonishingly cheap. Not the spec.

**Blurb volume discounts, DIRECT verbatim:** *"Photo Book 10-19 = 20% · 20-49 = 20% · 50+ = 25%."* Blurb's listed prices **are** the print cost — she orders at that price, there is no separate author-copy scheme.

🔴 **GAPS:** Blurb **shipping to Japan** is calculator-only, could not verify — treat as a material unpriced addition. **Lulu** (403 to fetch, publishes no static rate table), **IngramSpark** (calculator behind login), **BookBaby** (403) — all UNVERIFIED. A secondary blog figure of ~$32.50 for a Lulu 100pp full-colour hardcover circulates but the trim size is unstated; **do not quote it as fact.**

### 1.6 Turnaround — can she hit a deadline?

| Route | File sign-off → books in Tokyo | Confidence |
|---|---|---|
| **China by sea** | **5–8 weeks** | INFERRED |
| **China by air** | **4–6 weeks** | INFERRED |
| **Japan domestic hardcover, first run** | **4–6 weeks from 入稿** | INFERRED |
| Print-On | 12営業日 from 入稿 | DIRECT |
| MyBooks.jp | ≤10 business days | DIRECT |

China hardcover production alone is **2–3 weeks after proof approval** ([qinprinting.com](https://www.qinprinting.com/blog/what-happens-after-you-send-your-files-to-the-printer/), DIRECT), and Shanghai→Tokyo is only **3–7 days port-to-port** versus 11–18 days to the US West Coast.

**The honest answer: Japan domestic is only about 1–3 weeks faster once a proof round is included.** 栄光's 上製本 step alone adds +7営業日, and the published "10 business days" clocks start at **校了 (proof approval), not 入稿**. What China genuinely costs is **flexibility** — a reprint is 5–8 weeks away, not one.

---

## 2. Consignment terms at Japanese bookshops

### 2.1 Direction convention — stated unambiguously, because this is routinely misread

> **「7掛」 / 掛け率70% = the shop pays the maker 70% of cover price. The ARTIST RECEIVES 70%. The SHOP KEEPS 30%.**

Confirmed by worked examples in two independent sources: 「1冊1,000円のZINEを…書店が1冊600円で買い取ってくれた場合、掛け率は6割＝「6掛」となります。」 ([ya-hachi.com](https://ya-hachi.com/zine-bookstore-sell/)) and 「掛け率が6割だとすると、私が書店からいただく代金は500×0.6＝300円。残りの200円が…書店の利益」 ([note](https://note.com/z_franny/n/n524d7028d018)). Yahoo!知恵袋 carries a standing question titled 「『掛け率』は私の取り分？委託先の取り分？」 — **always restate both sides in words in any email.**

### 2.2 Her three pipeline targets: NONE publishes terms

| Shop | 掛率 | Quantity / payment / fees | How to initiate | Confidence |
|---|---|---|---|---|
| **UTRECHT** [utrecht.jp](https://utrecht.jp/) | **NOT PUBLISHED** | **NOT PUBLISHED** | **info@utrecht.jp** or 03-6427-4041 — the only channel | **DIRECT (verified absence)** |
| **Book and Sons** [bookandsons.com](https://bookandsons.com/) | **NOT PUBLISHED** | **NOT PUBLISHED** | [contact form](https://bookandsons.com/contact/); no email published, no 委託 category | **DIRECT (verified absence)** |
| **flotsam books** [flotsambooks.com](https://flotsambooks.com/) | **NOT PUBLISHED** | **NOT PUBLISHED** | [bare contact form](https://flotsambooks.com/pages/contact) | **DIRECT (verified absence)** |

These were verified by mapping each site in full — sitemaps, all nav/footer pages, blog archives — not inferred from a failed search.

⚠️ **UTRECHT's "Wholesale" page is a trap.** [utrecht.jp/pages/wholesale](https://utrecht.jp/pages/wholesale) reads like a maker-intake page and is the opposite: 「ユトレヒトでは日本国内の販売権を持つ書籍、雑誌のディストリビューション（卸販売）を行っています。」 — **UTRECHT acting as a distributor selling TO shops.** Do not apply through it. *(Worth correcting in the pipeline's opportunity record.)*

⚠️ Book and Sons demonstrably *does* run 委託 — a June 2026 Instagram post uses 「委託販売予定作家」 — but no terms are stated. **INFERRED, low confidence.** flotsam maintains a "Self Published" collection (15 titles), so self-published work is in scope; terms simply aren't posted.

🔴 **GAP, left open rather than filled:** no first-hand account of consigning at any of these three was recoverable. They carry **no rate figure at all** rather than a borrowed one.

### 2.3 Shops that DO publish real numbers

| Shop | Artist receives | Model | Quantity | Payment | Fees | Accepting? |
|---|---|---|---|---|---|---|
| **タコシェ Taco Ché** (Nakano) ⚠️ `http://` only — [tacoche.com/?page_id=25](http://tacoche.com/?page_id=25) | **70%** (shop 30%) | 委託 | No fixed min; by consultation | **月末締め・翌月末払い** | No 出品料; return shipping artist-paid after ~6mo | **Yes** — 「随時、募集しております」 |
| **模索舎 Mosakusha** (Shinjuku) [mosakusha.com](https://mosakusha.com/?page_id=255) | **70%** (shop 30%) | 委託 | Shop specifies | **Quarterly** | **Artist bears all** — 送料・返品送料・振込手数料 | **Yes, no jury** — 「原則的に無審査」 |
| **シカク出版** (Osaka) [tanoshikaku.net/terms](https://tanoshikaku.net/terms) | **70%** | 委託 | — | Twice yearly (4月末/10月末) | — | Excludes ISBN'd trade books |
| **HOCCH** [hocch.jp/zineitaku](https://www.hocch.jp/zineitaku) | **60%** (negotiable) | 委託 2ヶ月 | 初回3〜5冊 | 月末締め→翌月15日 | Artist pays shipping; shop absorbs transfer fee | Yes |
| **MOUNT ZINE** [zine.mount.co.jp](https://zine.mount.co.jp/mz31/) | **100%** of sales | Flat **出品料 ¥12,000/title** | 5 or 10 copies | After ~5-month period | ¥12,000 upfront | Verify edition dates |
| **banso books** (取次) — [via note](https://note.com/studio_takeuma/n/n443dd6e97567) | **60%** (shop 30%, banso 10%) | **買取**, not consignment | — | — | — | Launched winter 2025; "日本初の日本製アートブック専門取次" |

**All DIRECT.** ⚠️ Taco Ché's page uses a **5% consumption tax** worked example, so that text predates April 2014. The 70/30 split is stated three separate ways and is reliable; **call 03-5343-3010 before shipping** — their page requires prior consultation regardless.

**Taco Ché is the strongest real target found**: currently soliciting, complete published terms, unusually good monthly settlement, an art/画集 audience, in Tokyo.

⚠️ **SPBS makes you name the rate.** [shibuyabooks.co.jp/pages/product-inquiry](https://shibuyabooks.co.jp/pages/product-inquiry) has **required** fields for 掛け率（買取）and 掛け率（委託）as percentages, plus 初版部数 and 現在の主なお取引店. **She will be asked for a number.** 双子のライオン堂 likewise: 「取引条件をメールに記入していただけますと」.

**Not available / deprioritise:** **NADiff** — flagship a/p/a/r/t **closed 2025-03-23**; remaining branches are museum shops. **H.A.B** — 「現在新規の「直取引」の委託を休止しております」. **ブックスキューブリック** — 「現在、新規の受付を停止しております」. **POST** — publisher-representation model, not maker consignment. **森岡書店** — domain did not resolve 2026-09-05; invitation-only anyway.

⚠️ **Infrastructure note for the pipeline:** `tacoche.com`, `www.tacoche.com`, `post-books.jp` and `www.nadiff.com` **all fail over HTTPS** (Sakura shared-host cert mismatch) and resolve only over `http://`. A verification pass trying HTTPS alone will wrongly mark four shops dead.

### 2.4 The general Japanese standard — clearly labelled as general

**This is market data, NOT any named shop's offer to her.**

| Source | Type | 委託 (artist gets) | 買取 (artist gets) |
|---|---|---|---|
| [Nuts Book Stand](https://note.com/nutsbookstand/n/n7046afe040d0) (2026-05) | **shop owner, buy side** | **70%** | **60%** |
| [よはく舎／マルジナリア書店](https://yohakushapub.hatenablog.com/entry/2022/07/28/154454) | **shop owner** | **70%** | **60%** |
| [ナガサワケンタ](https://note.com/ken76a3/n/nb1c3b901eac7) | ex-bookseller guide | 60–70% | 50–70% |
| [ya-hachi](https://ya-hachi.com/zine-bookstore-sell/) | zine maker | 6–7割 一般的 | same |
| [シカク出版](https://tanoshikaku.net/terms) | published contract | **70%** | — |
| [オフショア](https://offshore-mcc.net/bookstore/) | publisher terms | **70%** | **60%** |
| [CONTE MAGAZINE](https://contemagazine.com/for-bookshop/) | publisher | 80% ← outlier | 65% |
| [studio_takeuma](https://note.com/studio_takeuma/n/n569c579f74c0) | working illustrator | 「書店が個人と取引する際の掛け率は60～70％が相場」 | — |

> **委託 = 70% artist / 30% shop. 買取 = 60% artist / 40% shop.** The ~10-point gap is universal across every source — the shop absorbs unsold-stock risk on 買取.

Stated from the buy side: 「書店への直販の基準としては**買取60％、委託70％**が相場なんじゃないかと思う。」「掛率は60％～70％ぐらい。**取次使ったら約80%**なので…」 (Nuts Book Stand).

**Comparison to the mainstream 取次 trade** ([日本出版者協議会, 2026-07-07](https://www.shuppankyo.or.jp/post/honnohitokoto20260707), DIRECT): 出版社 **70%** / 取次 **8%** / 書店 **22%**. From the shop's side that is 掛率 77–78%. **At 70掛 direct, she personally nets the same share a whole commercial publisher nets via 取次** — and the shop's 30% beats the 22–23% it earns on 取次 stock.

**Mechanics:**
- **送料:** default is maker pays outbound, shop pays returns — but many shops push both onto the maker (シカク出版, 模索舎, HOCCH, タコシェ). **振込手数料** is usually the maker's.
- **精算:** 「多くの書店では月末締め、翌月振込み」 is the mainstream cycle, **but zine consignment is often far slower** — シカク出版 and オフショア twice yearly, 模索舎 quarterly. Taco Ché's monthly cycle is unusually good. **Plan cash flow for 3–6 month lags.**
- **納品書 is required and shops are strict.** そぞろ書房: 「必ず請求書、もしくは納品書兼請求書をご用意ください。**納品書のみは受付しかねます。**」
- **ISBN is NOT required** for direct trade with indie shops — only for the 取次 route. Sites claiming otherwise are describing the 取次 channel.
- **一冊！取引所** (B2B bridge): 参加料 ¥5,500/yr + 商品登録料 ¥1,100/item + 決済手数料 8%.

⚠️ **Every rate above comes from the ZINE/リトルプレス tier, where unit prices are low.** Section 6 shows what happens when you apply a 70掛 to a high-unit-cost hardcover. Note also that some shops prefer **買取 only** — 「委託は管理に手間がかかり、返品や清算に手間と送料がかかるからだ」 (Nuts Book Stand). A 買切 offer at 60掛 can be more attractive to a small shop than 委託 at 70掛 despite the worse headline.

---

## 3. Art book fair economics

### 3.1 ⚠️ Scheduling reality first: the TABF door has closed

The next edition is branded **"TABF 2026" but held in January 2027**, and its exhibitor call **closed 2026-06-07 — three months ago.**

| Item | Value | Confidence |
|---|---|---|
| Next edition | **2027年1月21日(木)–24日(日)** and **1月29日(金)–31日(日)**, MOT | DIRECT — [application-addition](https://tokyoartbookfair.com/application-addition/), cross-confirmed by [MOT](https://www.mot-art-museum.jp/exhibitions/tokyo-art-book-fair-2026/) |
| Application deadline | **6月7日(日) 2026 — PASSED** | DIRECT |
| Notification | 「出展可否のご連絡は、7月中に行います」 | DIRECT |
| Historical call-close pattern | 2016: Jul 18 · 2019: Mar 31 · 2022: Jul 22 · 2024: Jun 16 · 2026: Jun 7 | DIRECT |

**Earliest realistic entry is the following edition. Watch the site from April onward.**

### 3.2 TABF booth fees — current (Jan 2027 edition)

**ZINE'S MATE (B2) — the individual-artist section, and the relevant one.** Cross-verified against both the Japanese and English versions ([en](https://tokyoartbookfair.com/en/application-form-addition/) / [ja](https://tokyoartbookfair.com/application-form-addition/)) — **DIRECT.**

| Table | Wall | Chairs | Week 1 (4 days) | Week 2 (3 days) |
|---|---|---|---|---|
| 1,500 × 450 mm | yes | 2 | ¥33,000 | ¥27,500 |
| 1,500 × 450 mm | no | 2 | ¥27,500 | ¥22,000 |
| **900 × 450 mm** | no | 1 | **¥22,000** | **¥16,500** |

Other sections for scale: EXHIBITION SPACE ¥44,000–66,000 · ENTRANCE (1F) ¥38,500–49,500 · PRINTER (1F) ¥38,500–49,500.

**Cheapest way in: ¥16,500.**

**What the fee includes** (all DIRECT): table + chair(s) ✅ · wall **optional +¥5,500** · **electricity NOT available** (「各ブースへの電源の貸し出しは原則として出来かねます」) · **no commission on sales — exhibitor keeps 100%** · **no insurance** (「盗難や…事故においては、事務局では責任を負いかねます」) · **must staff the booth at all times** (900mm table = 1 person max).

**Fee history — TABF has become *cheaper* for individuals since 2019** (all DIRECT): 2015 Z booth ¥5,400–16,200 · 2016 ¥10,800–21,600 · 2019 ¥27,000–37,800 · 2026/27 ¥16,500–33,000.

### 3.3 Selection, attendance, and an honest caveat

| Question | Answer | Confidence |
|---|---|---|
| Juried? | **Yes** — 「応募多数の場合は、選考により出展者を決定させて頂きます」 | DIRECT |
| Reasons given? | **No** — 「選考における出展可否の理由については、一切開示いたしません」 | DIRECT |
| Criteria | Priority to 「定期的に出版物を刊行している方」and 「積極的に出版を行なっている方」 | DIRECT |
| **Is ZINE'S MATE for first-timers?** | **Yes** — 「初めて出展する参加者を中心に構成されており」 | DIRECT ([pen-online.jp](https://www.pen-online.jp/article/020238.html), 2025) |
| Acceptance rate | **Never published** | UNVERIFIED |
| Free upside | **TABF Talent Award** — every exhibitor auto-entered; prizes include a **free booth at a future fair** | DIRECT ([2025 award page](https://tokyoartbookfair.com/2025/tabf-talent-award/)) |

| Scale figure | Value | Confidence |
|---|---|---|
| Visitors per edition | **「2万人以上」 (over 20,000)** | DIRECT but ⚠️ see below |
| Exhibitors 2025 (15th ed.) | ~560 total, ~280 per weekend | DIRECT |
| Exhibitors 2024 / 2023 / 2019 | ~300 each | DIRECT |

⚠️ **Flag the 20,000 hard.** It is marketing boilerplate, not an audited per-edition count — **TABF publishes no post-fair report with numbers**. The visitor model also changed materially: **2019 and earlier admission was FREE**; 2021 was capped at 300–450 people per 2h15m slot (~7,000 max across the fair); **2025 charged ¥1,000 online / ¥1,200 same-day with timed entry**. The "20,000+" figure likely descends from the free-admission era. **Footfall past any one booth in the paid, timed-entry era is UNVERIFIED and probably lower than the boilerplate implies.**

**TABF was not held every year:** 2018 **not held** · 2020 physical fair **cancelled** (virtual only) · 2021 capped. Full history verified at [tokyoartbookfair.com/archives/](https://tokyoartbookfair.com/archives/).

⚠️ **TOKIO ART BOOK FAIR is a different event.** [tokioartbookfair.com](https://tokioartbookfair.com/) — May 1–3 2026, Shiba Park Hotel, **52 exhibitors, invitation only, no open call.** Organised *by* TABF but not applicable. *(The pipeline holds records for both — worth distinguishing.)*

### 3.4 Comparable fairs

| Fair | Booth fee | Attendance | Confidence |
|---|---|---|---|
| **文学フリマ東京** | **¥6,900** / booth | **18,689** (2026-05, ed.42: 5,619 exhibitors + 13,070 general); 16,111 (ed.40); 14,967 (ed.39) | Fee DIRECT [bunfree.net](https://bunfree.net/rules/areas/tokyo/); ed.42 DIRECT [official X](https://x.com/Bunfreeofficial/status/2051597771376070862) |
| **デザインフェスタ** | S **¥27,000** (both days) · M ¥48,000 · L ¥72,000 — ⚠️ **floor space only, no table/chair/panel** | up to **140,000** over two days; ~6,500 booths/day | DIRECT [designfesta.com](https://designfesta.com/app-booth/) |
| **COMITIA** | **UNVERIFIED** — fee not locatable | 6,857 circles (ed.156, Jun 2026); no visitor count published | DIRECT [comitia.co.jp](https://www.comitia.co.jp/history/156report.html) |
| **NY Art Book Fair** | **Zine table $200** · 4′ table+wall $500 · 6′ $800 | "tens of thousands", never exact; ~300 exhibitors | DIRECT [printedmatterartbookfairs.org/faq](https://printedmatterartbookfairs.org/faq) |
| **Offprint Paris** | **UNVERIFIED — never published** | "over 35,000" (undated, [LUMA](https://luma.org/en/arles/about/offprint)) | Fee UNVERIFIED |
| **Unlimited Edition** (Seoul) | **UNVERIFIED** | UNVERIFIED | Dates DIRECT: Nov 6–8 2026 |

⚠️ Design Festa's price is misleading — table/chair/panel rental adds roughly ¥26,000–43,000 (INFERRED, secondhand: [note](https://note.com/jyo_ji_5030/n/n7c21da3f6058)).

**Notable: NYABF publishes its odds — ~700–1,000 applications, 20–25% accepted.** TABF publishes nothing comparable.

### 3.5 ⭐ Realistic sell-through — the number that matters most, and its honest confidence

**Read this before the numbers: there is essentially NO published sell-through evidence for TABF specifically.** TABF exhibitors write plenty of posts and consistently **omit the numbers**. Two confirmed 2025 TABF exhibitors were checked line by line — [SAUNTER Magazine](https://note.com/sauntermagazine/n/nd7394e7c0b0b) and [Tokyo Photographic Research](https://note.com/tpr/n/n1ed75125160a) — **neither discloses a single financial figure.**

**The only TABF copy count found anywhere:**

| Seller | Book | Copies | Days | Confidence |
|---|---|---|---|---|
| **NEUTRAL COLORS** — an established independent *publisher*, not a solo artist | 『How to Book in Japan』 | 「4日間のフェアで**400冊**を売り上げた」 | 4 | **ANECDOTE n=1** — [note](https://note.com/neutralcolors/n/n3131de7f7315), 2023 |

**This is a ceiling reference, not a target.** A publisher with an existing audience selling a book *about Japanese book-making* at a book fair.

**Everything below is from 文学フリマ, ZINEフェス, コミティア and Design Festa — NOT TABF.** TABF differs on both sides: a ¥1,000–1,200 paid, timed-entry gate (fewer but more committed, art-buying visitors) against a booth costing **2–4× more**. Whether that nets out better or worse is **genuinely unknown.**

**The anecdote corpus — 26 event-observations from ~20 independent exhibitors, 2023–2026. Every row ANECDOTE, n=1.**

| Fair | Date | Price point | Copies | P&L note | URL |
|---|---|---|---|---|---|
| 文学フリマ東京41 | 2025-11 | 3 zines @¥1,000 | **58** | — | [note](https://note.com/takanamishoten_/n/nd96dd36b267f) |
| 文学フリマ東京42 | 2026-05 | @¥1,500 | **20** (sold out early) | ¥30,000 | [note](https://note.com/matsumitsu320/n/neaf17f68085b) |
| 文学フリマ東京42 | 2026-05 | ¥500/¥600 | **52** | ¥27,100 rev · booth ¥7,900 · print ¥11,690 → 「本が完売しても黒字ではない」 | [note](https://note.com/kanouseiten/n/nb571f3da9ac3) |
| 文学フリマ東京42 | 2026-05 | anthology ¥500 | **8** | ¥4,000 vs ~¥124,000 all-in → 「純利益は出てないよ〜」 | [note](https://note.com/watatumimizuha/n/n463f16a5b562) |
| 文学フリマ東京40 | 2025-05 | 6 titles | **32** | — | [soyogobooks](https://soyogobooks.jp/essays-and-more/1654/) |
| **Same seller, 5 fairs** | 2024-12→2025-05 | diary/essay zines | 文フリ東京39 **53** · ZINEフェス東京 **42** · 詩歌と日記 **13** · 仙台 **31** · 文フリ東京40 **86** | 「文学フリマの方が売上は圧倒的に多かった」 | [note](https://note.com/rakugotosake/n/n36aba2897fae) |
| Same seller, tiny venues | — | zines | **2**, **10**, **2** | venue ¥1,800 → net loss | [note](https://note.com/rakugotosake/n/n7d4f810ecf37) |
| ZINEフェス東京 | 2026-07 | ZINE ¥1,500 | **20** | ¥40,000 rev vs **¥213,013 spent** → 「大赤字でした」 | [note](https://note.com/tabi_zukai/n/n8c4df5cc9a14) |
| ZINEフェス埼玉/東京/イマZINE | 2026-08 | ~¥500 | **66** / **14** / **42** | — | [note](https://note.com/daitai_de_ii/n/ne2acfa431680) |
| ZINEフェス詩歌と日記 | 2026-08 | 詩集 | **4** | 「出展料に僅か及ばない赤字」 | [note](https://note.com/dear_teacher1761/n/n3e2b3271e9bb) |
| ZINEフェス京都 | 2026-08 | ¥900+¥100 | **2** | ¥1,000 | [note](https://note.com/aloha_nori/n/na65cda7672d3) |
| ZINEフェス福岡 | 2025-09 | books+goods | 「数冊」 | 「過去最低売上でした」 | [konepan](https://konepan.com/repo02/) |
| **文学フリマ香川 (illustrator)** | 2026-08 | ¥500 | **11** (sold out) | ~¥5,800 vs ¥7,600 print | [note](https://note.com/haonns/n/n2fd7ac8b2cdb) |
| ZINEフェス / 文学フリマ | 2025 | one title | **27** / **17** | — | [note](https://note.com/ume10/n/n496828dbf186) |
| 文学フリマ東京42 | 2026-05 | book ¥1,000; cassette ¥2,000 | **30 + 7** | ~¥44,000 | [note](https://note.com/watasino_beats/n/n713734ad386f) |
| 文学フリマ東京37 | 2023-11 | 詩集 | **7** | ¥6,100 vs ¥3,000 booth → 「大赤字です！」 | [note](https://note.com/uutamomo/n/nce80393057d3) |
| 文学フリマ東京41 | 2025-11 | essay ¥500 | **31** (sold out 13:45) | ¥15,500 | [note](https://note.com/aoisan_no_note/n/n9006dcfc2ff9) |
| 文学フリマ札幌8 | — | ¥500–800 | **25** (brought 45) | 「初めは30部くらい刷るのがいい」 | [note](https://note.com/sunsetglow/n/n04e8c88e0ba2) |
| **Art Book Osaka 2026** | 2026-05 | artbook+ZINE | 「売上も過去一番」 | 「利益まではでませんでした」 after print+booth+Shinkansen+2 nights | [note](https://note.com/everest_copy/n/ned7508b6b06d) |
| 文学フリマ東京39 | 2024 | — | **under 50**, author calls it 「さほど多くない」 | after 2 years of production | [note](https://note.com/kasaikouhei/n/n5b11ec98373b) |

**The only aggregate data that exists:** 絵師白書2010 (サムライファクトリー), **n=3,986**, via [ITmedia](https://www.itmedia.co.jp/news/article/1008/25/1100825073/) — copies sold at 即売会: **<5 copies 13% · 5–9 copies 10% · 10–29 copies 24% → ~47% sold fewer than 30**; 90% under 300. Sixteen years old and a different community, but **directionally consistent** with the 2025–26 anecdotes.

**Sorted copy counts across 26 observations:**
`2, 2, 2, 4, 7, 8, 10, 11, 13, 14, 17, 20, 20, 25, 27, 30, 31, 31, 32, 42, 42, 52, 53, 58, 66, 86`

> ### **Median ≈ 20–25 copies. Middle half ≈ 8–42.**
> **Plan for 10–40 copies at a one-day Japanese zine/lit fair, at ¥500–¥1,500 per copy. Typical revenue ¥5,000–¥30,000.**
>
> **Confidence: LOW-to-MODERATE on the range · LOW on any point estimate · effectively ZERO evidence above ¥3,000.**

**Why that caveat is not boilerplate:**
- **~20 self-selected bloggers.** People who post sales reports skew toward those who had a decent day.
- **Heavy right-censoring.** At least four sold *out* (at 20, 31, 10, and 8-of-10). The community default print run is ~30 copies, so the distribution is capped by cautious inventory, not by demand.
- **Wrong genre** — mostly literary/travel/diary zines, not visual-art books.
- **Wrong fair** — none of it is TABF.
- Price was disclosed in only about half the cases.

**Every cost-disclosing account lost money or barely broke even** — including the one that sold out, and the one with the highest revenue (¥40,000 against ¥213,013 spent). **Exhibitors uniformly treat the day as marketing, not revenue.**

### 3.6 ⚠️ The "expensive books sell worse" hypothesis: NOT confirmed, and partly contradicted

This was specifically hunted for. Reporting the result straight:

- **No first-hand account of a ¥3,000+ book with a copy count exists in the reachable Japanese corpus. Not one.** The entire visible evidence base sits at ¥100–¥2,000.
- **Within the observed band, higher price did not suppress volume:** ¥1,000→58 · ¥1,000→30 · ¥1,500→20 (sold out) · ¥1,500→20, versus ¥500→8 · ¥500→31 (sold out) · ¥500/600→52. **Spread *within* each price tier exceeds spread *between* tiers.**
- **Direct contradiction** — motake, photo zines at ZINEフェス 2026: 「安価でもさほど量が出ませんでした。メインの作品は値段が上でも売れていたので」 — the cheap edition moved poorly while the pricier main work sold. 「安価であれば良いというものでもなさそうです」 ([note](https://note.com/motake3/n/n7a4e69c99506), ANECDOTE).
- **Weak support only:** Art Book Terminal Tohoku 2023's mid-fair top-5 clustered under ¥1,000 (4 of 5); one seller moved 30 books @¥1,000 but only 7 cassettes @¥2,000 — different product categories, not a clean test.

> **Pricing a watercolour hardcover at ¥4,400–5,500 is not contraindicated by evidence — it is simply un-evidenced. That is a different, and more uncomfortable, position than "it will sell fewer copies."**

---

## 4. Realistic pricing — what the Japanese market bears

### 4.1 The structural finding: two markets, two ceilings

| Market | Where | Observed range for indie art books | Effective ceiling |
|---|---|---|---|
| **Doujin / otaku platform** | BOOTH, COMITIA, pixiv orbit | ¥800–¥3,300 | **~¥3,300 hard** for indie analog/watercolor |
| **Art-book / zine / gallery** | UTRECHT, Nieves, NADiff, POST, TABF, direct BASE | ¥1,200–¥33,600 | **No practical ceiling**; ¥5,000–7,000 unremarkable |

Evidence for the split: across BOOTH's entire 水彩画集 category (**423 products**) there were **zero** indie watercolor art books above ¥3,300. Meanwhile UTRECHT's book collection is **1,076 products spanning ¥1,000–¥33,600** ([utrecht.jp/collections](https://www.utrecht.jp/collections/%E6%9C%AC-books), DIRECT).

A BOOTH search for 水彩 作品集 建築 街 returned **one result, and it was an AI horse image pack** — **the architecture/watercolor niche does not exist on that platform.** A watercolor/architecture/memory painter is in the second market.

### 4.2 ⭐ The closest comparable in existence: タケウマ / studio_takeuma

A Tokyo illustrator with **27K Instagram followers** — essentially identical scale — who self-publishes and sells direct plus via bookshops. Full ladder from [takeuma.buyshop.jp](https://takeuma.buyshop.jp/) — **DIRECT:**

| Title | Format | Price (inc. tax) | ¥/page | Status |
|---|---|---|---|---|
| Hedgehog's Hug | 92pp, bunko 14.8×11cm | ¥1,100 | ¥12 | — |
| IDEATITY | 124pp, mono, 17×12.8cm | ¥2,750 | ¥22 | — |
| A Sketchbook | 200pp, A5, colour | ¥4,400 | ¥22 | **Sold out** |
| **Travel Sketch** | **428pp, full colour, ドイツ装, 19×12.5cm, 625g** | **¥11,000** | ¥26 | **Sold out** |

His own published economics ([note](https://note.com/studio_takeuma/n/n569c579f74c0), **DIRECT**):
> 「Travel Sketchは１万円（税抜き）と高額な本だが、**４か月で400冊**が売れた。」
> 「初版の制作コストは約**60**％、重版からは…約**40**％になります」 — first-edition production cost ≈ 60% of retail; reprints ≈ 40%.

### 4.3 Indie hardcover comparables on BOOTH (2026-09-05, all DIRECT)

| Price | Title | Specs |
|---|---|---|
| ¥1,980 | ものの芽 shuu作品集 | **Hardcover, 64pp** |
| ¥3,000 | 画集2「ハレと額縁」 | B5, 128pp full colour, perfect-bound (¥23/pp) |
| ¥3,500 | 感情メトロ (兎黒舎) | 上製本 picture book |
| ¥4,400 | [画集] N/DOLL | — |
| **¥5,370** | **Brant Art Collection** | **A4, 100pp full colour, perfect-bound, matte PP** |
| ¥6,600 | 姫川明輝 35th ARTWORK画集 | — |
| ¥9,680 | BRILLIANCE — Tony個人画集第二弾 | **160pp full colour, hardcover, 31.5×24cm, clear box case** |
| ¥13,500 | SKETCHAOS 第3印刷 (Entei Ryu) | **A5, 312pp, leather cover, run of 100** |

⚠️ **Data-hygiene warning:** the BOOTH shop ☕️魔都喫茶 dominates the ¥3,000–8,500 band and is a **reseller of imported Chinese 商業画集**, not an indie creator — roughly 25 of the ~50 highest-priced 画集 results are that one shop. Excluded from the benchmark above.

**Indie watercolor/analog band on BOOTH** (45 listings sampled): **mode ¥1,500–2,200, ceiling ¥3,300.** 空の画集 ¥800 · まみた画集Ⅱ ¥1,100 · 水彩画集「黄道十三猫」 ¥1,500 · 夏神 ¥2,000 · 散歩途 ¥2,200 · くまちゃんといっしょ ¥2,500 · ハレと額縁 ¥3,000 · elkpot作品集 ¥3,300.

### 4.4 Tokyo indie shop stock — the market she's actually in

**UTRECHT** ([utrecht.jp](https://www.utrecht.jp/collections/all), DIRECT): AYA YAMANAKA Lookbook ¥2,500 · Nigel Peake *Appunti Su Alcuni Dipinti* ¥5,800 · Munari *XEROGRAFIA* ¥6,400 · *Low Fi Cats* ¥7,000 · *The Complete Before After & Beyond* ¥9,000.

**Nieves** — the canonical small-press artist-zine imprint ([via UTRECHT](https://www.utrecht.jp/collections/nieves), DIRECT, 50 titles): Jean Jullien *Punctuations* ¥1,500 · **Amelie von Wulffen *Some Watercolors* ¥2,000** · Samuelsson *Houses* ¥2,600 · Tiger Tateishi *Cheat Sheets* ¥3,600 · Warja Lavater *Pictograms* ¥3,800 · *Greenhouse Studies* ¥4,000 · Emi Ueoka *Intersections* ¥6,000.

**PIYO PIYO PRESS** (Japanese indie art press): （世界）² ¥3,900 · 花とイルカとユニコーン (signed) ¥4,200.

### 4.5 Commercially published 画集 — the ceiling reference

| Title | Publisher | Format | Price (inc.) | Source |
|---|---|---|---|---|
| **あべとしゆき水彩画集** | 芸術新聞社 | **B5横, 176pp, softcover** | **¥3,300** | [gei-shin.co.jp](https://gei-shin.co.jp/books/books-6935/) |
| Haる画集 essence | 玄光社 | **B5, 160pp, hardcover** | **¥2,750** | [genkosha.co.jp](https://www.genkosha.co.jp/book/b10094991.html) |
| **フランス水彩風景画紀行** (奥津国道) | 講談社 | **A4横, 146pp, hardcover** | **¥5,170** | [kodansha.co.jp](https://www.kodansha.co.jp/book/products/0000184997) |
| 日本を旅する水彩風景スケッチ | グラフィック社 | B5変, 200pp, 並製 | ¥2,640 | [graphicsha.co.jp](https://www.graphicsha.co.jp/detail.html?p=28951) |
| 澪 mio 友風子画集2 | PIE International | — | ¥3,300 | [honto.jp](https://honto.jp/) |
| Prism 森倉円作品集 | PIE International | — | ¥3,740 | [pie.co.jp](https://pie.co.jp/book/artbook/) |
| 草森秀一アニメーション美術画集 | PIE International | — | ¥6,050 | [pie.co.jp](https://pie.co.jp/book/artbook/) |

All **DIRECT**. PIE International's full 画集 line runs **¥2,200–¥6,050 inc.**, clustering ¥2,750–¥3,740.

**Key calibration:** Japan's most commercially successful living watercolorist publishes a 176-page collection at **¥3,300**. A commercial **A4 hardcover** watercolor collection from Kodansha is **¥5,170**. Those two bracket the commercial ceiling for exactly this subject matter.

### 4.6 What hardcover, page count and size do to the price

- **Softcover → hardcover:** worth roughly **+¥1,000–¥2,000**, not more. A 64pp hardcover sells at ¥1,980; a 100pp A4 perfect-bound sells at ¥5,370. (INFERRED from the BOOTH ladder.)
- **Page count:** the working rate for full-colour indie art books is **¥22–¥54 per page** (Takeuma consistently ¥22–26; A4 indie at ¥54). ⚠️ The classic doujin rule of **¥10/page** ([Togetter 2015](https://togetter.com/li/874685)) is calibrated for **monochrome** and is **2.3–5.4× too low** for full colour.
- **Size:** A4 carries a ~50% premium over A5 at the same page count, in both printing cost and retail.

**Japanese psychological price points (tax-inclusive round numbers):**
`¥1,980` · `¥2,750` · `¥3,300` · `¥3,850` · `¥4,400` · `¥5,500`
Visible directly in the data: her own zines ¥1,980 · Genkosha ¥2,750 · あべとしゆき ¥3,300 · PIE ¥3,300 · Takeuma ¥2,750/¥4,400/¥11,000 · Tony ¥5,500. **INFERRED from a consistent pattern across 12+ DIRECT observations.**

### 4.7 The answer: realistic band for a 100–150pp full-colour hardcover, Japan 2026

| Scenario | Price | Evidence |
|---|---|---|
| **Floor** — direct sales only, ≥300 copies printed | **¥3,850–¥4,400** | Takeuma's 200pp A5 colour = ¥4,400. Commercial 160pp hardcover = ¥2,750–3,300. Below ¥3,850 undercuts her own ¥22–26/page ladder — and at 100 copies is **below unit cost**. |
| **Centre of gravity** — direct + events + a few shops | **¥4,400–¥5,500** | A4 100pp indie = ¥5,370 (DIRECT). Kodansha A4 146pp hardcover = ¥5,170. Tony hardcover = ¥5,500. UTRECHT's stock median sits here. **This band survives a 30–35% shop margin.** |
| **Ceiling** — sustainable only as an *object* | **¥6,600–¥11,000** | Requires unusual binding/size/page count: 160pp + box ¥9,680 · 312pp leather ¥13,500 · **428pp German binding ¥11,000 and still sold 400 copies** |

> ### **Recommended band: ¥4,400–¥5,500 tax-inclusive.**
> ¥4,400 if A5/B5 and ~100pp; ¥5,500 if A4 or ~150pp.
>
> **¥3,300 is a trap** — it reads as the top of the *doujin* market rather than the bottom of the *art book* market, and at any run under ~300 copies it is at or below unit cost once a shop margin is taken.

### 4.8 Is there a ceiling above which shops won't stock or buyers won't buy?

**On BOOTH: yes, ~¥3,300 for indie analog work** — DIRECT, zero counter-examples across 423 products.

**In the indie art-book shop channel: no meaningful ceiling.** The constraint is margin and relationship, not price. Takeuma notes shops took **30%** on his **¥11,000** book, and 「大手の書店もZINEなど私家版画集を扱いはじめ」 — major bookstores have begun stocking self-published art collections, helped by inbound tourism favouring visually-driven books ([note](https://note.com/studio_takeuma/n/n5f9676271ef5), DIRECT).

**Maker/buyer commentary (ANECDOTE, named):**
- A B5 ~100pp **full-colour** book at **¥1,800** was called "expensive" by a passer-by; the community response was that it was conspicuously *cheap*: 「フルカラーB5.100Ｐ超えの同人誌が1800円は破格に安いです」 ([Togetter 2024-11-29](https://togetter.com/li/2472342))
- Buyer-side counter-consensus: 「3000円超でも気にしないｗ」/「どうしても欲しい本なら1万円越えてても出す」/「安すぎるの見て『えっ…大丈夫ですか…もっと出しますよ…？？？』」 ([Togetter 2016](https://togetter.com/li/1020352))

---

## 5. Direct-sales conversion from ~26k Instagram followers

### 5.1 HEADLINE: no reliable public benchmark exists. Do not budget against one.

This is the honest state of the evidence, not a hedge:

1. Across **27 live art-book and illustration Kickstarter campaigns** pulled 2026-09-05, **zero published a follower count.** The two halves of the ratio essentially never appear in the same document.
2. Same category, same week, backers ranged from **0 to 9,142**.
3. Where a real follower count could be paired with a real buyer count, conversion ranged **0.26% to 15.8% — a 60× spread**, and it runs **the wrong way with audience size**.
4. The dominant variables are not follower count. They are **whether an email list exists, audience geography, price point, and whether the audience has ever bought from you before.** None is visible in a follower number.

> **If anyone quotes a "1–3% of followers will buy" rule, ask for the dataset. No such dataset was found.**

### 5.2 Named paired data points — INDIVIDUAL OBSERVATIONS, EXPLICITLY NOT AN AVERAGE

Follower counts read from Instagram 2026-09-05; buyer counts from kicktraq the same day. ⚠️ **Applies to every row:** these creators also have X, Patreon, Twitch, email lists and physical events — **none of these is a pure Instagram conversion rate.** Kickstarter rows are **mid-campaign**, so buyer counts are partial.

| Creator | IG followers | Buyers | % of IG | Revenue | Product |
|---|---|---|---|---|---|
| ⭐ **タケウマ / studio_takeuma** (Tokyo) | **27K** | **400 copies / 4 months** | **1.48%** | ¥4.0M ex-tax | **¥11,000 self-published 428pp art book, direct + shops** |
| Century Guild | 28.1K | 110 backers | 0.39% | $15,211 | ANIMALIA COIN art book (mid-flight) |
| jingjiart | 28.6K | 606 backers | 2.12% | $51,840 | Bags & pins **(merch, not a book)** |
| thekansta | 15.8K | 305 backers | 1.93% | CA$17,754 | Xicheng AU artbook — funded in 2 hours |
| Adam Oehlers | **119K** | 309 backers | **0.26%** | £28,317 | The Wildered Lands (2nd book) |
| Tapling Zines | **906** | 143 backers | **15.8%** | €6,386 | Moments of Euphoria art book |

> **In the 26–29K follower band — her band — the observed buyer counts are 110, 400 and 606.** That is the honest answer: somewhere between roughly **100 and 600 buyers**, and that range is set by things a follower count cannot see.

**Weight the Takeuma row most:** same country, same platform economics, near-identical follower count, self-published, direct sales, published sales figure. **It is still n=1**, and he is an established commercial illustrator with a decade-plus career and existing bookshop relationships.

**Adam Oehlers vs Tapling Zines is the cautionary pair: 119K followers produced *fewer* backers than 906 followers did.**

### 5.3 The Japanese doujin folk rule exists — and the scene rejects it

| Claim | Figure | Source | Confidence |
|---|---|---|---|
| "~10% of followers" | 1,200 copies / 12,000 followers | [Chiebukuro](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12256404062) | **ANECDOTE n=1 — and the accepted answer *rejected* it:** 「ピクシブのフォロワー数というのは部数の参考になりますか？ なりませんね…」 |
| pixiv bookmarks → copies | **0.5× to 10×** | [Chiebukuro](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13163417088) | ANECDOTE n=4 — 20-fold spread, no predictive power |
| Not predictive below ~100k | qualitative | [Togetter](https://togetter.com/li/1744385): 「**Twitterのフォロワー数も（十万単位なら話は別だけど）アテにならんです**」 | Consensus across 4 sources |
| Online-only ≈ half of event sales | 50% | [Chiebukuro](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10310518845) | ANECDOTE n=1 |
| The scene's replacement heuristic | **Print what the budget absorbs, not what you predict you'll sell** | Togetter 1744385 | Consensus n=2 |

**Every named Japanese source that addressed the question directly said follower count does not work as a predictor.**

### 5.4 Instagram engagement benchmarks — context only; an engagement is not a purchase

| Figure | Value | Source | Sample | Confidence |
|---|---|---|---|---|
| IG median engagement, all industries | **0.36%** | [rivaliq.com](https://www.rivaliq.com/blog/good-engagement-rate-instagram/) 2025 | 150 cos, 4M+ posts | DIRECT |
| Influencers category | 0.576% | same | same | DIRECT |
| IG engagement by followers | **0.48%** | [socialinsider.io](https://www.socialinsider.io/social-media-benchmarks/instagram) 2025 | 35M posts, 447,613 accounts | DIRECT |
| Q2 2026 update | 0.48% | same | same | DIRECT |
| YoY engagement change | **−24%** / −16% | both above | — | DIRECT |
| Micro tier 10K–50K | 1.06% | Influencer Marketing Hub 2025 via [colorlib](https://colorlib.com/wp/instagram-engagement-rate/) | undisclosed | **UNVERIFIED** (secondary) |
| Micro tier 10K–100K | 2%–4% | [later.com](https://later.com/blog/instagram-engagement-rate/) | undisclosed | **UNVERIFIED** — reach-based formula |

⚠️ **Rival IQ and Socialinsider — the only two with large disclosed samples — do not publish engagement by follower band at all.** The 0.48% follower-based figure and the 2–4% reach-based figure use **different denominators and must never appear in the same calculation.**

### 5.5 Ecommerce conversion — the "after the click" half

[shopify.com](https://www.shopify.com/blog/ecommerce-conversion-rate) 2026, DIRECT: global average **2.66%** (Dynamic Yield) / 1.4% (Statista) · fashion 2.77% · **luxury & jewelry 0.63%** · desktop 3.7% / mobile 2%.

**The relevant pattern: the more expensive and considered the object, the lower the conversion.** A ¥5,500 art book behaves like a considered purchase, not an impulse one. There is **no published "Instagram-referred traffic converts at X%" figure** anywhere found.

### 5.6 "1,000 True Fans" is a thought experiment, not data

[kk.org/thetechnium/1000-true-fans/](https://kk.org/thetechnium/1000-true-fans/), Kevin Kelly, **2008**. The $100/fan/year figure is stated as an assumption: *"Assume conservatively that your True Fans will each spend one day's wages per year."* **Kelly's own caveat: "My formula may be off by an order of magnitude."** That means the honest range is 100–10,000 true fans for the same outcome. **HEURISTIC. Not measured.**

### 5.7 The geography problem — shipping from Japan

A 128pp A4 hardcover is **~0.9kg**; the 1kg row is the right one. All from japanpost.jp, fetched 2026-09-05, **DIRECT**.

| Destination | EMS 1kg | **Small Packet 小形包装物, air 1kg** | Surface 1kg |
|---|---|---|---|
| China / Korea / Taiwan | ¥2,200 | **¥1,250** | ¥1,300 |
| Europe | ¥4,400 | **¥2,130** | ¥1,300 |
| **USA** | **¥5,300** | **¥2,720** | ¥1,300 |

**Domestic, for contrast** ([note](https://note.com/studio_takeuma/n/n01d1658885dc), 2025-06, DIRECT): **Click Post ¥185** (≤1kg, **≤3cm thick**) · ネコポス ¥420 · **Letterpack Light ¥430** (≤4kg, ≤3cm) · Yamato Compact ¥440–650.

**International air shipping costs 50–62% of a ¥4,400 book's price to the US. EMS costs more than the book.** Takeuma, from experience: **「Higher shipping costs cause online cancellations before checkout」** — and his 428pp book at 4cm thickness was disqualified from every cheap domestic option.

> **Two consequences:** (1) **Thickness under 3cm is worth real money** — the difference between ¥185 and ¥650 domestically. (2) **If her ~26k following is substantially non-Japanese, the Takeuma 1.48% comparable is optimistic.**

### 5.8 Platform fees (BASE)

[thebase.com/price](https://thebase.com/price), **DIRECT**: **Standard plan — ¥0/month, 3.6% + ¥40 payment processing, plus 3% service fee ≈ 6.6% + ¥40 per sale.** Growth plan ¥16,580/mo (annual billing) drops it to 2.9% + 0%. ⚠️ PayPay/Amazon Pay/PayPal add 1%. Payout is 10営業日 after request.

On a ¥4,400 book, Standard costs ~¥330/sale. **Growth breaks even at roughly 60 books/month** — well above any realistic launch rate, so **Standard is the right plan.**
🔴 **UNVERIFIED:** BASE's 振込手数料 / 事務手数料 and their threshold — the help pages could not be reached.

---

## 6. ⭐ BREAK-EVEN ARITHMETIC

### 6.1 Net revenue per copy, by channel

Computed on the Japanese convention: **掛率 applies to 本体価格 (ex-tax)**. A ¥5,500 tax-inclusive cover has a 本体価格 of ¥5,000.

| Channel | Formula | @ cover ¥4,400 (本体 ¥4,000) | @ cover ¥5,500 (本体 ¥5,000) |
|---|---|---|---|
| **Direct — BASE** | cover × 0.934 − ¥40 | **¥4,070** | **¥5,097** |
| **Fair booth** (TABF takes **no commission**) | cover, cash | **¥4,400** | **¥5,500** |
| **委託 consignment 70掛** | 本体 × 0.70 | **¥2,800** | **¥3,500** |
| **買取 wholesale 60掛** | 本体 × 0.60 | **¥2,400** | **¥3,000** |

*Excludes outbound shipping to shops, and international shipping on direct sales (§5.7) where she absorbs it.*

### 6.2 Margin per copy — the decisive table

**Landed unit costs used** (all DIRECT except China, which is INFERRED per §1.2): China 500 **¥913** · China 300 **¥1,320** · China 100 **¥3,770** · 栄光 digital B5 96pp @100 **¥3,204** · 緑陽社 offset B5 @500 **¥3,927** · 緑陽社 offset A4 @500 **¥5,386** · 緑陽社 offset B5 @300 **¥6,005** · 緑陽社 offset A4 @100 **¥24,283** · Blurb 50 **¥7,706**.
*(プリントオン is excluded from these tables because its figures are contested — see §1.4.)*

**At cover ¥5,500:**

| Route (unit cost) | Direct ¥5,097 | Fair ¥5,500 | 委託 ¥3,500 | 買取 ¥3,000 |
|---|---|---|---|---|
| **China 500** (¥913) | **+¥4,184** | **+¥4,587** | **+¥2,587** | **+¥2,087** |
| **China 300** (¥1,320) | **+¥3,777** | **+¥4,180** | **+¥2,180** | **+¥1,680** |
| **栄光 digital, 100** (¥3,204) | **+¥1,893** | **+¥2,296** | **+¥296** | **−¥204** |
| China 100 (¥3,770) | +¥1,327 | +¥1,730 | **−¥270** | **−¥770** |
| 緑陽社 B5 offset, 500 (¥3,927) | +¥1,170 | +¥1,573 | **−¥427** | **−¥927** |
| 緑陽社 A4 offset, 500 (¥5,386) | **−¥289** | +¥114 | **−¥1,886** | **−¥2,386** |
| 緑陽社 B5 offset, 300 (¥6,005) | **−¥908** | **−¥505** | **−¥2,505** | **−¥3,005** |
| 緑陽社 A4 offset, 100 (¥24,283) | **−¥19,186** | **−¥18,783** | **−¥20,783** | **−¥21,283** |
| Blurb 50 (¥7,706) | **−¥2,609** | **−¥2,206** | **−¥4,206** | **−¥4,706** |

**At cover ¥4,400:**

| Route (unit cost) | Direct ¥4,070 | Fair ¥4,400 | 委託 ¥2,800 | 買取 ¥2,400 |
|---|---|---|---|---|
| **China 500** (¥913) | **+¥3,157** | **+¥3,487** | **+¥1,887** | **+¥1,487** |
| **China 300** (¥1,320) | **+¥2,750** | **+¥3,080** | **+¥1,480** | **+¥1,080** |
| 栄光 digital, 100 (¥3,204) | +¥866 | +¥1,196 | **−¥404** | **−¥804** |
| China 100 (¥3,770) | +¥300 | +¥630 | **−¥970** | **−¥1,370** |
| 緑陽社 B5 offset, 500 (¥3,927) | +¥143 | +¥473 | **−¥1,127** | **−¥1,527** |
| 緑陽社 A4 offset, 500 (¥5,386) | **−¥1,316** | **−¥986** | **−¥2,586** | **−¥2,986** |
| 緑陽社 B5 offset, 300 (¥6,005) | **−¥1,935** | **−¥1,605** | **−¥3,205** | **−¥3,605** |
| Blurb 50 (¥7,706) | **−¥3,636** | **−¥3,306** | **−¥4,906** | **−¥5,306** |

> ### The three most important lines in this report
> 1. **The bookshop channel only works if landed unit cost is under roughly ¥1,500.** At 70掛 consignment, every route except **China at 300 or 500 copies** loses money on every copy a shop sells. (栄光 at ¥5,500 clears by ¥296/copy — technically positive, functionally zero.)
> 2. **Japanese offset A4 never works at a market cover price.** At 500 copies (¥5,386/copy) it *loses* ¥289 on every direct sale at ¥5,500. It only turns viable at ~1,000 copies (¥3,257/copy) — a ¥3.3M commitment.
> 3. **Japanese offset is viable at B5, at 500 copies, direct-sale only** (¥3,927/copy → +¥1,170 direct at ¥5,500). Choosing B5 over A4 is worth ~¥1,460 per copy.

### 6.3 Copies needed to recover the print run

Total outlay ÷ net revenue per copy. **Bold = impossible (exceeds the run itself).**

**At cover ¥5,500:**

| Route | Total outlay | All direct | All 委託 70掛 |
|---|---|---|---|
| **China 500** | ~¥457,000 | **90 copies (18% of run)** | **131 copies (26%)** |
| **China 300** | ~¥395,000 | **78 copies (26%)** | **113 copies (38%)** |
| **栄光 digital, 100** (B5, 96pp) | **¥320,390** | **63 copies (63%)** | **92 copies (92%)** |
| China 100 | ~¥377,000 | 74 copies (74%) | **108 — IMPOSSIBLE** |
| 緑陽社 B5 offset, 500 | ¥1,963,510 | 385 copies (77%) | **561 — IMPOSSIBLE** |
| 緑陽社 B5 offset, 300 | ¥1,801,590 | **354 — IMPOSSIBLE** | **515 — IMPOSSIBLE** |
| 緑陽社 A4 offset, 500 | ¥2,693,120 | **528 — IMPOSSIBLE** | **770 — IMPOSSIBLE** |
| 緑陽社 A4 offset, 100 | ¥2,428,290 | **477 — IMPOSSIBLE** | **694 — IMPOSSIBLE** |

**At cover ¥4,400:**

| Route | Total outlay | All direct | All 委託 70掛 |
|---|---|---|---|
| **China 500** | ~¥457,000 | **113 copies (23%)** | **164 copies (33%)** |
| **China 300** | ~¥395,000 | **97 copies (32%)** | **141 copies (47%)** |
| 栄光 digital, 100 | ¥320,390 | 79 copies (79%) | **115 — IMPOSSIBLE** |
| China 100 | ~¥377,000 | 93 copies (93%) | **135 — IMPOSSIBLE** |
| 緑陽社 B5 offset, 500 | ¥1,963,510 | 483 copies (97%) | **701 — IMPOSSIBLE** |
| 緑陽社 A4 offset, 500 | ¥2,693,120 | **662 — IMPOSSIBLE** | **962 — IMPOSSIBLE** |
| 緑陽社 A4 offset, 100 | ¥2,428,290 | **597 — IMPOSSIBLE** | **867 — IMPOSSIBLE** |

### 6.4 The fair booth, costed separately

TABF ZINE'S MATE Week 2, 900mm table = **¥16,500 fixed**, no commission on sales.

**Copies needed to cover the booth fee alone, at cover ¥5,500:**

| Route | Margin/copy at fair | Copies to cover ¥16,500 |
|---|---|---|
| China 500 (¥913) | ¥4,587 | **4 copies** |
| China 300 (¥1,320) | ¥4,180 | **4 copies** |
| 栄光 digital 100 (¥3,204) | ¥2,296 | **8 copies** |
| China 100 (¥3,770) | ¥1,730 | **10 copies** |
| 緑陽社 B5 offset 500 (¥3,927) | ¥1,573 | **11 copies** |
| 緑陽社 A4 offset 500 (¥5,386) | ¥114 | **145 copies — never** |
| 緑陽社 B5 offset 300 (¥6,005) | −¥505 | **never — loses money per copy** |

**Compare against the measured median fair sell-through of 20–25 copies (§3.5).**

- At **China 300/500 costs, the booth pays for itself in 4 copies** — the first hour.
- At **栄光 or China-100 costs it needs 8–10 copies** — comfortably inside the median.
- At **緑陽社 A4 offset costs, the booth can never pay for itself.** Selling *more* books at 300 copies B5 offset makes the loss larger, not smaller.

**Copies to recover print run + booth from fair sales alone, China 300 @¥5,500:** (¥395,000 + ¥16,500) ÷ ¥4,180 = **99 copies** ≈ **4–5 fairs at the median sell-through.**

### 6.5 What the arithmetic says, without interpretation

1. **At 100 copies, printing in Japan digitally beats importing from China.** 栄光 at **¥3,204/copy, tax and delivery included**, against China's ¥3,360–4,010 landed — and with no freight risk, no customs, and a ~2-week turnaround instead of 5–8. **The catch is the spec: B5 and 96 body pages, not A4 and 128.** If the book can live inside those limits, this is the cheapest real route to 100 copies that exists.
2. **Japanese *offset* is not a 100-copy process.** 緑陽社 A4 at 100 copies is **¥24,283/copy** — you are buying ¥2.36M of plates and getting 100 books out. At 500 copies the same plates yield ¥5,386/copy. **The total barely moves; only the divisor does.**
3. **300 copies from China is where the economics change character.** ¥1,230–1,400 landed against ¥6,005 for Japanese offset B5 — roughly **4.5×** — on a total outlay of ~¥395,000. Break-even is **78–97 copies of 300**, and **consignment becomes viable for the first time.**
4. **500 copies from China gives the best unit price** (¥860–920) and the **sea freight costs the same as at 300**. Break-even falls to 18–23% of the run. The cost is 500 hardcover books to store and sell.
5. **B5 versus A4 is worth ~¥1,460 per copy at 緑陽社** — a 33% saving at every tier. It is the largest single lever on the Japanese side, and it is a design decision, not a negotiation.
6. **A ¥4,400 cover price forecloses options that ¥5,500 keeps open.** At ¥4,400, 緑陽社 B5 offset at 500 clears just ¥143/copy direct and 栄光 goes negative on consignment. At ¥5,500 both become workable. **The ¥1,100 difference is worth more than it looks** — and §4 says the market bears it.
7. **Blurb never works as a resale product** at any realistic Japanese cover price — it loses ¥2,200–3,600 per copy at ¥5,500. It is a proofing and personal-copy tool.
8. **KDP's ¥2,756 is the cheapest print cost in the report** but buys a non-square, US-or-EU-printed book with no Japan hardcover marketplace, plus unpriced international shipping.
9. **Sell-through is the binding constraint, not unit cost.** Even the best route (China 500, direct, ¥5,500) needs **90 copies sold**. The measured median at a Japanese fair is **20–25 copies** (§3.5), and no reliable follower-conversion benchmark exists (§5.1). **The cost side of this model is far better evidenced than the revenue side** — that asymmetry is the honest headline of the whole report.

### 6.6 Three things to insist on in any quote

1. **Incoterm in writing.** Nearly every published Chinese price is EXW. At 100 copies the gap between EXW and landed is roughly a third of the total.
2. **Itemised Japan-side charges** — THC, CFS, D/O, 通関料, domestic delivery. Verified twice that destination charges meet or exceed the ocean freight, and two of those lines have **no published figure anywhere**.
3. **State that the goods are HS 4901, duty-free**, so no forwarder defaults a ≤¥200,000 shipment into the 5% simplified-tariff bucket.

---

## 7. One non-cost item flagged because it gates everything

**Student visa / 資格外活動許可 — genuinely unresolved, and not resolvable from public sources.**

The Immigration Services Agency's own wording covers **operating a business**, not merely wage employment: 「…アルバイトなど、**収入を伴う事業を運営する活動**又は報酬を受ける活動」 ([moj.go.jp](https://www.moj.go.jp/isa/applications/procedures/16-8.html), **DIRECT**). The 留学 page names **個人事業主** explicitly and caps activity at **28 hours/week**.

- ✅ **Likely inside** (INFERRED): sole-proprietor income within 28 hrs/week, no company, no employees.
- 🔴 **Clearly outside** (DIRECT — the brightest line found): 「新たに**法人を設立**する場合や**従業員を雇用**する場合、**事業所を設けて**活動する場合等は、…「**経営・管理**」の在留資格への変更が必要となります。」 **Incorporating, hiring, or taking premises requires a visa change.**
- ⚠️ **Genuinely ambiguous:** the blanket permission reaches sole-proprietor work **only where 稼働時間を客観的に確認することができる** — where hours can be objectively verified. The official worked example is delivery gig work, which timestamps every job. **An artist selling her own books does not obviously produce objectively verifiable hours.**

**On whether "artist selling her own work" is treated differently from a retail business: could not determine.** No official source draws that distinction, and **no artistic-practice carve-out could be located.** The intuition is reasonable but **is not supportable from what the sources actually say.**

**Customs does not appear to care about visa status** (nothing in the import procedures conditions importing on residence status) — **UNVERIFIED but no contrary evidence found.** **Clearing the goods is not the risk. Selling them for profit is.**

Free consultation exists: [外国人在留総合インフォメーションセンター](https://www.moj.go.jp/isa/consultation/center/index.html) / [FRESC](https://www.moj.go.jp/isa/support/fresc/fresc01.html). Note also that a **開業届** is required within one month of starting a business ([nta.go.jp](https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/shinkoku/annai/04.htm), DIRECT) — and filing one is the formal act of declaring oneself to be operating a business, which is the very question at issue.

---

## 8. Gaps — clearly marked, not filled

| # | Gap | Status |
|---|---|---|
| 1 | **Chinese-language direct-factory pricing** (1688, Alibaba, 知乎, 小红书) | **Largest hole in the report.** 1688/Alibaba JS-rendered and returned empty; Zhihu 403; Baidu/Sogou CAPTCHA. Matters most to her specifically — a Chinese-fluent negotiator should beat the broker prices quoted. |
| 2 | **Any TABF-specific solo sell-through figure** | **Genuinely absent, not merely un-found.** Searched note.com, Hatena, Yahoo Japan. TABF exhibitors write posts and omit numbers. |
| 3 | **Year-specific TABF attendance** | TABF publishes **no post-fair report**. Only "20,000+" boilerplate exists, likely from the free-admission era. |
| 4 | **TABF acceptance rate** | Never disclosed, by stated policy. |
| 5 | **Any sell-through evidence at the ¥3,000+ price point** | **Zero observations exist** in the reachable Japanese corpus. The ¥4,400–5,500 band is un-evidenced, not contraindicated. |
| 6 | **UTRECHT / Book and Sons / flotsam consignment terms** | **Verified absence** — none publishes anything. No first-hand account of consigning at any of the three was recoverable. They carry **no rate figure**, not a borrowed one. |
| 7 | ~~Japanese 500-copy hardcover pricing~~ | ✅ **CLOSED.** 緑陽社 publishes 30–10,000 copies (§1.4). An earlier pass wrongly concluded no such table existed. |
| 7b | **A 210×210 square hardcover at 100–150pp, at any published Japanese price** | **Does not exist.** Square softcover yes (冊子印刷工房); square hardcover only to 30–42 pages. **Quote-only object** — オリンピア and 三景印刷 will quote it. |
| 7c | **プリントオン's hardcover figures** | ⚠️ **CONTESTED.** One read produced the rows in §1.4; another could not resolve the table layout and declined; a third put the product range at 12P–76P / max 100冊. **Re-verify before relying on them.** Excluded from all §6 arithmetic. |
| 8 | **東京印書館 and the art-book specialist printers** | Quote-only, both in Japan (東京印書館, 藤原印刷, 山田写真製版所, イニュニック, 修美社, ライブアートブックス, 三景印刷) and China (Artron, Asia Pacific Offset, Everbest, 1010, C&C, Regal). **A market fact, not a research failure** — for a monograph these are the calls to place, and they will never appear in a spreadsheet. |
| 9 | **Blurb shipping to Japan; Lulu / IngramSpark / BookBaby unit costs** | Calculators behind login or 403. Blurb shipping is a material unpriced addition. |
| 10 | **Japanese THC, 通関料, NACCS requirement for an individual** | No published figures found. A circulating ¥11,800/declaration figure **could not be confirmed and is deliberately not quoted.** |
| 11 | **BASE 振込手数料 / 事務手数料** | Help pages unreachable. |
| 12 | **A second Japanese case pairing followers with copies sold** | Not found. **Takeuma is n=1.** |
| 13 | **COMITIA booth fee; Offprint & Unlimited Edition booth fees** | Not publicly posted. |
| 14 | **Whether her ~26k IG following is majority Japanese** | Not researched — but it materially changes §5.7 shipping economics and the applicability of the Takeuma comparable. **Knowable from her own Instagram insights.** |

**Method note.** WebSearch was exhausted session-wide (200/200 calls) before this research began, and the Firecrawl MCP returned 401 Unauthorized throughout. All findings came from direct WebFetch of official pages plus Brave and Yahoo! Japan results pages, both of which rate-limited (HTTP 429) heavily during the work. DuckDuckGo, Bing, Mojeek, Ecosia, Startpage, Baidu and Sogou were all blocked, CAPTCHA'd, or returned unusable results. **Several gaps above are tooling artefacts rather than true absences** — items 2, 3, 5 and 6 were tested hard enough to call real; items 1, 9, 10 and 13 would likely close in a session with working search.

**No figure, price or URL in this report was invented.** Every number is either read off a cited page (DIRECT), derived by a stated method from cited pages (INFERRED), or marked as not found.
