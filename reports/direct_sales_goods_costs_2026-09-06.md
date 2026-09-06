# Physical Merchandise in Short Runs — What It Actually Costs to Make in Japan

**Prepared 2026-09-06 for GEGYjiji (Nin), Tokyo.**
Research only. No advice, no strategy — figures and their sources.

**Companion to** `reports/book_economics_2026-09-05.md`, and it uses the same method. All prices **JPY**. Tax status is stated for every figure; where a source publishes 税込, that is what is quoted.

**Confidence tags:** **DIRECT** = read off a published price table or API · **INFERRED** = derived, interpolated or arithmetic on DIRECT figures (method stated) · **UNVERIFIED** = could not confirm · **ANECDOTE** = single named source, n=1.

**Nothing in this report is a guess.** Where a figure could not be obtained it is marked 🔴 with what was tried.

---

## 0. ⭐ SUMMARY — ranked by margin per unit of her effort

**"Effort" here is packing effort, because that is the part she cannot buy back.** Three classes, defined by what the object physically requires:

| Class | What it needs | Domestic postage | Time per order |
|---|---|---|---|
| **FLAT** | Envelope + backing board. Under 3cm, under 34×25cm. | **クリックポスト ¥185** (→ **¥240 from 2026-10-01**) | ~1–2 min |
| **SEMI** | Padded envelope or a soft-goods mailer; still no box | レターパックライト ¥430 / プラス ¥600 | ~3–4 min |
| **BOXED** | Box, tube, or bubble wrap. Fragile or oversized. | 宅急便コンパクト (¥70 box + distance fare) / ゆうパック | ~6–10 min |

**The single hardest physical constraint found: A3 does not fit anything cheap.** クリックポスト's envelope maximum is 34×25cm and レターパック is 34×24.8cm. A3 is 42×29.7cm. An A3 print therefore either gets folded (ruins it) or goes in a tube, which jumps it from ¥185 to a distance-priced parcel. **A4 is the ceiling of the flat, cheap class.** (Size limits DIRECT, japanpost / clickpost; the conclusion INFERRED.)

### The ranking

Unit cost is the **cheapest sourced route at 100 units, 税込**. Retail is the **BOOTH median for that product category** (DIRECT scrape, 2026-09-06, n=60 first-page listings — caveats in §9). Margin is retail − unit cost, **before** BASE fees and postage.

| # | Product | MOQ | Unit cost @100 | Indie retail (BOOTH median / p25–p75) | Gross margin @100 | Class | Why it ranks here |
|---|---|---|---|---|---|---|---|
| **1** | **Zine, B5 24pp full colour** | 10 | **¥498** | her own price **¥1,980**; BOOTH ZINE median ¥1,100 (¥800–1,500) | **¥1,482 (75%)** at her price | FLAT | Highest absolute margin that still posts for ¥185 |
| **2** | **Art print, A4** | 10 | **¥28** | アートプリント median ¥2,000 (¥500–6,290) | **¥472–1,972** | FLAT | ~99% margin, one envelope, one board |
| **3** | **Stickers (die-cut)** | 30 | **¥22.5** | ステッカー median ¥480 (¥330–1,000) | **¥458 (95%)** | FLAT | Near-zero packing; weightless; cheapest thing here to make |
| 4 | Acrylic keychain, 50mm | 5 | **¥242** | median ¥760 (¥600–1,000) | ¥518 (68%) | FLAT | Small, light, robust — but 9 business days and a white-plate step |
| 5 | Postcards | 10 | **¥17** | median ¥600 (¥300–990) | ¥283–583 | FLAT | Best margin *rate* in the report; worst **margin per order** if sold singly |
| 6 | Wall calendar, A3 7-sheet | 1 | **¥289.5** | 壁掛けカレンダー median ¥1,600 (¥1,000–2,000) | ¥1,310 (82%) | SEMI | Big margin, but a hard ~10-week selling window and dead stock in January |
| 7 | Mug | 1 | **¥540** | median ¥1,925 (¥1,200–2,150) | ¥1,385 (72%) | **BOXED** | Good money, bad logistics — fragile, heavy, breakage risk |
| 8 | Tote bag | 3 | **¥660** | median ¥1,915 (¥1,280–2,530) | ¥1,255 (66%) | SEMI | Soft, compressible, but bulky to store |
| 9 | Ring memo, A6 | 10 | **¥336** | リングメモ median ¥500 (¥300–800) | ¥164 (33%) | FLAT | Cheap to post, but the margin is thin in yen |
| 10 | Masking tape, 15mm×5m | 1 | **¥427** | median ¥600 (¥500–800) | ¥173 (29%) | FLAT | Lowest yen margin found. Cheap to post; still not worth the shelf |
| 11 | T-shirt | 1 | **¥1,500** | median ¥2,550 (¥2,000–2,750) | ¥1,050 (41%) | SEMI | Worst percentage **and** carries size inventory across 4 SKUs |

**Read across the table and one pattern dominates: every product in the top five is flat, and every product in the bottom four is either bulky or low-value.** The two variables move together — the things that are cheap to make are also cheap to post, and the things that pay well per unit (mug, tote, T-shirt) cost the most minutes.

**Two structural notes on the ranking:**

