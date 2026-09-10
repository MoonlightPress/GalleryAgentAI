# Chinese cold read — the 2026-09-10 batch

Method: the Chinese was extracted and read standing alone, before any English was
seen. Then the pages were rendered in zh at `localhost:5177/mochi/#observe` and
read as she would read them. English was consulted only afterwards, to work out
what a broken sentence had been trying to say.

**Nothing has been rewritten.** This is findings only.

## Verification notes (read these before acting)

- **The dev API was serving pre-`2243bbc8` copy.** `/api/saffron` still returned
  `四个账号…16.8 万` while `futures_engine.py:1271` says `五个账号…23.3 万`.
  `build_futures` runs per request with no cache file, so this is purely a stale
  resident module in Scott's running `api.py` — restart it before judging any
  engine string in the browser. Engine strings below were verified by calling the
  engines directly instead.
- **`尚未拥有的credit` is NOT a defect.** It lives in a comment at
  `career_strategy_engine.py:735` documenting a past fix. My first extractor
  flagged it as live; the token-level recheck cleared it.
- **`山楂` for Saffron is correct**, not a hawthorn mistranslation — it is used
  consistently in `Nav.jsx`, `translations.js` and `SaffronPage.jsx`.
- **The five-platform / 233k figures are right** as of `3f13c4e0` (Weibo added).
  `CLAUDE.md`'s "All four counts, settled 2026-09-08" table is now the stale one.

---

## A. Sentences that do not parse — a Chinese reader stops here

| # | File:line | The problem |
|---|---|---|
| A1 | `strategy_ladders.js:130` | `2023 年那一轮有的是一个「钩子」` — **`有的是` is a fixed idiom meaning "there is no shortage of."** The sentence therefore reads "that run had plenty of hooks," the opposite of the point. This is the worst one on the page. |
| A2 | `strategy_ladders.js:155` | `增长最快的方式是借来的，而不是攒出来的` — a 方式 cannot be 借来的. The English "borrowed, not accumulated" has no Chinese footing here. |
| A3 | `strategy_ladders.js:70` | `认出来发生在读到名字之前` — a bare verb phrase as the subject of 发生. English nominalization ("recognition happens before…"); Chinese needs an agent. |
| A4 | `strategy_ladders.js:60` | `通常是通过代理画廊到达，而不是在那之前` — 到达 with no object, then a dangling calque of "not before that." |
| A5 | `strategy_ladders.js:91` | `你已经产出了一阵子了` — 产出 is not intransitive. |
| A6 | `strategy_ladders.js:94` | `是媒介做出观众预料不到的事的那些瞬间` — three stacked 的-clauses; unreadable at speed. |
| A7 | `strategy_ladders.js:56` | `因为画廊介绍的是它打算长期留住的藏家` — introduces them *to whom*? The sentence has no destination. |
| A8 | `outreach_kit_engine.py:92` | `任何一句回复，本身就是一份要求说明` — 要求说明 is not a thing. Note the **English is also broken** here ("any reply is a specification"), so this needs a decision about meaning, not a translation fix. |
| A9 | `futures_engine.py:304` | `一位东京插画师，两万七千粉丝，只是你影响力的一小部分，自出版的画集定价…` — garden path. The three appositives read as a complete sentence ("a Tokyo illustrator with 27,000 followers is a small part of your reach" — nonsense), and the next clause then has no subject. **The number 27,000 is also exactly her own Instagram count**, which makes the confusion worse. |
| A10 | `futures_engine.py:543` | `按你的价格，这个空间相当于卖出 1–4 张画` — a *space* is not equivalent to an *act of selling*. Needs 这个空间的成本相当于… or 租下这个空间，等于要卖出… |
| A11 | `saffron_insights.js:279`, `:287` | `且须在符合条件的补助经费范围内` / `不得超过符合条件的补助对象经费` — **`補助対象経費` borrowed straight from the Japanese; the compound means nothing in Chinese.** Verified in the DOM: line 279 renders as the *headline amount* on the Arts Council Tokyo card, directly under the title. This is the most prominent broken string in the batch. |

## B. Wrong word or wrong register

