// Structured insight content for Saffron's five new sections.
// Translations (_zh, _ja) are baked in — do not edit manually, run scripts/translate_saffron_insights.py

export const LICENSING_LANDSCAPE = {
  // REWRITTEN 2026-09-08. This block audited worst of any in the file: ~24% of
  // its claims were checkable and true, ~12% were wrong, and ~38% were
  // unfalsifiable — 114 lines carrying zero URLs and zero dates.
  //
  // What was wrong: Stalogy was attributed to Nakabayashi (it is Nitoms, a Nitto
  // Group company, art-directed by good design company) and named as a "natural
  // partner" despite having no illustration line and no external design route —
  // entry removed. Osaji was named as a brand that collabs with illustrators; it
  // does not (its collaborators are makeup artists, chefs, musicians) — HACCI
  // does, and now stands alone. Mark's carried an invented eligibility rule
  // ("open to submissions from Japanese-resident artists") for a company that
  // publishes no submissions route at all. Hobonichi's tag was #ほぼ日; the live
  // one is #ほぼ日手帳.
  //
  // And Midori said "send a lookbook directly to the creative director (not
  // info@)" — naming no director, at a company that publishes no individual
  // address. That is the fabricated-Bijutsu-Techo failure repeated: an
  // instruction to act, pointed at a contact that does not exist.
  //
  // Every yen figure that was unsourced has been removed or marked. The royalty
  // band is kept because it is real, with the thing that actually matters
  // attached: it is US/UK practice, and Japanese stationery deals are commonly
  // flat-fee 買い取り instead.
  //
  // _ja omitted — LANGUAGES is ['zh','en'].
  "titleKey": "sf.licensing.title",
  "summaryKey": "sf.licensing.summary",
  "where_to_start": "Two things cost nothing and can be done today: put \"licensing available\" and a contact link in your bio, and put 10–20 works into one PDF shown as product mock-ups. Neither is a guarantee of anything — nobody publishes how these deals actually originate — but they are what a brand needs to find and picture before a conversation can start at all.",
  "where_to_start_zh": "有两件事不花钱、今天就能做：在简介里写上“接受授权合作”并放一个联系方式链接；把 10–20 件作品做成产品效果图，整理成一个 PDF。这两件事都不保证什么——没有人公开过这类合作到底是怎么开始的——但它们是品牌方能找到你、并想象得出成品的前提。",
  "lead": "Your watercolor and stationery-leaning work suits calendars, postcards and greeting cards, washi tape and stickers, and notebook and planner covers. Two Japanese brands verifiably license illustrators for exactly this: Hobonichi, through its standing Artist Collection line, and Mark's, through EDiT.",
  "lead_zh": "你的水彩，尤其偏文具感的那一部分，适合日历、明信片和贺卡、和纸胶带和贴纸，还有笔记本和手账封面。有两个日本品牌确实在为这类东西签约插画师：ほぼ日（通过常设的「アーティストコレクション」系列）和 Mark's（通过 EDiT）。",
  "items": [
    {
      "category": "Japanese Stationery Brands",
      "category_zh": "日本文具品牌",
      "entries": [
        {
          "name": "Hobonichi",
          "name_zh": "ほぼ日",
          "note": "Verified: they run a standing Artist Collection line for Techo covers, and the 2027 edition includes named illustrators. Not verified, and worth knowing before you spend time on it: they publish no submission or discovery route at all — their only public address is order support. The one real entry route was an open call that closed in 2010. If you tag, the live tag is #ほぼ日手帳.",
          "note_zh": "已核实：他们有常设的「アーティストコレクション」手账封面系列，2027 年版上写了插画师的名字。有一件事没能核实，但在花时间之前值得知道：他们完全没有公开任何投稿或选人的入口——唯一的公开邮箱是订单客服。真正存在过的入口是一次公开征集，2010 年就结束了。如果要打标签，现在在用的是 #ほぼ日手帳。",
          "tier": "medium_term"
        },
        {
          "name": "Midori (Designphil)",
          "name_zh": "Midori（デザインフィル）",
          "note": "A real stationery publisher, but no submissions programme and no individual contact is published — only a general inquiry form and a recruitment page. An earlier version of this page told you to email their creative director instead of the general address; no such person is named anywhere, and that advice has been removed.",
          "note_zh": "确实是一家真实的文具出版商，但没有投稿计划，也没有公开任何个人联系方式——只有一个通用咨询表单和招聘页。这一页早先的版本让你“别发通用邮箱，直接发给他们的创意总监”；这个人的名字哪里都查不到，那条建议已经删掉了。",
          "tier": "medium_term"
        },
        {
          "name": "Mark's Inc.",
          "name_zh": "Mark's Inc.",
          "note": "Verified: the EDiT line licenses illustrators for planner covers — the 2026 edition ran 79 cover variants, including a collaboration with a painter. No submissions route is published, and an earlier claim here that they are \"open to submissions from Japanese-resident artists\" was invented; there is no such rule and no such door.",
          "note_zh": "已核实：EDiT 系列确实为手账封面签约插画师——2026 年版做了 79 种封面，其中包括一次与画家的联名。他们没有公开投稿入口；这一页早先写的“面向在日艺术家开放投稿”是编出来的，既没有这条规则，也没有这扇门。",
          "tier": "medium_term"
        }
      ]
    },
    {
      "category": "Publishing & Editorial",
      "category_zh": "出版与编辑",
      "entries": [
        {
          "name": "Book cover art (装画)",
          "name_zh": "书籍封面（装画）",
          "note": "Publishers commission cover art rather than license existing paintings. The Japan Illustrators' Association publishes a rate grid, and its figures are floors, not ceilings — covers run from ¥30,000 to ¥150,000 and up. Watercolour sits in its D rank, where a book cover starts at ¥70,000 and a magazine or catalogue cover at ¥100,000, so the bottom of that grid is not your row. It is dated January 2020 and says itself that prices will have moved since. There are named, dated ways in, which is what this entry used to be missing: ザ・チョイス, the quarterly competition run by illustration magazine, judged by a single rotating judge; and 装画コンペ at GALLERY HOUSE MAYA, judged by working book designers, open to all nationalities (資格：不問), grand prize a solo show — check its current status first, it was on hiatus in 2024.",
          "note_zh": "出版社是来“约”封面画的，不会买断你已经画好的画。日本插画家协会公开过一张报价表，上面写的是起价，不是上限——封面从 3 万日元到 15 万日元以上都有。水彩属于表上的 D 级：书籍封面 7 万日元起，杂志或画册封面 10 万日元起，所以最低那一档不是你这一类。表标的日期是 2020 年 1 月，它自己也写了价格以后会变。而这里确实有指名道姓、写明时间的入口——这正是这一条以前缺的：《ザ・チョイス》（The Choice），illustration 杂志办的季度赛，每期由一位评委轮流评选；以及 GALLERY HOUSE MAYA 的「装画コンペ」（书籍封面画比赛），由在职的装帧设计师评审，不限国籍（原文写的是「資格：不問」），大奖是一个个展——先确认它现在的状态，2024 年曾经停办过一届。",
          "tier": "medium_term"
        },
        {
          "name": "Agency representation",
          "name_zh": "经纪代理",
          "note": "CWC Tokyo has represented overseas illustrators into the Japanese market since 1991, and its contact form carries an illustrator category. Structurally this is the closest fit on the page to where you actually stand — a non-Japanese illustrator working in Japan — and it is the one route here with a published door.",
          "note_zh": "CWC Tokyo 从 1991 年起就在把海外插画师引进日本市场，他们的联系表单里有“插画师应征”这一类。这是这一页上最贴近你真实处境的一条——一个在日本工作的非日籍插画师——也是这里唯一一条有公开入口的路。",
          "tier": "medium_term"
        },
        {
          "name": "Lifestyle brands",
          "name_zh": "生活方式品牌",
          "note": "HACCI has done limited collaboration packaging with an illustrator, plus seasonal artist packaging — so this does happen. Neither it nor comparable brands publishes a submissions address, and no reliable fee range exists for this kind of campaign work, so any number here would be invented.",
          "note_zh": "HACCI 做过与插画师合作的限定包装，也做过季节性的艺术家包装——所以这类事确实会发生。但它和同类品牌都没有公开投稿邮箱，这类企划的报价也没有可靠的公开区间，所以这里写任何数字都会是编的。",
          "tier": "medium_term"
        }
      ]
    },
    {
      "category": "What the money actually looks like",
      "category_zh": "这笔钱实际长什么样",
      "entries": [
        {
          "name": "Royalty or buyout",
          "name_zh": "分成，还是买断",
          "note": "Published guidance puts art-licensing royalties at roughly 3–10%, with greeting cards and stationery at the low end — one widely cited US source gives 2–5% — and it is usually figured on NET sales, after returns, discounts and freight, not on the sticker price. Japan prices it differently again, and the difference is worth knowing before a first conversation: reusing an existing illustration is a 二次使用料, a percentage of the original fee, which the illustrators' association sets at 70% for a second use and the market runs at 20–80%. A full buyout (買い取り / 著作権譲渡) is not a fraction of your fee but a MULTIPLE of it — the same association puts it at two to three times. Running royalties do exist for merchandise, at roughly 4–6% of the retail price.",
          "note_zh": "公开资料里，艺术授权的分成大约在 3–10%，贺卡和文具在低的那一端——有一份常被引用的美国资料写的是 2–5%——而且通常是按净销售额算的，扣掉退货、折扣和运费之后，不是按标价。日本又是另一套，在谈之前值得先弄清楚：把已有的插画再用一次，日本叫「二次使用料」（二次使用费），按原稿费的某个比例收取——插画家协会定的是第二次 70%，市场上则在 20–80% 之间。而完全买断（買い取り／著作権譲渡，即买断／著作权转让）不是你稿费的一部分，而是它的倍数——同一个协会给的是两到三倍。商品化也确实有长期分成，大约是零售价的 4–6%。",
          "tier": "now"
        },
        {
          "name": "What an audience is worth here",
          "name_zh": "受众在这件事里值多少",
          "note": "A following is a real asset in these conversations — a brand is buying reach as well as a picture, and yours runs to about 232,800 across five accounts. What nobody publishes is how often that converts into a deal, or what it adds to a fee. Anyone who tells you a number for that is guessing.",
          "note_zh": "在这类洽谈里，受众是实打实的资产——品牌买的是一张画，也是这张画能被多少人看见，而你五个账号加起来大约有 23.3 万人。至于这有多大可能真换来一份合约、能让报价多出多少，没有人公开过。谁给你数字，谁就是在猜。",
          "tier": "now"
        }
      ]
    }
  ]
};

