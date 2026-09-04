# Weekend prose review — does the writing land?

*2026-09-04. Lens: when she reads this, does she feel seen, encouraged, and excited about what's next. Nothing else — no structure, no fact-checking. ZH read as the primary language (it is hers); EN alongside.*

---

## Overall verdict

The hand-written companion voice is the best writing in the app, and some of it is genuinely good. Saffron's career synopsis, the gap headline "从作品被展示，迈向作品被书写", the residency target that says "你往返东京与北京的创作实践，正是它面向的对象", the Kaikai Kiki line that turns her Instagram following into "一扇门" — these know who she is and say so with evidence. **Seen** is achieved wherever a human wrote the sentence with her in mind.

Where it misses, it misses in two specific places, and they are the two places she reads most:

1. **Today's Focus cards.** The three sentences at the top of Mochi's page — the whole product, per the Bible — are catalog descriptions. Today's actual picks read "以AQYLA水性丙烯颜料为指定媒材的绘画比赛，适合水彩及插画艺术家参与" and "面向国际视觉艺术家，覆盖绘画、素描及综合媒介等类别". Not one clause in any of the three could only have been written about her. The quick-win card even leaks the internal tier framework ("实在一级途径") and ends on a negative. The app's most personal writing lives three pages deep; its least personal writing is the first thing she sees.

2. **The seven levers written tonight.** Naming real galleries and grants did make them more alive — the *targets* are the most exciting material in the app. But the *details* became checklists, and not because of the facts. It's because every fact appears three times (detail paragraph, action line, target window), and because four of the seven actions begin with 留意 / "watch for". Watching is not doing. A TOKAS residency call that opens in ten days is written in the same register as a Holbein round in mid-2027.

**Encouraged** is mostly earned — the copy validates with counts and named credits, not adjectives, and the "if you want it" hedges keep it from pushing. Two lines undersell her (the synopsis says "一场东京个展" while the status line beneath it says "3 场个展"; Peppercorn still asks whether a *second* Japan exhibition is planned). One line stings before it opens a door ("你至今的个展都在付费租赁场地举办").

**Excited** is the weakest of the three. The app is good at "here is where you stand" and adequate at "here is a door". It is rarely good at "something is about to happen". The material to fix that already exists in the data — it just needs the near things to sound near and the actions to be things she can do on a Tuesday.

---

## Mochi — the action page

### The poems (`translations.js` zh 45–52) — keep, one small note

Eight Tang/Song poems about water, light, mist and moon. This is the most *seen* thing in the app precisely because it never talks about her — 返景入深林，复照青苔上 is her painting practice in ten characters. Do not touch these.

One note: seven of eight are dusk or night, and 张继's 江枫渔火对愁眠 ("I sleep facing sorrow") is a heavy line to rotate in at 9 a.m. If a ninth is ever added, a bright morning one would balance the set — 杜甫's 迟日江山丽，春风花草香, or 苏轼's 竹外桃花三两枝，春江水暖鸭先知.

### Mochi's intro (`mochi.intro.body`, `App.jsx:47`)

> 你好，我是麻薯。我在东京四处游走，探索这里的艺术世界，我找到了几个你或许会喜欢的机会。

Warm, but "几个你或许会喜欢的" is a hedge on a hedge, and "探索这里的艺术世界" could open any app. Mochi's spec is watchful and precise — she did legwork while the artist was away. Say that.

**Rewrite (zh):** 你好，我是麻薯。你画画的时候，我把东京的画廊、书店和征集都走了一遍——挑出了三件值得你看一眼的事。
**Rewrite (en):** Hi, I'm Mochi. While you were painting I walked Tokyo's galleries, bookshops and open calls — and kept three things worth your eye.

### Today's Focus frame (`tf.*`, `translations.js` zh 984–997)

> 麻薯为你找到了三件值得关注的事。

Good. This is the Bible's line and it lands.

> 没有紧急事项，明天再来。

Matches the spec but in zh it reads as an instruction. She is a painter; the empty state can honor that.

**Rewrite (zh):** 今天没什么急事。去画画吧——明天再来看看。
**Rewrite (en):** Nothing urgent today. Go paint — come back tomorrow.