- **Postcards win on rate and lose on order size.** At ¥17 cost and ¥300 retail the *percentage* is unbeatable, but one postcard sold alone earns ¥283 and costs the same ~1–2 minutes and same ¥185–240 postage as a ¥1,980 zine. Postcards pay when they are bought **in fours or fives**, or bundled with something else. This is arithmetic on the figures below, **INFERRED**.
- **BASE takes ~6.6% + ¥40 per sale** ([thebase.com/price](https://thebase.com/price), DIRECT, carried from the book report §5.8). On a ¥300 postcard that is ¥60 — **21% of the sale price, and more than three times the print cost.** On a ¥1,980 zine it is ¥171 (8.6%). **The platform fee, not the printing, is what punishes cheap items.** INFERRED, arithmetic.

---

## 1. Method, and one large piece of plumbing worth recording

Most Japanese printers' price tables are JavaScript-rendered and return nothing to a plain fetch. Three data routes were opened and are **reproducible**; anyone repeating this work should start here rather than from the product pages.

| Route | How | What it unlocks |
|---|---|---|
| **おたクラブ** `otaclub.jp` | POST to `/wp-admin/admin-ajax.php` with `action=in2cart_get_price_ajax`, `post_id`, and the `#filter_box` field defaults scraped from the product page. `action=in2cart_price_any_number_ajax` (plus `token` from the inline `WD` object and a `delivery` id) prices **any** quantity. | ~249 products: paper, acrylic, apparel, tableware, booklets. Doujin printer, low MOQs, 税込 |
| **ラクスル** `raksul.com` | `GET /print/api/v1/md/products/<md_product_id>/prices` returns the **full quantity ladder as JSON**, tax-inclusive, with per-day pricing. `md_product_id` is embedded in the server-rendered `/print/<product>/prices?...` page | Posters, flyers, postcards, stickers, calendars — full ladders |
| **グラフィック** `graphic.jp` | `/price/<id>` **server-renders** the whole ladder when the product has a single default paper (masking tape, mug). Multi-paper products need the panel API `/ajax/priceselect_ajax/selecting` and usually a further selection step | Masking tape, mugs; partial elsewhere |

🔴 **Not opened — and each is a real hole:** **プリントパック** loads prices via `ajax/get_page.php` + `get_price4leaflet.php` and the parameter shapes were not resolved (endpoint reachable, returns `データベースの読み込みに失敗しました`). **東京カラー印刷** `tcpc.co.jp` renders `読み込んでいます` and its fetch path was not located. **しまや出版 / ちょ古っ都** were not reached in this pass. **SUZURI's** 原価 help page returns **403** to both a scripted fetch and WebFetch, so the largest Japanese POD platform's base costs are absent.

🔴 **`canvath.jp` does not resolve** (DNS `getaddrinfo failed`, 2026-09-06). Canvath is now **pixivFACTORY** at `factory.pixiv.net`, which does publish full lot ladders — used throughout below as the POD comparator. **This is worth correcting wherever the pipeline holds the old domain.**

**Browser automation was unavailable** this session (the Claude-in-Chrome extension reported not connected), and **Firecrawl returned `Unauthorized: Invalid token`** — so JS-rendered tables had to be reached by finding their APIs or not at all.

---

## 2. Art prints

### 2.1 The cheapest honest route is a *flyer*, not a *poster*

Japanese net printers do not sell A4 "posters". They sell A4 **フライヤー/チラシ** — the identical object, sheet-fed offset on coated stock, at a fraction of the poster price. **ラクスル publishes no poster below A3.**

**ラクスル, 税込, 全国送料無料, cheapest business-day tier.** All **DIRECT** from the price API.

| Spec | 10 | 50 | 100 | 300 | 500 | 1,000 |
|---|---|---|---|---|---|---|
| **A4 flyer, coat 135kg, 片面カラー** (`md_product_id` 426) | ¥1,194 (**@119**) | ¥1,988 (**@40**) | ¥2,829 (**@28**) | ¥3,285 (**@11**) | ¥3,577 (@7.1) | ¥6,464 (@6.4) |
| A4 flyer, coat 90kg, 両面カラー (id 1) | ¥977 (@98) | ¥1,399 (@28) | ¥2,048 (@20) | ¥2,655 (@8.8) | ¥3,272 (@6.5) | ¥3,902 (@3.9) |
| **A3 flyer, coat 135kg, 両面カラー** (id 700) | ¥3,957 (**@396**) | ¥5,524 (**@110**) | ¥8,382 (**@84**) | ¥11,695 (**@39**) | ¥13,510 (@27) | ¥17,986 (@18) |
| **A3 poster, offset, coat 135kg, 片面カラー** (id 13469) | — MOQ 100 — | — | **¥6,380 (@63.8)** | ¥7,024 (**@23.4**) | ¥8,104 (@16.2) | ¥12,623 (@12.6) |
| A3 poster, **on-demand**, photo-coat 200kg (id 13474) | ¥5,219 (**@522**) | — caps at 30 — | — | — | — | — |

⚠️ **The on-demand-to-offset cliff at A3 is the sharpest curve in this report: ¥522/sheet at 10 copies, ¥63.8 at 100.** An eightfold drop for crossing the offset MOQ. Below 100 copies, A3 is a ¥500-a-sheet object; at and above it, a ¥64 one.

⚠️ Coat 90kg is flyer paper and will read as flyer paper. **Coat 135kg is the lowest weight that behaves like a print**; the A4 135kg row is the one to use. Heavier stocks exist and were not priced (🔴).

### 2.2 Giclée — a different product with different economics

**日精アート倶楽部** — [nspr.co.jp/art-club/giclee/price.html](https://www.nspr.co.jp/art-club/giclee/price.html), **DIRECT, 税別.**

| Item | Price |
|---|---|
| **First output (setup incl. scanning/colour), F8/B3 and under** | **¥17,000** (Moro paper) · ¥19,500 (natural cotton) |
| First output, F20/B2 and under | ¥22,000 · ¥26,000 |
| **Reprint, F3/A4** | **¥2,300** photo canvas/paper · ¥2,800 Moro · ¥4,500 satin canvas |
| **Reprint, F6/A3** | **¥3,500** · ¥4,000 · ¥5,500 |
| Reprint, F8/B3 | ¥4,500 · ¥5,000 · ¥7,000 |
| Digital photography of the artwork | 基本料金 1点 ¥5,000〜 |

**No quantity discount is published; reprints are priced per copy from 1.** So a 10-copy A4 giclée edition is roughly ¥17,000 + 9 × ¥2,300 = **¥37,700 税別, ¥4,190/copy** (INFERRED, arithmetic on the DIRECT table). That is **150× the offset A4 unit cost at 100** — giclée is an *editioned artwork* priced like an artwork, not a merchandise line.

🔴 **グラフィック's ジークレー service publishes no price at all** ([graphic.jp/lineup/giclee](https://www.graphic.jp/lineup/giclee), verified absence — order and enquiry forms only). Quote-only, like the art-book trade printers in the book report.

### 2.3 Risograph — cheap in short runs, and the arithmetic shows exactly where

**石引パブリック** — [ishipub-printing.com/risograph_printing/price/](https://ishipub-printing.com/risograph_printing/price/), **DIRECT, 税抜.**

**Formula: 色数(版) × setup + (印刷・用紙代 × 枚数) + 加工費.**

| Component | Price |
|---|---|
| Setup per colour, normal ink | **¥1,000／1色（版）** |
| Setup per colour, special ink | ¥1,500 |
| 断裁 (トンボ, full-bleed) | ¥400 / 100枚 |
| 断裁 (standard trim) | ¥200 / 100枚 |
| 角丸 | ¥20 / 枚 |
| ラミネート | B5 ¥350 · A4 ¥400 |

**Print + paper, per sheet (DIRECT excerpt):**

| Paper | B5 | A4 | B4 | A3 |
|---|---|---|---|---|
| わらばん紙 (更紙) 49g/m² | ¥4 | ¥5 | ¥8 | ¥10 |
| 書籍用紙 薄口 64g/m² | ¥6 | ¥9 | ¥12 | ¥18 |
| 色上質紙 60kg / 書籍用紙 中厚口 | ¥8 | ¥10 | ¥16 | ¥20 |
| **上質紙 最厚口 135kg** | **¥12** | **¥15** | **¥24** | **¥30** |
| モンテシオン 70.5kg | ¥15 | ¥18 | ¥30 | ¥36 |
| ブンペル / ファーストビンテージ | ¥40 | ¥60 | ¥80 | ¥120 |

**Derived cost of a 2-colour riso print on 上質135kg — INFERRED, arithmetic on the DIRECT table, 税抜, before trimming:**

| Size | 10 | 50 | 100 | 300 |
|---|---|---|---|---|
| **A4** (setup ¥2,000 + ¥15/sheet) | ¥2,150 (**@215**) | ¥2,750 (**@55**) | ¥3,500 (**@35**) | ¥6,500 (**@21.7**) |
| **A3** (setup ¥2,000 + ¥30/sheet) | ¥2,300 (**@230**) | ¥3,500 (**@70**) | ¥5,000 (**@50**) | ¥11,000 (**@36.7**) |

**Where riso actually wins: A3 at 10–50 copies.** ¥230/sheet against ¥396 (offset flyer) and ¥522 (on-demand poster) at 10 copies. Above ~100 copies offset overtakes it. **Riso is the short-run A3 answer, and it is also the only route here that gives a visibly hand-made surface** — which is a different product, not a cheaper version of the same one.

**Hand Saw Press (Tokyo)** — [handsawpresstokyo.com/riso-print.html](https://handsawpresstokyo.com/riso-print.html), **DIRECT:** self-print studio, **利用料 ¥2,000/h** plus 印刷費 + 紙代 + tax. Sizes B5/A4/B4/A3 (postcard size for 1-colour only), or 100×246mm–320×432mm. Paper 46–210g/m², uncoated only. 🔴 **Their per-sheet print-cost list is on external linked sheets that were not retrieved** — only the fee structure is confirmed.

**21print** — [21print.jp/料金表/](https://21print.jp/%E6%96%99%E9%87%91%E8%A1%A8/), **DIRECT, 税込・送料無料:** B5 1色片面 **¥5.2/枚 at 500+**, ¥4.5 at 1,000+; 2色 currently charged at 1色 rates. ⚠️ **Minimum order 500 sheets** ("500枚未満のご注文は500枚の料金となります"), copy paper only unless you supply your own. This is a duplicator-print shop, not an artist riso studio — a useful floor, not a comparable.

### 2.4 POD comparator — pixivFACTORY

[factory.pixiv.net/products/fast_poster](https://factory.pixiv.net/products/fast_poster), **DIRECT, 税込, MOQ 1, ~1 business day, all papers same price:**

| B3 | A2 | B2 | A1 | B1 |
|---|---|---|---|---|
| ¥1,280 | ¥1,400 | ¥1,890 | ¥2,550 | ¥3,180 |

⚠️ **No A3 and no A4.** B3 (370×521mm) is the smallest. So the POD platform cannot make the size that actually posts cheaply.

---

## 3. Postcards

**ラクスル, offset, アートポスト180kg, 両面カラー** (`md_product_id` 26642) — **DIRECT, 税込, 送料無料:**

| 10 | 20 | 30 | 50 | 100 | 200 | 300 | 500 | 1,000 |
|---|---|---|---|---|---|---|---|---|
| ¥997 (**@99.7**) | ¥1,565 (@78) | ¥1,607 (@53.5) | ¥1,743 (**@34.8**) | **¥1,701 (@17.0)** | ¥1,881 (@9.4) | **¥2,059 (@6.9)** | ¥2,833 (@5.7) | ¥3,609 (@3.6) |

⚠️ **Note the row that is not monotonic: 100 copies (¥1,701) is CHEAPER than 50 (¥1,743)** — because the 100 tier reaches a 7-business-day plate schedule the 50 tier cannot. **Ordering 50 is strictly worse than ordering 100.** DIRECT from the API, both figures verified.

**おたクラブ, offset, ボンアイボリー180kg, フルカラー両面** — **DIRECT, 税込, 10営業日発送, ships via Yamato at ¥600–1,200 by region (DIRECT, not included above):**

| 50 | 100 | 300 | 1,000 | 10,000 |
|---|---|---|---|---|
| ¥1,400 (@28) | ¥1,800 (@18) | ¥4,200 (@14) | ¥10,500 (@10.5) | ¥100,500 (@10.05) |

**おたクラブ, on-demand, ボンアイボリー180kg, 両面** — **DIRECT, 税込, 4営業日, MOQ 30:** 30 ¥1,500 (@50) · 50 ¥2,500 (@50) · 100 ¥3,500 (@35) · 300 ¥9,000 (@30) · 500 ¥12,500 (@25) · 1,000 ¥25,000 (@25).

**Other routes:**

| Source | Figure | Confidence |
|---|---|---|
| **コミグラ (グラフィック同人)** [graphic.jp/comic/lineup/postcard](https://www.graphic.jp/comic/lineup/postcard) | **最小ロット 10枚**; 100枚 ¥2,680〜 (100×148mm, コート180kg, 両面フルカラー, offset or on-demand); 送料全国一律 ¥350 | DIRECT |
| グラフィック campaign | 100部 ¥2,680 → **¥1,470** during the 名刺・ポストカード最大45%OFF campaign | DIRECT ([campaign/card_discount](https://www.graphic.jp/campaign/card_discount)) |
| **WAVE** [wave-inc.co.jp/products/hagaki](https://www.wave-inc.co.jp/products/hagaki/) | offset 100部 **¥4,807〜** (コート180kg, 両面, 7営業日); on-demand **50部 ¥5,368 (@107.36)**, MOQ 50; 税込, 送料無料 | DIRECT |
| **東京カラー印刷** [tcpc.co.jp](https://www.tcpc.co.jp/price_tables/index/%E3%83%9D%E3%82%B9%E3%83%88%E3%82%AB%E3%83%BC%E3%83%89%EF%BC%88%E3%81%AF%E3%81%8C%E3%81%8D%EF%BC%89/100%C3%97148mm) | **MOQ 100枚**, up to 50,000; 税込; 送料無料 even under ¥1,000 | DIRECT (spec only — 🔴 price table is JS-only and was not reached) |
| **pixivFACTORY (POD)** [products/postcard](https://factory.pixiv.net/products/postcard) | **10枚から**; ヴァンヌーボVG 195kg ¥2,300 · **マットコート220kg ¥1,835** · 竹はだGA 180kg ¥1,970, 税込, ~1営業日 | DIRECT for the prices; ⚠️ **the page does not label whether these are per-sheet or per-10-sheet lot.** Read alongside "10枚から印刷できます" they are almost certainly the 10-sheet lot (≈¥184/card) — **INFERRED, and worth confirming before use** |

**The shape:** postcards are the cheapest thing in this report to manufacture and among the most expensive to *sell*, because BASE's ¥40 flat fee and ¥185–240 postage do not shrink with the item.

---

## 4. Stickers

**おたクラブ, 定型ダイカットシール, 丸・中サイズ, キャストコート** — **DIRECT, 税込, 9営業日, MOQ 30:**

| 30 | 50 | 100 | 300 | 1,000 | 3,000 |
|---|---|---|---|---|---|
| ¥900 (@30) | ¥1,350 (@27) | **¥2,250 (@22.5)** | **¥6,300 (@21)** | ¥18,000 (@18) | ¥45,000 (@15) |

🔴 The physical dimensions behind 「丸 中サイズ」 were not captured — the size table is a separate JS panel. Treat the size as unconfirmed.

**ラクスル, on-demand sheet, 50×50mm, アート紙, 標準糊, 角型カット** (`md_product_id` 57530) — **DIRECT, 税込, 送料込:**

| 1 | 10 | 30 | 50 | 100 | 300 | 500 | 1,000 |
|---|---|---|---|---|---|---|---|
| ¥1,063 | ¥1,447 (@145) | ¥1,859 (@62) | ¥2,219 (@44) | ¥2,690 (**@26.9**) | ¥4,620 (**@15.4**) | ¥6,435 (@12.9) | ¥11,886 (@11.9) |

**pixivFACTORY (POD), ロット製造価格, 税込** — [products/sticker](https://factory.pixiv.net/products/sticker), **DIRECT, ~10営業日:**

| 枚数 | White 100×100mm | White 160×160mm | Clear 100×100mm | Clear 160×160mm |
|---|---|---|---|---|
| 1〜 | ¥670 | ¥740 | ¥720 | ¥770 |
| 10〜 | ¥640 | ¥710 | ¥700 | ¥740 |
| 20〜 | ¥410 | ¥590 | ¥420 | ¥570 |
| 30〜 | ¥340 | ¥460 | ¥380 | ¥530 |
| **50〜** | **¥290** | ¥420 | ¥350 | ¥490 |

⚠️ **pixivFACTORY's sticker is 10× the size of ラクスル's 50mm sample and ~11× the unit cost at 100.** These are not the same object; the comparison to make is size-for-size, and it was not possible to price a 100×100mm sticker at ラクスル in this pass (🔴).

**グラフィック** sells both シール印刷 and ステッカー印刷 across ~20 substrates each ([/price/1891](https://www.graphic.jp/price/1891), [/price/4751](https://www.graphic.jp/price/4751)) — **🔴 both require a substrate selection before a ladder renders, and the panel API needed a further step that was not resolved.**

---

## 5. Calendars

**おたクラブ, 組立カレンダー (desk), ケンラン スノー, 黒リング** — **DIRECT, 税込, 9営業日, MOQ 10:**

| 10 | 50 | 100 | 300 | 500 | 1,000 |
|---|---|---|---|---|---|
| ¥2,700 (@270) | ¥13,500 (@270) | **¥22,000 (@220)** | ¥66,000 (@220) | ¥100,000 (@200) | ¥200,000 (@200) |

⚠️ **The curve is almost flat** — ¥270 at 10, ¥200 at 1,000. Calendars are assembly-cost dominated, so scale buys almost nothing. **This is the opposite of every print product above**, and it means a 10-copy calendar is a perfectly rational thing to make.

**ラクスル, 卓上カレンダー 13ページ, CDジャケットサイズ, コート135kg, 片面カラー** (`md_product_id` 634314) — **DIRECT, 税込, 6営業日, MOQ 100:** 100 ¥52,401 (**@524**) · 300 ¥86,991 (@290) · 500 ¥120,528 (@241) · 1,000 ¥204,495 (@204).

**グラフィック 壁掛けカレンダー** — [graphic.jp/lineup/wall_calendar](https://www.graphic.jp/lineup/wall_calendar), **DIRECT for the 100-copy reference prices:**

| Type | MOQ | 100部 | Spec |
|---|---|---|---|
| **ハンガーカレンダー (ring)** | **1** | **¥28,950 (@289.5)** | A3, 7 sheets, コート110kg, 7日 |
| 中綴じカレンダー | 100 | ¥50,540 (@505) | S size, 16pp, コート110kg, 7日 |
| 金具付カレンダー | 100 | ¥92,450 (@924) | A3, 7 sheets, 10日 |
| タンザックカレンダー | 10 | ¥57,900 (@579) | A4, 7 sheets, 13日 |
| タンザック3ヶ月 | 10 | ¥76,900 (@769) | A2, 5 sheets, 13日 |

🔴 **The グラフィック ladder below and above 100 copies could not be read** — the wall-calendar lineup page carries no `/price/` links at all, and the panel API path was not found. Only the published 100-copy reference prices are DIRECT.

🔴 **Seasonal selling window — GAP, deliberately left open.** No published Japanese data on when indie calendars sell (share of sales by month, cut-off date, sell-through) was found. Searches for 販売時期/売れる時期 data returned only vendor marketing copy with no numbers behind it. **The obvious structural facts — a calendar for year N is worthless after roughly February of year N, and printers here quote 6–14 business days — are true but are not a measured selling window, and no figure is offered in their place.** What *is* DIRECT and relevant: **at ¥220–290/unit with an almost flat cost curve, a small print run carries very little dead-stock risk.**

---

## 6. Apparel, tableware and acrylic

All **おたクラブ, DIRECT, 税込, 9営業日 unless noted**, plus Yamato shipping ¥600–1,200 by region.

| Product | Spec | 1 | 10 | 30 | 50 | 100 | 300 | 1,000 |
|---|---|---|---|---|---|---|---|---|
| **Canvas tote** | DTF print, MOQ 3 | (3 for ¥2,370, @790) | ¥7,580 (@758) | ¥20,790 (@693) | ¥34,650 (@693) | **¥66,000 (@660)** | ¥198,000 (@660) | @660 |
| **T-shirt** | front print, M | ¥1,800 | ¥17,250 (@1,725) | — | ¥86,250 (@1,725) | **¥150,000 (@1,500)** | ¥450,000 (@1,500) | @1,500 |
| **Mug** | white, 6営業日 | ¥860 | ¥7,020 (@702) | ¥17,820 (@594) | ¥29,700 (@594) | **¥54,000 (@540)** | ¥162,000 (@540) | @540 |
| **Acrylic keychain 50mm** | 両面印刷, 透明クリア, シルバーナスカン, MOQ 5 | (5 for ¥2,200, @440) | ¥2,970 (@297) | ¥8,580 (@286) | ¥13,200 (@264) | **¥24,200 (@242)** | ¥72,600 (@242) | ¥231,000 (@231) |
| **Acrylic stand 60mm** | 両面印刷, 透明クリア, MOQ 5 | (5 for ¥2,500, @500) | ¥3,370 (@337) | ¥9,750 (@325) | ¥15,000 (@300) | **¥27,500 (@275)** | — | @262.5 |

**グラフィック mug** ([/price/2392](https://www.graphic.jp/price/2392) and ミニマグ [/price/2394](https://www.graphic.jp/price/2394), identical prices) — **DIRECT, MOQ 1:** 1 ¥1,100 · 5 ¥4,300 (@860) · 10 ¥8,300 (@830) · 30 ¥24,300 (@810) · **50 ¥36,300 (@726)** · **100 ¥66,300 (@663)**. **おたクラブ is ~19% cheaper at 100** (¥540 vs ¥663).

**pixivFACTORY POD comparators — DIRECT, 税込, MOQ 1:**

| Product | Price |
|---|---|
| **Acrylic keychain 50mm** ([/acrylic_key_chain](https://factory.pixiv.net/products/acrylic_key_chain)) | 1 ¥1,390 · 10 ¥1,110 · 20 ¥1,050 · 30 ¥950 · 50 ¥810 · **100 ¥760** · 300 ¥700 · 500 ¥670 · 1,000 ¥560 |
| Acrylic keychain 70mm | 1 ¥1,650 · 50 ¥970 · 100 ¥940 · 1,000 ¥690 |
| Acrylic keychain 100mm | 1 ¥1,980 · 50 ¥1,360 · 100 ¥1,200 · 1,000 ¥990 |
| **Tote bag** ([/tote_bag](https://factory.pixiv.net/products/tote_bag), 5営業日) | S (300×200, マチ100) **¥920** · M ¥1,020–1,530 · L ¥1,220–1,730 |
| Eco bag | ¥1,250 |

> ⭐ **The largest single cost gap found anywhere in this report: an acrylic keychain at 100 units costs ¥242 at おたクラブ and ¥760 at pixivFACTORY — 3.1×.** POD buys zero inventory risk and MOQ 1; it does not buy a competitive unit cost. At the ¥760 BOOTH median retail, POD leaves **¥0 margin** on a 50mm keychain. **DIRECT both sides.**

Same comparison for totes: おたクラブ ¥660 at 100 vs pixivFACTORY ¥920 at 1 — only **1.4×**, because the tote is a bought-in blank either way and the print is the small part.

---

## 7. Notebooks, memo pads, masking tape

**おたクラブ リングメモ A6** (縦型, サンカード+ 360kg クリアPP, 本文モノクロ) — **DIRECT, 税込, 7営業日, MOQ 10:**

| 10 | 30 | 100 | 300 | 500 | 1,000 |
|---|---|---|---|---|---|
| ¥5,600 (@560) | ¥12,600 (@420) | **¥33,600 (@336)** | ¥92,400 (@308) | ¥140,000 (@280) | ¥280,000 (@280) |

🔴 The 50-unit price was not queried; it sits between ¥420 and ¥336.

**グラフィック マスキングテープ 15mm×5m** ([/price/4399](https://www.graphic.jp/price/4399), マスキングシール, 納期10日) — **DIRECT, full 140-row ladder, MOQ 1:**

| 1 | 5 | 10 | 20 | 30 | 50 | 100 | 200 | 300 | 500 |
|---|---|---|---|---|---|---|---|---|---|
| ¥1,020 | ¥3,860 (@772) | ¥7,410 (@741) | ¥12,110 (@606) | ¥16,810 (@560) | ¥26,210 (@524) | **¥42,710 (@427)** | ¥66,710 (@334) | **¥90,710 (@302)** | ¥134,710 (@269) |

Widths 15/20/25/30/40/50mm and lengths 5m/10m are offered ([lineup/masking_tape](https://www.graphic.jp/lineup/masking_tape), price ids 4399–4415); only the 15mm×5m ladder was pulled. Sheet type also exists in A7–A3.

**Secondary masking-tape market data (search-derived, sources named but pages not read — ANECDOTE, do not treat as quotes):** mt's *my mt FACTORY* MOQ 100 at ¥128–87; ミライテープ MOQ 150 from ¥160 税込; 販促ドットコム from 50 units; 三森特殊印刷 digital from 10 rolls. **These undercut グラフィック's ¥427 substantially and should be checked directly before any conclusion — a 🔴 on the cheap end of this market.**

**グラフィック 中綴じノート** (B6, 28ページ, [/price/2991](https://www.graphic.jp/price/2991)) exists with 11 paper choices — **🔴 the ladder needs a paper selection the panel API would not render.**

**Verdict from the figures above:** masking tape at ¥427/unit against a ¥600 BOOTH median, and a ring memo at ¥336 against ¥500, are **the two thinnest margins in the report.** Both are cheap to post — which is exactly why the yen margin matters more than the class does.

---

## 8. Zines

Her existing zine sells at **¥1,980**. Here is what a run costs.

**おたクラブ 中綴じ B5, 24ページ, 本文フルカラー** — cover ボンアイボリー180kg, body コート110kg, PP加工なし, 遊び紙なし, 左綴じ — **DIRECT, 税込, MOQ 10:**

| Delivery | 10 | 30 | 50 | 100 | 300 | 1,000 | 2,000 |
|---|---|---|---|---|---|---|---|
| **13営業日** | ¥7,700 (**@770**) | ¥19,020 (@634) | ¥29,440 (@589) | **¥49,830 (@498)** | **¥135,900 (@453)** | ¥430,350 (@430) | ¥815,400 (@408) |
| 10営業日 | ¥8,470 (@847) | ¥20,920 (@697) | ¥32,380 (@648) | ¥54,810 (@548) | ¥149,490 (@498) | ¥473,380 (@473) | ¥896,940 (@448) |

⚠️ **Rushing from 13 to 10 business days costs 10%.** DIRECT, both ladders published side by side.

**At her ¥1,980 price and a 100-copy run: ¥498 cost, ¥1,482 gross margin, 75%.** After BASE (6.6% + ¥40 = ¥171) that is **¥1,311 net before postage** — and the object posts flat for ¥185 (→¥240). **INFERRED, arithmetic on DIRECT figures.**

⚠️ **The page count is an assumption.** 24pp full colour is the priced spec; her actual zine may differ, and the ladder is steeply page-sensitive. The おたクラブ 中綴じ product caps at **32 pages** (options: 8/12/16/20/24/28/32) — **anything longer becomes 無線綴じ and a different price table** (🔴 not pulled). The book report covers the larger-book economics.

**BOOTH ZINE/画集 median is ¥1,100 (p25 ¥800, p75 ¥1,500, n=59)** — **her ¥1,980 sits above the 75th percentile of that sample.** DIRECT scrape; caveats in §9.

---

## 9. What comparable work actually sells for

**Method: a direct scrape of BOOTH search results, 2026-09-06** (`booth.pm/ja/search/<term>`, `data-product-price` attributes, first results page, n=60 per term). **DIRECT** for what the listings say.

| Search term | n | p25 | **median** | p75 | min | max |
|---|---|---|---|---|---|---|
| ポストカード | 60 | ¥300 | **¥600** | ¥990 | ¥100 | ¥11,000 |
| ステッカー | 60 | ¥330 | **¥480** | ¥1,000 | ¥110 | ¥5,000 |
| アートプリント | 60 | ¥500 | **¥2,000** | ¥6,290 | ¥100 | ¥20,000 |
| アクリルキーホルダー | 60 | ¥600 | **¥760** | ¥1,000 | ¥110 | ¥2,980 |
| 壁掛けカレンダー | 60 | ¥1,000 | **¥1,600** | ¥2,000 | ¥550 | ¥3,800 |
| マグカップ イラスト | 60 | ¥1,200 | **¥1,925** | ¥2,150 | ¥100 | ¥5,000 |
| トートバッグ イラスト | 60 | ¥1,280 | **¥1,915** | ¥2,530 | ¥480 | ¥6,500 |
| Tシャツ イラスト | 60 | ¥2,000 | **¥2,550** | ¥2,750 | ¥100 | ¥7,800 |
| マスキングテープ | 60 | ¥500 | **¥600** | ¥800 | ¥100 | ¥2,060 |
| リングメモ | 60 | ¥300 | **¥500** | ¥800 | ¥100 | ¥4,950 |
| ZINE 画集 | 59 | ¥800 | **¥1,100** | ¥1,500 | ¥180 | ¥3,500 |

⚠️ **Four caveats, and they are not small.** (1) These are **asking prices, not sales** — nothing here says anything sold. (2) The samples **mix singles with sets and bundles**, which is why the postcard median (¥600) sits well above the single-card price. (3) They mix sizes; the アートプリント spread (¥100–20,000) is a category, not a product. (4) First page only, BOOTH's own relevance ordering.

**Independent cross-check for postcards, and it is the more useful number:** 「多くのアートギャラリーやイベントでは、ポストカードが**150円から200円**で販売されているのを目にします」 and a recommendation to consider 「**250円から500円**といった価格帯」 — [artlib.biz/column/2934](https://artlib.biz/column/2934/), **ANECDOTE**, author Nagaoka Yoshiharu, stating ten years running art events and department-store gallery spaces. **This is a named practitioner's observation, not measured market data**, but it brackets the BOOTH p25 (¥300) sensibly and is the reason ¥300 rather than ¥600 is used in §0.

**minne, same day, same method** (`price` fields in the category pages): ポストカード median **¥500** (p25 ¥300, n=70) · ステッカー median **¥990** (p25 ¥550, n=82) · イラスト category median **¥4,250** (p25 ¥2,500, n=86, includes originals). Same caveats. **minne's search and most of its category slugs are client-rendered and could not be scraped** (🔴), so this is three categories, not a survey.

---

## 10. Postage — domestic

All **税込**.

| Service | Price | Limits | Confidence |
|---|---|---|---|
| **クリックポスト** | **¥185 — rising to ¥240 on 2026-10-01** | ≤1kg, **≤3cm**, 34×25cm max, 14×9cm min; postbox-droppable, tracked | **DIRECT** — [clickpost.jp](https://clickpost.jp/): 「2026年10月1日（木）より、クリックポストの運賃を185円(税込)から240円(税込)に改定します」 |
| **ゆうパケット** | **1cm ¥250 · 2cm ¥310 · 3cm ¥360** | ≤1kg, ≤3cm | **DIRECT** — [japanpost yu-packet](https://www.post.japanpost.jp/service/send/domestic/delivery/yu-packet/) |
| **レターパックライト** | **¥430** | 340×248mm (A4), **≤3cm**, ≤4kg | **DIRECT** — [japanpost letterpack](https://www.post.japanpost.jp/service/letterpack/) |
| **レターパックプラス** | **¥600** | Same envelope, **no thickness limit**, ≤4kg, hand-delivered with signature | **DIRECT** |
| 宅急便コンパクト | **専用BOX ¥70** + a distance-based fare; 薄型BOX also ¥70; 専用薄型 sleeve ¥80 | BOX 25×20×5cm (inner 24.7×19.3×4.7cm); 薄型 34×24.8cm | Box price **DIRECT** ([kuronekoyamato compact](https://www.kuronekoyamato.co.jp/ytc/customer/send/services/compact/)); 🔴 **the fare itself is a JS calculator and was not read** |
| Yamato 宅急便, as a real inbound reference | 近畿 ¥600 · 関東/信越/中部/北陸/東海/中国 ¥700 · 九州 ¥800 · 東北 ¥900 · 北海道/四国 ¥1,200 | — | **DIRECT** — おたクラブ's own published delivery table |
| **ネコポス** | **⚠️ Not directly available to a private seller.** Individual use continues only through flea-market/auction platforms contracted with Yamato; **クロネコゆうパケット is restricted to Yamato-contracted 法人・団体・個人事業主** | ≤1kg, ≤2.5–3cm | **UNVERIFIED — search-derived summary of secondary logistics blogs, no primary Yamato page read.** ⚠️ The brief assumed ネコポス was an option; **it may not be one for her, and this should be confirmed before relying on it** |
| 定形外郵便 規格内 | 🔴 **not fetched** — the japanpost URL tried returned 404 | ≤1kg, ≤3cm, ≤34×25cm | 🔴 |

> ⭐ **The most consequential domestic finding: クリックポスト goes from ¥185 to ¥240 on 2026-10-01 — a 30% rise, three and a half weeks from this report's date.** Every flat product's shipping economics shift on that date. On a ¥300 postcard the postage goes from 62% to 80% of the sale price.

**Thickness is the whole game.** Under 3cm: ¥185 (¥240 from October). Over 3cm: ¥600 (レターパックプラス) or a parcel fare. **A 3.2× step for one centimetre.**

---

## 11. Postage — international, for light items

**小形包装物 (Small Packet), 航空便, per japanpost's zone rate tables.** All **DIRECT**, fetched 2026-09-06 from `post.japanpost.jp/int/charge/list/normal{1,2,3,4}.html`. This extends §5.7 of the book report downward from its 1kg row; the 1.0kg figures below match that report exactly, which cross-validates the zone identification (Europe = 第3地帯, USA = 第4地帯).

| Weight | **Zone 1** (China/Korea/Taiwan) | Zone 2 | **Zone 3** (Europe) | **Zone 4** (USA) |
|---|---|---|---|---|
| **≤100g** | **¥350** | ¥380 | **¥510** | **¥830** |
| ≤200g | ¥450 | ¥500 | ¥690 | ¥1,040 |
| ≤300g | ¥550 | ¥620 | ¥870 | ¥1,250 |
| ≤400g | ¥650 | ¥740 | ¥1,050 | ¥1,460 |
| ≤500g | ¥750 | ¥860 | ¥1,230 | ¥1,670 |
| ≤1.0kg | ¥1,250 | ¥1,460 | ¥2,130 | ¥2,720 |
| ≤2.0kg (max) | ¥2,250 | ¥2,660 | ¥3,930 | ¥4,820 |

**The step per 100g is constant within a zone: ¥100 (Z1) · ¥120 (Z2) · ¥180 (Z3) · ¥210 (Z4).** Every zone's table is linear above 100g.

**Small Packet limits — DIRECT** ([small_packing.html](https://www.post.japanpost.jp/service/send/oversea/list/delivery/small_packing.html)): max **2kg**; **length + width + thickness = 90cm, length max 60cm**; **rolls: length + 2× diameter = 104cm, length max 90cm**; minimum 14.8×10.5cm. **An A3 print in a tube (roughly 35cm long, 6cm diameter → 47cm) is comfortably inside the roll allowance** — the constraint on tubes is domestic, not international.

**Cheaper alternatives for flat paper, DIRECT from the same tables:**

| Service | Zone 1 | Zone 2 | Zone 3 | Zone 4 |
|---|---|---|---|---|
| **印刷物 (Printed Matter), ≤50g** | **¥180** | ¥180 | ¥250 | ¥250 |
| 印刷物, ≤100g | ¥290 | ¥290 | ¥390 | ¥390 |
| 印刷物, ≤200g | ¥410 | ¥410 | ¥600 | ¥600 |
| **はがき (postcard)** | **¥100 flat, worldwide** | ¥100 | ¥100 | ¥100 |
| 手紙 定形外, ≤50g | ¥230 | ¥230 | ¥280 | ¥280 |

> ⭐ **印刷物 rate is ¥180–250 for up to 50g worldwide — half to a third of the Small Packet rate at the same weight.** A few postcards or a flat A4 print plausibly qualify as Printed Matter. ⚠️ **The eligibility rules for 印刷物 (what counts as printed matter, whether goods sold commercially qualify, what may be enclosed) were NOT verified in this pass — 🔴.** This is potentially the largest single saving available on international orders and it is **unconfirmed.**

**Worked weights — INFERRED, calculated from paper weight × sheet area, no published item weights were found (UNVERIFIED):**

| Item | Weight each | 5 of them | Fits Small Packet ≤100g? |
|---|---|---|---|
| Postcard, アートポスト180kg, 100×148mm | ~3.3g | ~17g | Yes, comfortably |
| A4 print, coat 135kg (≈157g/m²) | ~9.7g | ~49g | Yes |
| A3 print, coat 135kg | ~19.5g | ~97g | 5 sheets is right at the line |
| Sticker, 50×50mm | <1g | — | Yes |
| Zine, B5 24pp full colour | ~65–80g | — | One zine ≈ the ¥350/¥830 row |

**So: a single A4 print to the USA costs ¥830 to post (Small Packet) or possibly ¥250 (Printed Matter) against a ¥28 print cost.** International postage is **30× the manufacturing cost** of the object. Same pattern the book report found at ¥4,400 book / ¥2,720 postage, only more extreme, because the object is cheaper and postage does not scale down with it.

---

## 12. Effort — which things pack themselves

| Product | Packing | Thickness | Cheapest domestic | Notes |
|---|---|---|---|---|
| **Stickers** | Envelope. Optionally a card stiffener. | <1mm | **¥185 → ¥240** | Lightest, fastest, least damageable thing in the report |
| **Postcards** | Cello sleeve + backing board + envelope | ~3mm for 5 | **¥185 → ¥240** | Corner damage is the only real risk |
| **A4 print** | Backing board + cello sleeve + card mailer | ~3mm | **¥185 → ¥240** | Fits 34×25cm with millimetres to spare |
| **Zine, B5 24pp** | Cello sleeve + card mailer | ~2mm | **¥185 → ¥240** | Flat, robust, high margin — the best combination here |
| **Ring memo A6** | Envelope; the ring is the thickness | ~10mm | ¥185 → ¥240 (or ゆうパケット ¥250) | Ring may push past 3cm in multiples |
| **Masking tape** | Small box or padded envelope | ~15mm (roll dia.) | ¥185 → ¥240 / ゆうパケット ¥250 | Round object in a flat envelope; fine singly |
| **Acrylic keychain** | Cello sleeve + card; the ナスカン is the bulk | ~5–8mm | ¥185 → ¥240 | Robust, but plate/cut-line setup is fiddly at order time |
| **Acrylic stand** | Base + body separately, small box or padded | ~10–20mm | ゆうパケット ¥310–360 | Two parts, needs a stiff mailer |
| **A3 print** | **⚠️ Tube, or a 44×31cm stiff mailer** | — | **Neither クリックポスト (34×25cm) nor レターパック (34×24.8cm) accepts it** | **This is the cliff.** A3 forces a parcel fare and a several-minute pack |
| **Tote bag** | Fold, cello sleeve, レターパックプラス | compressible | **¥600** | Soft — survives anything; bulky to store |
| **T-shirt** | Fold, cello sleeve, レターパックプラス | compressible | **¥600** | Plus size-SKU inventory across M/L/WM/WL |
| **Mug** | **Box + bubble wrap + void fill** | — | 宅急便コンパクト (¥70 box + fare) | Fragile, ~350–400g, breakage replacement risk |
| **Calendar (A3 wall)** | Flat, board-backed, but 42cm long | ~5mm | **Same A3 problem** | Desk/組立 versions are small and post flat |

**The pattern, stated plainly: everything that fits inside 34×25×3cm costs ¥185 (¥240 from October) and about ninety seconds. Everything else costs three to six times as much in postage and three to six times as long to pack.** A4 is the boundary. It is why the top of the §0 ranking is entirely A4-and-under.

---

## 13. 🔴 Open gaps, listed honestly

| Gap | What was tried |
|---|---|
| **Calendar seasonal selling window** | Searched Japanese sources for 販売時期/売れ時 sell-through data. Only vendor marketing copy with no numbers. **No figure offered rather than a plausible one.** |
| **印刷物 (Printed Matter) eligibility for sold goods** | Rate table obtained (DIRECT); the eligibility conditions page was not read. Potentially the biggest international saving in the report, and it is unconfirmed. |
| **ネコポス availability to a private seller** | Yamato's own ネコポス page 404'd; conclusion rests on secondary logistics blogs. Flagged in §10 rather than asserted. |
| **プリントパック price tables** | Found the AJAX endpoints (`ajax/get_page.php`, `get_price4leaflet.php`) and the static `/contents/pricepages/*.html` family, but did not resolve the parameter mapping. A major Japanese printer is therefore missing entirely. |
| **東京カラー印刷 price tables** | Spec and MOQ confirmed DIRECT; the price table renders `読み込んでいます` and its fetch path was not located. |
| **しまや出版, ちょ古っ都製本工房** | Named in the brief, not reached in this pass. |
| **SUZURI item base costs (原価)** | Help page returns **403** to both scripted fetch and WebFetch. Only a secondary figure circulates (standard T-shirt ¥2,871 single-side) — **deliberately not quoted as fact.** |
| **UP-T, グッズラボ, オリジナルプリント.jp** | Named in the brief; not priced. おたクラブ + pixivFACTORY + グラフィック covered the same product set with better-verified tables, but the cheap end of the goods market may sit below what is shown. |
| **Cheap masking-tape vendors** | mt my mt FACTORY / ミライテープ / 三森特殊印刷 figures are search-summary only, and they undercut the one DIRECT ladder substantially. |
| **Sticker size behind おたクラブ's 「丸 中サイズ」** | Size panel is a separate JS component; not captured. |
| **A4 art print on heavier stock than coat 135kg** | Not priced. Likely the paper a real print should use. |
| **グラフィック wall-calendar and notebook ladders; sticker/シール ladders** | Base pages render nothing; panel API needs a further selection step that was not resolved. |
| **Retail comparables: sales, not asking prices** | Every retail figure in §9 is a listing price. No sell-through, no sales volume, for any product. |
| **おたクラブ ring memo @50** | Simply not queried; the endpoint would return it. |

---

## 14. Sources

**Price APIs and tables read directly.** おたクラブ [otaclub.jp](https://otaclub.jp/products/) · ラクスル [raksul.com](https://raksul.com/poster/) (`/print/api/v1/md/products/*/prices`) · グラフィック [graphic.jp](https://www.graphic.jp/price/4399) · pixivFACTORY [factory.pixiv.net](https://factory.pixiv.net/) · WAVE [wave-inc.co.jp](https://www.wave-inc.co.jp/products/hagaki/) · コミグラ [graphic.jp/comic](https://www.graphic.jp/comic/lineup/postcard) · 東京カラー印刷 [tcpc.co.jp](https://www.tcpc.co.jp/) · 石引パブリック [ishipub-printing.com](https://ishipub-printing.com/risograph_printing/price/) · Hand Saw Press [handsawpresstokyo.com](https://handsawpresstokyo.com/riso-print.html) · 21print [21print.jp](https://21print.jp/%E6%96%99%E9%87%91%E8%A1%A8/) · 日精アート倶楽部 [nspr.co.jp](https://www.nspr.co.jp/art-club/giclee/price.html).

**Postage.** 日本郵便 [int/charge/list/normal1–4.html](https://www.post.japanpost.jp/int/charge/list/normal1.html) · [小形包装物](https://www.post.japanpost.jp/service/send/oversea/list/delivery/small_packing.html) · [ゆうパケット](https://www.post.japanpost.jp/service/send/domestic/delivery/yu-packet/) · [レターパック](https://www.post.japanpost.jp/service/letterpack/) · [クリックポスト](https://clickpost.jp/) · ヤマト運輸 [宅急便コンパクト](https://www.kuronekoyamato.co.jp/ytc/customer/send/services/compact/).

**Retail.** BOOTH [booth.pm](https://booth.pm/ja/) search scrape · minne [minne.com](https://minne.com/category/saleonly/stationery/postcard) category scrape · Artlib [artlib.biz/column/2934](https://artlib.biz/column/2934/).

**Carried from the companion report.** BASE fees [thebase.com/price](https://thebase.com/price).