export const PRESS_PITCH_MAP = {
  "titleKey": "sf.press.title",
  "summaryKey": "sf.press.summary",
  "where_to_start": "Press comes from being found, not applying — so tag your strongest work where editors look (#美術手帖, #illustration) and keep a one-page press kit ready (bio, statement, 10 images) for when they reach out. The one exception you can pitch directly: It's Nice That — a daily watercolor practice is exactly their thing.",
  "where_to_start_zh": "媒体报道多半是编辑自己发现的，不是靠投稿投出来的——所以把你最好的作品打上编辑会看的标签（#美術手帖、#illustration），并随时备好一页纸的新闻资料包（简介、创作陈述、10 张图），以便对方联系时立刻可发。唯一可以直接投稿的例外是 It's Nice That——每日水彩创作正是他们钟爱的那一类。",
  "items": [
    {
      "name": "美術手帖 (Bijutsu Techo)",
      "type": "Fine art magazine — Japan",
      "why_fits": "Japan's top fine art magazine. Features emerging Tokyo-based artists with a distinct voice. Urban watercolor + daily practice + Chinese perspective = editorial angle.",
      "how_discovered": "They discover via Instagram, gallery shows, and word of mouth from other featured artists.",
      "how_to_pitch": "They take submissions through a form, not by email. Have the press kit ready (bio, statement, 10 images) to paste and link. Also: tag #美術手帖 on relevant work.",
      // No editorial address is published anywhere — an earlier version of this
      // file carried an invented "editorial@bijutsutecho.com", which would have
      // bounced and cost her a first impression. Their contact page was read on
      // 2026-09-08: it is a form with seven categories and no email at all.
      // Never write a contact here that has not been read off the source.
      "contact": "No editorial email is published. Their contact form is at bijutsutecho.com/contact — choose 「情報のご提供」(information submission). Checked 2026-09-08.",
      "contact_zh": "他们没有公开编辑部邮箱。投稿入口是 bijutsutecho.com/contact 的表单，类别选「情報のご提供」（提供信息）。2026 年 9 月 8 日核实。",
      "contact_ja": "編集部のメールアドレスは公開されていません。窓口は bijutsutecho.com/contact のフォームで、種別は「情報のご提供」を選びます。2026-09-08 確認。",
      "contact_url": "https://bijutsutecho.com/contact",
      "type_zh": "纯艺术杂志 — 日本",
      "type_ja": "美術雑誌 — 日本",
      "why_fits_zh": "日本顶级纯艺术杂志。专注报道在东京活跃、有自己一套视觉语言的新兴艺术家。都市水彩 + 日常创作 + 中国视角 = 编辑切入点。",
      "why_fits_ja": "日本を代表する美術専門誌。独自の視点を持つ東京在住の新進アーティストを特集。都市の水彩画＋日々の制作＋中国人としての視座＝編集上の切り口。",
      "how_discovered_zh": "他们通过 Instagram、画廊展览以及其他已刊登艺术家的口碑推荐来发现新人。",
      "how_discovered_ja": "Instagram、ギャラリー展示、既掲載アーティストからの口コミを通じて新たな作家を発掘している。",
      "how_to_pitch_zh": "他们通过表单接收投稿，而非邮件。事先备好资料包（简介、创作陈述、10 张图），以便直接粘贴与附上链接。同时：在相关作品上标注 #美術手帖。",
      "how_to_pitch_ja": "メールではなくフォームでの受付です。プレスキット（プロフィール、ステートメント、画像10点）を貼り付け・リンクできる形で用意しておく。また、関連作品には #美術手帖 のタグをつける。"
    },
    {
      "name": "Pen Magazine",
      "type": "Lifestyle/design — Japan",
      "why_fits": "Tokyo design/culture magazine. Covers artists with strong visual identity. Urban architecture watercolor is on-brand for their audience.",
      "how_discovered": "Instagram, recommendations from designers and architects they already feature.",
      "how_to_pitch": "Through their inquiry form; no editorial email is published anywhere on either domain. Key: frame the story — not just 'I paint', but 'I document disappearing Tokyo'.",
      "how_to_pitch_zh": "通过他们的咨询表单；两个域名上都没有公开任何编辑部邮箱。关键是把故事讲出来——不是“我画画”，而是“我在记录正在消失的东京”。",
      "contact": "There is no form on pen-online.jp itself. The print edition's inquiry form is form.run/@cccmh-1668417933 (the web edition and the English site have separate ones). No editorial email is published. Checked 2026-09-08.",
      "contact_zh": "pen-online.jp 本身没有表单。纸刊的咨询表单在 form.run/@cccmh-1668417933（网络版和英文站各有各的）。没有公开的编辑部邮箱。2026 年 9 月 8 日核实。",
      "contact_url": "https://form.run/@cccmh-1668417933",
      "type_zh": "生活方式／设计 — 日本",
      "type_ja": "ライフスタイル／デザイン — 日本",
      "why_fits_zh": "东京设计与文化杂志。关注具有鲜明视觉风格的艺术家。都市建筑水彩与其受众的品味高度契合。",
      "why_fits_ja": "東京のデザイン・文化誌。強いビジュアルアイデンティティを持つアーティストを取り上げる。都市建築の水彩画は読者層に合ったテーマ。",
      "how_discovered_zh": "Instagram，以及他们已合作的设计师和建筑师的推荐。",
      "how_discovered_ja": "Instagram、および既に取り上げているデザイナーや建築家からの推薦。",
      "how_to_pitch_ja": "編集部の問い合わせページやコールドメールで連絡する。重要なのはストーリーの組み立て方——「絵を描いている」ではなく、「消えゆく東京を記録している」という切り口で。"
    },
    {
      "name": "It's Nice That",
      "type": "Illustration/design — UK (international reach)",
      "why_fits": "2M+ readers globally. Regularly features illustrators with a quiet, personal visual language. Your daily watercolor diary format is exactly the kind of practice they cover.",
      "how_discovered": "Almost entirely via Instagram and submissions. They actively scout.",
      "how_to_pitch": "Read the submissions guide at itsnicethat.com/submissions, then email submit@itsnicethat.com — bio, project description, and links rather than large attachments. Lead with the daily practice angle.",
      "how_to_pitch_zh": "先看 itsnicethat.com/submissions 上的投稿指南，然后发邮件到 submit@itsnicethat.com——简介、项目说明，用链接而不是大附件。开门见山讲每日创作这件事。",
      "contact": "submit@itsnicethat.com (submissions) — the old /submit URL now just redirects to their contact page. They read everything within about two weeks and only reply if they are running it. Checked 2026-09-08.",
      "contact_zh": "submit@itsnicethat.com（投稿）——旧的 /submit 网址现在只是跳转到联系页。他们大约两周内会看完，只有决定刊登才会回复。2026 年 9 月 8 日核实。",
      "contact_url": "https://www.itsnicethat.com/submissions",
      "type_zh": "插画／设计 — 英国（国际影响力）",
      "type_ja": "イラストレーション／デザイン — イギリス（国際的な影響力）",
      "why_fits_zh": "全球读者超过200万。持续关注具有安静、个人化视觉语言的插画师。你的每日水彩日记形式正是他们所报道的那类创作实践。",
      "why_fits_ja": "世界で200万人以上の読者を持つ。静かで個人的なビジュアル言語を持つイラストレーターを継続的に特集。日々の水彩日記というフォーマットは、まさに彼らが取り上げる創作スタイル。",
      "how_discovered_zh": "几乎完全依赖 Instagram 和投稿。他们会主动发掘新人。",
      "how_discovered_ja": "ほぼ Instagram と投稿のみで発掘している。積極的にスカウトも行っている。",
      "how_to_pitch_ja": "itsnicethat.com/submit から投稿する。日々の制作習慣を前面に出すこと——体系的な創作への取り組みを高く評価している。"
    },
    {
      "name": "Apartamento",
      "type": "Lifestyle/interiors/culture — Spain (international)",
      "why_fits": "Warm, intimate, everyday life aesthetic. Your urban interior and atmospheric work fits perfectly. The 'foreigner observing Tokyo' angle is strong for their editorial.",
      "how_discovered": "Word of mouth, curator recommendations, Instagram. Not submission-based.",
      "how_to_pitch": "Not pitch-based. Build relationships with the people they already feature. Be at the right book fairs (Tokyo Art Book Fair, Offprint).",
      "contact": "No editorial or submissions route exists — their contact page lists shop, general, wholesale and advertising addresses and nothing else. The account is @apartamentomagazine (not @apartamentostudios, which is their commercial arm). Checked 2026-09-08.",
      "contact_zh": "没有编辑或投稿入口——他们的联系页只列了店铺、通用咨询、批发和广告四个邮箱，没有别的。账号是 @apartamentomagazine（不是 @apartamentostudios，那是他们的商业部门）。2026 年 9 月 8 日核实。",
      "contact_url": "https://www.instagram.com/apartamentomagazine/",
      "type_zh": "生活方式／室内／文化 — 西班牙（国际）",
      "type_ja": "ライフスタイル／インテリア／文化 — スペイン（国際的）",
      "why_fits_zh": "温暖、亲密、日常生活的美学。你的都市室内与氛围感作品与其风格完美契合。“外来者观察东京”这个视角，很合他们的编辑方向。",
      "why_fits_ja": "温かく、親密で、日常の美しさを大切にした美学。都市の室内や空気感を捉えた作品は完璧に合っている。「外国人として東京を観察する」という視点は、彼らの編集方針にとって非常に魅力的。",
      "how_discovered_zh": "口碑传播、策展人推荐、Instagram。不接受主动投稿。",
      "how_discovered_ja": "口コミ、キュレーターからの推薦、Instagram。投稿による応募は受け付けていない。",
      "how_to_pitch_zh": "不适合主动投稿。与他们已合作的人建立关系。出现在合适的书展上（Tokyo Art Book Fair、Offprint）。",
      "how_to_pitch_ja": "売り込み型のアプローチは向かない。既に取り上げられている人たちと関係を築くこと。適切なブックフェアに参加する（Tokyo Art Book Fair、Offprint）。"
    },
    {
      "name": "Casa Brutus",
      "type": "Architecture/design/lifestyle — Japan",
      "why_fits": "Architecture and space focus. Your urban watercolor work documenting Tokyo buildings is directly relevant.",
      "how_discovered": "Instagram, gallery shows, architect connections.",
      "how_to_pitch": "By post, not email. Magazine House takes press material by mail only, addressed per title. Keep the architectural angle — position the work as documentation of a place, not just art.",
      "how_to_pitch_zh": "寄信，不是发邮件。マガジンハウス（Magazine House）只接受邮寄的新闻资料，并且要写明刊名。保留建筑这个切入点——把作品定位成对一个地方的记录，而不只是艺术。",
      "contact": "No editorial email or form exists. Press goes by post: 〒104-8003 東京都中央区銀座3-13-10 株式会社マガジンハウス『Casa BRUTUS』情報掲載担当者 宛. @casabrutus on Instagram is genuine. Careful — the one Magazine House email that turns up in a search belongs to advertising sales, not the editors. Checked 2026-09-08.",
      "contact_zh": "没有编辑部邮箱，也没有表单。新闻资料走邮寄：〒104-8003 東京都中央区銀座3-13-10 株式会社マガジンハウス『Casa BRUTUS』情報掲載担当者 宛。Instagram 上的 @casabrutus 是真的。注意：搜索能搜到的那个マガジンハウス邮箱属于广告部，不是编辑部。2026 年 9 月 8 日核实。",
      "type_zh": "建筑/设计/生活方式 — 日本",
      "type_ja": "建築・デザイン・ライフスタイル — 日本",
      "why_fits_zh": "聚焦建筑与空间。你记录东京建筑的城市水彩作品与该方向高度契合。",
      "why_fits_ja": "建築と空間に特化した媒体。東京の建物を記録した都市水彩作品は、そのテーマと直接つながる。",
      "how_discovered_zh": "Instagram、画廊展览、建筑师人脉。",
      "how_discovered_ja": "Instagram、ギャラリー展示、建築家とのつながり。",
      "how_to_pitch_ja": "建築的な切り口を明確にして編集者にメールを送る。作品を単なるアートではなく、建築ドキュメンテーションとして位置づけること。"
    },
    // ILOVETOYS / neuprint removed 2026-09-08. Neither publication could be
    // shown to exist: eight searches in English and Chinese surfaced only a UK
    // toy retailer and a 2006 TV series. Its contact named no account, on a
    // platform (Weibo) she does not use, while Xiaohongshu - where she has 44k -
    // went unmentioned; and its _zh invented "Beijing" as her origin, which the
    // English never said. The opposite failure to the fabricated Bijutsu Techo
    // address: too vague for anything in it to be caught.
    {
      "category_note": "Being discovered vs. applying",
      "how_discovered": "Most press features happen via discovery, not application. Editors follow Instagram. They read other publications. They attend book fairs. The path to press coverage is: (1) be findable on Instagram with correct hashtags and language, (2) show up at physical events (art book fairs, gallery openings), (3) have a press kit ready when they reach out.",
      "contact": "",
      "category_note_zh": "被发现，还是主动投稿",
      "category_note_ja": "発見されること vs. 自ら売り込むこと",
      "how_discovered_zh": "大多数媒体报道来自被编辑发现，而不是自己投稿。编辑会关注 Instagram，阅读其他刊物，参加书展。获得媒体报道的路径是：(1) 在 Instagram 上使用正确的标签和语言，确保被搜索到；(2) 出现在线下活动中（艺术书展、画廊开幕式）；(3) 当对方主动联系时，备好完整的新闻资料包。",
      "how_discovered_ja": "メディアへの掲載は、自ら売り込むよりも発見されることで実現する場合がほとんどだ。編集者は Instagram をフォローし、他の媒体を読み、ブックフェアに足を運ぶ。メディア掲載への道は次の通り：(1) 適切なハッシュタグと言語で Instagram 上で見つけてもらえる状態にする、(2) リアルなイベント（アートブックフェア、ギャラリーのオープニング）に顔を出す、(3) 問い合わせが来たときにすぐ渡せるプレスキットを用意しておく。"
    }
  ]
};