| # | File:line | The problem |
|---|---|---|
| B1 | `strategy_ladders.js:112,119,126,134,174,176` (影片) · `124,126,130` (短片/长片) | **`影片` means *motion picture* in mainland usage; `短片`/`长片` mean short film / feature.** She is mainland (小红书, B站, 微博). The words she and Bilibili use are 视频 / 短视频 / 长视频. This runs through the entire `a_weekly` treatment block — the single most pervasive issue in the batch. |
| B2 | `strategy_ladders.js:100` | `录像` — VHS-era. → 视频. |
| B3 | `strategy_ladders.js:94` | `一片洗染` — **`洗染` is textile washing-and-dyeing.** A watercolour wash is 渲染 / 晕染 / 一层薄涂. She will notice this one immediately; it is her own craft vocabulary. |
| B4 | `strategy_ladders.js:40` | `它们没有货要卖` — `货` is merchandise-crude for a museum. |
| B5 | `strategy_ladders.js:134` | `触到了` (physical touch) → 触达. |
| B6 | `strategy_ladders.js:126,130` | `139 播放`, `播放大多在…` → 播放量. |
| B7 | `strategy_ladders.js:36` | `初登场` is 初登場, Japanese. → 首秀 / 初次亮相. |
| B8 | `strategy_ladders.js:88` · `saffron_insights.js:79` | `结构上` / `从结构上说` — "structurally" does not carry as an intensifier in Chinese; it reads as an engineering term. |
| B9 | `strategy_ladders.js:138` | `延时完全可以` — 延时 alone is "time delay," not timelapse (延时摄影). And `压缩过` reads as *video* compression. |
| B10 | `strategy_ladders.js:32,97,204,272` · `outreach_kit_engine.py:96` | **`成立` is used five times for English "holds,"** and is slightly wrong each time — 履历里出版的那一半已经成立, 原样成立 (×2), 印出来依然成立, 正文对任何一家都成立. 成立 means an argument is valid; it does not mean a thing works or survives. |
| B11 | `career_strategy_engine.py:671` | `车站直连` — 駅直結, a Japanese real-estate calque. |
| B12 | `career_strategy_engine.py:800`, `:811` | `入管` is Japanese (入国管理局) and unglossed. Also `入管方面的授权` — 授权 is wrong for a permit; → 许可. |
| B13 | `career_strategy_engine.py:769` | `与上者同批征集` — 与上者 is classical/legalese in a page written to be warm. |
| B14 | `career_strategy_engine.py:748` | `在墨田连着几个月的工作室时间` — "studio time" calque; 工作室时间 is not a Chinese noun. |
| B15 | `career_strategy_engine.py:579` | `附三张日记系列` — measure-word mismatch: 三张 counts sheets, 系列 is a series. |
| B16 | `futures_engine.py:229`, `:1271` | `一套跑起来的创作和生意`, `店铺已经在跑` — **`跑` here is developer jargon** ("running"). → 运转起来 / 已经开着. |
| B17 | `saffron_insights.js:137` | `具有独特声音` — an artist's "voice" does not render as 声音 in Chinese. |
| B18 | `saffron_insights.js:191` | `对他们的编辑内容极具吸引力` — content cannot be attracted to something. Category error. |
| B19 | `saffron_insights.js:226`, `:228` | `主动申请` for press → 投稿 / 自荐. You don't 申请 a magazine feature. |
| B20 | `saffron_insights.js:295` | `一笔发放` → 一次性发放. |
| B21 | `saffron_insights.js:321` | `这和你现在的画法是两回事` — 画法 is *brush technique*; the English meant her whole practice. Narrows it wrongly. |
| B22 | `strategy_ladders.js:219` | `效果图替他想` — "the mockup thinks for him." → 替他想好了 / 直接给他看. (The rest of `l_lookbook` **does** end cleanly after the clause removal — verified.) |
| B23 | `futures_engine.py:1298` | `一个日本文学出版社会买来做封面的题材` — 出版社会 garden-paths as 出版+社会 on first read. |
| B24 | `translations.js:405` | `sf.audience.fact` — `五个平台上稳固且持续增长的受众`. 稳固 is for structures; an audience is 稳定. Minor. |

## C. Untranslated Japanese she cannot read

Kana is opaque to a Chinese reader. Each of these needs a gloss, not removal.

- `strategy_ladders.js:245` — `ほぼ日`, `「アーティストコレクション」`
- `saffron_insights.js:35`, `:45` — same two
- `saffron_insights.js:72` — `《ザ・チョイス》`, `「装画コンペ」`, and `資格：不問` (Japanese kanji forms inside a Simplified sentence)
- `saffron_insights.js:99` — `買い取り／著作権譲渡`
- `saffron_insights.js:204`, `:206` — `マガジンハウス`

(The postal address block at `:206` should of course stay in Japanese — it gets copied onto an envelope.)

## D. Contradictions and duplication — all confirmed in the rendered DOM