**Role labels:** 快速行动 / 重点任务 / 挑战目标. In English "Quick Win / High Impact Move / Stretch Goal" is spec'd; in Chinese the literal renderings read like a corporate OKR sheet — 重点任务 is "key task", 挑战目标 is "challenge target". The hero block uses 延伸目标 for the same slot (`hero.tier.stretch`), which is warmer; the two disagree.

**Rewrite (zh only):** 五分钟的事 / 今天最值得做的 / 往远处走一步

### The actual cards — the biggest miss on the page

Computed from `api.py get_today()` at review time. Quick Win (B&B, Shimokitazawa):

> 下北泽一家知名的书店酒吧，以低门槛寄售艺术书与 zine，并有活动企划——是在东京建立印刷品存在感的实在一级途径。适合自出版或艺术家书，而非原作绘画。

Three problems in two sentences. "实在一级途径" is "a concrete Tier-1 route" — she has never heard of Tier 1; it reads as a bureaucratic grade. It ends on 而非原作绘画 — a negative — after the builder's own rule of no negative framing. And there is nothing of her in it: no *Colour Diary*, no diary zine, nothing she'd put on that shelf.

**Rewrite (zh):** 下北泽的书店酒吧，卖艺术书和 zine，也常办活动。寄售门槛很低、不收费——把《Colour Diary》或一本新的日记小册子放上他们的书架，是让作品在东京流通起来的一个很自然的起点。
**Rewrite (en):** A Shimokitazawa bookshop-bar that stocks art books and zines and hosts events. Consignment is easy and free — *Colour Diary*, or a new diary zine, on their shelf is a natural first way to put your work into circulation in Tokyo.

High Impact (第10回アキーラコンテスト):

> 以AQYLA水性丙烯颜料为指定媒材的绘画比赛，适合水彩及插画艺术家参与。

This is the summary field repeated as the "why". It's flat, and "适合水彩" next to "丙烯颜料" reads like a keyword match rather than a judgment. If there is a real reason this is today's most important move — a Japanese manufacturer's prize that Japanese galleries recognize, a water-based medium close to her hand — the card has to say it, or it should not be the High Impact slot.

**Rewrite shape (zh):** [品牌]的年度绘画大赛——日本画材品牌办的奖，在日本画廊眼里是实打实的一行履历。指定媒材是水性颜料，和你的水彩手法相近，值得用一张日记试试。
**Rewrite shape (en):** [Brand]'s annual painting prize — a Japanese materials-maker's award that Japanese galleries read as a real CV line. The medium is water-based, close to your hand; worth trying with one diary piece.

Stretch (Artist Grant, city "Unknown"):

> 面向国际视觉艺术家，覆盖绘画、素描及综合媒介等类别，资金使用不受限制。

Could be any artist on earth. And `city: Unknown` renders as the English word "Unknown" on her Chinese page.

**The rule worth adopting:** every `why_card` must contain one clause that could only be written about her — her medium, her diary, her book, her city, her stage. If the generator can't produce that clause, that is the signal the pick is weak.

### Smaller Mochi copy

- `opps.strongest.desc` "几个看起来已就绪、契合信号清晰的建议。分数留在幕后。" — "契合信号" is engine vocabulary. **Rewrite:** 几个麻薯有把握的推荐——为什么选它，都写在卡片上；打分留在幕后。
- `section.immediate_best_moves.desc` "已确认截止日期或已知提交路径。优先处理这些。" — form-letter. **Rewrite:** 截止日期和投递方式都已经核实过——如果今天只做一件事，从这里选。 / *Deadlines and how-to-apply already checked. If you do one thing today, pick from here.*
- `card.toast.notForMe` "已从此面板隐藏。" — cold next to the lovely `card.toast.maybe` "麻薯会先帮你留着。" **Rewrite:** 好的，麻薯收起来了。 / *Okay — Mochi's tucked it away.*
- `newOpps.found` "麻薯这周发现了 {n} 个新机会" — good as is.

---

## Peppercorn — the quiet corner

### The intro (`pp.intro.body`)