export const GRANT_LANDSCAPE = {
  // REWRITTEN 2026-09-08 after every claim was checked against the funders' own
  // pages. Of the five programmes previously listed, TWO were closed to her in
  // writing (Bunka-cho: Japanese nationality or PR; Japan Foundation: Japan or
  // ASEAN nationality/PR), ONE could not be shown to exist at all ("China Arts
  // Foundation International", with an invented embassy-attaché route), the only
  // URL on the page (acc.org) was the American College of Cardiology, and ACC's
  // award was understated by about half while its full-time-student bar and its
  // refusal to fund production went unmentioned.
  //
  // Every `competition` field is gone: no funder here publishes acceptance
  // rates, so all five were unfalsifiable.
  //
  // _ja omitted deliberately — LANGUAGES is ['zh','en'], so ja is unreachable
  // UI. Same precedent as COLLABORATION_MAP below.
  "titleKey": "sf.grant.title",
  "summaryKey": "sf.grant.summary",
  // "the only one that asks nothing about your passport" was false on this
  // block's own evidence — Arts Council Tokyo, two entries down, says "No
  // nationality clause" in its own eligibility line. Corrected 2026-09-10.
  "where_to_start": "TOKAS-Emerging is the best fit, and it asks nothing about your passport — it wants you living in Japan and born on or after 1 April 1990, and it gives a solo show at TOKAS Hongo plus ¥150,000 toward making the work. The 2027 call closed on 31 July 2026; timing for the following call has not been announced.",
  "where_to_start_zh": "TOKAS-Emerging 是最合适的一个，而且不问国籍——只要你住在日本，且出生于 1990 年 4 月 1 日或之后。它给的是 TOKAS 本乡的一个个展，再加 15 万日元的制作支持。2027 年度征集已于 2026 年 7 月 31 日截止；下一轮时间尚未公布。",
  "items": [
    {
      "name": "TOKAS-Emerging (トーキョーアーツアンドスペース)",
      "website": "https://www.tokyoartsandspace.jp/",
      "country": "Japan (Tokyo)",
      "country_zh": "日本（东京）",
      "amount": "Solo show at TOKAS Hongo + ¥150,000 production support",
      "amount_zh": "TOKAS 本乡的个展 ＋ 15 万日元制作支持",
      "eligibility": "Living in Japan (日本在住) and born on or after 1 April 1990. No nationality requirement — checked 2026-09-08.",
      "eligibility_zh": "住在日本（日本在住），且 1990 年 4 月 1 日或之后出生。没有国籍要求——2026 年 9 月 8 日核实。",
      "deadline": "The 2027 call ran 26 June–31 July 2026 and is closed; the following call has not been announced",
      "deadline_zh": "2027 年度征集于 2026 年 6 月 26 日至 7 月 31 日开放，现已截止；下一轮尚未公布",
      "why_apply": "A solo exhibition at a public institution, with money toward making the work, and nothing in the criteria about where you are from.",
      "why_apply_zh": "在一个公立机构做一个个展，带制作费，而且条件里没有一句话提到你来自哪里。",
      "tip": "TOKAS and Arts Council Tokyo are two different organisations with separate portals and separate calls, despite sitting under the same foundation. There is no combined application.",
      "tip_zh": "TOKAS 和东京艺术委员会是两个不同的机构，各有各的入口、各自开放，尽管同属一个基金会。没有“合并申请”这回事。"
    },
    {
      "name": "Arts Council Tokyo — Startup Grant",
      "website": "https://www.artscouncil-tokyo.jp/",
      "country": "Japan (Tokyo)",
      "country_zh": "日本（东京）",
      "amount": "Up to ¥300,000 for an individual, within eligible subsidized expenses",
      "amount_zh": "个人最高 30 万日元，且不超过项目本身的合规支出",
      "eligibility": "An individual living in Tokyo (東京都内に居住する個人). No nationality clause. One thing nobody publishes: whether a student visa satisfies that residence test. Worth a phone call (03-6256-8431) before building anything around it.",
      "eligibility_zh": "住在东京都内的个人。没有国籍条款。有一件事没有任何地方写明：留学签证算不算“居住”。在为它做任何准备之前，值得先打一通电话（03-6256-8431）。",
      "deadline": "Second round closes 24 September 2026, 18:00 JST",
      "deadline_zh": "第二轮截止：2026 年 9 月 24 日 18:00（日本时间）",
      "why_apply": "It funds a project you organise yourself rather than an application into someone else's open call — a different shape from everything else here.",
      "why_apply_zh": "它资助的是你自己组织的项目，而不是去投别人的征集——和这页上其他所有东西都不同。",
      "tip": "The award is capped at ¥300,000 for an individual and must stay within eligible subsidized expenses. Check the detailed guidelines before budgeting.",
      "tip_zh": "个人申请的资助上限为 30 万日元，实际金额还不能超过项目里算得上合规支出的那部分。做预算前先对一遍详细指南。"
    },
    {
      "name": "Asian Cultural Council — Individual Fellowship",
      "website": "https://www.asianculturalcouncil.org/grant-opportunities",
      "country": "USA (for artists from Asia)",
      "country_zh": "美国（面向亚洲艺术家）",
      "amount": "Up to US$35,000 as a lump sum you budget yourself, for 1–6 months",
      "amount_zh": "最高 35,000 美元，一次性发放、预算由你自己安排，为期 1–6 个月",
      "eligibility": "Nationality or permanent residency of one of 26 listed locations, including the U.S. — China (Mainland) is on the list, so you pass that test. Applicants must be 21 or over and have five years of professional experience. You may apply while enrolled, but during the funded fellowship you must arrange a leave of absence and do no university coursework or teaching.",
      "eligibility_zh": "需要属于官方列出的 26 个国家或地区（包括美国）之一的国籍或永久居留权——中国大陆在列，这一关你过。申请人须年满 21 岁，并有五年专业经历。在读期间可以申请，但在受资助的奖学金期间必须办理休学，且不得修读大学课程或从事教学。",
      "deadline": "2027 cycle: 1 October – 10 November 2026, 09:59 ET",
      "deadline_zh": "2027 年度：2026 年 10 月 1 日 至 11 月 10 日 09:59（美东时间）",
      "why_apply": "The one programme here you clear on nationality outright, and the largest sum on the page.",
      "why_apply_zh": "这是这页上唯一一个你在国籍上直接过关的，金额也是最大的。",
      "tip": "It funds looking, not making. ACC says outright that it does not fund producing work or mounting exhibitions — it supports open-ended research. A proposal built around a finished body of work is the shape they refuse.",
      "tip_zh": "它资助的是“去看”，不是“去做”。ACC 明确说明不资助创作与办展，只支持开放式的考察研究。以“做出一批作品”为目标写的申请，正是他们会拒绝的那种。"
    },
    {
      "name": "国家艺术基金 (China National Arts Fund)",
      "website": "https://www.cnaf.cn/",
      "country": "China",
      "country_zh": "中国",
      // Was "¥100,000 RMB" — ¥ means JPY everywhere else on this page, so the
      // one RMB figure read as a Japanese-yen amount twenty times too small.
      "amount": "Up to RMB 100,000",
      "amount_zh": "最高 10 万元人民币",
      "eligibility": "Chinese nationals; it tests 户籍. Needs either a work-unit letter or three mainland experts at 副高级 or above to recommend you. Watercolour is a named category (水彩（粉）画).",
      "eligibility_zh": "面向中国公民，以户籍为准。需要单位推荐函，或三位副高级以上的内地专家推荐。水彩（粉）画是列明的类别。",
      "deadline": "The 2027 cycle closed 15 June 2026",
      "deadline_zh": "2027 年度已于 2026 年 6 月 15 日截止",
      "why_apply": "The only Chinese-national route on this page that could be verified as real. It is here with its weight stated rather than left out.",
      "why_apply_zh": "这是这页上唯一一条核实过、确实存在的中国国籍途径。",
      "tip": "The requirements are heavy: finished works must be at least 1.5m × 1.5m, and on the 美术创作 route the painting is collected by a Chinese state museum. That is a different practice from the one you have.",
      "tip_zh": "门槛不低：成品尺寸至少 1.5 米 × 1.5 米；走美术创作这条线的话，作品要交给国内国有美术馆收藏。这和你现在做的事是两回事。"
    },
    // This item is intentionally NOT rendered — GrantLandscape (SaffronPage.jsx)
    // skips any item with category_note. It used to show as a callout at the end
    // of the Grant Landscape section; Scott, 2026-09-10: "there is a section that
    // says one opportunity doesn't apply. then why are you showing it to her?"
    // Kept here so nobody re-adds Bunka-cho or the Japan Foundation as a live
    // option without re-checking eligibility first — it's the record of why they
    // were removed, not something meant for her to read.
    {
      "category_note": "Checked, and closed to you",
      "category_note_zh": "已核实：这两扇门对你是关着的",
      "note": "Two doors that look open are not. Bunka-cho's overseas study programme (新進芸術家海外研修制度) requires Japanese nationality or permanent residency, and the form asks for documentary proof of it. The Japan Foundation's one individual arts fellowship requires nationality or permanent residency of Japan or an ASEAN country. Both were checked on 8 September 2026, and they are named here only so that nobody spends a month finding out.",
      "note_zh": "有两扇门看上去开着，其实并没有开。文化厅的“新进艺术家海外研修制度”要求日本国籍或永久居留资格，表格里还要求附证明文件。国际交流基金会唯一面向个人的艺术类项目，要求日本或东盟国家的国籍或永久居留权。两项均于 2026 年 9 月 8 日核实。写在这里，是免得你白花一个月才发现。",
      "apply": ""
    }
  ]
};

