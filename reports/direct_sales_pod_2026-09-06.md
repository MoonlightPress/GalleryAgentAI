# Print-on-Demand & Fulfilment in Japan — What She Can Sell Without Touching Stock

**Prepared 2026-09-06 for GEGYjiji (Nin), Tokyo.**
Research only. Figures and their sources. No advice, no legal opinion.

**Who this is priced for:** 27, Chinese citizen on a Japanese **student visa**, resident in Tokyo. Watercolour — urban architecture, light, atmosphere. ~26,000 Instagram followers. Currently sells on BASE (`gegyjiji.base.shop`) and **self-fulfils** — buys stock, packs and posts every order. Originals ¥31,900–115,500; zines ¥1,980. **Has never used print-on-demand.**

**The axis that matters:** *effort*, not margin. The question is which routes let her upload a file and never again touch stock, packing, or a post office.

**Confidence tags:** **DIRECT** = read off an official price page, help article or API response · **INFERRED** = derived, method stated · **UNVERIFIED** = could not confirm · **ANECDOTE** = single self-report, source named.

**All prices in JPY, tax-inclusive unless stated.** No FX conversion is used anywhere in this report — every figure is natively yen.

---

## 0. The four findings that decide this

Before the tables, the four things that came out of the research and actually change the answer:

1. **Two platforms give genuinely zero per-order work: SUZURI and BOOTH×pixivFACTORY.** Everything else in the Japanese market — BASE's POD apps, オリジナルプリント.jp, グッズラボ, UP-T — requires her to log in **after every single sale**, place and pay for a wholesale order herself, and manually update the order status. That is not print-on-demand in the sense she needs; it is a supplier relationship with extra steps. **DIRECT** (§4, §5).

2. **SUZURI cannot print a postcard or a paper art print.** Its 450-item catalogue has stickers, badges, acrylic, mugs, totes, notebooks and a cling-film poster — but no postcard, no giclée, no framed print. **pixivFACTORY can print all of them**, at prices that are startlingly low (B3 poster **¥1,280**, 10 postcards **¥1,835**, F3 canvas **¥3,350**, A4 archival giclée **¥12,000**). For a watercolour painter this is the single biggest differentiator in the report. **DIRECT** (§1.1, §2.1).

3. **No Japanese POD platform ships internationally.** Not one. Every route to an overseas buyer goes through a third-party proxy forwarder (WorldShopping, 転送コム, Buyee, ANYBUY) that the buyer signs up for and pays. She does nothing, but the overseas buyer pays a substantial premium. **The only genuinely borderless zero-fulfilment product is a digital download** — SUZURI charges 5.6%+¥22 on those and confirms they sell overseas. **DIRECT** (§6).

4. **BOOTH pays out to PayPal with no transfer fee, and requires no Japanese bank account.** SUZURI and BASE both require a Japanese bank account. Given §7, that is a structural difference, not a detail. **DIRECT** (§5.3).

---

## 1. SUZURI (suzuri.jp) — GMOペパボ

### 1.0 Method note on the "blocked" help centre

The previous attempt found `help.suzuri.jp` returning **HTTP 403** to WebFetch, and the Firecrawl MCP returned **401 Unauthorized** again this session (tested first, before anything else). **What worked: the Zendesk Help Center REST API.** `help.suzuri.jp` is a Zendesk Guide instance, and

```
https://help.suzuri.jp/api/v2/help_center/ja/articles.json?per_page=100&page=N
```

returns every article body as JSON with no 403. **All 446 SUZURI help articles were retrieved this way.** The same trick worked on `booth.pixiv.help`, `factory.pixiv.help`, `help.thebase.in` and `spicelifehelp.zendesk.com` — 428, 184, 800 and 168 articles respectively. This is worth writing down: it is the reason this report has figures where the last one had holes.

### 1.1 What she can actually make, and what it costs her