> 我是胡椒粒。这是你安静的角落——把正在发生的事、你期待的方向告诉我，我会让麻薯和山楂真正读懂你。这里没有急事，我会记住一切。

The voice is right — small, quiet, remembers. One word: 我会记住一切 ("I will remember everything") has a faint surveillance edge in Chinese that the English "I remember everything" also carries. Softer, same meaning:

**Rewrite (zh, last clause):** 这里没有急事，你说的我都会记着。
**Rewrite (en, last clause):** Nothing here is urgent, and whatever you tell me, I keep.

### Section synopses (`pp.syn.*`, `pp.sub.*`)

These are good. "来自山楂的安静提问——你的回答会让她看得更准" and "山楂留了{n}条提问 — 有空的时候再答" are exactly Peppercorn's register. "你在为什么努力？不需要任何格式 — 胡椒粒会理解的" is warm. Nothing to change here.

### The artist statement section — the note, the example, and what's in the box

The note (`pp.stmt.note`):

> 这段文字为麻薯起草的每封联络邮件、每封求职信、每个由麻薯生成的机会描述提供素材。真实具体的自述能产出听起来像你的文字。通用的自述只会产出通用的文字。

Three things. 求职信 is a *job* cover letter — wrong register for an artist (投稿信 / 申请信). "产出…文字" is manufacturing language. And the whole note is about what the system needs from her, which is the opposite of the page's purpose.

**Rewrite (zh):** 这一段是麻薯替你写信时的底稿——给画廊的邮件、投稿的附信、机会的说明，都会从这里取你的语气。写得越像你自己，寄出去的每一封信就越像你说的话。
**Rewrite (en):** This is the ground Mochi draws from every time she writes on your behalf — a gallery email, a submission letter, a description of your work. The more it sounds like you, the more every letter sent out will.

The "specific" example (`pp.ex.specific.text`) is lovely and is about her — "人来之前的街道，人离去之后的咖啡馆". Keep it exactly.

But the seed statement actually *in the box* (`peppercorn_profile.json artist_statement_zh`) opens "GEGYjiji 是一位旅居东京的中国水彩艺术家，来自湖南，曾在北京服装学院学习插画与设计" — third person, name, province, university. It is a press bio, and it is the generic pattern the example directly above it warns against. It also ends on her February 2023 first Japan show as if that were the latest news. She will notice that the box that says "sound like you" contains a catalog entry about her. The middle of the bio is beautiful, though ("红墙与巷弄、水池与绿塘、室内的房间、熟悉街道上那一缕特有的暖阳"). A first-person draft built from the same material, marked as a draft for her to overwrite:

**Draft (zh):** 我从2020年开始每天画一张水彩，叫它「日记」。画的多半是平常的东西：红墙和巷子、水池和绿塘、房间里的光、熟悉的街道上某个时刻的太阳。我用水彩，因为它留下的正是记忆留下的：边缘是软的，颜色会呼吸。《Colour Diary》（2021）是这些日记的第一本集子；从北京到东京，画的仍然是那些人来之前、人走之后的地方。
**Draft (en):** Since 2020 I have painted one watercolor a day and called it "diary." Mostly ordinary things: red walls and alleys, pools and green ponds, the light inside a room, the sun on a familiar street at one particular hour. I use watercolor because what it keeps is what memory keeps — soft edges, colors that breathe. *Colour Diary* (2021) was the first collection of these; from Beijing to Tokyo, I am still painting the places from before people arrive and after they leave.

### Saffron's questions (`pp.q.*`) — one un-sees her, several speak in the wrong voice

Q5 is the best question on the page: "你还和《来自中国的浪潮》展览中的任何人保持联系吗？" names a real show and real people. (Small thing: the statement calls the same show 潮自中国 Part1 — pick one name for her own exhibition.)

Q6 is the most damaging line on Peppercorn:

> 在日本已经有第二次展览在谈或计划中了吗？ / 系统假设还需要2到3次群展，但也许已经有一次在进行中了。

She has eight group shows and a Tokyo solo. Asking about a *second* Japan exhibition tells her the system has not been paying attention — and the "why" says so out loud ("系统假设还需要2到3次群展"). This one line undoes the synopsis on Saffron's page.