export const REVENUE_STREAMS = {
  "titleKey": "sf.revenue.title",
  "summaryKey": "sf.revenue.summary",
  "where_to_start": "There's no single right way to earn from your work, and none of this is urgent. If you ever want a gentle place to begin, the lowest-effort step is simply linking wherever your work can be found in your Instagram bio, so people who already love it can find it. Everything below is optional — pick only what feels good.",
  "where_to_start_zh": "靠作品赚钱没有唯一正确的方式，而且这些都不急。如果哪天你想轻松地起个头，最省力的一步，是在 Instagram 简介里放一个链接，指向能看到、能买到你作品的地方，让已经喜欢你画的人找得到。以下内容都是可选的——只挑让你觉得舒服的去做就好。",
  "where_to_start_ja": "作品で収入を得る「正解」は一つではありませんし、どれも急ぐ必要はありません。もし気軽に始めたくなったら、いちばん手間のかからない一歩は、あなたの作品を見られる場所を Instagram のプロフィールにリンクしておくこと。すでに作品を好きでいてくれる人が見つけやすくなります。以下はすべて任意です——心地よいと感じるものだけを選んでください。",
  "items": [
    {
      "stream": "Print-on-demand merch (optional)",
      "setup_time": "1–2 days if you ever try it; 1 hr/week", "setup_time_zh": "若想试试，初期 1–2 天；每周约 1 小时", "setup_time_ja": "もし試すなら初期1〜2日、維持は週1時間ほど",
      "description": "Print-on-demand platforms (e.g. SUZURI) produce and ship merch — totes, pouches, cases, art prints — from an uploaded image, with no inventory to hold. It's a hands-off option some illustrators enjoy, not something you need.",
      "why_now": "This is purely optional. If the idea of low-effort merch sounds fun, it's there; if it doesn't, there's nothing to fix by skipping it.",
      "leaving_on_table": false,
      "stream_zh": "按需印刷周边（可选）",
      "stream_ja": "プリントオンデマンドのグッズ（任意）",
      "description_zh": "按需印刷平台（如 SUZURI）可以根据你上传的图像生产并配送周边——帆布包、小袋、手机壳、艺术印刷品——无需囤货。这是一些插画师喜欢的省心选项，但并非必需。",
      "description_ja": "プリントオンデマンドのプラットフォーム（例：SUZURI）は、アップロードした画像からグッズ（トートバッグ、ポーチ、ケース、アートプリントなど）を製造・発送してくれます。在庫を抱える必要はありません。手間のかからない選択肢として楽しむ人もいますが、必須ではありません。",
      "why_now_zh": "这完全是可选项。如果你觉得做点省心的周边挺有意思，它就在那儿；如果不感兴趣，跳过它也不会损失什么。",
      "why_now_ja": "これは完全に任意です。手軽なグッズづくりが楽しそうだと感じたら選べますし、そうでなければ、やらないことで失うものは何もありません。"
    },
    {
      "stream": "Booth.pm (another optional home for work)",
      "description": "Booth.pm is a Japanese direct-to-artist platform (a bit like Gumroad). If you ever want a simple place for digital goods — process videos, reference photos, custom brushes — or to announce a piece, it's a low-friction option. Purely one more open door, not something to set up unless it appeals.",
      "why_now": "Useful to know it exists; nothing about it is urgent or expected.",
      "leaving_on_table": false,
      "stream_zh": "Booth.pm（作品另一个可选的去处）",
      "stream_ja": "Booth.pm（作品のもう一つの任意の置き場所）",
      "description_zh": "Booth.pm 是日本一个面向创作者的直销平台（有点像 Gumroad）。如果你哪天想给数字商品——过程视频、参考照片、自定义笔刷——找个简单的去处，或想发布某件作品，它是个省事的选项。它只是又一扇开着的门，不感兴趣就不必去搭建。",
      "description_ja": "Booth.pm はクリエイター向けの日本の直販プラットフォームです（Gumroad に少し似ています）。もしいつか、デジタル商品（制作過程の動画、参考写真、カスタムブラシなど）の簡単な置き場所が欲しくなったり、作品を告知したくなったりしたら、手軽な選択肢になります。あくまでもう一つの開いた扉であり、気が向かなければ用意する必要はありません。",
      "why_now_zh": "知道有这么个平台就好；它一点也不急，也不是非做不可。",
      "why_now_ja": "そういう場所があると知っておくだけで十分です。急ぐことも、求められることも何もありません。"
    },
    {
      "stream": "Sharing originals when you want to",
      "description": "For many artists with an engaged following, simply letting people know directly (a quiet 'DM to inquire' note, or a link) is the most natural way work finds a home. There's no schedule you owe anyone — share a piece when it feels right.",
      "why_now": "An audience that loves your daily work is a gentle, real foundation. Nothing here needs to happen on a timeline.",
      "leaving_on_table": false,
      "stream_zh": "想分享时再分享原作",
      "stream_ja": "気が向いたときに原画をシェアする",
      "description_zh": "对很多拥有活跃受众的艺术家来说，直接让大家知道（一句安静的“私信咨询”，或一个链接）往往是作品找到归属最自然的方式。你不欠任何人一个时间表——想分享某幅作品时再分享就好。",
      "description_ja": "熱心なフォロワーがいる多くのアーティストにとって、ただ直接知らせること（「購入希望の方はDMへ」という静かな一言や、リンク）が、作品が居場所を見つけるいちばん自然な方法であることが多いです。誰に対しても予定を負う必要はありません——気が向いたときに作品をシェアすれば十分です。",
      "why_now_zh": "一群喜爱你日常作品的受众，本身就是温和而真实的基础。这里的一切都无需赶时间。",
      "why_now_ja": "あなたの日々の作品を愛してくれるオーディエンスの存在は、穏やかで確かな土台です。ここにあることは、何ひとつ急ぐ必要はありません。"
    },
    {
      "stream": "A numbered-print tier (one option, if you'd like)",
      "description": "Some artists add a small line of numbered, signed prints alongside their originals — it's one way to let more people live with the work without parting with the original. It's entirely optional, and many artists are happy never doing it. Mentioned only so you know the door exists.",
      "edition_discipline": "If you ever try it: a fixed edition size (say ≤30), signed and numbered, keeps prints feeling special. There's no rush and no quota.", "edition_discipline_zh": "如果哪天想试：固定一个版数（比如 ≤30 版），签名并编号，能让版画保持特别感。不急，也没有任何指标。", "edition_discipline_ja": "もし試すなら：エディション数を固定し（例：30点以下）、サインと番号を入れると、プリントが特別なものに保たれます。急ぐ必要も、ノルマもありません。",
      "why_now": "There's no gap here and nothing missing — this is simply an idea on the shelf for whenever (or never) you want it.",
      "leaving_on_table": false,
      "stream_zh": "编号限量版画（一个可选项，如果你愿意的话）",
      "stream_ja": "ナンバリング入りプリントの展開（やってみたければ、という一つの選択肢）",
      "description_zh": "一些艺术家会在原作之外，再做一小批编号、签名的版画——这是让更多人把作品带回家、同时又不必割舍原作的一种方式。它完全是可选的，许多艺术家也乐于从不涉足。在这里提到，只是想让你知道这扇门存在。",
      "description_ja": "原画とは別に、ナンバリング・サイン入りのプリントを少量展開するアーティストもいます。原画を手放さずに、より多くの人に作品を楽しんでもらう一つの方法です。これは完全に任意で、まったくやらないという選択をするアーティストもたくさんいます。ここで触れたのは、そういう扉があると知っておいてもらうためだけです。",
      "why_now_zh": "这里没有任何缺口、也没有任何缺失——这只是一个搁在架上的想法，你想要的时候（或永远不想）都可以。",
      "why_now_ja": "ここには欠けているものも、埋めるべき隙間もありません——これは棚に置いてあるアイデアにすぎず、欲しくなったとき（あるいは一度も欲しくならなくても）それで構いません。"
    },
    {
      "stream": "Commissions, if they find you",
      "description": "If commission requests come your way and you'd enjoy them, they're a natural fit for your kind of work. The one gentle thing worth holding onto: artists often undercharge because they feel they should — your work is worth what it's worth, so don't let anyone talk you down. Taking commissions or not is entirely up to you.",
      "leaving_on_table": false,
      "stream_zh": "如果有人来约稿",
      "stream_ja": "依頼が来たときのコミッション",
      "description_zh": "如果有人来约稿、而你也乐意去做，这与你的创作方向很契合。唯一值得轻轻记住的一点是：艺术家常因为“觉得应该”而压低价格——你的作品值多少就是多少，别让任何人把你说低。接不接约稿，完全由你决定。",
      "description_ja": "もしコミッションの依頼が舞い込み、それを楽しめそうなら、あなたの作風にとても合っています。一つだけ、そっと心に留めておきたいこと：アーティストは「そうすべき」という思い込みから値段を低くしがちです——あなたの作品の価値は、その価値のままです。誰かに安く言いくるめられないでください。受けるかどうかは、あなた次第です。"
    },
    {
      "stream": "Putting work in shops you love (consignment)",
      "description": "Bookshops, galleries and cafés will sometimes hold a few pieces on consignment — your work lives somewhere lovely and finds people while you're elsewhere. It's a calm, low-pressure way to be present in the city, and a nice excuse to visit spaces you already like.",
      "venues_note": "If you ever feel like it, places like UTRECHT, flotsam books, or B&B (now at BONUS TRACK in Setagaya-Daita, one stop from Shimokitazawa, though it still calls itself a Shimokitazawa bookshop) are the kind of warm, on-brand spots worth a friendly hello.", "venues_note_zh": "如果哪天有心情，像 UTRECHT、flotsam books、B&B（现在在世田谷代田的 BONUS TRACK，离下北泽一站，不过它仍自称下北泽的书店）这样温暖、气质契合的小店，值得去打个招呼。", "venues_note_ja": "もし気が向いたら、UTRECHT、flotsam books、B&B Shimokitazawa のような、温かく世界観の合う場所に気軽に声をかけてみる価値があります。",
      "leaving_on_table": false,
      "stream_zh": "把作品放进你喜欢的店里（寄售）",
      "stream_ja": "好きなお店に作品を置いてもらう（委託販売）",
      "description_zh": "书店、画廊和咖啡馆有时会代售几件作品——你的作品安放在某个可爱的角落，在你不在场时也能遇见喜欢它的人。这是一种平静、无压力的方式，让你温和地存在于这座城市里，也是个去逛逛你本就喜欢的空间的好借口。",
      "description_ja": "書店やギャラリー、カフェは、作品を数点、委託で預かってくれることがあります。あなたの作品が素敵な場所に置かれ、あなたが他の場所にいる間も、好きになってくれる人と出会えます。穏やかで気負いのない形で街の中に存在できる方法であり、もともと好きな空間を訪ねる良い口実にもなります。"
    },
    {
      "stream": "Summary assessment",
      "description": "None of the above is a to-do list, and nothing here is being left undone. Your daily practice and the people who love it are already the foundation — everything on this page is just an open door, there if and when you want it. The healthiest pace is your own.",
      "leaving_on_table": false,
      "stream_zh": "一点温柔的话",
      "stream_ja": "そっと一言",
      "description_zh": "以上这些都不是待办清单，这里也没有任何“没做完”的事。你每天的创作，以及喜爱它的人们，本身就已经是基础——这一页上的一切，都只是一扇开着的门，等你想要的时候再进去。最健康的节奏，是属于你自己的节奏。",
      "description_ja": "上に書いたことは、どれもやることリストではありませんし、ここに「やり残し」は一つもありません。あなたの日々の制作と、それを愛してくれる人たちが、すでに土台になっています——このページにあるものはすべて、開いている扉にすぎず、欲しくなったときにくぐればいいのです。いちばん健やかなペースは、あなた自身のペースです。"
    }
  ]
};

export const PRICING_INTELLIGENCE = {
  titleKey:   "sf.sec.pricing",
  summaryKey: "sf.sum.pricing",
  // WHAT WENT WRONG HERE (fixed 2026-09-08). This block used to carry a
  // hardcoded band — ¥30,000-115,000 originals, ¥3,000-15,000 prints,
  // ¥1,200-2,800 zines — under the line "General context from Tokyo
  // emerging-illustrator market observation". There was no such observation.
  // The originals figures were HER OWN published prices rounded off and handed
  // back to her as though the market had said them, and the print and zine
  // bands were invented ABOVE what she actually charges (¥2,200 and ¥1,980),
  // so the page implied she was underpricing while claiming not to judge.
  // The numbers now come from the profile via /api/saffron, sourced to her shop
  // with a read date. Never put a price in this file again.
  source_note: "These are your own prices, read off your shop — not a market estimate. Nothing here is a target and nothing needs changing; it's here so the rest of the page can do arithmetic in your actual numbers.", "source_note_zh": "这些是你自己的价格，取自你的店铺——不是市场估算。这里没有任何目标值，也没有需要改的地方；把它放在这儿，只是为了让这一页其余的计算能用你真实的数字。", "source_note_ja": "これはあなた自身の価格で、ショップから読み取ったものです——市場の推計ではありません。ここに目標値はなく、変えるべきものもありません。このページの他の計算を、あなたの実際の数字で行うために置いてあります。",
  // Copy only. The figures live on the profile and arrive from the API; these
  // are keyed by the band's `note` field.
  band_notes: {
    originals: {
      label: "Original watercolours", "label_zh": "水彩原作", "label_ja": "水彩原画",
      note: "The spread across what you have listed — smaller diary pieces at the lower end, larger work higher.", "note_zh": "你上架作品的价格跨度——小幅日记作品偏低，大幅作品偏高。", "note_ja": "出品中の作品の価格幅です——小判の日記作品は下限寄り、大きめの作品は上限寄り。",
    },
    prints: {
      label: "Prints", "label_zh": "版画", "label_ja": "プリント",
      note: "One price across the line.", "note_zh": "整条产品线统一定价。", "note_ja": "ライン全体で一律の価格です。",
    },
    zines: {
      label: "Zines and art books", "label_zh": "Zine 与画集", "label_ja": "Zineとアートブック",
      note: "One price across the line. This is the tier a book fair sells from.", "note_zh": "整条产品线统一定价。书展上卖的就是这一档。", "note_ja": "ライン全体で一律の価格です。ブックフェアで売れるのはこの価格帯です。",
    },
    postcards: {
      label: "Postcards", "label_zh": "明信片", "label_ja": "ポストカード",
      note: "Sold in packs of 6 and 10, so the cheapest thing anyone can buy from you is ¥1,100 rather than the price of one card.", "note_zh": "以 6 张、10 张成套出售，所以别人能从你这里买到的最便宜的东西是 1,100 日元，而不是单张的价格。", "note_ja": "6枚組・10枚組での販売なので、いちばん安く買えるものは1枚の値段ではなく1,100円になります。",
    },
  },
  commission_note: "No published rate — negotiated per piece. For scale: a Western 8×10 watercolour house portrait runs ¥31,000–39,000, which brackets your originals floor almost exactly. Japanese commission platforms pay roughly half that before an 11–22% cut.", "commission_note_zh": "没有公开报价——按件商议。作为参照：欧美一张 8×10 英寸的水彩房屋肖像约 31,000–39,000 日元，几乎正好卡在你原作的起价线上。日本的约稿平台大约只有这个数的一半，还要再抽 11–22%。", "commission_note_ja": "公開料金はなく、案件ごとの相談です。目安として、欧米の8×10インチの水彩ハウスポートレートは31,000〜39,000円で、あなたの原画の下限とほぼ重なります。日本の依頼プラットフォームはその半分ほどで、さらに11〜22%が引かれます。",
  what_affects_price: [
    { factor: "Venue context", "factor_zh": "场地背景", "factor_ja": "会場の文脈", impact: "high",   note: "The same piece tends to sell for more at a gallery opening than at a zine fair — the setting carries part of the price. Just how the market reads context, nothing you need to act on.", "note_zh": "同一件作品在画廊开幕上往往比在独立刊物展会上卖得更高——场地本身也承载了一部分价格。这只是市场解读情境的方式，并不需要你为此做什么。", "note_ja": "同じ作品でも、ギャラリーのオープニングではzineフェアより高く売れる傾向があります——場が価格の一部を担うのです。市場が文脈を読み取る仕組みにすぎず、何かする必要はありません。" },
    { factor: "Edition discipline", "factor_zh": "版数固定", "factor_ja": "エディションの規律", impact: "high",   note: "If you ever do editions, a fixed size (e.g. 30 or 50) keeps each print feeling intentional and protects its value over open-ended runs.", "note_zh": "如果你哪天做限量版，固定一个版数（如 30 或 50）能让每件版画都显得用心，也比无限量印刷更能保值。", "note_ja": "もしエディションを作るなら、数を固定する（例：30や50）と、一点一点に意図が感じられ、無制限の刷りよりも価値が保たれます。" },
    { factor: "Audience", "factor_zh": "受众", "factor_ja": "オーディエンス", impact: "medium", note: "An engaged following is a genuine asset: it shows that people choose to keep up with the work. Yours runs across five places at once: about 89,300 on X, 65,000 on Weibo, 44,000 on Xiaohongshu, 27,000 on the Instagram diary, and 7,500 on Bilibili for the painting videos — roughly 233,000 follows in total. Sales conversion has not been measured, so this is evidence of attention, not a claim about collectors or buyers.", "note_zh": "持续关注你的受众是一项真实的资产：这说明有人主动选择继续看你的作品。关注分布在五个平台：X 约 8.93 万、微博约 6.5 万、小红书约 4.4 万、Instagram 日记约 2.7 万、B 站绘画视频约 7,500——合计约 23.3 万次关注。销售转化尚未测量，因此这只能证明关注度，不能据此断言藏家或买家行为。", "note_ja": "継続的に作品を見てくれるフォロワーは確かな資産です。人々が自ら作品を追い続けていることを示します。Xに約89,300、Weiboに約65,000、REDに約44,000、Instagramの日記に約27,000、Bilibiliの制作動画に約7,500、合計およそ233,000のフォローがあります。販売への転換は測定されていないため、これは関心の証拠であり、コレクターや購入者についての断定ではありません。" },
    { factor: "Exhibition CV", "factor_zh": "展览履历", "factor_ja": "展示歴",       impact: "medium", note: "As exhibition credits accumulate, the market naturally supports a little more over time. No need to chase this — it follows the work you're already doing.", "note_zh": "随着展览履历的积累，市场自然会随时间逐渐支撑更高一些的价格。无需刻意追求——它会跟随你本就在做的创作自然而来。", "note_ja": "展示の実績が積み重なると、時間とともに市場が少しずつ高い価格を自然に支えるようになります。追い求める必要はありません——あなたが今している制作に、自然とついてきます。" },
    { factor: "Certificate of authenticity", "factor_zh": "作品真品证书", "factor_ja": "真作証明書", impact: "medium", note: "A simple, hand-signed certificate adds a sense of permanence buyers appreciate, and takes about two minutes. A small, optional nicety.", "note_zh": "一份简单的手签真品证书能带来一种买家所珍视的恒久感，只需约两分钟。一个可有可无的小用心。", "note_ja": "手書きサイン入りのシンプルな証明書は、買い手が大切にする「永続性」の感覚を添えてくれます。所要時間は約2分。あってもなくてもよい、ささやかな心づかいです。" },
    { factor: "Work size", "factor_zh": "作品尺幅", "factor_ja": "作品サイズ",           impact: "low",    note: "Smaller formats are often easiest for buyers to live with. The one gentle guard: small doesn't mean cheap — value small work fully.", "note_zh": "较小的尺幅往往最便于买家收纳与悬挂。唯一值得轻轻提醒的一点：小不等于廉价——别低估了小幅作品的价值。", "note_ja": "小判は買い手にとって取り入れやすいことが多いです。ひとつだけそっと添えるなら：小さいことは安いことではありません——小品の価値を十分に評価してください。" },
  ],
  credibility_signals: [
    "Signed, dated, and titled on the back of every original",
    "Edition numbers visible on any prints (e.g., 7/30)",
    "A simple certificate of authenticity if you like",
    "Consistent handle/name across platforms",
    "A clear photo of the work",
  ], "credibility_signals_zh": ["每幅原作背面签名、标注日期与标题", "若有版画，标注版数（如 7/30）", "如果你愿意，可附一份简单的真品证书", "各平台使用一致的账号名／姓名", "一张清晰的作品照片"], "credibility_signals_ja": ["原画はすべて裏面に署名・日付・タイトルを記入", "プリントがある場合はエディション番号を表示（例：7/30）", "よければ簡単な真作証明書を添える", "各プラットフォームで一貫したハンドル／名前", "作品の鮮明な写真"],
  edition_discipline: {
    rule: "If you ever make editions, pick a size and stick to it — 30 or 50 both work nicely. There's no quota and nothing you have to do here.", "rule_zh": "如果你哪天做限量版，选定一个版数并保持一致即可——30 版或 50 版都很好。这里没有任何指标，也没有任何非做不可的事。", "rule_ja": "もしエディションを作るなら、数を決めてそれを守るだけ——30でも50でも素敵です。ここにノルマはなく、しなければならないことも何もありません。",
    why: "Consistency is simply what keeps prints feeling special. Entirely up to you.", "why_zh": "保持一致，只是为了让版画始终显得特别。完全由你决定。", "why_ja": "一貫性は、プリントを特別なものに保つためのものにすぎません。すべてあなた次第です。",
    current_gap: "Nothing here needs fixing — this is background, offered only for the day you might find it useful.", "current_gap_zh": "这里没有任何需要改进的地方——只是背景信息，留待你哪天可能用得上。", "current_gap_ja": "ここに直すべきものはありません——これは背景情報であり、いつか役に立つかもしれない日のために添えているだけです。",
  },
  red_flags: [
    "The only real trap is the common one: undervaluing your own work because you feel you should. Don't let anyone talk you down.",
    "Keeping 'sold' and 'available' work clearly separated saves collectors confusion.",
  ],
};