The base cost (原価) table lives **not** in the help centre but at [suzuri.jp/item_templates](https://suzuri.jp/item_templates), which the 原価 help article points to ([help.suzuri.jp/hc/ja/articles/47325201727251](https://help.suzuri.jp/hc/ja/articles/47325201727251), **DIRECT**). Full catalogue scraped 2026-09-06; the illustrator-relevant subset:

| Item | 原価 (from) | Notes |
|---|---|---|
| **缶バッジ** | **¥495** | cheapest thing on the platform |
| **ステッカー** | **¥512** | multiple designs can share one sheet |
| **スライドケース（L）** | ¥935 | |
| **リサイクルA7メモパッド / マルチメモM** | ¥990 | |
| **マスキングテープ** | **¥1,045** | |
| **アクリル定規** | ¥1,100 | |
| **クリアファイル** | **¥1,180** | |
| **フラット缶ケース** | ¥1,232 | |
| **アクリルキーホルダー** | ¥1,234 | |
| **ハードカバーハンディノート** | ¥1,252 | |
| **フラットポーチ** | ¥1,310 | |
| **デイリーユースノート** | ¥1,356 | |
| **アクリルパネル** | **¥1,371** | closest thing to a framed print |
| **卓上カレンダー** | **¥1,489** | annual, seasonal |
| **ミニクリアマルチケース** | ¥1,639 | |
| **キャンバスブックカバー** | ¥1,776 | |
| **クリアマルチケース** | ¥1,837 | |
| **アクリルスタンド** | ¥1,876 | |
| **ノート** | ¥1,892 | |
| **マグカップ** | ¥2,046 | |
| **マルマン クロッキーブック（SQ）** | ¥2,046 | her own sketchbook, printed cover |
| **フェイスタオル** | ¥2,065 | |
| **吸着ポスター** | **¥2,178** | static-cling, no adhesive — **the only wall product** |
| **バンダナ** | ¥2,310 | |
| **サコッシュ** | ¥2,288 | |
| **ロンググラス** | ¥2,640 | |
| **エコバッグ** | ¥2,706 | |
| **トートバッグ** | ¥2,860 | |
| **スマホケース（iPhone / Android）** | ¥2,695 | |
| **クリアスマホケース** | ¥2,414 | |
| **ブランケット** | ¥3,630 | |
| **アクリルブロック** | ¥3,498 | |
| **クッション** | ¥4,279 | |
| **スタンダードTシャツ** | ¥3,091 | apparel range runs ¥2,370–9,680 |

Source: [suzuri.jp/item_templates](https://suzuri.jp/item_templates), scraped in full 2026-09-06 — **DIRECT**. ~150 items priced; ~450 including size/colour variants per SUZURI's own copy.

🔴 **Discrepancy flagged, not resolved.** A search-engine snippet of an older SUZURI help article gave the Standard T-shirt 原価 as **¥2,871** (single-sided) / **¥3,608** (dark colours). The live template page today says **¥3,091〜**. These are probably a price rise plus a variant difference, but the older article ([articles/360020009434](https://help.suzuri.jp/hc/ja/articles/360020009434)) no longer exists in the API dump, so it could not be checked. **The ¥3,091 figure is the current live one and is what is used here.**

**What is conspicuously absent:** no postcard, no paper art print, no giclée, no greeting card, no framed anything. For a painter, this catalogue is *merchandise*, not *editions*.

### 1.2 How the money works — トリブン

> 「トリブンは、アイテムが売れたときにもらえるお金のことです。各アイテムごとに原価が表示されていますが、**トリブンを設定すると原価＋トリブンが販売価格となります**。トリブンは原価（トリブンなし）から**最大5,000円まで**設定することが可能です。発生したトリブンについては、**すべてクリエイターさまにお振込みいたします**。」
> — [help.suzuri.jp/hc/ja/articles/360011006033](https://help.suzuri.jp/hc/ja/articles/360011006033), **DIRECT**

And, from the 原価 article:

> 「※**トリブンを設定した場合はその10％が手数料として加算された金額が原価となります。**」
> — [help.suzuri.jp/hc/ja/articles/47325201727251](https://help.suzuri.jp/hc/ja/articles/47325201727251), **DIRECT**

**Reading of the arithmetic — INFERRED, with an ambiguity flagged.** The natural reading is that SUZURI's 10% cut is added *on top of* the base cost and *paid by the buyer*, so:

```
buyer pays  =  原価 + 1.1 × トリブン
she receives =  トリブン  (in full)
```

🔴 **The alternative reading — that the buyer pays 原価 + トリブン and SUZURI deducts 10% of the トリブン from her — could not be excluded.** The gap between the two readings is about 10% of her margin. Attempts to settle it: the two Japanese third-party explainers found ([guriyu.com](https://guriyu.com/2021/03/29/toribun/)) discuss pricing strategy but state no formula; an attempt to reverse-engineer it from live SUZURI listing prices failed (the category listing URL returns 404 to a plain client, and no seller publishes their own トリブン alongside a price). **The conservative reading (×1.1) is used in the table below, so her take is if anything understated.**

**Consumption tax:** 「トリブンには、消費税は含まれます。そのため、トリブンの金額は税込価格となります。」 — [articles/15254864606611](https://help.suzuri.jp/hc/ja/articles/15254864606611), **DIRECT.** Whether she must remit any of it is explicitly pushed back to her and a tax office.

### 1.3 Her realistic take at a sensible retail price

**INFERRED**, method: solve `retail = 原価 + 1.1 × t` for `t`, using the §1.1 原価 figures. Buyer pays shipping on top (§1.5).

| Item | 原価 | If she prices at | Her トリブン | Her share of retail |
|---|---|---|---|---|
| 缶バッジ | ¥495 | ¥900 | **¥368** | 41% |
| ステッカー | ¥512 | ¥1,000 | **¥443** | 44% |
| マスキングテープ | ¥1,045 | ¥1,600 | **¥504** | 32% |
| クリアファイル | ¥1,180 | ¥1,800 | **¥563** | 31% |
| アクリルパネル | ¥1,371 | ¥2,500 | **¥1,026** | 41% |
| 卓上カレンダー | ¥1,489 | ¥2,500 | **¥919** | 37% |
| アクリルスタンド | ¥1,876 | ¥2,800 | **¥840** | 30% |
| ノート | ¥1,892 | ¥2,800 | **¥825** | 29% |
| マグカップ | ¥2,046 | ¥3,000 | **¥867** | 29% |
| 吸着ポスター | ¥2,178 | ¥3,300 | **¥1,020** | 31% |
| トートバッグ | ¥2,860 | ¥4,000 | **¥1,036** | 26% |
| アクリルブロック | ¥3,498 | ¥5,000 | **¥1,365** | 27% |

**Shape of it:** her share is **26–44%**, and it is *highest on the cheapest paper-and-tin items* and lowest on the expensive fabric ones. The ¥495 badge and ¥512 sticker are the two products where the margin structure genuinely works.

### 1.4 Payout

| | |
|---|---|
| **Transfer fee** | **¥176 per payout, deducted** — [articles/115007857247](https://help.suzuri.jp/hc/ja/articles/115007857247), **DIRECT** |
| **Manual payout** | press 【金にする】 on the トリブン page; paid **end of the following month** (or the preceding business day if that's a weekend/holiday) — same source, **DIRECT** |
| **Automatic payout** | any トリブン unpaid **5 months** after the sale is confirmed is paid automatically the following month-end, **provided the total is ≥ ¥177** and bank details are registered — same source, **DIRECT** |
| **Effective minimum** | **¥177** (i.e. ¥1 after the fee) — **DIRECT** |
| **Bank account** | **Japan only.** 「日本国内の銀行口座のみ対応しており、海外の口座には対応しておりません。」 — [articles/218144168](https://help.suzuri.jp/hc/ja/articles/218144168), **DIRECT** |
| **What registration asks for** | 「本人情報と銀行口座情報を入力し【振込先を申請する】」 — [articles/226558487](https://help.suzuri.jp/hc/ja/articles/226558487), **DIRECT.** No ID upload, no My Number, no 開業届 is documented anywhere in the 446 articles. |
| **Tax paperwork** | SUZURI will **not** issue a 支払調書, on the stated grounds that トリブン is not 報酬. She downloads a CSV of the year's orders instead — [articles/14650483728403](https://help.suzuri.jp/hc/ja/articles/14650483728403), **DIRECT** |

### 1.5 Shipping — buyer pays, she never sees it

> 「送料は、購入数やアイテムの組み合わせで異なります。…※アイテムを複数ご購入いただいても、**送料は無料にはなりません**。」
> — [articles/1500013116101](https://help.suzuri.jp/hc/ja/articles/1500013116101), **DIRECT**

Confirmed carriers: 佐川急便 and ヤマト運輸 ([articles/44026135927699](https://help.suzuri.jp/hc/ja/articles/44026135927699), **DIRECT**).

Two shipping figures are published, incidentally, inside other articles:

| Rate | Amount | Source |
|---|---|---|
| 通常配送料 | **¥740** | [articles/50309248770579](https://help.suzuri.jp/hc/ja/articles/50309248770579) (特急便 page), **DIRECT** |
| Tシャツ便 (ネコポス, single qualifying tee) | **¥420** | [articles/9157430695443](https://help.suzuri.jp/hc/ja/articles/9157430695443), **DIRECT** |

🔴 **No published shipping table for small items exists.** SUZURI's answer is "put it in the cart and look." Tried: the help API (all 446 articles — no rate table), the SUZURI journal, and third-party blogs. A 2023 SUZURI announcement ([suzuri.jp/media/journal_price-revision-20230403](https://suzuri.jp/media/journal_price-revision-20230403/), **DIRECT but stale**) documents a rise from ¥600→¥780 standard and ¥260→¥395 ネコポス for acrylic/clear-file/sandal items. Those are **three years old and inconsistent with the current ¥740**, so they are recorded here and **not** used. Sticker/badge shipping today is **UNVERIFIED**; it is plausibly around ¥400.

**This matters more than it looks.** A ¥1,000 sticker plus ~¥400 shipping is a ¥1,400 purchase. Shipping is roughly 30–40% of the ticket on her cheapest items, and there is no multi-buy discount.

### 1.6 Overseas

> 「海外からでもSUZURIのアイテムは購入可能です。海外からの購入は、越境購入代行サービス「WorldShopping」「Bibian」「転送コム」を経由して行われます。…**クリエイターさまによる、特別な対応は必要ございません。**」
> — [articles/4407005863187](https://help.suzuri.jp/hc/ja/articles/4407005863187), **DIRECT**

- **WorldShopping** — everywhere except Taiwan. **Bibian** — Taiwan. **転送コム** — general (silkscreen orders only).
- Mechanically: the proxy company buys the item domestically on SUZURI and re-ships it abroad. SUZURI never handles an international parcel; **she does nothing at all**.
- 🔴 **The cost to the overseas buyer is not published by SUZURI** and varies by proxy, destination and weight. Not researched further — it is the buyer's cost, not hers, but it is the reason overseas conversion on this route will be poor.

### 1.7 The digital route — the cheapest and most borderless thing on the platform

SUZURI sells **デジタルコンテンツ**: 壁紙, イラスト, 電子書籍, 素材データ, 写真, 動画, デジタルアート and more ([suzuri.jp/item_templates](https://suzuri.jp/item_templates) category list, **DIRECT**).

| | |
|---|---|
| **Fee** | 「販売価格から手数料を引いた金額がトリブンになります。手数料は、**設定した販売価格 × 5.6%＋22円**」 — [articles/11288748576787](https://help.suzuri.jp/hc/ja/articles/11288748576787), **DIRECT** |
| **Overseas** | 「デジタルコンテンツは**海外からもご購入いただけます**。」 — [articles/13602953896723](https://help.suzuri.jp/hc/ja/articles/13602953896723), **DIRECT** |
| **Effort per order** | zero, and there is no physical object at all |
| **Restriction** | browser purchase only, not via the SUZURI app — [articles/50802964584339](https://help.suzuri.jp/hc/ja/articles/50802964584339), **DIRECT** |

**INFERRED:** on a ¥1,000 wallpaper set she keeps **¥922** (92.2%). On a ¥2,000 PDF she keeps **¥1,866** (93.3%). Nothing else in this report comes close, and it is the only SUZURI product an overseas follower can buy without a forwarding agent.

### 1.8 Barriers for her specifically

| Requirement | Status |
|---|---|
| Japanese address | **Required.** 「「SUZURI」は、国内向けサービスとして提供をしております。**海外在住クリエイターさまに関しましては、ご利用いただくことができかねます。**」 — [articles/44057520323731](https://help.suzuri.jp/hc/ja/articles/44057520323731), **DIRECT.** She lives in Tokyo, so this is satisfied — but it means the account dies if she leaves Japan. |
| Japanese bank account | **Required for payout** (§1.4). **DIRECT.** |
| Nationality / visa status | **Not mentioned anywhere** in 446 help articles. The stated test is residence, not citizenship. **DIRECT (absence).** |
| My Number | **Not requested.** The only mention across all articles is in a deceased-account procedure, and there the instruction is to *redact* it. **DIRECT.** |
| 開業届 | **Not mentioned.** SUZURI's line is that トリブン is not 報酬 and it issues no 支払調書 (§1.4). |
| Japanese phone number | 🔴 **Not determined.** No article states a phone requirement for creator registration; two-factor auth is offered. Untested because it would need an actual signup. |
| Minimum age | 🔴 **Not found** in the help centre. (BOOTH and BASE both publish 18+; SUZURI does not.) She is 27 either way. |
| **Public disclosure of her name/address** | **No 特定商取引法 obligation surfaced.** A keyword sweep of all 446 articles for 特定商取引 returned **nothing** — consistent with SUZURI (GMOペパボ) being the seller of record, not her. Compare BASE (§4.5), where her legal name is unavoidably public. **DIRECT (absence) — worth confirming at signup.** |

---

## 2. pixivFACTORY (factory.pixiv.net)

This is the manufacturing layer. §3 (BOOTH) is the shop layer. Together they are the on-demand system.

### 2.1 What she can make — the paper and wall range SUZURI doesn't have

All **DIRECT** from individual product pages, scraped 2026-09-06. Prices tax-inclusive, per unit or per stated set.

**Paper / wall — the relevant half of the catalogue:**

| Item | Size | Price | Source |
|---|---|---|---|
| **ポストカード** | 100×148mm, **set of 10** | **¥1,835** (マットコート220kg)<br>¥1,970 (竹はだGA180kg)<br>¥2,300 (ヴァンヌーボVGスノーホワイト195kg) | [/products/postcard](https://factory.pixiv.net/products/postcard) |
| **ポスター** | B3 370×521 | **¥1,280** | [/products/fast_poster](https://factory.pixiv.net/products/fast_poster) |
| | A2 426×600 | ¥1,400 | |
| | B2 521×734 | ¥1,890 | |
| | A1 600×847 | ¥2,550 | |
| | B1 734×1036 | ¥3,180 | |
| **パネル** (mounted board) | B3 | ¥2,550 | [/products/panel](https://factory.pixiv.net/products/panel) |
| | A2 | ¥3,050 | |
| | B2 | ¥4,350 | |
| | A1 | ¥5,900 | |
| | B1 | ¥8,100 | |
| **キャンバス** | F3 220×273 | **¥3,350** | [/products/canvas](https://factory.pixiv.net/products/canvas) |
| | F4 242×333 | ¥3,650 | |
| | F6 318×410 | ¥4,450 | |
| | F10 455×530 | ¥4,950 | |
| **複製画（プリモアート）** — framed archival reproduction | A4 (frame 287×387) | **¥12,000** | [/products/primo_art](https://factory.pixiv.net/products/primo_art) |
| | A3 (frame 423×545) | ¥19,000 | |
| | A2 (frame 544×726) | ¥29,500 | |
| **色紙 (shikishi board)** | mini 135×120 | ¥1,110 | [/products/shikishi_board](https://factory.pixiv.net/products/shikishi_board) |
| | standard 242×272 | ¥1,690 | |
| **タペストリー** (suede) | B2 | ¥3,850 @1–4 → ¥2,440 @100+ | [/products/tapestry](https://factory.pixiv.net/products/tapestry) |
| **アートプリント名刺** | 91×55mm | ¥620 per 10 @50+ → ¥340 per 10 @500+ | [/products/art_print_business_card](https://factory.pixiv.net/products/art_print_business_card) |

**Goods:**

| Item | From | Source |
|---|---|---|
| ステッカー | ¥290 | [/products/sticker](https://factory.pixiv.net/products/sticker) |
| 缶バッジ | ¥70 | [/products/can_badge](https://factory.pixiv.net/products/can_badge) |
| アクリルキーホルダー | ¥390 | [/products/standard_acrylic_key_chain](https://factory.pixiv.net/products/standard_acrylic_key_chain) |
| マスキングテープ | ¥430 | [/products/masking_tape](https://factory.pixiv.net/products/masking_tape) |
| クリアファイル | ¥900 | [/products/clear_file_folder](https://factory.pixiv.net/products/clear_file_folder) |
| メモ帳 | ¥950 | [/products/notepad](https://factory.pixiv.net/products/notepad) |
| トートバッグ S / M / L | ¥920 / ¥1,530 / ¥1,730 | [/products/tote_bag](https://factory.pixiv.net/products/tote_bag) |
| リングノート | ¥1,280 | [/products/notebook](https://factory.pixiv.net/products/notebook) |
| マグカップ | ¥1,400 | [/products/standard_mug](https://factory.pixiv.net/products/standard_mug) |
| アクリルフォトパネル | ¥2,210 | [/products/acrylic_photo_panel](https://factory.pixiv.net/products/acrylic_photo_panel) |
| アクリルブロック | ¥3,800 (clear 10×10cm) | [/products/acrylic_block](https://factory.pixiv.net/products/acrylic_block) |

Full catalogue: 117 product pages under `factory.pixiv.net/products/`, plus a separate 同人誌 (book) service at `/books`. All prices are **税込** — 「アイテムの価格は、すべて消費税が含まれた価格となっております。BOOTHで販売する際も、すべて消費税込みの価格を設定してください。」 ([factory.pixiv.help/hc/ja/articles/235612068](https://factory.pixiv.help/hc/ja/articles/235612068), **DIRECT**).

**Read the poster line again.** A **B3 (370×521mm) archival-ish poster print costs ¥1,280 to manufacture, one at a time, with no minimum and no stock.** For an artist whose originals start at ¥31,900, that is a genuine ¥2,500–4,000 rung on the ladder that currently does not exist between her ¥1,980 zine and a five-figure painting.

⚠️ **The postcard caveat.** 「10枚単位でのご購入となります。現時点では1枚単位などで購入することができませんので、あらかじめご了承ください。」 ([/products/postcard](https://factory.pixiv.net/products/postcard), **DIRECT**). A postcard listing is necessarily a **10-pack**, not a single card. That is fine for a set of ten views, and wrong for a pick-one-card impulse buy.

### 2.2 Shipping — the full published table

Unlike SUZURI, pixivFACTORY publishes its shipping matrix in full. All 税込, 全国一律 ([factory.pixiv.help/hc/ja/articles/115000182314](https://factory.pixiv.help/hc/ja/articles/115000182314), **DIRECT**, last revised 2022-12-01):

| Group | Items (relevant subset) | 1 item | 2+ or mixed |
|---|---|---|---|
| **1** | ステッカー, クリアファイル, リングノート, メモ帳, マスキングテープ (15/20mm), 色紙(ミニ), アクリルキーホルダー(コーティング), アクリルフォトパネル, 手帳型ケース, タオル(ハンド) | **¥400** | **¥840** (stickers-only stays ¥400) |
| | マグカップ, ポーチ, ペンケース, ブランケット, パズル, 色紙(通常), マスキングテープ (25/30mm) | ¥840 | ¥840 |
| **2** | ミニタペストリー, 枕カバー, クッションカバー, 抱き枕カバー | ¥550 | ¥880 |
| | タペストリー, 等身大タペストリー | ¥880 | ¥880 |
| **3** | カラーTシャツ, ビッグシルエットT, フルグラフィックT, パーカー, サコッシュ, **アクリルブロック**, コースター, タオル(フェイス/マフラー) | **¥820 regardless of quantity** | |
| **4** | **ポスター** | **¥326 regardless of quantity** | |
| | **パネル** (or any order containing one) | **¥1,100** | |
| **6** | 缶バッジ類 + フォト風カード | ¥440 up to 15 badges / 100 cards | ¥1,000 above |
| **9** | **ポストカード**, iPhoneケース, 名刺, メガネ拭き, **トートバッグ**, ピンバッジ, タンブラー | **¥400 regardless of quantity or mix** | |
| **10** | クリアiPhoneケース | ¥380 (1–6) | ¥1,100 (7+) |

**Poster shipping is ¥326 for any number of posters.** Ten B3 posters ship for ¥326. Ten postcard packs ship for ¥400.

🔴 **キャンバス and 複製画（プリモアート） do not appear in the shipping table.** Groups 1–10 do not name them, and no other page prices their delivery. Tried: the full 184-article pixivFACTORY help dump, the two product pages, and the BOOTH shipping FAQ. **Unpriced.** Given the F10 canvas is 455×530mm and the A2 primo art frame is 544×726mm, these are almost certainly above ¥1,000 — but that is a guess and is not used anywhere in this report.

### 2.3 Overseas

> 「**直接、お届け先を海外に指定することはできません。** なお、「転送コム」など海外発送代行サービスを利用し専用の住所を発行いただくことで、海外への発送も可能です。」
> — [factory.pixiv.help/hc/ja/articles/235679667](https://factory.pixiv.help/hc/ja/articles/235679667), **DIRECT**

Same structure as SUZURI: proxy-only, buyer-arranged, zero work for her.

### 2.4 Lot discounts

Some items get cheaper per unit at volume for the *same variation* — the tapestry table in §2.1 shows the pattern (¥3,850 → ¥2,440), and can badges, stickers, acrylic keychains and business cards all have ladders. 「同じサイズでもデザインが異なる場合は、すべて別のバリエーションとなり割引の対象になりません。」 ([factory.pixiv.help/hc/ja/articles/235678487](https://factory.pixiv.help/hc/ja/articles/235678487), **DIRECT**.) **Irrelevant to on-demand selling** (one order = one unit) but relevant if she ever pre-prints for a fair.

---

## 3. BOOTH (booth.pm) — the shop layer

### 3.1 The fee schedule, in full

> ■「自宅から発送」商品 — **（商品価格＋送料）× 5.6％ ＋ 45円**
> ■「ダウンロード」商品 — **商品価格 × 5.6％ ＋ 45円** ※無料配布の場合、サービス利用料は発生しません
> ■「倉庫から発送」商品 — **商品価格 × 5.6％ ＋ 45円** ※倉庫発送手数料が別途発生します
> ■「**pixivFACTORYから発送**」商品 — **マージン × 5.6％ ＋ 45円** ※小数点以下切り上げ
> — [booth.pixiv.help/hc/ja/articles/115004576874](https://booth.pixiv.help/hc/ja/articles/115004576874), **DIRECT**

**Read the last line carefully.** On the pixivFACTORY route the commission is charged on **her margin only** — not on the manufacturing cost, not on the shipping. This is structurally the most generous fee in this report. On BASE (§4) the equivalent charge lands on the whole ticket including postage.

### 3.2 What the on-demand flow actually is

> 「BOOTHオンデマンド販売は、pixivFACTORYでつくったグッズや同人誌の入稿データを、…「BOOTH」へ登録しておくだけで、購入者の注文に応じて**1点から製造・販売できる仕組み**です。グッズは購入されるたびに製造し**購入者へ直接発送されるため**、ショップオーナーは事前に在庫を抱えず販売することができます。…**費用は一切かかりません。**」
> — [factory.pixiv.help/hc/ja/articles/235613628](https://factory.pixiv.help/hc/ja/articles/235613628), **DIRECT**

And from the landing page:

> 「商品は、ショップオーナーを介さずにpixivFACTORYから購入者へ直接発送します。めんどうな梱包や発送の作業は、すべておまかせください！」
> 「pixivFACTORYから発送するので、**住所や名前が知られることのない匿名配送**ができます。」
> 「pixivFACTORYおよびBOOTHは、月額固定費などはありません。**ショップ開設も、出品も無料**です！」
> — [factory.pixiv.net/lp/booth_pod](https://factory.pixiv.net/lp/booth_pod), **DIRECT**

**Setup, once per design:** choose item → upload one image → confirm the auto-generated preview → click オンデマンド販売 → set name, category and margin → live. (Three steps, per the LP.) The preview image doubles as her product photo.

**Per order: nothing.** Shipping is set automatically — 「pixivFACTORYの各製造業者が定める送料が自動的に適用されます。ショップオーナーが設定する必要はありません。」 ([booth.pixiv.help/hc/ja/articles/230690387](https://booth.pixiv.help/hc/ja/articles/230690387), **DIRECT**). The parcel's sender reads 「pixivFACTORY」 or 「ピクシブ株式会社」.

### 3.3 Her realistic take

**INFERRED**, method: `take = margin − ceil(margin × 0.056 + 45)`, per §3.1. Buyer pays manufacturing + margin + shipping.

| Product | Mfg cost | Her margin | Buyer pays (+ shipping) | **She keeps** | Her share of ticket |
|---|---|---|---|---|---|
| **ポスター B3** | ¥1,280 | ¥1,200 | ¥2,480 (+¥326) | **¥1,087** | 39% |
| **ポスター A2** | ¥1,400 | ¥1,600 | ¥3,000 (+¥326) | **¥1,465** | 44% |
| **ポスター A1** | ¥2,550 | ¥2,450 | ¥5,000 (+¥326) | **¥2,268** | 43% |
| **ポストカード ×10** | ¥1,835 | ¥1,165 | ¥3,000 (+¥400) | **¥1,055** | 31% |
| **色紙 (mini)** | ¥1,110 | ¥890 | ¥2,000 (+¥400) | **¥795** | 33% |
| **色紙 (standard)** | ¥1,690 | ¥1,310 | ¥3,000 (+¥840) | **¥1,192** | 31% |
| **キャンバス F3** | ¥3,350 | ¥2,650 | ¥6,000 (+🔴) | **¥2,457** | 41% |
| **パネル A2** | ¥3,050 | ¥1,950 | ¥5,000 (+¥1,100) | **¥1,796** | 29% |
| **複製画 A4 (framed)** | ¥12,000 | ¥8,000 | ¥20,000 (+🔴) | **¥7,507** | 38% |
| **クリアファイル** | ¥900 | ¥700 | ¥1,600 (+¥400) | **¥616** | 31% |
| **ステッカー** | ¥290 | ¥510 | ¥800 (+¥400) | **¥436** | 36% |
| **トートバッグ M** | ¥1,530 | ¥1,470 | ¥3,000 (+¥400) | **¥1,343** | 38% |

Her share is **29–44%** of the item price, before shipping — the same band as SUZURI, but on products that suit her work. And note the poster rows: **at A2 she keeps ¥1,465 on a ¥3,000 print**, which is a real number for a painter with 26,000 followers.

### 3.4 Payout

| | |
|---|---|
| **Schedule** | 「毎月1日から月末までに発送完了になった注文の売上が、翌月20日から5営業日以内に振り込まれます。」 — [articles/230690667](https://booth.pixiv.help/hc/ja/articles/230690667), **DIRECT** |
| **Bank transfer fee** | **¥200** if the payout is < ¥30,000; **¥300** if ≥ ¥30,000 — [articles/231284808](https://booth.pixiv.help/hc/ja/articles/231284808), **DIRECT** |
| **PayPal transfer fee** | **¥0** — same source, **DIRECT** |
| **Wise** | ¥0 from BOOTH, but Wise's own fees apply; offered only as a **fallback** to users who can no longer use the other methods, on request — same source, **DIRECT** |
| **Automatic payout** | ≥ ¥5,000 goes automatically (bank: ≥¥4,800 net; PayPal: ≥¥5,000) — [articles/115003162794](https://booth.pixiv.help/hc/ja/articles/115003162794), **DIRECT** |
| **Manual application** | needed between **¥201 and ¥5,000**, submitted between the 1st and 19th of the month — [articles/230690647](https://booth.pixiv.help/hc/ja/articles/230690647), **DIRECT** |
| **Expiry** | unpaid balances auto-transfer after 6 months; if the transfer fails on bad details the sale **expires** — [articles/230690667](https://booth.pixiv.help/hc/ja/articles/230690667), **DIRECT** |
| **Registrable accounts** | 「売上の振込先には、**日本国内の銀行口座、またはPayPal**が登録できます。」 — [articles/115001538147](https://booth.pixiv.help/hc/ja/articles/115001538147), **DIRECT**. Explicitly **not** allowed: Payoneer, WorldFirst, Kyash, Onebank, Coincheck, BitTrade — [articles/4415068029593](https://booth.pixiv.help/hc/ja/articles/4415068029593), **DIRECT** |

### 3.5 BOOTH倉庫 — the warehouse (for her *existing* zines, not for POD)

This is the answer to "I already have 200 printed zines in my flat."

| | Figure | Source |
|---|---|---|
| **Storage fee** | **¥1,000/month + tax**, charged **only if the month's sell-through rate is under 20%**. At ≥20% it is **¥0**. Sell-through = (units shipped that month) ÷ (units held at previous month-end + units received that month). | [articles/231284468](https://booth.pixiv.help/hc/ja/articles/231284468), **DIRECT** |
| **Per-shipment fee** | **商品価格 × 2.5% + 商品個数 × ¥25** per order (税込, rounded up), **on top of** the 5.6%+¥45 service fee | [articles/49117259932697](https://booth.pixiv.help/hc/ja/articles/49117259932697), **DIRECT** |
| **Buyer-paid shipping** | ネコポス **¥400** · 宅配便 **¥730**, fixed nationwide, set automatically | [articles/231285528](https://booth.pixiv.help/hc/ja/articles/231285528) + [articles/230690007](https://booth.pixiv.help/hc/ja/articles/230690007), **DIRECT** |
| **Minimum intake** | **30 units per storage application** (restocking an existing line: from 1) | [articles/900000275366](https://booth.pixiv.help/hc/ja/articles/900000275366), **DIRECT** |
| **Cost to send stock in** | **Her own courier cost, 元払い (prepaid) only.** Cash-on-delivery consignments are refused and returned. | [articles/115000123734](https://booth.pixiv.help/hc/ja/articles/115000123734), **DIRECT** |
| **Storage caps** | ネコポス size: 1,000 units · 60-size A (**同人誌・冊子等印刷物**, ≤3.5cm high, ≤2kg): **1,000 units** · 60-size B (non-print goods): 200 · 80-size: 100 · 100-size: 100 · 120/140: 70 · 160: 50 | [articles/230690167](https://booth.pixiv.help/hc/ja/articles/230690167), **DIRECT** |
| **Retrieving stock (返送料)** | 返送基本料 **¥800** flat up to 200 units (¥4/unit above 200) **+** picking fee: ¥500 per SKU if returning ≥13 of it in full, else ¥40/unit. **Worked example given by BOOTH: 100 postcards returned in full = ¥800 + ¥500 = ¥1,300.** | [articles/52804439847705](https://booth.pixiv.help/hc/ja/articles/52804439847705), **DIRECT** |
| **Prep work she must do herself** | Bag anything that needs bagging (OPP), fold anything that needs folding, apply printed SKU labels to each bundle, write the 保管ID on the courier waybill, pack with cushioning. 「対応いただいていない場合、**着払いにて返送**いたします。」 | [articles/115000123734](https://booth.pixiv.help/hc/ja/articles/115000123734), **DIRECT** |
| **pixivFACTORY → warehouse direct** | Books and goods made at pixivFACTORY can be shipped **straight into the BOOTH warehouse** without passing through her flat — she registers the product, gets a 保管ID and warehouse address, then orders that quantity from pixivFACTORY to that address. No 商品保管申込書 needed. | [articles/900001001166](https://booth.pixiv.help/hc/ja/articles/900001001166) + [factory.pixiv.help/hc/ja/articles/235613728](https://factory.pixiv.help/hc/ja/articles/235613728), **DIRECT** |

**Honest read of the warehouse:** it is *not* a low-effort route on its own — she still has to produce, bag, label and courier 30+ units in. **But the pixivFACTORY→warehouse direct path is the exception**, and it is the one route in this entire report by which a printed zine could reach buyers without ever entering her flat. Storage is free in any month she sells 20% of what's stored, which for a small batch is a low bar.

🔴 **Cost of couriering stock into the warehouse: not researched.** It is a normal Yamato/Sagawa 宅配便 charge determined by her origin and box size, not a BOOTH fee, and BOOTH publishes nothing.

### 3.6 Overseas — proxy only

「購入者が海外発送（国際配送）代行サービスの**転送コム**を利用することで、日本国外のユーザーは商品を購入することができます。別途、ショップオーナーが商品編集画面で「代理購入サービスの掲載」を許可することで、**「Buyee」「ANYBUY」**に商品を表示させることもできます。」 — [articles/230689967](https://booth.pixiv.help/hc/ja/articles/230689967) (warehouse) and [articles/230689807](https://booth.pixiv.help/hc/ja/articles/230689807) (home dispatch), **DIRECT**. The same answer appears on the pixivFACTORY POD LP for on-demand goods.

**One-click opt-in:** the 「代理購入サービスの掲載許可」 toggle puts her catalogue in front of Buyee/ANYBUY's international audience with no further work. **DIRECT.**

BOOTH also maintains **English and Simplified/Traditional Chinese storefronts** — `booth.pm/en` and `booth.pm/zh-cn` both return HTTP 200 (**DIRECT**, tested 2026-09-06) — and publishes a ready-made multilingual announcement template for artists telling overseas followers how to buy, in Japanese, English, 简体, 繁體 and Korean ([articles/115005850707](https://booth.pixiv.help/hc/ja/articles/115005850707), **DIRECT**). For an artist who is a native Chinese speaker with an international following, this is not nothing.

### 3.7 Barriers

| Requirement | Status |
|---|---|
| Account | A **pixiv account** logs into both BOOTH and pixivFACTORY. Free. **DIRECT** ([factory.pixiv.net/lp/booth_pod](https://factory.pixiv.net/lp/booth_pod)) |
| Age | **18+**, or under-18 with a guardian's consent — [articles/231282288](https://booth.pixiv.help/hc/ja/articles/231282288), **DIRECT** |
| Japanese bank account | **Not required — PayPal is accepted, fee-free** (§3.4). **DIRECT.** This is the only mainstream Japanese POD route in this report that works without one. |
| Japanese address | **Not required to open a shop.** 「海外でショップを開設する場合…振込先はPayPal、または日本国内の銀行口座のみです。」 — [articles/360001199594](https://booth.pixiv.help/hc/ja/articles/360001199594), **DIRECT.** BOOTH explicitly contemplates overseas shop owners. (**BOOTH倉庫 does require a Japanese address**; on-demand and downloads do not.) |
| My Number | Not mentioned anywhere in 428 articles. **DIRECT (absence).** |
| 開業届 | Not mentioned. BOOTH offers an invoice-registration feature but does not require it. |
| **特定商取引法 disclosure** | 「BOOTHでの商品販売は…**特定商取引法に基づく表記は必要です。ただし、特定商取引法に基づく「販売業者」に該当しない場合は、連絡先や住所などを記載する義務はありません。**」 — [articles/115000340874](https://booth.pixiv.help/hc/ja/articles/115000340874), **DIRECT.** BOOTH pushes the判断 to her and points at the Consumer Affairs Agency. Contrast BASE (§4.5), where her legal name is mandatory and unhideable. |

---

## 4. BASE — where she already is

### 4.1 Fees on the plan she is presumably on

**スタンダードプラン** ([help.thebase.in/hc/ja/articles/5701758066585](https://help.thebase.in/hc/ja/articles/5701758066585), **DIRECT**):

| | |
|---|---|
| Monthly cost | **¥0** |
| BASEかんたん決済手数料 | **3.6% + ¥40** per order, **on the order total including shipping**, rounded to the nearest yen (4.6% + ¥40 for Amazon Pay / PayPal / PayPay) |
| サービス利用料 | **3%** |
| **Effective take rate** | **6.6% + ¥40**, charged on item + postage |

**グロースプラン** ([articles/5701824979353](https://help.thebase.in/hc/ja/articles/5701824979353), **DIRECT**): 2.9% payment fee, 0% service fee, but **¥19,980/month (monthly) or ¥16,580/month (annual, ¥198,960/yr)**, credit card only, and BASE states it pays off above roughly **¥500,000/month** in sales. **Not relevant to her**, and note this is more than triple the ¥5,980 figure that still circulates in older write-ups.

### 4.2 Payout — this is where BASE is expensive

| | |
|---|---|
| **振込手数料** | **¥250 flat, every time** |
| **事務手数料** | **¥500 if the payout is under ¥20,000; ¥0 at ¥20,000+** |
| Formula | 振込申請額 − 振込手数料 − 事務手数料 = amount received |
| Minimum balance | **¥751** to apply |
| Frequency | one application per day, up to ¥1,000,000 |
| お急ぎ振込 / 最速振込 | +1.5% / +3% of the applied amount |

Sources: [articles/206341302](https://help.thebase.in/hc/ja/articles/206341302) and [articles/206418201](https://help.thebase.in/hc/ja/articles/206418201) — both **DIRECT**. *(This closes gap #11 of the 2026-09-05 book economics report, which recorded these pages as unreachable.)*

**The practical consequence:** every payout under ¥20,000 costs her **¥750**. On a ¥10,000 withdrawal that is 7.5% — a bigger bite than the sales commission. SUZURI's equivalent is ¥176; BOOTH's is ¥200, or ¥0 via PayPal.

### 4.3 Its print-on-demand options

BASE has **no first-party POD**. It has partner Apps. The one that matters:

**オリジナルプリント.jp App** (株式会社イメージ・マジック) — [apps.thebase.com/detail/91](https://apps.thebase.com/detail/91), **DIRECT**

| | |
|---|---|
| Catalogue | **~1,500 items** — includes ポスター, ファブリックパネル, カレンダー, タペストリー, シール・ステッカー, 名刺・カード, ノート, クリアファイル, マグカップ, トートバッグ, アクリルグッズ |
| App cost | **Free** |
| Pricing | BASE-routed orders are priced **5% below** ordering directly on originalprint.jp — [originalprint.jp/store.php/page/thebase](https://originalprint.jp/store.php/page/thebase), **DIRECT** |
| Sender name | Ships **under her shop's name**, not the printer's |
| Minimum | 1 unit, no inventory |

**And here is why it does not qualify as low-effort.** The official flow, quoted:

> 「ステップ① マイページで確認 — BASEネットショップにご注文が入ると、そのご注文情報を、オリジナルプリント.jpのマイページで確認・**発注**することができます。
> ステップ② カートにいれて発注 — 該当する注文リストから該当注文を選択して、詳細ページから**カートに入れてそのまま発注**できますので、ご注文リスト単位ごとに**注文完了までお進みください**。」
> 「発注が完了した後は？ — …お手数ですが、出荷完了メールにて「お問い合わせ番号」をご確認いただき、**BASEの管理画面でご注文のステータスは手動で更新願います。（自動では更新されません）**」
> — [originalprint.jp/store.php/page/thebase](https://originalprint.jp/store.php/page/thebase), **DIRECT**

**Per order she must:** open originalprint.jp → find the order → add it to a cart → pay for it out of her own pocket → wait for a dispatch email → copy the tracking number → go back to BASE and mark the order shipped. **Six steps, every single sale, and she fronts the cash.** Plus: 「仕入価格の合計金額に関わらず**別途送料を頂戴します**」 (**DIRECT**) — she pays wholesale postage on top, on every order, with no free-shipping threshold.

There are also two operational traps documented on the same page (**DIRECT**): adding a size on the BASE side breaks the link and the order **cannot be fulfilled**; and two separate BASE orders to the same address cannot be combined into one cart, so they ship separately.

🔴 **Per-unit base costs for オリジナルプリント.jp were not extracted.** Its catalogue is ~1,500 SKUs behind a JS-driven configurator; no static price table equivalent to SUZURI's or pixivFACTORY's exists. Tried: the guide pages, the BASE app listing, the category index. **Not filled.** Given the flow above, it did not seem worth further effort.

### 4.4 かんたん海外販売 — BASE's one real international advantage

> 「海外からのアクセスに対して自動的に海外専用ショッピングカートを表示し、海外の購入者に商品を販売できる機能です。**海外発送は代行事業者の「want.jp株式会社」がおこなうため、ショップオーナーは国内発送のみで海外販売を実現できます。**」
> 「基本利用料：無料 / **かんたん海外販売利用料：注文合計金額（商品代金＋国内送料に対して）の5%**」
> — [help.thebase.in/hc/ja/articles/52804478331929](https://help.thebase.in/hc/ja/articles/52804478331929), **DIRECT**

Overseas buyers get a native checkout in their own currency with **Alipay, WeChat Pay, PayPal, Google/Apple Pay, UnionPay and cards** — a materially better experience than being bounced to a Japanese forwarding agent. **This is the only route in this report where an overseas follower buys the way she expects to.**

🔴 **Whether かんたん海外販売 composes with a POD App is unresolved and probably negative.** The オリジナルプリント.jp App page carries the warning 「※**日本国外からの購入や配送に対応していない可能性がございます。**必ず、連携先サービスまでご確認の上で「送料詳細設定App」の設定をご検討ください」 (**DIRECT**), and BASE separately notes 「そのほかにも「BASE Apps」を利用して販売いただく商品（ショップオーナーが発送作業をおこなわない商品）において、日本国外に発送できない場合があります」 ([articles/206418881](https://help.thebase.in/hc/ja/articles/206418881), **DIRECT**). Neither says outright that it fails. **Not resolvable without a live test.**

### 4.5 Barriers — and the one that is genuinely uncomfortable

| Requirement | Status |
|---|---|
| Age | **18+** — [articles/206341522](https://help.thebase.in/hc/ja/articles/206341522), **DIRECT** |
| Japanese address | **Required.** 「BASEは日本国内にお住まいの方向けにサービスを提供しており…」 — [articles/206417961](https://help.thebase.in/hc/ja/articles/206417961), **DIRECT** |
| **Foreign resident on a Japanese address** | **Explicitly permitted.** 「**海外から日本へ一時的に在住の場合** — 日本国内に住所をお持ちである場合、ショップを運営していただくことが可能です。※BASEで商品を販売するにあたり「BASEかんたん決済の利用申請」が必須となっておりますが、ご状況次第では「**在留カード**」などの提出を別途お願いすることがあります。」 — same source, **DIRECT.** This is the clearest platform-level statement found anywhere in this research that a foreign resident can legitimately run a Japanese shop. |
| Accepted ID | 運転免許証 / **マイナンバーカード（表面のみ）** / **在留カード（有効期限が60日以上先のもの）** / 特別永住者証明書 — [articles/900004783746](https://help.thebase.in/hc/ja/articles/900004783746) (eKYC) and [articles/206340862](https://help.thebase.in/hc/ja/articles/206340862) (決済申請), both **DIRECT.** A residence card is a first-class ID here; **the My Number *number* is never requested** — BASE explicitly instructs that the card's reverse side must not be submitted. |
| Japanese bank account | **Required for payout.** 「振込申請の振込先口座は**日本国内の銀行口座に限ります**。」 — [articles/206417961](https://help.thebase.in/hc/ja/articles/206417961), **DIRECT** |
| **Public name** | **Her legal name is mandatory and cannot be hidden.** 「※特定商取引法に基づく表記に、**氏名の記載は必須事項です**。…BASEでは、ネットショップを運営される事業者にはかならずお名前の記載をお願いしており、**非表示にすることはできません**。」 Katakana, hiragana and shop names are rejected. — [articles/360000005601](https://help.thebase.in/hc/ja/articles/360000005601), **DIRECT** |
| Address & phone | **Can** be hidden — BASE's own address and number are shown instead. But she must still register them accurately, **the 発送元 on the parcel must be her own address**, the 納品書 carries her address, and they must be disclosed on request in a dispute. — [articles/4413887418393](https://help.thebase.in/hc/ja/articles/4413887418393), **DIRECT** |

**The size of that last row.** On BASE she publishes her real legal name and her flat is on the parcel and the packing slip. On BOOTH-with-pixivFACTORY the sender reads 「ピクシブ株式会社」 and contact details are only required if she is a 販売業者. On SUZURI no 特商法 obligation surfaced at all. For a 27-year-old woman with ~26,000 followers, living alone in Tokyo, that is a real difference and not a compliance footnote.

---

## 5. The other Japanese POD services

### 5.1 オリジナルプリント.jp (イメージ・マジック, 東証上場)

Covered in §4.3. Standalone, without BASE, it is a printer with a design tool: **1 unit minimum, quote instantly, ~1,500 SKUs, 代行出荷 (ships under her name)**. Effort per order is high (manual reorder + payment + status update). **Best read as her supplier if she ever wants a specific object nobody else makes, not as a sales channel.**

### 5.2 グッズラボ / オリジナルグッズラボ (orilab.jp) — two different products

**(a) The printer with a direct-ship function** — [original-goods.orilab.jp/info/cyokusou](https://original-goods.orilab.jp/info/cyokusou), **DIRECT**

| | |
|---|---|
| 代行出荷機能 fee | **¥0** |
| Shipping | **¥170 + tax (¥187) flat nationwide; free at ¥3,500 (¥3,850 税込) per order** |
| Sender identity | her own shop name; the enclosed 納品書 shows **item name and quantity only — no prices** |
| Minimum | 1 unit |
| BASE link | yes — a 「BASE注文一覧」 panel exists in the account menu, and BASE listing is a documented flow ([spicelifehelp.zendesk.com/hc/ja/articles/900004627703](https://spicelifehelp.zendesk.com/hc/ja/articles/900004627703), **DIRECT**) |
| **Effort per order** | 「1つのご注文につき、1つの配送先を設定することが可能です。そのため**直送を希望されているお客様毎にご注文・決済をいただく必要がございます**。」 — **manual, per order.** **DIRECT** |

Its shipping is the cheapest in this report (¥187), and free above ¥3,850 — but the manual per-order step is the same trap as §4.3.

**(b) オリラボマーケット (market.orilab.jp) — a SUZURI-style marketplace, and its terms are the best found**

| | | Source |
|---|---|---|
| **Commission on her margin** | **Zero.** 「販売手数料は**一切かかりません**。オリラボマーケットでは、商品が販売された際にクリエイター様に対して手数料を差し引くことはございません。」 | [articles/16228046022681](https://spicelifehelp.zendesk.com/hc/ja/articles/16228046022681), **DIRECT** |
| **Reward** | 「販売時に設定いただいております**販売利益の100%が報酬**となります。」 | [articles/900000850786](https://spicelifehelp.zendesk.com/hc/ja/articles/900000850786), **DIRECT** |
| **Consumption tax** | paid **on top** of her margin: 販売報酬 + 販売報酬 × 消費税 | [articles/22837731121945](https://spicelifehelp.zendesk.com/hc/ja/articles/22837731121945), **DIRECT** |
| **Transfer fee** | **¥0 at ¥5,000+** (paid automatically, no application). ¥150 between ¥1,500 and ¥5,000 (manual application). Below ¥1,500 it rolls over. 「なお、銀行振込手数料はオリラボ負担となります。」 | [articles/900000850786](https://spicelifehelp.zendesk.com/hc/ja/articles/900000850786) + [articles/900000847423](https://spicelifehelp.zendesk.com/hc/ja/articles/900000847423), **DIRECT** |
| **Schedule** | confirmed by the 15th of the following month, paid at that month's end | [articles/900000850706](https://spicelifehelp.zendesk.com/hc/ja/articles/900000850706), **DIRECT** |
| **Effort per order** | **Zero.** 「ご注文を受け付けた後の制作発送及び発送後に何らかのサポートが必要になった場合の**購入者へのサポート業務もオリラボマーケットにて行っております**」 | [articles/4910282958617](https://spicelifehelp.zendesk.com/hc/ja/articles/4910282958617), **DIRECT** |
| **Her identity on the parcel** | 「納品書の記載については**オリジナルラボ株式会社名**を記載しております。デザインをご登録いただいたユーザ様の個人情報などは一切記載されません」 | [articles/900001497386](https://spicelifehelp.zendesk.com/hc/ja/articles/900001497386), **DIRECT** |
| **Overseas** | 転送コム banner appears automatically for overseas visitors; buyer-arranged, zero work for her | [articles/900004897823](https://spicelifehelp.zendesk.com/hc/ja/articles/900004897823), **DIRECT** |
| **Art-relevant categories** | ポスター, パネル, タペストリー, アクリルスタンド・フィギュア, カード, クリアファイル, ノート・手帳, マスキングテープ, ステッカー | [market.orilab.jp](https://market.orilab.jp/), **DIRECT** |

⚠️ **One catch, and it is a real one.** 「インボイス未登録の免税販売者様：…**免税事業者手数料として2％を報酬から控除**させていただきます…2026年9月30日までの期間は免税事業者手数料2％、その後2029年9月30日までの期間は**5％**、2029年10月1日以降は**消費税の振り込みはできなくなり**ます」 — [articles/43335077887641](https://spicelifehelp.zendesk.com/hc/ja/articles/43335077887641), **DIRECT.** She is almost certainly a 免税事業者. **The 2% step becomes 5% in 24 days** (2026-10-01), and the tax top-up disappears entirely in 2029.

🔴 **No per-item base costs were extracted from オリラボマーケット.** The catalogue is behind a JS filter UI; the two prices that rendered were unrelated bags. **Not filled.** Structurally its economics look the best in this report (0% commission, ¥0 transfer fee), but the marketplace is far smaller than SUZURI or BOOTH — a factor that plausibly dominates a few percent of fee.

### 5.3 UP-T (up-t.jp, 丸井織物株式会社)

Has a documented **BASE連携**, a **直送機能** (direct dispatch), an own-brand shop feature, and a **マーケット** at `market.up-t.jp`. Product range is apparel-heavy but does include **ポスター, タペストリー, アートパネル・アクリルパネル, ステッカー, クリアファイル, ノート・手帳, カレンダー-adjacent stationery, 紙印刷 (名刺・チラシ・冊子)**.

🔴 **UP-T's fee structure, base costs, and — crucially — whether its BASE integration auto-fulfils or requires a manual reorder could not be established.** The pages at `up-t.jp/page.php?p=base` and `?p=cyokusou` return HTTP 200 but their body content is JavaScript-rendered and arrives empty to every fetch method available here (curl with a browser UA, WebFetch). Tried: both pages, the news article `up-t.jp/news/371`, and a Japanese-language web search. **Genuinely unfilled.** Given it is a large apparel printer, it is likely closer to the オリジナルプリント.jp pattern (manual per order) than the SUZURI pattern — but that is an inference from category, not evidence, and is not relied on below.

### 5.4 Canvath — **dead, do not consider**

Canvath (formerly GMOペパボ's dropship arm, acquired 2018) **terminated its service on 2023-11-30**, last orders 2023-09-15. Corroboration: multiple independent Japanese write-ups ([happyprinters.jp/article/9102](https://happyprinters.jp/article/9102), [value7.link/6713](https://www.value7.link/6713.html)) reference the official closure notice.

🔴 **The official announcement page could not be read** — both `canvath.jp` and `blog.canvath.jp` now fail DNS resolution entirely (`getaddrinfo ENOTFOUND`, tested twice by two different methods, 2026-09-06). **That failure is itself strong corroboration.** The closure is treated here as fact; the exact dates are **INFERRED from secondary sources**. It is named only because it still appears in current BASE-adjacent listicles and would otherwise waste her time.

### 5.5 ラクスル

🔴 **Not researched.** ラクスル is a commercial print marketplace (flyers, business cards, novelty goods) with **no known dropship or marketplace layer for individual illustrators**. It was deprioritised in favour of closing the SUZURI, pixivFACTORY and BOOTH questions properly. **If someone wants it filled, that is the one remaining named platform in the brief with no coverage.**

---

## 6. International shipping — the honest cross-platform picture

This deserves its own section because the answer is uniform and unwelcome.

| Route | Direct international shipping? | How an overseas buyer actually buys | Her effort |
|---|---|---|---|
| **SUZURI** goods | **No** | WorldShopping (worldwide), Bibian (Taiwan), 転送コム | **Zero** — proxy buys domestically and re-ships |
| **SUZURI** digital | **Yes** | normal checkout | **Zero** |
| **BOOTH / pixivFACTORY** on-demand | **No** | 転送コム; or she toggles 代理購入サービスの掲載 to appear on **Buyee / ANYBUY** | **Zero**, plus one toggle |
| **BOOTH倉庫** | **No** | same | **Zero** |
| **BOOTH** download | 🔴 **not explicitly documented** — but BOOTH runs English and 简体/繁體 storefronts (both HTTP 200) and publishes multilingual buyer templates, so overseas download purchase is near-certain | normal checkout | **Zero** |
| **BASE かんたん海外販売** | **Yes, effectively** — want.jp exports on her behalf | **native overseas cart**, local currency, Alipay/WeChat Pay/PayPal/UnionPay | She ships **domestically to want.jp**; **5%** of (item + domestic postage) |
| **BASE + POD App** | 🔴 **unresolved, probably not** (§4.4) | — | — |
| **オリラボマーケット** | **No** | 転送コム banner | **Zero** |

**Three things follow.**

1. **For physical goods, no Japanese POD platform will ship to her overseas followers.** Every route dumps them onto a forwarding agent with a signup, a Japanese warehouse address, and a re-shipping bill. Conversion through that funnel will be poor. This is a structural feature of the Japanese market, not a gap in the research.
2. **The only genuinely borderless, genuinely zero-effort product is digital** — and SUZURI prices that at **5.6% + ¥22**, leaving her ~92–93%.
3. **BASE's かんたん海外販売 is the only native overseas checkout available to her** — but it works on goods *she* ships, which is exactly the effort she is trying to escape. It is the answer for her **existing zines and originals**, not for POD.

🔴 **What share of her ~26,000 Instagram followers is outside Japan is unknown and unresearched here.** It is the single input that would most change which of the above matters — and it is the one figure she can read off her own Instagram insights in thirty seconds. (This is the same open item as #14 in the 2026-09-05 book economics report; it remains open.)

---

## 7. The visa question — unchanged, and it gates all of this

**Nothing found in this research resolves §7 of `book_economics_2026-09-05.md`, and nothing found contradicts it.** The position there stands:

- The Immigration Services Agency's wording for 資格外活動許可 covers 「収入を伴う**事業を運営する**活動」 — operating a business, not just wage work — with a 28 hours/week cap and 個人事業主 named explicitly ([moj.go.jp](https://www.moj.go.jp/isa/applications/procedures/16-8.html), **DIRECT**).
- The brightest line is that **incorporating, hiring, or taking premises requires a change to 経営・管理** — none of which POD involves.
- The genuinely ambiguous part is the 「稼働時間を客観的に確認することができる」 test. Selling files that a robot prints does not obviously produce objectively verifiable hours.
- **No artistic-practice carve-out was located** in the previous research and none surfaced in this one.

**What this research adds is narrower and factual, not legal:**

| | Finding |
|---|---|
| **What platforms actually ask for** | A **Japanese residential address** (SUZURI, BASE; not BOOTH), a **Japanese bank account** (SUZURI, BASE; **not BOOTH — PayPal works**), and, where ID is checked, a **在留カード is a first-class accepted document** (BASE, **DIRECT**). |
| **What no platform asks for** | **My Number** (the number, as opposed to the card as photo ID) — not requested by any of the five. **開業届** — not requested by any of the five. Nationality — not asked by any of the five; the test everywhere is residence. |
| **BASE's own statement** | 「海外から日本へ一時的に在住の場合 — 日本国内に住所をお持ちである場合、ショップを運営していただくことが可能です」 ([articles/206417961](https://help.thebase.in/hc/ja/articles/206417961), **DIRECT**). BASE contemplates exactly her situation and permits it. |
| **The counter-fact** | 「「SUZURI」は、国内向けサービスとして提供をしております。**海外在住クリエイターさまに関しましては、ご利用いただくことができかねます。**」 ([articles/44057520323731](https://help.suzuri.jp/hc/ja/articles/44057520323731), **DIRECT**). SUZURI's account is tied to living in Japan and would not survive her leaving. |
| **The 開業届 tension** | Unchanged: 開業届 is due within a month of starting a business ([nta.go.jp](https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/shinkoku/annai/04.htm), **DIRECT**) — and filing one is the formal act of declaring oneself to be operating a business, which is the very question at issue. |

**No platform's permission is immigration permission.** BASE saying she may open a shop is a statement about BASE's terms of service, not about her residence status. The free consultation route remains: [外国人在留総合インフォメーションセンター](https://www.moj.go.jp/isa/consultation/center/index.html) / [FRESC](https://www.moj.go.jp/isa/support/fresc/fresc01.html).

**One structural note, offered as a fact and not as advice:** a route where she is *not* the seller of record (SUZURI, オリラボマーケット, and to a lesser degree BOOTH-with-pixivFACTORY) has a materially different shape from one where she is a named 事業者 publishing her own 特定商取引法 disclosure with her legal name on it (BASE). Whether that difference matters legally is exactly the question this report cannot answer.

---

## 8. Side-by-side

### 8.1 The comparison table

| | **SUZURI** | **BOOTH × pixivFACTORY** | **BOOTH倉庫** | **BASE + オリジナルプリント.jp** | **オリラボマーケット** |
|---|---|---|---|---|---|
| **Effort to set up, once** | signup + upload per design | pixiv account, link two services, upload + set margin per item | register, print/bag/label 30+ units, courier them in | already has BASE; install App, design per item | signup + upload per design |
| **Effort per order** | **zero** | **zero** | **zero** | **6 manual steps + she fronts the cash** | **zero** |
| **Fee on her margin** | 10% (see §1.2 ambiguity) | **5.6% + ¥45** | 5.6% + ¥45 **+** 2.5% + ¥25/unit | 6.6% + ¥40 on **item + postage** | **0%** (−2% now / −5% from 2026-10-01 if 免税) |
| **Payout fee** | ¥176 | ¥200 bank / **¥0 PayPal** | ¥200 / ¥0 PayPal | **¥250 + ¥500 under ¥20,000** | **¥0** at ¥5,000+ |
| **Payout minimum** | ¥177 | ¥201 (manual) | ¥201 | ¥751 | ¥1,500 |
| **Japanese bank needed?** | **yes** | **no** (PayPal) | no | **yes** | yes |
| **Japanese address needed?** | **yes** | no | **yes** | **yes** | 🔴 not determined |
| **Her legal name public?** | no obligation found | only if 販売業者 | only if 販売業者 | **yes, unhideable** | no — 納品書 is the operator's |
| **Paper art prints?** | **no** | **yes** — posters ¥1,280, canvas ¥3,350, framed giclée ¥12,000 | via pixivFACTORY direct-in | yes (range unpriced) | yes (unpriced) |
| **Postcards?** | **no** | **yes** — ¥1,835 / 10 | yes | yes | 🔴 |
| **International** | proxy only; **digital ships worldwide** | proxy + one-click Buyee/ANYBUY; EN & 中文 storefronts | proxy only | **native overseas cart via want.jp, 5%** (but 🔴 with POD) | proxy only |
| **Fixed monthly cost** | ¥0 | ¥0 | **¥1,000+tax, waived at 20% monthly sell-through** | ¥0 | ¥0 |

### 8.2 What she nets on a ¥3,000 sale (item price, before postage)

**INFERRED**, method stated per row. Payout fees excluded (they're per-payout, not per-sale).

| Route | Product at ¥3,000 | Manufacturing | Fee | **She keeps** |
|---|---|---|---|---|
| BOOTH × pixivFACTORY | ポスター A2 | ¥1,400 | ¥135 (5.6%+¥45 on ¥1,600 margin) | **¥1,465** |
| BOOTH × pixivFACTORY | 色紙 (standard) | ¥1,690 | ¥119 | **¥1,191** |
| SUZURI | マグカップ | ¥2,046 | 10% of トリブン, buyer-borne | **¥867** |
| SUZURI | 吸着ポスター (at ¥3,300) | ¥2,178 | ditto | **¥1,020** |
| SUZURI (digital) | PDF / wallpaper set | — | ¥190 (5.6%+¥22) | **¥2,810** |
| BASE (self-fulfilled, as today) | a zine or original | her own cost | ¥238 (6.6%+¥40) | **¥2,762 − her costs − her time** |

The digital row is not a trick. It is the actual arithmetic, and it is why §1.7 is in this report at all.

---

## 9. Ranked by effort, lowest first

**Effort = setup once + work per order + ongoing obligations.**

| # | Route | Setup | Per order | Ongoing | Verdict |
|---|---|---|---|---|---|
| **1** | **SUZURI デジタルコンテンツ** | upload a file | **nothing** | none | Lowest effort that exists. Sells worldwide. She keeps ~92%. But it is a file, not an object. |
| **2** | **SUZURI goods** | one signup, one upload per design | **nothing** | none — auto-payout after 5 months | Simplest physical route. **Wrong catalogue for a painter.** |
| **3** | **BOOTH × pixivFACTORY on-demand** | pixiv account, link two services, upload + set a margin per item | **nothing** | none | Marginally more setup than SUZURI. **Right catalogue.** PayPal payout. Anonymous dispatch. |
| **4** | **オリラボマーケット** | one signup, upload per design | **nothing** | none | Best economics on paper (0% commission, ¥0 transfer). Small audience; 免税 deduction rises to 5% on 2026-10-01. |
| **5** | **BOOTH倉庫** (for her *existing* zines) | produce, bag, label, courier 30+ units in | **nothing** | ¥1,000+tax/month unless 20% sells | Real up-front labour, then zero. **The pixivFACTORY→warehouse direct path skips the labour entirely** and is the only way a printed zine reaches buyers without entering her flat. |
| **6** | **BASE + オリジナルプリント.jp** | App install, design per item | **6 steps + she pays the printer** | ¥750 in payout fees under ¥20,000 | Least disruptive on paper because she is already on BASE. **In practice the highest per-order workload here.** |
| **7** | **グッズラボ 直送 / UP-T 直送 / オリジナルプリント.jp direct** | account + design | **manual reorder per order** | — | Suppliers, not channels. Cheapest postage (¥187, グッズラボ). UP-T's mechanics 🔴 unverified. |
| **—** | **Canvath** | — | — | — | **Closed 2023-11-30. Domain is gone.** |
| **—** | **ラクスル** | — | — | — | 🔴 Not researched. |

---

## 10. Which one to start with

### **BOOTH × pixivFACTORY on-demand.**

**Why, plainly:**

1. **It is the only zero-per-order route whose catalogue matches what she makes.** SUZURI is marginally simpler to set up — one service instead of two — but SUZURI **cannot print a postcard or a paper art print**. pixivFACTORY prints a **B3 poster for ¥1,280**, a **10-postcard set for ¥1,835**, an **F3 canvas for ¥3,350**, and an **A4 framed archival giclée for ¥12,000**. For a watercolour painter of urban architecture and light, that is the difference between selling merchandise and selling her work.

2. **It fills the missing rung on her price ladder.** She sells at ¥1,980 (zines) and then nothing until ¥31,900 (originals). An A2 poster at ¥3,000 keeps her **¥1,465**; an A1 at ¥5,000 keeps **¥2,268**; the framed giclée at ¥20,000 keeps **¥7,507**. These are the ¥2,000–20,000 products she does not currently have, and she can list all of them in an afternoon without buying a single sheet of paper.

3. **The fee lands on her margin, not the ticket.** 5.6% + ¥45 **of the margin only** — the most favourable structure of any platform here, and structurally better than BASE's 6.6% + ¥40 on item-plus-postage.

4. **It does not require a Japanese bank account.** PayPal, fee-free. Given §7, that is the one route whose payout does not depend on a piece of Japanese financial infrastructure.

5. **It does not put her name and flat on the parcel.** Sender reads 「ピクシブ株式会社」; 特商法 contact details are only required if she is a 販売業者. On BASE her legal name is mandatory and unhideable, and her address is on the packing slip.

6. **Overseas is one toggle**, plus English and Chinese storefronts and a ready-made multilingual announcement she can post to Instagram.

**Start with one product, not twelve.** An **A2 poster of a single strong architectural piece, priced at ¥3,000.** Upload one image, set the margin, publish. Manufacturing is ¥1,400, shipping is ¥326 regardless of quantity, and she keeps ¥1,465 per sale having touched nothing. If it sells, add sizes and a postcard set. If it does not, she has lost an afternoon and no money at all.

**Then, in order:** (a) **SUZURI デジタルコンテンツ** for the overseas half of her audience, because it is the only borderless thing in this report and she keeps 92% of it; (b) **SUZURI goods** for the ¥900–1,500 sticker-and-badge impulse tier that pixivFACTORY does not price as sharply; (c) **BOOTH倉庫 via the pixivFACTORY direct-intake path** if the printed zine ever goes to a second run.

**What to stop expecting:** that BASE will become a POD platform. Its App route costs her six manual steps and her own cash on every order. Her BASE shop remains the right home for originals and for her existing zines — and **かんたん海外販売 is the one thing BASE does that nobody else here does**, for exactly those self-shipped items.

---

## 11. Gaps — marked, not filled

| # | Gap | Status and what was tried |
|---|---|---|
| 1 | **SUZURI's exact トリブン arithmetic** — whether the buyer or she absorbs the 10% | 🔴 **Ambiguous.** The official wording (§1.2) supports the buyer-pays reading, and that is used. Tried: the full 446-article API dump, two Japanese third-party explainers, and reverse-engineering from live listing prices (the category URL 404s to a plain client). **Worth ~10% of her margin.** Resolvable in 60 seconds inside SUZURI's own item-creation screen, which requires an account. |
| 2 | **SUZURI's small-item shipping rate** | 🔴 **Not published.** SUZURI's official answer is "look in the cart." Only ¥740 (standard) and ¥420 (Tシャツ便) exist as current figures. A 2023 announcement gives ¥780/¥395 for acrylic-class items — three years stale and inconsistent with ¥740, so recorded but unused. |
| 3 | **キャンバス and 複製画 shipping at pixivFACTORY** | 🔴 **Absent from an otherwise complete 10-group shipping matrix.** Tried: the full 184-article help dump, both product pages, the BOOTH shipping FAQ. Materially affects the ¥12,000–29,500 giclée economics. |
| 4 | **オリジナルプリント.jp per-unit base costs** | 🔴 **Not extracted.** ~1,500 SKUs behind a JS configurator; no static table exists. Deprioritised once the six-step per-order flow was confirmed. |
| 5 | **UP-T: fees, base costs, and whether its BASE link auto-fulfils** | 🔴 **Genuinely unfilled.** `up-t.jp/page.php?p=base` and `?p=cyokusou` return HTTP 200 with JS-rendered empty bodies to every available fetch method. Also tried the news article and a Japanese web search. **The likeliest remaining find of any gap here.** |
| 6 | **オリラボマーケット per-item base costs** | 🔴 **Not extracted** — JS-filtered catalogue. Its *terms* (0% commission, ¥0 transfer) are fully DIRECT and are the best in the report; only the prices are missing. |
| 7 | **ラクスル's goods line** | 🔴 **Not researched at all.** Named in the brief; deprioritised to close SUZURI/pixivFACTORY/BOOTH properly. |
| 8 | **Whether BASE かんたん海外販売 composes with a POD App** | 🔴 **Unresolved.** Both BASE and the App carry hedged warnings (§4.4); neither states a definite answer. Needs a live test. |
| 9 | **BOOTH download items sold overseas** | 🔴 **Not explicitly documented** in 428 articles. Circumstantially near-certain (EN and 中文 storefronts both live, multilingual buyer templates published). SUZURI's equivalent **is** documented. |
| 10 | **Canvath's official closure notice** | 🔴 **Unreadable — the domain no longer resolves at all.** Closure corroborated by two independent Japanese sources; dates are INFERRED from them. The DNS failure is itself corroboration. |
| 11 | **SUZURI: minimum age, phone-number requirement, and 特商法 obligation** | 🔴 **Absent from the help centre.** BOOTH and BASE both publish 18+; SUZURI does not. The 特商法 absence is consistent with SUZURI being the seller of record but **should be confirmed at signup, not assumed.** |
| 12 | **Cost of couriering stock into BOOTH倉庫** | 🔴 **Not a BOOTH fee** — a normal Yamato/Sagawa charge set by her origin and box size. Not published by anyone, and not knowable without her actual parcel. |
| 13 | **What share of her ~26,000 followers is outside Japan** | 🔴 **Unknown, and the single input that would most change §6.** Not researched — **she can read it off her own Instagram insights.** Carried over unresolved from the 2026-09-05 report. |
| 14 | **The SUZURI T-shirt 原価 discrepancy** (¥2,871 archived vs ¥3,091 live) | 🔴 **Unexplained.** The older help article is no longer in the API dump. The live figure is used throughout. |

**Method note.** The Firecrawl MCP returned **401 Unauthorized** again this session (tested first). WebSearch and WebFetch both worked. **The breakthrough was the Zendesk Help Center REST API** (`/api/v2/help_center/ja/articles.json`), which returned complete article bodies from all five platforms' help centres — 446 SUZURI, 428 BOOTH, 184 pixivFACTORY, 800 BASE, 168 spicelife/オリラボ, **2,026 articles in total** — including `help.suzuri.jp`, which returns HTTP 403 to ordinary fetching. **That single technique is why §1 exists.** Product catalogues came from direct scrapes of `suzuri.jp/item_templates` (150 items priced) and 21 `factory.pixiv.net/products/*` pages. The gaps that remain (4, 5, 6) are all the same failure mode: **JavaScript-rendered commerce catalogues with no static price table**, which no tool available in this session can read. A browser-driving tool would likely close all three.

**No figure, price, percentage or URL in this report was invented.** Every number is read off a cited page (DIRECT), derived by a stated method from cited pages (INFERRED), or marked 🔴 as not found.