**Rewrite (zh):** 接下来有在谈或在计划中的展览吗——个展、联展都算？ / 如果已经有一场在路上，山楂会把它算进去，而不是把你已经在做的事再推荐一遍。
**Rewrite (en):** Is there a next show already in conversation or planned — solo or group? / If one is already on its way, Saffron will count it rather than recommend what you're already doing.

The "why" lines generally are written in Saffron's analyst register, not Peppercorn's: "最可控的变量", "彻底改变地域扩张策略的方向", "揭示了哪些形式和价格段有转化". Peppercorn is shy; he would explain why he's asking in his own quiet way. Three examples:

- Q0 why → **zh:** 知道你的节奏，麻薯就不会拿一个你根本不想要的发帖计划来烦你。 **en:** If I know your rhythm, Mochi won't bother you with a posting plan you never asked for.
- Q1 why → **zh:** 你的观众在哪里，决定了山楂往哪个方向看。 **en:** Where your audience is decides which way Saffron looks.
- Q2 why → **zh:** 知道什么卖得动，山楂才知道哪些博览会值得你花一张桌子的钱。 **en:** Knowing what sells tells Saffron which fairs are worth the price of a table.

### Seed goals (`peppercorn_profile.json goals`)

> 在门槛较低的东京场地积累最初的展览经历

A goal card telling her to build her *first* exhibition history, years after she did. Same failure as Q6. Either seed goals that match her stage or leave the list empty — the empty copy ("胡椒粒还不知道你的目标。你在为什么努力？") is better than a stale goal.

**Replacement seeds (zh):** 找到一家愿意长期代理我的东京画廊 / 在《Colour Diary》之后出第二本书
**(en):** Find a Tokyo gallery that wants to represent me long-term / A second book after *Colour Diary*

### Empty states (`pp.sub.sublog.empty`, `pp.sub.exlog.empty`, `pp.sub.venuelog.empty`)

> 暂无提交记录 / 暂无展览记录 / 暂无场地记录

These are "No data found" with a Chinese accent — the exact thing CLAUDE.md says not to do. On Peppercorn's page they should sound like Peppercorn.

- sublog → **zh:** 还没记过投递——第一次投出去的时候，回来告诉我。 **en:** Nothing submitted yet — when you send one out, come tell me.
- exlog → **zh:** 这里还没记新的展览——你以前的参展履历山楂那边都有，这里只记接下来的。 **en:** No new shows noted here yet — Saffron already has your record; this is for what comes next.
- venuelog → **zh:** 还没记过场地。下次去看展、和谁聊了，回来记一句就好。 **en:** No venues yet. Next time you visit a show or talk to someone, come back and jot a line.

---

## Saffron — the view from above

### The intro and the synopsis — the best writing in the app

`sf.intro.body`: "上来吧，我带你看看这片风景" — perfect; the perch, the invitation. Keep.

`CAREER_SYNOPSIS` zh (`SaffronPage.jsx:519`):

> 你是一位持续在办展的艺术家——个展与联展遍及中国、日本及海外，其中包括美术馆群展，以及一场东京个展——还有首部个人出版物，和一群稳定、持续增长的受众。根基是扎实的。接下来与其说是再添履历，不如说是往深处走：画廊关系、（如果你愿意）一次代理的洽谈，以及你的日常创作本就在滋养的那条出版之路。

Seen (specific credits), encouraged with evidence, and forward — "往深处走" is the right idea and "你的日常创作本就在滋养的那条出版之路" is the single best clause in the product. One undersell: 一场东京个展, while the status line one section down says 3 场个展. She will see both. **Change the clause to:** 其中有美术馆群展，也有东京的个展.

### The status line (`careerStatusLine`, `SaffronPage.jsx:2236`)

> 你已经建立了扎实的根基——8 场联展、3 场个展、海外的展出。接下来的方向是画廊关系与代理（如果你想要的话）。

Honest and earned. Only issue: 扎实的根基 repeats the synopsis's 根基是扎实的 — two adjacent sections say the same sentence. Let this one move forward instead.