// ── Collaboration Map ──────────────────────────────────────────────────────
// Real, verified people whose work rhymes with hers, in three honest groups,
// plus a low-pressure how-to. Replaces the old "list of 5 strangers" (Scott,
// 2026-06-26). zh baked in; ja falls back to en (known follow-up gap).
export const COLLABORATION_MAP = {
  title: "Collaboration Map",
  title_zh: "合作地图",
  title_ja: "コラボレーション・マップ",
  summary: "Real people whose work rhymes with yours — and small, low-pressure ways to build with them.",
  summary_zh: "与你气味相投的创作者——以及几种和他们轻松开启合作的小方式。",
  summary_ja: "あなたの作品と響き合う実在の人たち——そして、低圧力で一緒に始められる小さな方法。",
  lead: "These aren't cold contacts — they're a map of the world your work already belongs to. Start by being a real reader of their work; collaboration grows from staying in the room, not from a pitch.",
  lead_zh: "这不是一份陌生人名单，而是一张地图，标出你的作品原本就属于的世界。先真心关注和欣赏他们的作品；合作往往是在同一个圈子里相处久了自然发生的，不是一次自我推销换来的。",
  groups: [
    {
      label: "The shape of your world: webcomic & daily-life illustrators",
      label_zh: "你世界的样子：网络漫画与日常生活插画家",
      entries: [
        {
          name: "Sarah Andersen (Sarah's Scribbles)",
          who: "American cartoonist behind Sarah's Scribbles, one of the best-known daily relatable webcomics.",
          who_zh: "美国漫画家，《Sarah's Scribbles》作者，最知名的日常共鸣网络漫画之一。",
          why_fit: "You've already shown in the same exhibition context as her (London, Dec 2025). She's living proof your world is the webcomic / illustration community, not the watercolor society.",
          why_fit_zh: "你已经和她在同一个展览中出现过（伦敦，2025 年 12 月）。这也说明，你的作品更自然地属于网络漫画与插画社群，而不是水彩协会的体系。",
          link: "https://www.instagram.com/sarahandersencomics/",
          collab_form: "Contribute to a daily-life / 'feelings' comics anthology or charity zine in that orbit; keep building presence in the curatorial circles that already placed you near her.",
          collab_form_zh: "在那个圈子里为日常生活或“心情”主题的漫画合志／公益zine供稿；继续留在那个已经让你与她同台过的策展圈子里，慢慢积累存在感。",
        },
        {
          name: "War and Peas (Elizabeth Pich & Jonathan Kunz)",
          who: "A two-person webcomic duo who post once a week and exhibit together.",
          who_zh: "双人网络漫画组合，每周更新一次，一起办展。",
          why_fit: "The clearest working model of the small, repeatable two-person collaboration that suits a quiet maker like you — built on consistency and showing up together, the strength your six-year diary already has.",
          why_fit_zh: "最清晰的“小而可重复的双人合作”范本，正适合像你这样安静的创作者——靠的是持续与共同露面，而这正是你六年手账的力量。",
          link: "https://www.instagram.com/war.and.peas/",
          collab_form: "Borrow the format, not the fame — a two-person mini-zine or a single shared post with one peer, repeated until it's a habit.",
          collab_form_zh: "借用的是形式而非名气——和一位同辈做一本双人小zine，或一次共同发布，重复到成为习惯。",
        },
        {
          name: "Liz Climo",
          who: "Cartoonist and former Simpsons artist whose gentle animal comics find humor and tenderness in everyday moments.",
          who_zh: "漫画家、前《辛普森一家》画师，用温柔的动物漫画在日常瞬间里捕捉幽默与柔情。",
          why_fit: "Small, kind, everyday moments drawn with animals — bears and dinosaurs have whole books to themselves — and the same warmth that runs through your interiors. Her readers would recognise yours instantly.",
          why_fit_zh: "她借动物描绘日常里细小而温柔的瞬间——熊和恐龙甚至各自有一本书——那份温暖与你的室内画很相近。她的读者也很可能会喜欢你的作品。",
          link: "https://www.instagram.com/lizclimo/",
          collab_form: "A 'cats and quiet days' themed anthology contribution, or a print collaboration with proceeds to an animal shelter.",
          collab_form_zh: "为“猫与安静的日子”主题合志供稿，或做一次版画联名、收益捐给动物收容所。",
        },
        {
          name: "Mari Andrew",
          who: "Writer-illustrator who built her name on one watercolor diary entry a day about ordinary city life.",
          who_zh: "作家兼插画家，凭借每天一张关于城市日常的水彩手账成名。",
          why_fit: "Her practice is your practice — a daily watercolor diary. You've kept yours since 2020; that consistency is rare and instantly legible to someone who's done the same.",
          why_fit_zh: "她的创作方式就是你的——每日水彩手账。你从2020年坚持至今；这种坚持，同样做过的人一眼就能认出来，也十分难得。",
          link: "https://www.instagram.com/bymariandrew/",
          collab_form: "A daily-diary group zine, or a swapped 'a week in my city' Instagram diary takeover (your Tokyo for her city).",
          collab_form_zh: "一本每日手账合志，或者跟她互换一次“我城市里的一周”Instagram手账更新（你写东京，她写她的城市）。",
        },
        {
          name: "Puuung (퍼엉)",
          who: "Korean illustrator behind the Love Is series. The medium is not watercolour and is not stated publicly; the subject is the one you share — small everyday moments of love at home.",
          who_zh: "韩国插画家，《Love Is》系列的作者。用的是什么材料，没有公开说过；画的却正是你也在画的东西——家里那些微小的爱意瞬间。",
          why_fit: "Domestic stillness, interior light, the tenderness of ordinary rooms — the closest thematic cousin to your work, just with figures where you have cats and quiet.",
          why_fit_zh: "居家的静谧、室内的光、平凡房间里的温柔——主题上离你最近的一位，只是那边画的是人，你画的是猫和安静。",
          link: "https://www.instagram.com/puuung1/",
          collab_form: "A 'small moments of home' print or anthology collaboration pairing those figures with your interiors.",
          collab_form_zh: "一次“家中微小瞬间”的版画或合志联名，把那些人物与你的室内场景并置。",
        },
      ],
    },
    {
      label: "Peers you can actually build with: Tokyo & China-rooted illustrators",
      label_zh: "真的能一起做点东西的同辈：扎根东京与中国的插画家",
      entries: [
        {
          name: "Mateusz Urbanowicz",
          who: "Polish, Tokyo-based watercolourist; his Tokyo Storefronts turned ordinary shops and streets into quiet atmospheric paintings. Published by MdN, with the series past 100,000 copies, and he sells originals himself rather than through a gallery.",
          who_zh: "波兰籍、定居东京的水彩画家；《Tokyo Storefronts》把普通店铺与街道画成安静而有氛围的作品。由 MdN 出版，系列累计超过 10 万册；原作由他自己出售，没有走画廊。",
          why_fit: "Same medium (watercolor), same city (Tokyo), same subject (ordinary urban atmosphere), same ecosystem (self-run shows + book fairs). The most natural two-person-show partner on the map.",
          why_fit_zh: "同样的媒介（水彩）、城市（东京）、题材（普通城市氛围）、生态（自办展览＋书展）。他是整张地图上最自然的双人展搭档。",
          link: "https://www.instagram.com/mateusz_urbanowicz/",
          collab_form: "A two-person Tokyo bookshop-gallery show on 'Tokyo in watercolor', or tabling side by side at an art-book fair.",
          collab_form_zh: "在东京书店画廊办一场“水彩里的东京”双人展，或在艺术书展上并排摆桌。",
        },
        {
          name: "Tatsuro Kiuchi (木内達朗)",
          who: "Tokyo illustrator whose quiet work makes the ordinary feel extraordinary — book jackets, editorial and advertising, including the New York Times and Penguin. He works without an agent; commissions come to him directly.",
          who_zh: "东京插画家，让平凡显得不凡——做书籍封面、编辑与广告插画，包括《纽约时报》和企鹅出版社。他没有经纪人，约稿直接找上门。",
          why_fit: "'Making the ordinary extraordinary' is almost your own artist statement; his calm works-on-paper sensibility sits right next to yours, and he's rooted in the exact Tokyo bookshop circles you want to be in.",
          why_fit_zh: "“让平凡变得不凡”几乎就是你的艺术家自述；他那种平静的纸上作品气质与你非常相近，且深深扎根于你想进入的东京书店圈。",
          link: "https://www.instagram.com/tatsurokiuchi/",
          collab_form: "A quiet-life works-on-paper two-person show, or a shared risograph zine of small daily scenes.",
          collab_form_zh: "一场“安静生活”的纸上作品双人展，或一本以日常小场景为主题的合作riso zine。",
        },
        {
          name: "卤猫 Oamul (Oamul Lu)",
          who: "Chinese illustrator and animator who self-publishes personal art books about people and nature.",
          who_zh: "中国插画家、动画师，自出版关于人与自然的个人画册。",
          why_fit: "A peer connected to your illustration background in China — art-book culture and a steady personal practice — while you are now based in Tokyo. Oamul is already in the self-publishing world you're building toward.",
          why_fit_zh: "她与你有相近的中国插画与画册文化背景，也一直稳定地进行个人创作。她既能连接你在中国与东京的创作经验，也已经身处你想进一步进入的自出版领域。",
          link: "https://www.instagram.com/oamul/",
          collab_form: "A China–Japan illustration art-book or risograph zine swap — two cities, one small book.",
          collab_form_zh: "一本中日插画画册，或一次riso zine互换——两座城市，一本小书。",
        },
      ],
    },
    {
      label: "Your existing seeds: a warm-intro network, not strangers",
      label_zh: "已有的合作种子：可以请熟人引荐的关系网，而不是一群陌生人",
      entries: [
        {
          name: "富大貴 (kuribulb)",
          who: "Co-exhibitor from Tide from China Part1 (Tokyo, 2023); illustrator in watercolour and marker, with the collection オーロラ曲 (2021). Known works include 四季 and 蜥蜴と猫.",
          who_zh: "2023 年在东京和你一起参加过《Tide from China Part1》；用水彩与马克笔创作的插画家，出版过画集《オーロラ曲》（2021）。代表作有《四季》和《蜥蜴と猫》。",
          why_fit: "The warmest, closest match among your seeds — same city, same medium, same love of cats. If any of these five becomes a real collaboration, it's most likely this one.",
          why_fit_zh: "这些人里最暖、最贴近的一个——同城、同媒介，而且你们真的一起展出过。若其中有谁能变成真正的合作，最可能就是他。",
          link: "https://x.com/kuribulb",
          collab_form: "A small two- or three-person cats-and-watercolor show in Tokyo.",
          collab_form_zh: "在东京办一场小型的“猫与水彩”双人或三人展。",
        },
        {
          name: "邦乔彦 (Bang Joy)",
          who: "Co-exhibitor; Hangzhou illustrator with a published illustration collection.",
          who_zh: "同展者；杭州插画家，已出版插画集。",
          why_fit: "A peer who has already made the leap from posting to print — useful company as you move toward your own publishing.",
          why_fit_zh: "一位已从发帖走到出版的同辈——当你迈向自己的出版时，是有用的同行伙伴。",
          link: "https://www.instagram.com/bangjoy1992/",
          collab_form: "A shared zine, or an Instagram print swap.",
          collab_form_zh: "一本合作zine，或一次Instagram版画互换。",
        },
        {
          name: "TUOER (托兒)",
          who: "Co-exhibitor; active illustrator with a sizeable following, sold work through ACG_Labo.",
          who_zh: "同展者；活跃插画家，拥有不小的粉丝量，曾通过ACG_Labo售出作品。",
          why_fit: "Already inside the same ACG_Labo / Tide-from-China network that gave you your first Japan show — a known quantity, not a stranger.",
          why_fit_zh: "已身处那张为你带来首场日本展的ACG_Labo／潮自中国关系网里——是熟面孔，不是陌生人。",
          link: "https://x.com/tuoer_sg",
          collab_form: "An anthology contribution together, or a cross-post collaboration.",
          collab_form_zh: "一起为某本合志供稿，或一次互相转发的联名。",
        },
        {
          name: "Doakmoon",
          who: "Co-exhibitor; illustrator based in Chengdu (also active on Weibo as doakmoon).",
          who_zh: "同展者；成都插画家（亦活跃于微博 doakmoon）。",
          why_fit: "Same first-show cohort; a relationship that already exists and just needs a friendly note to stay warm.",
          why_fit_zh: "你们曾参加同一场日本首展，这段联系已经存在；发一条友好的消息，就能自然地保持往来。",
          link: "https://www.instagram.com/doakdoakyu/",
          collab_form: "A two-city diary zine (Chengdu / Tokyo).",
          collab_form_zh: "一本双城手账zine（成都／东京）。",
        },
      ],
    },
  ],
  how_to: [
    "Start where you already are. Spend a while just being a real reader of their work — a genuine comment, a save, a share. Let your name become familiar before you ask for anything.",
    "Send one short, specific message. Not a pitch: one honest line about a piece of theirs you love, and that you're a watercolor illustrator keeping a daily diary in Tokyo. No ask attached yet.",
    "Propose the smallest possible thing. A print swap, one shared post, a single page in a zine. Small is easy to say yes to — and it's the seed of everything larger.",
    "Lead with your daily diary. Six years of it is your most distinctive gift, not a request. 'I keep a daily watercolor diary' opens more doors than any portfolio.",
    "Let it be slow, and let some fade. Some threads become a show; some quietly don't, and that's completely fine. Collaboration grows from staying in the room, not from closing a deal.",
  ],
  how_to_zh: [
    "从你已经在的地方开始。先花一段时间，只是真心做他们作品的读者——一句真诚的评论、一次收藏、一次转发。在开口提任何请求之前，先让对方对你的名字熟悉起来。",
    "发一条简短而具体的消息。不是推销：只用一句真心话说出你喜欢他们的哪一幅，并说明你是一位在东京坚持每日手账的水彩插画家。先不要附带任何请求。",
    "先提一个尽可能轻量的合作：互换一张版画、共同发一篇帖子，或各为合志画一页。事情越小，对方越容易答应，也更可能成为日后合作的起点。",
    "以你的每日手账开场。六年的坚持是你最独特的礼物，而不是一个请求。“我坚持画每日水彩手账”比任何作品集都更能打开门。",
    "不妨慢慢来，也接受有些联系会自然淡去。有些往来最终会促成展览，有些不会，这都没关系。合作来自长期留在圈子里、持续与人来往，而不是急着谈成一笔交易。",
  ],
};

