# Saffron Chinese audit — all 52 venue rows

Reviewed on the live 概况 → 场地关系追踪 panel on 2026-09-10. This appendix covers every displayed row, including duplicate venues. Source owners are `api.py` → `venue_tracker`, the contact source data/deriving engine and translation layer; the React renderer is `SaffronPage.jsx` → `VenueTrackerRow`.

The recommended product change is to keep this research catalogue secondary. Do not ship a list of 52 revised instructions asking her to do the work. The replacement sentences below describe the research question clearly and avoid directing premature visits, unsolicited physical deliveries or guesses at editorial contacts. For a prominent recommendation, **the system should answer that question first** and display the result, official link and checked date.

## Section and status copy

| Current | Replacement | Required behavior |
|---|---|---|
| 场地关系追踪 | 空间与联系记录 | Distinguish researched targets from actual relationships. |
| 已追踪52个场地 | 已收录 52 个条目 | Count is records, including duplicates/platforms, not 52 real relationships or unique venues. Dedup before later saying 家空间. |
| 你正在联系的场地、当前状态，以及建议的后续行动。 | 已收录的空间、联系记录与待确认事项。 | Unknown/no recorded contact is not a conversation. |
| 冷淡 | 尚无联系记录 | “Cold” is CRM state, not their attitude toward her. |
| 尚未联系 | 尚无联系记录 | Unless she explicitly recorded no contact; missing log cannot prove she never contacted them. |
| 调研中 | 资料待补充 | More useful than pipeline state; keep 了解中 for a state she personally selected. |
| 待审阅 | 联系方式待确认 | Only where this matches actual unresolved condition. A real review-ready item may instead use 待查看. |
| 可以联系了 | 已备好联系资料 | Does not imply invitation or verified acceptance. |
| 优先级 高／中／低 | 推荐理由 (plain text below name) | She needs why now, not internal ranking. If priority retained, call it 近期可了解／以后可了解 only with evidence. |
| 已回复 | 收到回复 | Clarifies who replied. |
| 一句备注（可选） | 备注（可选） | Keep input optional; preserve authored notes verbatim. |

**Technical cause of a second localization problem:** `saffronTx` translates all values, including enum strings, then `venueStatusLabel()` attempts to look them up as English internal IDs. An already translated value falls through to raw display. Keep status/priority enums and entity IDs stable; localize their labels only. Never write translated enum values back on Save. Saving was not tested on her real records in this review.

## Imported English notes

The panel displays internal notes such as “Reclassified from cold,” “Type corrected from zine_shop to opportunity_platform,” “contact/fees/process confirmed via verification pass,” and “26k Twitter following.” These should not be passed off as her private notes. Identify imported research separately, translate substantive verified information at its source, and keep migration/verification commentary out of the artist-facing record.

Specific note fixes:

- B&B's “Books + beer + events … Check event/consignment inquiry process” → **书店、酒吧与活动空间；寄售和活动提案渠道仍需确认。**
- TABF's “Table/booth target for 2026” → replace with the dated current-cycle state; do not preserve stale future tense.
- UTRECHT's “Top-tier … consignment target” → **艺术书与独立出版物相关空间；需确认当前寄售要求。** Remove ranking and assumed acceptance.
- ZINE Fest's June 27 deadline → expired historical cycle; never urgent next action.
- flotsam / HATTIFNATT's “strong fit” → describe actual stock/exhibitions with an example before claiming fit.
- MOUNT ZINE's “Tokyo's leading … strong pitch angle” → a sourced stock/category description, without superlatives.
- SUZURI's “Passive income from 26k Twitter following” → delete. Wrong platform/count and passive-income claim. Platform setup is not a relationship record.
- KAYOKOYUKI's manual verification note → show official website plus **是否接受主动投稿：尚待确认**; no internal workflow labels.
- Media “Reclassified from cold” notes → remove migration history. Surface one checked editorial route, not research instructions.
- ART BOX's “For when Colour Diary 2 is ready” → **后续画集的潜在出版研究对象。** Do not invent a sequel title or plan.
- Books Ruhe / tata / Gallery 456's “contact confirmed” → attach actual route and verification date; never preserve undated verification language.
- Book and Sons / COW BOOKS / reload / Tacoche / Yonchome notes → fold substantive description into sourced venue summary; do not invent walk-in permission or exhibition availability.
- Empty notes remain empty. Do not manufacture a note to fill every card.