**Rewrite (zh):** 8 场联展、3 场个展、海外的展出——这早就不是起点了。接下来是画廊关系与代理，如果你想要的话。
**Rewrite (en):** Eight group shows, three solos, a showing abroad — this stopped being a beginning a while ago. What's next is gallery relationships and representation, if you want it.

### Section titles that still sound like an assessment

- `sf.cr.title` 职业准备度 / "Career Readiness" — 准备度 is an HR readiness score. The intro already gave the metaphor: doors. **Rewrite:** 接下来的门 / *The next doors*. Subtitle 当前进展与下一步方向 → 你走到了哪里，下一步通向哪里 / *Where you are, and where the next step leads.*
- `sf.depmap.title` 职业解锁树 / "Career Unlock Tree" — the videogame framing the readiness section explicitly removed survives here. **Rewrite:** 哪扇门通向哪扇门 / *How the doors connect.*

### The hint under the next step (`NEXT_STEP_HINT`)

> 没有截止日期，也不催你——想做的时候再做。

A lovely line — sitting directly beneath an action that says "在2026年9月24日截止前申请" and "现在就去查 HB Gallery FILE 大赛的征集截止时间". The hint contradicts the sentence above it and cancels the one moment of urgency the page has.

**Rewrite (zh):** 不急。有截止日期的地方山楂写清楚了；其余的，想做的时候再做。
**Rewrite (en):** No rush. Where there's a real date, Saffron has written it down; everything else is whenever you feel like it.

### The seven levers (`career_strategy_engine.py _next_tier_levers`, lines 485–901)

The test case the review was asked about. Verdict: **the targets made it alive; the details made it a checklist — and the fix is subtraction, not rewriting.** Each lever has three places to put a fact (detail, action, targets) and tonight every fact went in all three. She reads "grid next…通常每年12月开放" three times inside one card. Let the detail carry the story and one sentence per door with no dates; let the targets carry the specifics; let the action be *one thing she can do this week*.

**1. Gallery representation.** Headline 画廊代理，是下一个关键的结构性跃升 — 结构性跃升 is consultant vocabulary in the first line she reads. The detail's Tokyo-etiquette sentence (没有作品投递箱…先以观众身份看展、认识画廊主、再被引荐) is genuinely useful and seen. The Kaikai Kiki target ("证明像你这样的关注度本身也能成为一扇门") is the most encouraging line in the seven. The action is three tasks in one sentence.

- Headline → **zh:** 下一扇门：一家愿意长期代理你的画廊 **en:** The next door: a gallery that takes you on
- Detail → **zh:** 你已经有个展和美术馆联展的履历——接下来最能改变格局的，是一家替你销售、带你去博览会、慢慢替你积累藏家的画廊。东京的画廊很少设投稿入口，通常的路是先去看展、认识画廊主、被人引荐。下面几扇门是山楂找到的、离你的作品最近的：一家可以直接写信的画廊，两个曾把获奖者直接送进个展的公开征集。
- Action → **zh:** 这周做一件事就够：给 Gallery Kogure 写一封短信（works@gallerykogure.com），附三张日记系列。 **en:** One thing this week is enough: a short note to Gallery Kogure (works@gallerykogure.com) with three diary paintings attached.

**2. Solo venue quality.** The only line in all seven that stings before it opens a door:

> 你至今的个展都在付费租赁场地举办——下一步是找到一个反过来为展览付费的场地。

True, and worth saying. But it leads with the deflation. Three solos she made happen herself deserve the first clause; the rental point can be the second. The "2026年入选者中有两位是中国艺术家" detail is a real *seen* moment — keep it.

- **zh:** 三场个展，每一场都是你自己做出来的。下一步，是让场地反过来为展览付钱——东京都现代美术空间的两个项目正为此而设……
- **en:** Three solos, each one you made happen yourself. The next step is a venue that pays for the show instead of the other way round — Tokyo Arts and Space runs two programs built for exactly this…

**3. Art fairs.** Opens on the closed door (Art Fair Tokyo 与 Tokyo Gendai 都只接受画廊申请) before the open ones. Reverse it, and turn the closed door into a future.