// ── Collector Ecosystem ────────────────────────────────────────────────────
// Replaces the old "the pipeline tracks opportunities not buyers" non-answer
// (Scott, 2026-06-26) with the real channels collectors of watercolor/illustration
// originals and artist-books actually use, plus a low-pressure how-to. Links
// verified 2026-06-26. zh baked; ja → en.
export const COLLECTOR_ECOSYSTEM = {
  title: "Collector Ecosystem",
  title_zh: "藏家生态",
  title_ja: "コレクター・エコシステム",
  summary: "Where people who buy work like yours actually gather — and gentle ways to be findable.",
  summary_zh: "买你这类作品的人，实际上聚集在哪里——以及让自己被找到的温和方式。",
  summary_ja: "あなたのような作品を買う人が実際に集まる場所と、見つけてもらうための穏やかな方法。",
  intro: "This is not a to-do list and nothing here is urgent. You're already doing the thing that matters most: making the work and sharing it daily. Below are the real places where people who love watercolor originals and artist-books tend to gather, plus a few low-pressure ways to make it easy for the people who already love your work to buy it, if and when you ever feel like it.",
  intro_zh: "这不是任务清单，也没有任何一件事是紧急的。你已经在做最重要的事：持续创作、每天分享。下面是喜欢水彩原作和艺术书的人通常聚集的真实场所，再加上几条低压力的小方法，方便那些已经喜欢你作品的人买到它——只在你想做的时候做就好。",
  channels: [
    {
      name: "Instagram — direct (DM to inquire)",
      name_zh: "Instagram — 私信咨询",
      link: "https://www.instagram.com/gegyjiji/",
      what: "Where people already meet the work, whatever they do next with it. Nothing here has ever measured how many of them buy, so this is a description of where the audience is, not a claim about what it converts to. The people who follow your daily watercolor diary are the audience these formats are made for. It works quietly: someone sees a piece they love, sends a DM, and you reply.",
      what_zh: "这是别人最先遇见你作品的地方。有多少人后来会买，这里从来没统计过，所以下面说的是受众在哪儿，不是它能换来多少订单。关注你每日水彩日记的人，正是这些形式所面向的受众。运作方式很安静：有人看到喜欢的作品，发私信，你回复即可。",
      fit_for_her: "Yes — more than any other channel here. Your audience is already present and engaged. The only gentle, optional addition is making it obvious that inquiries are welcome.",
      fit_for_her_zh: "是的——比这里任何渠道都更现实。你的观众已经在这里、已经在互动。唯一可加的、完全随意的一步，是让大家清楚知道欢迎咨询。",
    },
    {
      name: "BASE — your own shop (you already use this)",
      fee: "6.6% + ¥40 per order (3.0% service + 3.6% + ¥40 payment, Standard plan). Checked 2026-09-08.",
      fee_zh: "每笔订单 6.6% + 40 日元（标准版：3.0% 服务费 + 3.6% + 40 日元支付费）。2026 年 9 月 8 日核实。",
      name_zh: "BASE — 你自己的店铺（你已经在用）",
      link: "https://gegyjiji.base.shop/",
      what: "Your existing storefront on BASE, a free Japanese platform (you only pay a fee when something sells) with built-in Instagram linking. Your shop already handles originals, zines, postcards, and clear SOLD OUT marking well.",
      what_zh: "你在 BASE 上的现有店铺。BASE 是日本的免费开店平台（卖出才收费），并自带 Instagram 链接。你的店铺已经把原作、画册、明信片以及清晰的 SOLD OUT 标记都做得很好。",
      fit_for_her: "Already real and already working. It's your calm buy button so purchasing never depends only on catching you in DMs. Nothing needs to change.",
      fit_for_her_zh: "已经真实存在并已在运作。这是你平静的购买按钮，让购买不必只依赖于在私信里恰好找到你。无需改动。",
    },
    {
      name: "Tokyo Art Book Fair (TABF)",
      name_zh: "东京艺术书展（TABF）",
      link: "https://tokyoartbookfair.com/",
      what: "The biggest art-book and zine fair in Asia by its own description — more than 350 participants and over 20,000 visitors a year — at the Museum of Contemporary Art Tokyo. Its audience is your native ecosystem — people who collect zines, artist books, and printed matter and buy on the spot. Artists apply to exhibit, and the application window is the thing to watch, not the fair: applications for the 2026 edition closed on 7 June 2026, the fair itself runs across January 2027, and the next window opens around mid-2027. Application does not guarantee a booth — it is oversubscribed and selected — and you have to staff the booth yourself throughout.",
      what_zh: "亚洲最大的艺术书与 zine 书展，在东京都现代美术馆举办。来的正是你的读者——会收藏 zine、艺术书和印刷品，而且当场就买的人。艺术家申请参展，而真正要盯的是申请窗口，不是展期本身：2026 年这一届的申请已于 2026 年 6 月 7 日截止，展会在 2027 年 1 月举行，下一个申请窗口大约在 2027 年年中。申请不等于一定有摊位——报名人数超出时会做筛选——而且展期里摊位得你自己守着。",
      fit_for_her: "Very fitting in spirit — your zines are made for exactly this room, and you already exhibit in Tokyo. It's a bigger commitment than an online listing, so it's a someday-if-you-want rather than a today thing.",
      fit_for_her_zh: "气质上很合——你的画册本来就是为这种场合做的，而你人就在东京。只是它比在网上上架费力得多，所以这是哪天你想做时的事，不是今天的事。",
    },
    {
      name: "Creema — Japanese handmade & art marketplace",
      fee: "10.67% including tax, charged on the whole settlement INCLUDING shipping — changed 5 Nov 2025 from 11% excluding shipping, so any older figure understates it. Transfer ¥176–275.",
      fee_zh: "含税 10.67%，按含运费的总金额收。2025 年 11 月 5 日之前是“11%、不含运费”，因为不算运费，实际扣得比现在少，所以网上流传的旧数字偏低。提现费 176–275 日元。",
      name_zh: "Creema — 日本手作与艺术市集",
      link: "https://www.creema.jp/",
      what: "One of Japan's largest creator marketplaces, skewing toward higher unit prices. (A buyer-age breakdown circulates widely online but Creema publishes none, so it is left out here.) You list work; the platform brings the audience.",
      what_zh: "日本规模最大的创作者市集之一，客单价偏高。（关于买家年龄层的说法在网上流传很广，但 Creema 自己从未公布过，所以这里不写。）你上架商品，平台带来观众。",
      fit_for_her: "A natural fit for zines, postcards, and prints, and reasonable for smaller originals. It reaches Japanese buyers who may never find your Instagram. Fully optional and low-effort.",
      fit_for_her_zh: "很适合销售画册、明信片和版画，小幅原作也可以尝试。它能让你接触到一些从未在 Instagram 上发现你的日本买家。是否开店完全由你决定，维护成本也不高。",
    },
    {
      name: "minne — Japan's largest handmade marketplace",
      fee: "10.659% normally, or up to 10.45% on the applicable minne PLUS plan, charged on item + options + shipping. Transfer ¥220.",
      fee_zh: "通常为含税 10.659%；符合条件的 minne PLUS 方案最高为 10.45%，按商品 + 选项 + 运费计算。提现费 220 日元。",
      name_zh: "minne — 日本最大的手作市集",
      link: "https://minne.com/",
      what: "Japan's biggest handmade marketplace, very beginner-friendly to set up, with a broad casual-browsing audience. Strong for accessible price points like postcards and zines.",
      what_zh: "日本最大的手作市集，开店非常适合新手，受众广、随意浏览多。对明信片、画册这类亲民价位尤其有利。",
      fit_for_her: "A gentle, no-commitment option that pairs well with Creema if you ever want a second Japanese storefront for the affordable tier. Not essential — listed so you know it exists.",
      fit_for_her_zh: "一个温和、零承诺的选项，若你想为亲民价位再开一个日本店面，它与 Creema 可以互补。并非必需——列在这里只是让你知道它存在。",
    },
    {
      name: "BOOTH (pixiv) — illustration-community marketplace",
      fee: "5.6% + ¥45 per order — the fixed part rose from ¥22 on 28 Oct 2025. Transfer ¥200–300, or free via PayPal.",
      fee_zh: "每笔订单 5.6% + 45 日元——固定部分于 2025 年 10 月 28 日从 22 日元上调。提现费 200–300 日元，PayPal 免费。",
      name_zh: "BOOTH（pixiv）— 插画社区市集",
      link: "https://booth.pm/en",
      what: "pixiv's creator marketplace — the heart of the illustration community you came up in. Free to open a shop, English interface available, handles both physical goods (zines, prints, postcards) and digital. The audience is illustration-native and used to buying directly from artists.",
      what_zh: "pixiv 的创作者市集——你成长所在的插画社区的核心。免费开店，有英文界面，既能卖实体（画册、版画、明信片）也能卖数字内容。受众本就是插画圈、习惯直接向艺术家购买。",
      fit_for_her: "A good cultural fit given your illustration-community roots. Best for zines, prints, and postcards; most shipping is within Japan. Optional, but it speaks your first language as an artist.",
      fit_for_her_zh: "你本就来自插画社群，因此这里的文化氛围与你很契合。最适合销售画册、版画和明信片；多数配送仅限日本国内。它不是必选项，但很贴近你熟悉的创作语境。",
    },
    {
      name: "Bookshop-gallery consignment (e.g. UTRECHT)",
      name_zh: "书店画廊寄售（例如 UTRECHT）",
      link: "https://utrecht.jp/",
      what: "Tokyo has a small network of art bookshops that stock self-published artist books on consignment — UTRECHT (Shibuya, a co-host of TABF) is the well-known anchor. Utrecht does not publish a consignment policy, so how it works there — and what cut they take — is genuinely unknown; the only trade page they publish is wholesale, which runs the other direction. Asking is the way to find out.",
      what_zh: "东京有一小批艺术书店以寄售方式代销自出版艺术书——UTRECHT（位于涩谷，也是 TABF 的共同主办方）是知名代表。UTRECHT 没有公开寄售规则，所以在他们那里怎么放、抽多少成，其实并不清楚；他们公开的只有一个批发页面，那是他们卖给店家，不是收别人的书。想知道，只能去问。",
      fit_for_her: "A quiet, ambient way for your zines to live in the city without performing or pitching. It's a short, friendly email to ask about their consignment policy — no exhibition, no deadline.",
      fit_for_her_zh: "一种安静自然的方式，让你的画册留在这座城市里，而你无需表演或推销。只需一封简短友好的邮件询问寄售政策——不必办展、没有截止日期。",
    },
  ],
  how_to: [
    { step: "Keep one link in your bio that goes to your shop. Just your gegyjiji.base.shop link in your Instagram bio, so anyone who loves a piece can find where to buy without asking. Highest value, lowest effort.", step_zh: "在简介里放一个指向店铺的链接。只需把 gegyjiji.base.shop 放进 Instagram 简介，让任何喜欢某幅作品的人不必开口就能找到购买入口。价值最高、最省力。" },
    { step: "Add one quiet line: 'DM to inquire about originals.' A single calm sentence in your bio or a pinned post tells people a message is welcome. No catalog, no prices needed — just that the door is open.", step_zh: "加一句安静的话：“原作请私信咨询”。简介或置顶里一句平静的话，就告诉大家欢迎来消息。不需要目录、不需要价格——只是表明门是开着的。" },
    { step: "Let 'sold' and 'available' be visible. You already mark SOLD OUT beautifully on BASE; carrying that same small note to a caption when something sells quietly signals that pieces are real, finite, and collectible — without any urgency.", step_zh: "让“已售”和“在售”可见。你在 BASE 上的 SOLD OUT 标记已经很好；卖出时在配文里加同样的小注脚，就安静地表明作品是真实、有限、可收藏的——毫无紧迫感。" },
    { step: "(Optional) A simple price list, once. A single pinned post or highlight with your four calm tiers — postcards, zines, prints, originals — answers the most common question before it's asked. Easy to skip.", step_zh: "（可选）一份简单的价目表，做一次就好。一条置顶或精选，列出四个平静的档位——明信片、画册、版画、原作——在被问到之前就答好了最常见的问题。跳过也没关系。" },
    { step: "(Optional) A second storefront only if it feels easy. Creema or BOOTH can hold your zines and postcards for buyers who never see your Instagram. Set it up only on a day it feels light — no rush, and no penalty for never doing it.", step_zh: "（可选）只有觉得不费力时，再考虑开第二家店。Creema 或 BOOTH 能让没在 Instagram 上见过你的买家找到你的画册和明信片。哪天有余力再做就好——不用着急，不做也没关系。" },
  ],
};