| # | Where | The problem |
|---|---|---|
| D1 | `strategy_ladders.js:161` vs `:191` | One card says `中文这边现在明显更大`; the disclosure below it says Chinese 116,500 vs English 116,300 — `几乎追平`. `这两边` is ambiguous (中文 vs 英文? or 中文 vs Instagram?), so the two read as a straight contradiction. |
| D2 | `strategy_ladders.js:227` | `至于你的名字在不在上面，这个系统没有查过` renders **directly beneath the auto-generated label `系统从来没有核实过这一项`**. The same fact, twice, in two different voices, in one card. |
| D3 | `saffron_insights.js:279` vs `:287` | The amount line and the 提示 line say the same thing — and both carry the A11 unparseable phrase. |
| D4 | `strategy_ladders.js:119` | `连续六周的翻翻乐，播放量分别是 55,000、49,000、16,000` — **three numbers for six weeks.** |
| D5 | `strategy_ladders.js:97`, `:145`, `:176` | `因为看颜料流动不需要语言` appears three times near-verbatim, twice within one expanded ladder. |

## E. Typography — visible on the page

1. **Mixed quote marks.** `「」` at `strategy_ladders.js:100,130,227,245`; `“”` in `outreach_kit_engine.py:74,76` and `futures_engine.py`. Both render on the Saffron page. zh-CN standard is `“”`; `「」` is the Japanese/Traditional convention.
2. **Mixed colons.** `要准备好的: ` (ASCII colon + space) against `资格要求：` (fullwidth) — same tab, a few hundred pixels apart.
3. `下一级：␣被评论` — an ASCII space after a fullwidth colon, which already carries its own spacing.
4. **Mixed currency.** `¥394,500` on the same panel as `394,500 日元`.
5. **Mixed digit spacing.** `每年12月` (career engine) vs `2026 年 9 月` (saffron_insights).
6. Fullwidth `＋` in `个展 ＋ 15 万日元` and `“费用＋授权”`.

## F. `LETTER_JA` — the letter she would actually send

The **new opening line reads well**: `若い作家の仕事を丁寧に紹介していらっしゃる場だと感じ` is natural and correctly humble, and `HAGI ART ご担当者様` is the right form of address for a gallery with no named contact. The problems are elsewhere in the letter.

1. **No closing.** The letter ends at `［リンク］` and the signature with no `何卒よろしくお願い申し上げます。` A Japanese business email essentially always closes this way; its absence is the single most conspicuously foreign thing in the letter. **This is the one that could cost her the opportunity.**
2. **Politeness level flips mid-paragraph.** `個展を開催しました` (丁寧語) then `個展を三度開催いたしました` (謙譲語), two sentences apart, about the same subject.
3. **The exhibition count reads as 1 + 3 = 4.** "This year I held a solo show at LE MONDE" followed by "I have held three solo shows in Shanghai and Tokyo" — a reader cannot tell whether the LE MONDE show is inside the three. It is.
4. **The request is incomplete.** `実物をお持ちしてご覧いただければ幸いです` chains two humble forms without ever asking for the occasion. Standard: `…ご覧いただく機会をいただけましたら幸いです`.
5. **Subject line is a question.** `件名：作品を見ていただけますでしょうか` — Japanese business subject lines are noun phrases (`作品ご高覧のお願い（水彩画家 GEGYjiji）`). `見ていただけますでしょうか` is also the doubled-polite form often flagged as 二重敬語; `ご覧いただけます` is cleaner. The `—` separator is not a Japanese convention either.
6. **Signature is a bare handle.** `GEGYjiji` + `@gegyjiji`, no contact line — reads as social media, not correspondence.

Minor: `若い作家の仕事` → `作品` is the more idiomatic collocation for artwork.

## G. Facts worth checking (not language)

- `career_strategy_engine.py:774`, `:1279` — `你往返东京与北京的创作实践`. **Beijing does not appear anywhere else in her record** (Shanghai, Guangzhou, Tianjin, Taizhou, Tokyo, London). If it is wrong, it is a claim that would be made on her behalf.
- `career_strategy_engine.py:637`, `:747` — `东京都现代美术空间（Tokyo Arts and Space）` appears to be an invented Chinese rendering of TOKAS. Worth confirming there is no established Chinese name.

## H. Reads well — leave alone

- `strategy_ladders.js:245` `这样的门，只会从另一边打开` — the metaphor lands cleanly in Chinese. Keep it.
- `saffron_insights.js:106` `谁给你数字，谁就是在猜。`
- `saffron_insights.js:315` — the China National Arts Fund entry is the best Chinese in the batch (`户籍`, `单位推荐函`, `副高级` are all exactly right).
- `saffron_insights.js:334` `写在这里，是免得你白花一个月才发现。`
- `career_strategy_engine.py:697` `等代理之后，自然会到。`
- `futures_engine.py:270-272`, `:318-321` — the print-on-demand and book-economics prose is natural throughout.
- The `career_strategy_engine` grant f-string composes cleanly — verified by running it: `两扇门此刻开着：东京艺术委员会（Arts Council Tokyo）面向新锐艺术家的扶持金，9月24日截止；加拿大的…`