- **zh (ending):** ……至于 Art Fair Tokyo 和 Tokyo Gendai，那是画廊替你申请的——等代理之后，自然会到。
- **en (ending):** …As for Art Fair Tokyo and Tokyo Gendai, those are the ones a gallery applies to on your behalf — after representation, they come on their own.

SICF's target line "同时达成博览会与个展两个目标" is exactly the kind of sentence that creates momentum. Keep.

**4. Residency.** The most alive lever, written in the flattest verb. The detail says 尚未拥有的少数credit之一 — English "credit" untranslated inside a Chinese sentence, and 尚未拥有 is deficit framing (the docstring says never). The call opens in roughly ten days and the action says 留意 (keep an eye on).

- Detail opening → **zh:** 驻地是少数你还没试过的事——而最适合你的几个，就在日本。 **en:** A residency is one of the few things you haven't tried yet — and the best-fitting ones are right here in Japan.
- Action → **zh:** TOKAS 的驻地征集大概就在这两周开放——这是今年秋天最值得盯住的一扇门。先把作品集和三句话的驻地计划准备好，开放当天就能投。 **en:** TOKAS's residency call should open within the next couple of weeks — the door most worth watching this autumn. Have your portfolio and a three-sentence residency idea ready, so you can apply the day it opens.

The Fukuoka target ("你往返东京与北京的创作实践，正是它面向的对象") is the best target line of the night. Keep.

**5. Grants.** Six grants with dates in one paragraph — the checklist feeling is strongest here. Yet it holds two of the most *seen* lines in the app: "凭中国国籍即可申请其中国大陆项目，无论是否居住在东京" and Greenshields "明确接受学生申请" (she is a student; the system knows). The paragraph buries them. Also アーツカウンシル东京创业期扶持金 mixes katakana into a Chinese sentence and 创业期 (startup) sounds like a business loan.

- Detail → **zh:** 你的履历现在已经撑得起申请奖助了。两扇门此刻开着：东京艺术委员会（Arts Council Tokyo）的新人扶持金，最高30万日元、不限国籍，9月24日截止；加拿大的 Elizabeth Greenshields 基金会专门资助你这个阶段的具象绘画者，学生也可以，随时可投。10月还有三扇会开——野村财团、朝日新闻文化财团，以及亚洲文化协会：凭你的中国国籍就能走它的中国大陆通道，住在东京也没关系。
- **en:** Your record can carry a grant application now. Two doors are open this minute: Arts Council Tokyo's startup grant (up to ¥300,000, no nationality clause) closes September 24; Canada's Elizabeth Greenshields Foundation funds representational painters at exactly your stage, students included, any time. Three more open in October — Nomura, Asahi Shimbun, and the Asian Cultural Council, whose Mainland China track you qualify for by citizenship, Tokyo address and all.

**6. Critical press.** Headline 从作品被展示，迈向作品被书写 is the best of the seven — keep. Colossal's "一份持续数年的东京水彩日记，正是它偏爱的故事类型" is seen and exciting. One target un-sees her: Tokyo Weekender "来自海外的画家在东京的首次个展" — she has had her first Tokyo solo; "first" is past.

- **zh:** 常报道旅日画家在东京的展览——下一场个展开幕前3-4周投稿正合适。
- **en:** Regularly covers painters from abroad showing in Tokyo — pitch three or four weeks before your next solo opens.

**7. Monograph.** "五年过去，作品已积累许多" is warm and evidenced. If the diary count is known, saying it would be thrilling — five years of daily paintings is a very large number. Optional: 五年的日记，早已够一本厚书。

**Across all seven:** four actions begin with 留意 / watch. Even when a call is closed, the action can be a thing she does this week — 把驻地计划写成三句话, 挑出十张给画廊看的图, 把 Colour Diary 之后的画按季节排一遍. Watching is a state; the page should hand her a verb.

### Long-term scenarios (`api.py:2754–2808`)