// ── Press Kit ──────────────────────────────────────────────────────────────
// A ready-to-use press kit generated from her real profile (no fabrication),
// plus a how-to, because the app tells her to "have a press kit ready" but she
// likely doesn't know how to make one (Scott, 2026-06-26). Fields carry {en,zh,
// ja}; accessed by lang directly (not localizeDeep).
export const PRESS_KIT = {
  title: { en: "Your Press Kit", zh: "你的新闻资料包", ja: "あなたのプレスキット" },
  summary: { en: "How to make a press kit — and a ready-to-use draft built from your real details.", zh: "如何做一份新闻资料包——以及一份用你真实信息生成、可直接使用的草稿。", ja: "プレスキットの作り方——そして、あなたの実際の情報から作った、すぐ使える下書き。" },
  intro: { en: "Press, galleries, and brands often ask: 'Do you have a press kit?' It's just a small folder you build once — a bio, an artist statement, a few images, your links — so you can answer in one reply. Below is a ready-to-use draft made entirely from your real details. Copy what's useful; change anything that doesn't sound like you.", zh: "媒体、画廊和品牌常会问：“你有新闻资料包吗？”它其实只是一份做一次就好的小文件夹——简介、艺术家自述、几张图片、你的链接——这样你一条回复就能答上。下面是一份完全用你真实信息生成、可直接使用的草稿。有用的就拿去用；任何不像你的地方，改掉就好。" },
  one_line: {
    en: "GEGYjiji is a Chinese watercolor artist based in Tokyo, painting quiet, atmospheric daily life.",
    zh: "GEGYjiji，常驻东京的中国水彩画家，描绘安静而充满氛围的日常。",
    ja: "GEGYjiji（ゲギジジ）は、東京を拠点に活動する中国出身の水彩画家。静けさと空気感に満ちた日常を描く。",
  },
  short_bio: {
    en: "GEGYjiji is a Chinese watercolor painter based in Tokyo. Originally from Hunan Province, she studied illustration and design at the Beijing Institute of Fashion Technology. Since 2020 she has kept a daily watercolor diary, painting interior light, cats, city corners, and the quiet texture of ordinary life across two countries. Her first solo collection, Colour Diary, appeared in 2021. She has exhibited in China, Japan, and the United Kingdom — including solo shows in Shanghai and Tokyo — and shares her work with an established, growing following on Instagram (@gegyjiji).",
    zh: "GEGYjiji 是一位常驻东京的中国水彩画家。她出生于长沙，在北京服装学院学习插画与设计。自2020年起，她坚持每日水彩日记，描绘室内光线、猫、街角，以及横跨两国的平凡生活肌理。2021年，她出版了首部个人作品集《色彩日記》（Colour Diary）。她曾在中国、日本与英国参展——包括在上海与东京举办的个展——并在 Instagram（@gegyjiji）上与稳定增长的关注者分享作品。",
    ja: "GEGYjijiは、東京を拠点に活動する中国の水彩画家です。湖南省・長沙の出身で、北京服装学院でイラストレーションとデザインを学びました。2020年から毎日の水彩日記を描き続け、室内に差し込む光、猫、街角、二つの国にまたがる何気ない日常の質感を題材としています。2021年には初の個人作品集『Colour Diary（色彩日記）』を刊行。中国・日本・イギリスで作品を発表し、上海と東京では個展も開催しています。Instagram（@gegyjiji）には着実に広がるフォロワーがいます。",
  },
  long_bio: {
    en: "GEGYjiji is a Chinese watercolor artist based in Tokyo. She is from Hunan Province, and she studied illustration and design at the Beijing Institute of Fashion Technology (BIFT), and her practice remains rooted in the illustration and artist-book community as much as in the gallery. Since 2020 she has maintained a daily watercolor diary — a continuous series simply called diary — from which her first solo collection, Colour Diary (2021), grew directly. She paints the ordinary and the overlooked: a street after rain, interior light moving across a room, the particular grey-green of a Tokyo afternoon, and — often — a cat settled in a warm corner. Architecture and the spaces between buildings are where the work is strongest. Working between two cities, her paintings hold China and Japan at once, with watercolor's transparency letting atmosphere and memory accumulate in layers. She has exhibited across China, Japan, and the United Kingdom since 2021, including two museum group exhibitions and three solo shows: Light, Shadow, Cats (Shanghai, 2025), The Eternal Yesterday (Tsuki Gallery, Tokyo, 2026), and Light and Shadows and Cats (Galerie LE MONDE, Harajuku, 2026). She shares the daily practice with about 233,000 follows across X, Weibo, Xiaohongshu, Instagram and Bilibili.",
    zh: "GEGYjiji 是一位常驻东京的中国水彩画家，来自湖南，毕业于北京服装学院（BIFT）插画与设计专业。她的创作既进入画廊，也扎根于插画与艺术书社群。自 2020 年起，她每天以水彩记录生活，并将这个持续至今的系列命名为「diary」；2021 年出版的首部个人作品集《色彩日記》（Colour Diary）也源自这一系列。她描绘寻常而容易被忽略的事物：在房间里移动的光、蜷在温暖角落的猫、雨后的街道，以及东京午后特有的灰绿色。生活往返于两座城市之间，她的画也同时容纳中国与日本的经验；透明的水彩让氛围与记忆一层层沉淀。自 2021 年以来，她在中国、日本与英国举办或参加多场展览，包括两场美术馆群展和三次个展：上海 77ART 的首次个展《和光和影和猫》（2025 年）、东京月画廊的《永遠の昨日》（2026 年），以及东京原宿 Galerie LE MONDE 的《Light and Shadows and Cats》（2026 年）。她的作品曾两次获 Bored Panda 报道；她也持续在 Instagram 上分享每日水彩创作，受众稳步增长。",
    ja: "GEGYjijiは、東京を拠点に活動する中国の水彩画家です。湖南省の出身で、北京服装学院（BIFT）でイラストレーションとデザインを学びました。その制作は、ギャラリーと同じくらい、イラストレーションやアートブックのコミュニティに根ざしています。2020年から、彼女は「diary」と名づけた毎日の水彩日記を描き続けており、2021年の初個人作品集『Colour Diary（色彩日記）』はそこから直接生まれました。描くのは、ありふれた、見過ごされがちな情景です。部屋を移ろう光、暖かな隅でくつろぐ猫、雨上がりの通り、東京の午後特有の灰みがかった緑。二つの都市を行き来しながら、その絵は中国と日本を同時に抱きとめ、水彩の透明感が空気と記憶を幾層にも重ねていきます。2021年以降、中国・日本・イギリスで作品を発表してきました。二つの美術館でのグループ展のほか、三度の個展があります——上海での初個展『和光和影和猫』（2025年）、東京・月画廊での個展『永遠の昨日』（2026年）、そして東京・原宿の Galerie LE MONDE での個展『Light and Shadows and Cats』（2026年）。作品はBored Pandaに二度取り上げられ、Instagramでは毎日の水彩制作を、着実に広がるフォロワーと分かち合っています。",
  },
  statement: {
    en: "I paint the ordinary. Since 2020 I have kept a daily watercolor diary — small studies of the places I move through, made the way you might write a single sentence at the end of a day. My subjects are quiet ones: light falling through a window, a cat asleep on a warm floor, a street corner after rain, the grey-green hour particular to Tokyo. I am Chinese, and I live between Beijing and Tokyo, so my work holds two cities at once — red walls and alleyways, pools and green ponds, rooms I half-remember. Watercolor suits this slow looking; its transparency lets atmosphere accumulate in layers, the way memory does. Like a train traveling through the north, the paintings carry all four seasons. I want the viewer to feel they are walking through somewhere familiar — to find an ordinary day turned, for a moment, into something worth keeping.",
    zh: "我画寻常之物。自2020年起，我每天画一幅小小的水彩，像写日记一样持续着——就像在一天结束时写下一句话。我的题材都很安静：穿过窗子的光、睡在暖和地板上的猫、雨后的街角、东京特有的那种灰绿色的时刻。我是中国人，往返于北京与东京之间，所以我的画同时容纳着两座城市——红墙与巷弄，水池与绿塘，我依稀记得的房间。水彩适合这种缓慢的观看：它的透明让氛围像记忆一样层层累积。像一列穿行于北国的火车，画里装着春夏秋冬。我希望观者觉得自己正走过一个熟悉的地方——也希望一个平凡的日子，能在某个瞬间成为值得珍藏的记忆。",
    ja: "わたしは、ありふれたものを描いています。2020年から、毎日小さな水彩を描き、日記のように続けてきました。一日の終わりに一文を書きとめるように。題材は静かなものばかりです。窓から差し込む光、暖かな床で眠る猫、雨上がりの街角、東京特有の灰みがかった緑の時間。わたしは中国の人間で、北京と東京のあいだで暮らしています。だから絵は、二つの街を同時に抱いています。赤い壁と路地、プールと緑の池、半ば憶えている部屋。水彩は、このゆっくりとした観察によく合います。その透明感が、記憶のように、空気を幾層にも積み重ねていくからです。北国を旅する列車のように、絵は春夏秋冬を運びます。見る人に、見覚えのある場所を歩いているように感じてほしい。ありふれた一日が、ほんの一瞬、とっておきの何かに変わる——その瞬間を。",
  },
  fact_sheet: {
    en: [
      "Name / Handle: GEGYjiji (GEGY挤挤) · Instagram @gegyjiji",
      "Based: Tokyo, Japan",
      "From: Hunan Province, China",
      "Medium: Watercolor (primary); occasional ink",
      "Education: Beijing Institute of Fashion Technology (北京服装学院 / BIFT) — illustration and design",
      "Languages: Chinese (native) · Japanese (JLPT N2)",
      "Selected exhibitions: Light and Shadows and Cats (solo, Galerie LE MONDE, Harajuku, Tokyo, Aug–Sep 2026); The Eternal Yesterday (solo, Tsuki Gallery, Tokyo, 2026); MiniArt, GrandStar (group, Tsuki Gallery, Tokyo, 2026); Scribbles Winter Wonderland (London, UK, Dec 2025, first international showing); Light, Shadow, Cats (solo, 77ART, Shanghai, 2025, first solo); PiPa – The Sound of Growing (group, Hengdu Art Museum, Taizhou, 2024–25); Living Elsewhere (group, Mian Art Museum, Tianjin, 2024–25); Tide from China Part 1 (group, ACG_Labo, Tokyo, 2023, first in Japan); The Recorded Journey (group, Whale Zihao bookstore, Shanghai, 2021)",
      "Publications: Colour Diary (色彩日記), first solo collection, 2021; contributor, defined Definition 02: A Documented Journey",
      "Audience: about 233,000 follows across five accounts — X @GegYjiji (89.3k), Weibo (65k), Xiaohongshu (44k), Instagram @gegyjiji (27k), Bilibili (7.5k)",
      "Press: work picked up by Bored Panda (twice) and Design You Trust — image features rather than interviews",
      "Links / Contact: Instagram @gegyjiji (preferred contact) · Shop gegyjiji.base.shop",
    ],
    zh: [
      "姓名 / 账号：GEGYjiji（GEGY挤挤）· Instagram @gegyjiji",
      "常驻地：日本东京",
      "出生地：中国湖南长沙",
      "媒介：水彩（主要）；偶用水墨",
      "教育：北京服装学院（BIFT）——插画与设计",
      "语言：中文（母语）· 日语（JLPT N2）",
      "精选展览：《Light and Shadows and Cats》（个展，Galerie LE MONDE，东京原宿，2026 年 8–9 月）；《永遠の昨日》（个展，月画廊，东京，2026）；《MiniArt, GrandStar》（群展，月画廊，东京，2026）；《Scribbles Winter Wonderland》（伦敦，英国，2025 年 12 月，首次海外参展）；《和光和影和猫》（个展，77ART，上海，2025，首次个展）；《PiPa 生长的声音》（群展，横渡美术馆，台州，2024–25）；《生活在别处》（群展，棉美术馆，天津，2024–25）；《Tide from China Part 1》（群展，ACG_Labo，东京，2023，首次在日本参展）；《被记录的旅行》（群展，鲸字号本屋，上海，2021）",
      "出版物：《色彩日記》（Colour Diary），首部个人作品集，2021；参与《defined Definition 02: A Documented Journey》",
      "受众：五个账号合计约 23.3 万关注——X @GegYjiji（8.93 万）、微博（6.5 万）、小红书（4.4 万）、Instagram @gegyjiji（2.7 万）、B 站（7,500）",
      "媒体报道：作品被 Bored Panda（两次）与 Design You Trust 收录——是图片专题，不是访谈",
      "链接 / 联系：Instagram @gegyjiji（首选联系方式）· 店铺 gegyjiji.base.shop",
    ],
    ja: [
      "名前 / アカウント：GEGYjiji（GEGY挤挤）· Instagram @gegyjiji",
      "拠点：日本・東京",
      "出身：中国湖南省",
      "媒体：水彩（主）／ときに墨",
      "学歴：北京服装学院（BIFT）── イラストレーション・デザイン",
      "言語：中国語（母語）· 日本語（JLPT N2）",
      "主な展覧会：『Light and Shadows and Cats』（個展、Galerie LE MONDE、東京・原宿、2026年8〜9月）；『永遠の昨日』（個展、月画廊、東京、2026）；『MiniArt, GrandStar』（グループ展、月画廊、東京、2026）；ロンドン（イギリス、2025、初の海外発表）；『和光和影和猫』（個展、77ART、上海、2025、初個展）；『PiPa 生长的声音』（グループ展、横渡美術館、台州、2024–25）；『生活在别处』（グループ展、棉美術館、天津、2024–25）；『Tide from China Part 1』（グループ展、ACG_Labo、東京、2023、日本での初発表）；『被记录的旅行』（グループ展、鲸字号本屋、上海、2021）",
      "刊行物：『Colour Diary（色彩日記）』初の個人作品集、2021；『defined Definition 02: A Documented Journey』に参加",
      "オーディエンス：5つのアカウント合計で約233,000フォロー——X @GegYjiji（8.93万）、Weibo（6.5万）、小紅書（4.4万）、Instagram @gegyjiji（2.7万）、Bilibili（7,500）",
      "メディア掲載：Bored Panda（2回）と Design You Trust に作品が取り上げられた（インタビューではなく画像特集）",
      "リンク / 連絡先：Instagram @gegyjiji（連絡はこちらが希望）· ショップ gegyjiji.base.shop",
    ],
  },
  selected_works: {
    en: [
      "Tokyo Still Life — Interiors, cats, and light through windows: the quiet architecture of daily life in a Tokyo apartment and neighborhood. Stillness as the subject itself.",
      "Urban Atmosphere — Streetscapes, corners, rain-wet pavement, and the particular grey-green light of Tokyo. Place treated as an emotional subject rather than a backdrop.",
      "Memory and Distance — Work that holds both China (Changsha, her origin) and Japan (Tokyo, her present) — the feeling of living between two cities, two languages, and two versions of ordinary life.",
    ],
    zh: [
      "东京静物（Tokyo Still Life）——室内、猫与穿窗而入的光：从东京公寓和街区的日常空间中，描绘生活安静的结构。以“静”本身为题。",
      "都市氛围（Urban Atmosphere）—— 街景、街角、雨湿的路面，以及东京特有的灰绿色光。把“地点”当作情感主体，而非背景。",
      "记忆与距离（Memory and Distance）—— 同时承载中国（长沙，原乡）与日本（东京，当下）的作品——身处两座城市、两种语言、两种平凡生活之间的感受。",
    ],
    ja: [
      "Tokyo Still Life（東京静物）── 室内、猫、窓越しの光。東京の部屋と街にある、日常の静かな建築。「静けさ」そのものを主題に。",
      "Urban Atmosphere（都市の空気）── 街並み、街角、雨に濡れた舗道、東京特有の灰みがかった緑の光。場所を、背景ではなく感情の主体として描く。",
      "Memory and Distance（記憶と距離）── 中国（長沙＝出自）と日本（東京＝現在）の両方を抱える作品。二つの都市、二つの言語、二つの「ふつうの暮らし」のあいだに生きる感覚。",
    ],
  },
  image_guidance: {
    en: [
      "Aim for 8–10 images that show range without repeating yourself.",
      "1 artist photo — you working, or a calm portrait (optional but warm; credit the photographer if there is one).",
      "1 signature work from each body — one Tokyo Still Life, one Urban Atmosphere, one Memory and Distance.",
      "A spread of paintings — e.g. a cat interior, a window-light interior, a rain-wet street; vary mood and palette.",
      "1 exhibition / installation photo — a wall from a recent show (e.g. The Eternal Yesterday at Tsuki Gallery) if you have one.",
      "1 page or spread from Colour Diary or your daily diary — shows the practice behind the work.",
      "1 detail shot — a close crop showing watercolor texture and edges; useful for print.",
      "Caption + credit template: Title (year). Watercolor on paper, height × width cm. © GEGYjiji.",
      "Name files clearly (e.g. gegyjiji_tokyo-still-life_01.jpg); send high-res JPEGs only when print is requested, otherwise web-sized.",
    ],
    zh: [
      "目标是 8–10 张能展现广度、彼此不重复的图片。",
      "1 张本人照片 —— 工作中的你或一张安静的肖像（可选，但有温度；如有摄影师请署名）。",
      "三大系列各一张代表作 —— 各取一张《东京静物》《都市氛围》《记忆与距离》。",
      "选几幅不同的画作——例如猫所在的室内、窗边光影和雨后街道；让情绪与色调有所变化。",
      "1 张展览 / 布展照片 —— 近期展览的一面墙（例如月画廊《永遠の昨日》），若有的话。",
      "《色彩日記》或每日 diary 的一页 / 跨页 —— 展现作品背后的日常实践。",
      "1 张细节图 —— 显示水彩肌理与边缘的近景特写，对印刷很有用。",
      "图注 + 署名模板：《作品名》（年份）。纸本水彩，高 × 宽 厘米。© GEGYjiji。",
      "文件命名清晰（例如 gegyjiji_tokyo-still-life_01.jpg）；仅在对方需要印刷时发高分辨率 JPEG，否则用网页尺寸。",
    ],
    ja: [
      "重複を避け、幅を見せる 8〜10枚を目安に。",
      "本人写真を1枚 —— 制作中の姿または静かなポートレート（任意・温かみあり。撮影者がいればクレジット）。",
      "3つのシリーズから代表作を各1枚 —— Tokyo Still Life / Urban Atmosphere / Memory and Distance。",
      "作品を数点 —— 例：猫のいる室内、窓の光の室内、雨の街。気分とパレットに変化を。",
      "展示風景を1枚 —— 近作展のひと壁（例：月画廊『永遠の昨日』）があれば。",
      "Colour Diary または毎日の diary の1ページ／見開き —— 作品の背後にある実践が伝わる。",
      "ディテール写真を1枚 —— 水彩の質感や滲みが見える接写。印刷に役立つ。",
      "キャプション＋クレジットの型：『作品名』（年）。紙に水彩、高さ × 幅 cm。© GEGYjiji。",
      "ファイル名は分かりやすく（例：gegyjiji_tokyo-still-life_01.jpg）。高解像度JPEGは印刷時のみ、それ以外はウェブ用サイズで。",
    ],
  },
  press: [
    { outlet: "Bored Panda", type: "Watercolor image feature", url: "https://www.boredpanda.com/watercolor-paintings-cats-nature-city-gegyjiji/" },
    { outlet: "Bored Panda", type: "Watercolor image feature, part 2", url: "https://www.boredpanda.com/watercolor-paintings-cats-nature-city-gegyjiji-part-2/" },
    { outlet: "Design You Trust", type: "Short image feature, Aug 2024", url: "https://designyoutrust.com/2024/08/chinese-artist-captures-the-quiet-solitude-of-modern-life-through-delicate-watercolor-art/" },
  ],
  how_to_use: {
    en: [
      "Keep it ready. Save it as a PDF (and keep the editable file). When someone asks 'do you have a press kit?', you reply and attach it — nothing new to write in the moment.",
      "Pick the language and the length. Send the Japanese version to Japanese press and galleries, Chinese as your default, English for international. Most people only need the short bio + fact sheet + a few images.",
      "Attach 3–5 images, not the whole portfolio. Choose the strongest works for that reader (cats-and-interiors → Tokyo Still Life; city/architecture → Urban Atmosphere). Use the caption format so credits travel with the files.",
      "Add one warm line of your own. A single personal sentence — 'I loved your recent feature on ___ and thought my work might suit it' — makes it human. Then send.",
    ],
    zh: [
      "随时备好。把它存成 PDF（并保留可编辑源文件）。当对方问“你有新闻资料包吗？”时，你回复并附上即可，当下无需再写。",
      "选择语言与篇幅。日文版发给日本媒体与画廊，中文版作为默认，英文版用于海外。多数人只需要短简介 + 资料速览 + 几张图片。",
      "附 3–5 张图，而非整个作品集。为对方挑选最合适的作品（猫与室内 → 东京静物；城市/建筑 → 都市氛围）。使用图注格式，让署名随文件传递。",
      "加一句你自己的暖心话。一句私人化的话——“我很喜欢你们最近关于 ___ 的报道，觉得我的作品也许合适”——会让它有人情味。然后发送即可。",
    ],
  },
  how_to_update: {
    en: [
      "After each show or publication, add one line to Selected Exhibitions / Publications (newest first). Two minutes.",
      "Refresh the artist statement only when your work genuinely shifts — not on a schedule.",
      "Swap in newer images as you make stronger work; quietly retire older ones.",
      "Leave the audience line as 'established, growing' — no need to chase a number.",
      "Re-export the PDF whenever you change something, and keep one master file so there's only ever one true version.",
    ],
    zh: [
      "每办一次展或出版一部作品，就在“精选展览／出版物”中补上一行，并把最新的放在最前面；两分钟就能完成。",
      "艺术家自述只在创作真正转向时更新——不必按时间表来。",
      "有更强的新作就替换新图，悄悄淘汰旧的。",
      "受众那行随时可以更新，也可以整行删掉——那是给对方看的参考，不是你要去追的指标。",
      "每次改动后重新导出 PDF，并只保留一份主文件，确保始终只有一个真实版本。",
    ],
  },
};