## Row-by-row action wording

The “current” column is the exact displayed next-action sentence in the snapshot. The final column is a clear research brief / safe interim state, **not a completed recommendation**. Rows marked **merge** should be resolved by stable venue identity without overwriting distinct contact history.

| # / Venue | Current next-action sentence | Proposed wording / treatment |
|---|---|---|
| 1 B&B 下北泽 | 完成对 B&B Shimokitazawa 的调研：查看其官网，了解近期展览、公开征集公告及具名联系人。 | 确认 B&B 当前是否接受出版物寄售，以及所需材料和联系渠道。 |
| 2 东京艺术书展 | 完成对 Tokyo Art Book Fair 的调研：查看其官网，了解近期展览、公开征集公告及具名联系人。 | 当前一届的申请已截止；下一轮公告发布后，再核对作品要求、费用和展期。 Keep current-cycle facts consistent with calendar. |
| 3 UTRECHT | 完成对 UTRECHT 的调研：查看其官网，了解近期展览、公开征集公告及具名联系人。 | 确认 UTRECHT 的出版物寄售方式、材料要求与当前联系渠道。 |
| 4 ZINEフェス東京 | 了解 ZINEフェス東京 的报名流程和摊位费用。截止日期为 2026 年 6 月 27 日——请立即行动。 | 已记录的 2026 年 6 月 27 日截止日期已过；下一轮时间与报名方式尚待确认。 Remove urgency automatically at source. |
| 5 flotsam books | 亲自前往 flotsam books（或浏览其线上库存），确认风格契合度，然后起草一封简短的寄售咨询邮件。 | 比较近期在售出版物，并确认是否接受寄售及其材料要求。 |
| 6 HATTIFNATT Koenji | 前往 HATTIFNATT Koenji 实地察看展示空间，并与负责人洽谈近期展览档期。 | 先确认高圆寺店当前的展览安排、申请方式和费用，再决定是否到访。 Merge with 28 after identity check. |
| 7 MOUNT ZINE | 请将作品实体样本邮寄或亲自送至 MOUNT ZINE——zine 文化重视实物，而非电子邮件投稿。 | 按 MOUNT ZINE 当前的寄售说明确认材料和提交方式；需要样书时，再安排寄送。 Never direct uninvited packages. |
| 8 SUZURI | 注册 SUZURI 账号，从现有水彩作品中上传 3–5 个设计。预计完成时间：2–3 小时。 | 比较一种产品的制作费用、样品和配送方式，再决定是否使用该平台。 Move to product research; no assumption she lacks account. |
| 9 KAYOKOYUKI | 查看 KAYOKOYUKI 网站上的当前及近期展览，评估其与你的作品风格（静谧的日常写实／近插画感绘画）是否契合。通过 FAQ、艺术家申请页面或直接联系，确认他们是否接受主动投稿。若契合度确认且接受投稿，将状态更新为"ready_to_contact"并起草个性化提案。 | 是否接受主动投稿尚待确认。可先比较近期展览与现有作品，再按官方公开渠道准备联系资料。 Remove internal enum and false official applicant-page assumption. |
| 10 Apartamento Magazine | 仔细研究 Apartamento 的艺术家专题报道格式，围绕以下具体角度撰写一份投稿提案：一位中国艺术家静静观察东京正在消逝的家居空间。 | 比较其关于居住与创作的具体专题，确认实际联系渠道；选题应依据你的真实作品与经历。 Do not invent disappearance theme from biography. |
| 11 Casa Brutus | Research Casa Brutus's recent editorial focus on architecture and design, identify a named editor, and develop a pitch around your Tokyo architectural watercolor documentation. | 比较近期建筑与设计选题，确认官方接收资料的方式，再准备相关作品介绍。 No demand to guess a named editor. |
| 12 FACE Exhibition 2026 | 调研 FACE Exhibition 2026 的投稿截止日期、参赛费用、作品尺寸要求及评审标准，在投入准备时间前确认非日本国籍人士是否具备参赛资格。 | 区分 FACE 2026 历史记录与 FACE 2027 当前征集；按当届要项显示作品要求、费用和送件安排。 Do not rename historical record to current year. |
| 13 It's Nice That | 了解 It's Nice That 的"Submit Your Work"流程，研究近期东京艺术家专题以确定提案角度，然后精选 8–10 件最具代表性的作品。 | 按官方投稿页要求整理一组作品和简短说明，并附上真实的创作背景。 Exact count comes from current requirements. |
| 14 Pen Magazine | 在联系之前，研究 Pen Magazine 近期的专题格式，找到负责设计与艺术板块的编辑姓名，并确定具体的选题角度。 | 比较近期设计与艺术专题，确认官方咨询或资料接收渠道。 |
| 15 美術手帖 | 在联系之前，研究 美術手帖 近期的专题格式，找到负责新兴艺术家板块的编辑姓名，并确定具体的选题角度。 | 比较与作品相关的专题，并确认媒体公开的联系渠道及所需材料。 |
| 16 Antenna Books | 亲自前往 Antenna Books 考察空间及风格契合度，然后起草一封简短的寄售询问邮件。 | 核对店铺身份、所在地与当前寄售渠道，再比较在售出版物。 Venue identity/location in source needs verification. |
| 17 B&B（Book & Beer） | 亲自前往 B&B (Book & Beer) 考察空间及风格契合度，然后起草一封简短的寄售询问邮件。 | Merge with 1; preserve any separate real interaction records. Use the same verified consignment question. |
| 18 BALLOND'ESSAI Shimokitazawa | 亲自前往东京 BALLOND'ESSAI Shimokitazawa——Shimokitazawa 参观展示空间，并与负责人洽谈近期展览档期。 | 确认当前是否提供艺术展示空间，以及申请方式、展期和费用。 |
| 19 Book and Sons | 亲自前往 Book and Sons（或浏览其线上库存）确认风格契合度，然后起草一封简短的寄售询问邮件。 | 比较其近期出版物，并确认是否接受寄售或出版提案。 |
| 20 Book Culture Club | 在联络前，先了解 Book Culture Club 的版式偏好和投稿要求。 | 先确认当前业务、店铺身份和合作方式，再整理相应材料。 A shop need not have editorial format preferences. |
| 21 CLOUDS Gallery+Coffee 高円寺 | 前往东京高圆寺的 CLOUDS Gallery+Coffee Koenji 实地察看展示空间，并与负责人洽谈近期展览档期。 | 确认当前展览安排、申请渠道及场地和销售费用。 |
| 22 COW BOOKS 中目黑 | 亲自前往 COW BOOKS Nakameguro（或浏览其线上库存）确认风格契合度，然后起草一封简短的寄售询问邮件。 | 比较在售出版物，并确认是否接受作者的寄售询问。 |
| 23 CuratorSpace 公开征集 | 注册 CuratorSpace 账号，并设置标签提醒，关键词包括：watercolor、works on paper、zine、Tokyo、Japan。 | 作为机会检索来源使用；具体项目需回到主办方核对资格、费用和截止日期。 Move out of venue-relationship count. |
| 24 Design Festa Gallery | 在正式接洽之前，先参加 Design Festa Gallery 的开幕式或活动，观察其策展风格与受众群体。 | 查看空间申请方式、使用费用和展示规则，再比较是否适合这组作品。 A rental model should not require networking ritual. |
| 25 Gallery EF 浅草 | 前往东京台东区浅草的 Gallery EF Asakusa 实地察看展示空间，并与负责人洽谈近期展览档期。 | 先核对当前所在地、营业状态与展览安排。 Do not send her to potentially stale location. |
| 26 Gallery Rocket 原宿 | 前往东京涩谷区原宿的 Gallery Rocket Harajuku 实地察看展示空间，并与负责人洽谈近期展览档期。 | 先核对空间是否仍在运营及当前所在地，再确认合作方式。 |
| 27 HATTIFNATT 吉祥寺店 | 前往东京武藏野市吉祥寺的 HATTIFNATT Kichijoji 实地察看展示空间，并与负责人洽谈近期展览档期。 | 单独确认吉祥寺店是否接受展览提案；不要沿用其他分店的条件。 |
| 28 HATTIFNATT 高円寺咖啡画廊 | 前往东京高圆寺的 HATTIFNATT Koenji Cafe Gallery 实地察看展示空间，并与负责人洽谈近期展览档期。 | Merge with 6 after identity check; one source of terms and one contact history. |
| 29 Kamome Roastery Tokyo | 前往东京葛饰区龟有的 Kamome Roastery Tokyo 实地察看展示空间，并与负责人洽谈近期展览档期。 | 确认当前展示项目、申请时间和空间条件，再判断是否到访。 |
| 30 LOCAL Gallery・Books | 在联络前，先了解 LOCAL Gallery・Books 的版式偏好和投稿要求。 | 确认当前业务与合作渠道，再区分是寄售、展览还是出版提案。 |
| 31 Mograg Gallery | 前往东京涩谷区幡谷的 Mograg Gallery 实地察看展示空间，并与负责人洽谈近期展览档期。 | 先核对当前地址、展览方向与作品提案渠道。 Specific address in old data needs official verification. |
| 32 Mona Records | 在联系之前，先了解 Mona Records 的格式偏好和投稿规范。 | 确认这个对象与艺术出版或作品展示的具体关联；如无明确用途，不列为近期联系对象。 |
| 33 Nui. Hostel Bar & Lounge 浅草 | 亲自前往东京浅草台东区的 Nui. Hostel Bar & Lounge Asakusa，了解展示空间并与负责人沟通近期的展览档期。 | 确认是否接受艺术展示，以及展示区域、费用和联系渠道。 |
| 34 POST | 亲自前往 POST，评估空间与风格的契合度，然后起草一封简短的寄售咨询邮件。 | 比较近期出版物，确认作者寄售是否属于其当前业务。 |
| 35 Route Books | 亲自前往 Route Books，评估空间与风格的契合度，然后起草一封简短的寄售咨询邮件。 | 分别核对出版物寄售与空间展示的条件，避免把两种合作混在一起。 |
| 36 SHIBUYA CAST. Gallery | 亲自前往东京涩谷的 SHIBUYA CAST. Gallery，了解展示空间并与负责人沟通近期的展览档期。 | 核对实际空间名称、管理方和项目申请方式，再评估费用与准备量。 |
| 37 SPBS（涩谷出版书店） | 亲自前往 SPBS (Shibuya Publishing Booksellers)，评估空间与风格的契合度，然后起草一封简短的寄售咨询邮件。 | 分别查看图书寄售、活动和出版业务的联系渠道。 |
| 38 Submissions - Little Press Publishing | 研究 Little Press Publishing 的投稿规范和当前征稿信息，然后准备一份有针对性的提案并附上样稿。 | 先确认出版社身份、所在地与当前征稿范围，再判断作品是否相符。 “Submissions” is a scraped page title, not entity name. |
| 39 Village Vanguard 下北泽店 | 亲自前往 Village Vanguard Shimokitazawa，评估空间与风格的契合度，然后起草一封简短的寄售咨询邮件。 | 核对该分店是否接收作者出版物，以及采购或寄售的联系方式。 |
| 40 円盤（Enban）高円寺 | 在联系之前，先了解 円盤 (Enban) Koenji 的格式偏好和投稿规范。 | 先核对当前经营状态、地址和出版物合作方式。 |
| 41 本店・本屋の実験室 | 在联系之前，先了解 本店・本屋の実験室 的格式偏好和投稿规范。 | 确认当前项目、寄售或活动合作方式，以及所需材料。 |
| 42 ART BOX Publishing | 在开始联络前，先调研 ART BOX Publishing 当前的项目计划、投稿政策及关键联系人。 | 核对出版社身份、当前书目、费用承担和提案渠道。 |
| 43 Books Ruhe | 亲自前往 Books Ruhe（或浏览其线上库存）确认风格契合度，然后起草一封简短的寄售询问邮件。 | 核对店铺的正式名称与业务，再确认是否接受作者寄售。 |
| 44 ERA 下北沢 | 在正式接洽之前，先参加位于东京下北泽的 ERA Shimokitazawa 的开幕式或活动，观察其策展风格。 | 确认该空间实际提供的艺术展示或出版合作；相关性不足时不列入近期名单。 |
| 45 Gallery 456 | 投稿前请核实当前征集状态并确认费用——这是未来目标，暂不紧迫。 | 可作为长期研究对象，按当届公告核对征集状态、费用与运输要求。 |
| 46 高円寺 SANAGI | 前往东京高圆寺的 Koenji SANAGI 实地察看展示空间，并与负责人洽谈近期展览档期。 | 确认当前展览项目、提案渠道与费用，再决定是否到访。 |
| 47 Komiyama Tokyo | 调研 Komiyama Tokyo 的投稿要求和当前征稿信息，然后准备一份附有样页的针对性提案。 | 区分其书店、展览与出版业务，先确认适用的合作渠道。 |
| 48 reload 下北泽 | 在正式接洽之前，先参加 reload Shimokitazawa 的开幕式或活动，观察其策展风格与受众群体。 | 确认具体空间或项目的管理方，再核对活动申请方式。 Multi-use complex is not one curator. |
| 49 投稿 — porkbelly press | 研究 porkbelly press 的投稿规范和当前征稿信息，然后准备一份有针对性的提案并附上样稿。 | 核对出版社所在地与当前征稿类别，再判断是否适合现有作品。 Remove scrape-prefix and unverified Japan/Tokyo location. |
| 50 Tacoche | 请将作品实体样本邮寄或亲自送至 Tacoche——zine 文化重视实物，而非电子邮件投稿。 | 按当前寄售说明确认是否需要样书，再安排材料或寄送。 |
| 51 tata bookshop/gallery | 亲自前往 tata bookshop/gallery（或浏览其线上库存），确认风格契合度，然后起草一封简短的寄售咨询邮件。 | 比较近期出版物与展览，分别确认寄售和展示的合作条件。 |
| 52 Yonchome Cafe | 前往 Yonchome Cafe，了解展示空间并与负责人沟通近期的展览档期。 | 核对当前是否开放展示提案，以及展期、费用和作品要求。 |

## Production rules that preserve these corrections

1. Imported generic next-actions must not override specific, newer verified information. A freshly verified FACE 2027 brief should not coexist with a top-ranked instruction to research FACE 2026 eligibility.
2. Derive expiration at read time using a date type. Keep old events as history, not invitations to act.
3. Link known official URLs directly. Every venue currently falling back to Google means the page gives her the research job back. Use search only when identity or route is unresolved and label it honestly.
4. Preserve user-entered contact notes and dates. Clean imported research and derived suggestions through source/engine rules; do not mass rewrite her app-state records.
5. Keep observed interactions separate from discovered names. “尚无联系记录” must never become “她没有联系过”.