The names — Gallery Track / Publication Track / Hybrid Track — are athletic-corporate. The Chinese labels 瓶颈 ("bottleneck") and 适合条件 ("fit conditions") read like eligibility criteria on what the code calls "her three possible lives". The Hybrid line "The daily diary is simultaneously publication material and gallery-worthy work" is the one that sees her; the Publication bottleneck's "it just needs packaging" is reductive for an artist's book.

- Names → **zh:** 画廊这条路 / 书这条路 / 两条一起走 **en:** The gallery road / The book road / Both at once
- `sf.label.bottleneck` 瓶颈： → 难处在于： / *The hard part:*
- `sf.label.rightIf` 适合条件： → 适合你，如果： / *Yours if:*
- Publication bottleneck → **en:** The next book is the open lever — the daily diary is already there; it needs a sequence, not more paintings. **zh:** 下一本书是现成的杠杆——日记已经画在那里了，缺的是一个顺序，而不是更多的画。
- `saffron_view` "These are directions, not a verdict" is an "it's not A, it's B" construction. **zh:** 这是三个方向，选哪个由你。想两条都要，那就让它们互相喂养——书店里的画廊展，一步就能同时推进两边。 **en:** Three directions, and the choice is yours. If you want both, let them feed each other — a bookshop-gallery show moves both at once.

(One line, no more: Gallery and Hybrid copy exist in English only in the source; worth a glance that they arrive in Chinese on her screen.)

### Empty states (`sf.empty.calendar`, `sf.empty.venues`)

> 目前没有已确认的截止日期。大多数机会的截止日期标注为"未知"或"滚动" — 随着核实工作推进，日历会逐步填充。
> 暂无已追踪的场地。此栏将在场地加入CRM后自动填充。

System-status language — "verification work", "CRM", "will populate". Saffron describes; she doesn't report pipeline health.

- Calendar → **zh:** 这个月没有定了日子的截止。多数机会常年开放——一旦有了确定的日期，山楂会放到这里。 **en:** No fixed dates this month. Most of these stay open year-round — when one gets a real date, Saffron will put it here.
- Venues → **zh:** 还没有在联系中的场地。你在胡椒粒那里记下的第一家，会出现在这里。 **en:** No venues in conversation yet. The first one you note with Peppercorn will show up here.

### What's already right on Saffron

`sf.sec.peers` 你身处优秀的同道之中; `sf.label.peersCaveat` ("是同道，而非高下的比较" — a rare negative construction that earns its place); `sf.cr.hedge` ("往往只是我没能找到"); `sf.sub.oppGap` "一些你的作品也许会喜欢的新方向——纯属可选"; `pp.ig.analysis` "按自己的节奏来就好". These are the voice. Everything above should be measured against them.

---

## Fix these first

1. **Today's Focus `why_card` copy** — the three most-read sentences in the app have zero her-specific content, leak "Tier-1", and end on negatives. Adopt the rule: one clause per card that could only be about her. (`api.py get_today` / the generator that writes `why_card_zh`.)
2. **Peppercorn Q6 and the seed goals** — "second Japan exhibition" and "build first exhibition history" tell her the system hasn't noticed her record. Two strings and two JSON entries; the highest emotional payoff per character in this review. (`translations.js pp.q.6.*`, `peppercorn_profile.json goals`.)
3. **Residency and grant lever actions** — turn 留意 into a this-week verb and let the near dates sound near (TOKAS mid-September, Arts Council Sept 24). This is where "excited" lives and it is currently written flat. (`career_strategy_engine.py` 691–692, 749–750.)
4. **Two lines that sting or undersell** — the solo-venue opener (honor the three solos before the rental point) and the residency's 尚未拥有的credit. Plus the synopsis's 一场东京个展 against the status line's 3 场个展. (`career_strategy_engine.py` 561/570, 674/683; `SaffronPage.jsx:519`.)
5. **Empty states on Peppercorn and Saffron** — 暂无…记录, "CRM", 核实工作推进. Five strings, all currently "No data found" in disguise, on the two pages whose companions are defined by warmth. (`translations.js` zh 437–438, 784, 805, 860.)

If there is a sixth: de-triplicate the levers (facts in the targets only, story in the detail, one verb in the action). Not a rewrite — a deletion pass — and it is what turns the checklist back into doors.
