// Strategy ladders — prototype content.
//
// Hand-authored and deliberately temporary. The engine that should own this is
// specced in docs/NEXT_PHASE_strategies.md and is not built. It lives in its own
// file so that when the engine arrives there is one thing to delete.
//
// FORMAT (Scott, 2026-09-08): these follow the existing career pathway — a
// sequence of PROGRESSIVE STATES, from "First publication" to "Gallery
// representation", not a list of chores. A rung names something she has reached
// or will reach; the detail underneath carries the evidence, with her real work
// named. The first draft of this file was tasks ("Something between ¥2,200 and
// ¥31,900"), which is a to-do list wearing a ladder's clothes.
//
// Each ladder ends in a TERMINAL state that is the goal itself, so the shape of
// the climb is visible from the top rung down.
//
// Third person throughout, per the rule recurring_calendar_engine documents.
// (Note: StrategicPathway's own details are still second person — "your CV" —
// which is an unfixed remnant, not the standard.)

const T = (en, zh, ja) => ({ en, zh, ja })

export const STATES = {
  // ── gallery ────────────────────────────────────────────────────────────────
  g_publication: {
    label: T('First publication', '第一本出版物', '最初の出版'),
    detail: T('Colour Diary (2021), grown out of the daily diary practice. The publishing half of the CV is established.',
              '《色彩日记》（2021），从每日日记的实践里长出来。履历里出版的那一半已经成立。',
              '『色彩日記』（2021）、日々の日記から育ったもの。経歴の出版側はすでに成立している。'),
  },
  g_group: {
    label: T('Group shows across China and Japan', '中国与日本的联展', '中国と日本でのグループ展'),
    detail: T('8 confirmed, from Shanghai and Guangzhou to Tokyo — a real exhibition history rather than a first outing.',
              '已确认 8 场，从上海、广州到东京——是一段真正的展览史，而不是一次初登场。',
              '確認済み8件、上海・広州から東京まで。初出演ではなく、実際の展示歴。'),
  },
  g_institutional: {
    label: T('Museum and institutional exhibitions', '美术馆与机构展览', '美術館・機関での展示'),
    detail: T('Mian Art Museum in Tianjin and Hengdu Art Museum in Taizhou. Institutions vouch in a way a commercial room cannot — they have no stock to sell.',
              '天津的缅艺术馆与台州的横渡美术馆。机构的背书是商业空间给不了的：它们没有货要卖。',
              '天津の緬芸術館、台州の横渡美術館。機関の裏書きは商業空間には出せない。売る在庫がないから。'),
  },
  g_solo: {
    label: T('Solo shows, including in Tokyo', '个展，包括在东京', '個展、東京を含む'),
    detail: T('Three on record, most recently Light and Shadows and Cats at Galerie LE MONDE in Harajuku, closed 6 September 2026. The work has carried a room alone.',
              '记录中有三场，最近一次是原宿 Galerie LE MONDE 的《光与影与猫》，2026 年 9 月 6 日结束。作品已经能独自撑起一个空间。',
              '記録上3件。直近は原宿ギャルリー・ル・モンドの「光と影と猫」、2026年9月6日終了。作品はすでに空間を単独で支えている。'),
  },
  g_international: {
    label: T('First international showing', '第一次国际展出', '最初の海外展示'),
    detail: T('A London showing in December 2025 took the work beyond China and Japan — the start of an international record.',
              '2025 年 12 月的伦敦展出，把作品带出了中国和日本——国际记录由此开始。',
              '2025年12月のロンドンでの展示が、作品を中国と日本の外へ運んだ。国際的な記録の始まり。'),
  },
  g_press: {
    label: T('Written about, rather than reproduced', '被评论，而不只是被转载', '掲載ではなく、論じられる'),
    detail: T('Three features on record — Bored Panda twice, Design You Trust once. All reproduce the pictures; none makes an argument about them, and criticism is what a curator can cite.',
              '记录中有三篇报道——Bored Panda 两次，Design You Trust 一次。都是把图放上去，没有一篇在论述；而策展人能引用的，恰恰是论述。',
              '記録上3件——Bored Panda 2回、Design You Trust 1回。いずれも絵を並べただけで、論じてはいない。学芸員が引けるのは批評のほう。'),
  },
  g_representation: {
    label: T('A gallery that sells on her behalf', '一家代理她销售的画廊', '代わりに売ってくれる画廊'),
    detail: T('The largest structural step available now, and it grows from the shows already on record. Representation moves the price of a single painting, not only the number sold, because a gallery introduces collectors it intends to keep.',
              '目前可走的最大一步，而且是从已有的展览记录里长出来的。代理抬的是单张画的价格，不只是卖出的张数——因为画廊介绍的是它打算长期留住的藏家。',
              '今とりうる最も大きな構造的な一歩で、すでにある展示歴から育つもの。代理が動かすのは売れた枚数ではなく一点の価格。画廊が紹介するのは長く付き合うつもりの相手だから。'),
  },
  g_fairs: {
    label: T('Stronger solo venues and art fairs', '更强的个展场地与艺博会', 'より強い個展会場とアートフェア'),
    detail: T('Established commercial galleries, institutional solos, and the fairs where collectors gather — Art Fair Tokyo, Tokyo Gendai. Usually reached through a representing gallery rather than before one.',
              '成熟的商业画廊、机构个展，以及藏家聚集的艺博会——东京艺术博览会、Tokyo Gendai。通常是通过代理画廊到达，而不是在那之前。',
              '確立した商業画廊、機関での個展、そしてコレクターの集まるフェア——アートフェア東京、Tokyo Gendai。多くは代理画廊を通じて届く場所で、その前ではない。'),
  },

  // ── audience ───────────────────────────────────────────────────────────────
  a_cadence: {
    label: T('A daily practice that does not stop', '不停下来的每日实践', '途切れない日々の実践'),
    detail: T('A watercolour diary kept daily since 2020. Everything further up this ladder assumes a steady supply of work, and this is the rung most practices never clear.',
              '自 2020 年起每天不断的水彩日记。这条阶梯往上的一切都建立在稳定的作品产出之上，而这一级是多数创作者始终没跨过的。',
              '2020年から毎日続く水彩の日記。この梯子の上にあるものはすべて安定した制作を前提にしており、多くの実践が越えられないのがここ。'),
  },
  a_look: {
    label: T('A look recognisable at thumbnail size', '缩略图大小也认得出的面貌', 'サムネイルでもわかる佇まい'),
    detail: T('Urban architecture, interior light, watercolour transparency — consistent for six years. In a feed, recognition happens before the name is read, so the look has to work alone.',
              '城市建筑、室内光线、水彩的透明感——已经稳定了六年。在信息流里，认出来发生在读到名字之前，所以那种面貌必须自己撑住。',
              '都市の建築、室内の光、水彩の透明感——六年間一貫している。流れの中では名前を読む前に見分けがつく。だから佇まいが単独で働かねばならない。'),
  },
  a_found: {
    label: T('An audience that found her', '一群自己找上来的读者', '自ら見つけてくれた観客'),
    detail: T('About 26,000 on the daily-diary account, built without advertising. That is an audience, and it is the base the rest of this ladder multiplies.',
              '每日日记账号上大约 26,000 人，没有投过广告。这已经是一群受众，也是这条阶梯往上乘算的基数。',
              '日記アカウントに約26,000人、広告なしで積み上がったもの。すでに観客であり、この先が掛かる土台。'),
  },
  a_series: {
    label: T('Work that continues rather than accumulates', '会延续的作品，而不是堆积的作品', '積み上がるのではなく、続いていく仕事'),
    detail: T('A diary is watched; a named, numbered, continuing series is followed, because it gives a reason to come back for the next one. Six years of work with no named body inside it.',
              '日记是被看的；一个有名字、有编号、还在继续的系列是被追的——因为它给人回来看下一张的理由。六年的作品里，还没有一个被命名的系列。',
              '日記は見られ、名前と番号があり続いていく連作は追われる。次を見に戻る理由になるから。六年分の仕事の中に、名前のついたまとまりがない。'),
  },
  a_motion: {
    label: T('The work seen in motion', '被看见的作画过程', '動いているところを見せる'),
    detail: T('Watercolour spreading is one of the few things a still image cannot show. It costs no extra painting — the camera watches work already being done.',
              '水彩在纸上化开，是静止图像拍不到的少数东西之一。它不需要多画一张——镜头拍的是本来就在做的事。',
              '水彩がにじむ瞬間は静止画では見せられない数少ないもの。余分に描く必要はない。カメラはすでにしている仕事を見ているだけ。'),
  },
  a_borrowed: {
    label: T('Appearing inside other audiences', '出现在别人的受众里', '他の人の観客の中に現れる'),
    detail: T('The fastest growth is borrowed rather than built — a shared zine, a two-person show, a trade of features. Twelve artists working in adjacent territory are already mapped; none approached.',
              '增长最快的方式是借来的，而不是攒出来的——一本合印的 zine、一个双人展、互相介绍。已经梳理出十二位在相邻领域创作的艺术家，尚未接触任何一位。',
              'いちばん速いのは積み上げるより借りること——合同のzine、二人展、相互の紹介。隣接する領域の作家十二名がすでに把握されているが、誰にも声はかけていない。'),
  },
  a_second: {
    label: T('A second audience somewhere else', '在别处的第二群受众', '別の場所にもう一つの観客'),
    detail: T('Architecture and light need no translation, and the paintings already exist. Almost all of the audience currently sits on one platform.',
              '建筑和光不需要翻译，而画已经画好了。目前几乎全部受众都集中在一个平台上。',
              '建築と光に翻訳はいらず、絵はすでにある。いまは観客のほぼすべてが一つの場所にいる。'),
  },
  a_inbound: {
    label: T('An audience that arrives without being asked', '不用去找、自己会来的受众', '呼ばなくても集まる観客'),
    detail: T('The state the rest of this ladder is for. At scale a print run stops being a gamble — her best route breaks even at 109 copies, which is one follower in 240 today and one in 4,600 at half a million.',
              '这条阶梯上其余的一切，都是为了到达这个状态。到了这个规模，印一版书不再是赌博——她最好的印制方案 109 本回本，按今天的受众是 240 人里有 1 人，到五十万时是 4,600 人里有 1 人。',
              'この梯子の残りすべてが向かう状態。規模がつけば印刷は賭けでなくなる。最良の経路は109部で採算が合い、今なら240人に1人、50万人なら4,600人に1人。'),
  },

  // ── licensing ──────────────────────────────────────────────────────────────
  l_reproduces: {
    label: T('A subject that survives reproduction', '经得起复制的题材', '複製に耐える主題'),
    detail: T('Watercolour architecture and interior light hold up printed small and in quantity, and they suit the categories licensing actually buys — stationery, calendars, covers, interiors.',
              '水彩的建筑与室内光线，缩小、量产地印出来依然成立，也正好落在授权真正会买的品类里——文具、日历、书封、室内。',
              '水彩の建築と室内の光は、小さく大量に刷っても崩れない。しかもライセンスが実際に買う分野——文具、カレンダー、装画、インテリア——に合っている。'),
  },
  l_inprint: {
    label: T('Work already in print', '已经印出来的作品', 'すでに印刷されている仕事'),
    detail: T('Eight zines and two publications. A commissioner can see the work has been through production before, which is a different question from whether it is good.',
              '八本 zine，两本出版物。委托方能看到这些作品已经走过一次生产流程——这和作品好不好，是两个问题。',
              'zineが8冊、出版が2件。発注側は、この仕事がすでに製造を通っていることを確認できる。良し悪しとは別の問い。'),
  },
  l_lookbook: {
    label: T('A portfolio that can be sent the same day', '当天就能发出去的作品集', 'その日のうちに送れる作品集'),
    detail: T('Ten to twenty works shown as product mockups, one PDF. An art director cannot picture a painting on a notebook cover; a mockup does it for them. Nothing in her record is one.',
              '十到二十件作品做成产品效果图，一份 PDF。美术总监没法凭空想象一张画印在笔记本封面上是什么样，效果图替他想。她的记录里还没有这样一份东西。',
              '作品10〜20点を製品モックアップにしたPDF一つ。アートディレクターは絵がノートの表紙にのった姿を想像できない。モックアップがそれを代わりにする。記録の中にそれはまだない。'),
  },
  l_findable: {
    label: T('Listed where commissioners search', '出现在委托方检索的地方', '発注側が検索する場所に載る'),
    detail: T('Licensing is mostly inbound, so being on the files and libraries art directors search is the difference between pitching and being found. Not listed on any of the four routes the app has verified.',
              '授权大多是对方找上门，所以出现在美术总监会检索的档案库和图库里，就是「主动去投」和「被找到」之间的差别。应用已核实的四条渠道里，都还没有登记。',
              'ライセンスの多くは向こうから来る。だからアートディレクターが検索するファイルやライブラリに載っているかが、売り込むか見つけられるかの差。確認済みの四つの経路のいずれにも登録がない。'),
  },
  l_first: {
    label: T('A first paid usage', '第一笔付费授权', '最初の有償利用'),
    detail: T('Worth more as a precedent than as money: a published rate to quote and a client who can be asked again. Magazine illustration starts around ¥5,000, a book cover around ¥70,000.',
              '它作为先例，比作为收入更值钱：一个可以引用的价格，和一个可以再问一次的客户。杂志插图大约从 5,000 日元起，书封大约 70,000 日元。',
              '金額より前例として価値がある。提示できる相場と、もう一度声をかけられる相手。雑誌のイラストは5,000円前後から、装画は70,000円ほど。'),
  },
  l_repeat: {
    label: T('Repeat clients and a rate she sets', '回头客，和一个由她定的价', 'リピートの相手と、自分で決める料率'),
    detail: T('One licence is a job; three from the same category is a rate. Published Japanese figures run to ¥100,000 for a magazine cover and ¥800,000 for a calendar, with copyright transfer priced at two to three times a normal licence.',
              '一笔授权是一份工作；同一品类里的三笔，就是一个价位。日本已公开的价格，杂志封面到 100,000 日元，日历到 800,000 日元，而买断版权的定价是普通授权的两到三倍。',
              '一件は仕事、同じ分野で三件なら相場になる。公開されている日本の数字では雑誌の表紙で10万円、カレンダーで80万円、著作権譲渡は通常の2〜3倍。'),
  },
  l_inbound: {
    label: T('Brands arriving unprompted', '品牌自己找上门', 'ブランドから声がかかる'),
    detail: T('The state this ladder is for. Hobonichi hand-picks illustrators whose work has a distinct voice rather than reading submissions — at this end of the ladder she is found rather than pitching.',
              '这条阶梯要到达的状态。ほぼ日是自己去挑面貌鲜明的插画师，而不是看投稿——走到这一端，是被找到，而不是去投。',
              'この梯子が向かう状態。ほぼ日は投稿を読むのではなく、はっきりした個性を持つ作家を自ら選ぶ。この端に立てば、売り込むのではなく見つけられる。'),
  },
}

// A goal is a name plus an ORDER of states. `why` overrides the detail where a
// shared state earns its place for a different reason in this ladder.
export const GOALS = [
  {
    id: 'gallery_success',
    name: T('Gallery success', '画廊这条路', '画廊での成功'),
    ladder: ['g_publication', 'g_group', 'g_institutional', 'g_solo',
             'g_international', 'g_press', 'g_representation', 'g_fairs'],
    why: {},
  },
  {
    id: 'a_following',
    name: T('A following', '一群固定的读者', '見てくれる人たち'),
    ladder: ['a_cadence', 'a_look', 'a_found', 'a_series',
             'a_motion', 'a_borrowed', 'a_second', 'a_inbound'],
    why: {},
  },
  {
    id: 'intl_licensing',
    name: T('International licensing', '国际授权', '海外のライセンス'),
    ladder: ['l_reproduces', 'a_look', 'l_inprint', 'a_series',
             'l_lookbook', 'l_findable', 'l_first', 'l_repeat', 'l_inbound'],
    why: {
      a_look: T('Brands license a look they can put across a product line, so it has to survive being reproduced small and in quantity — the same consistency that earns recognition in a feed.',
                '品牌买的是一种能铺成产品线的面貌，所以它必须经得起被缩小、被大量复制——和在信息流里被认出来，靠的是同一种稳定。',
                'ブランドが買うのは製品ラインに展開できる佇まい。小さく大量に複製されても崩れないこと——流れの中で見分けられるのと同じ一貫性。'),
      a_series: T('A range needs several related pieces at once, so a named series licenses more easily than a strong single image.',
                  '一个产品系列一次要用好几件相关的作品，所以有名字的系列，比一张强的单图更容易授权。',
                  'シリーズ商品は関連する複数点を一度に必要とする。だから名前のある連作は、強い一点より通しやすい。'),
    },
  },
]

// Which OTHER goals a state also belongs to. Derived from the ladders, so it can
// never disagree with them.
export const alsoServes = (stateId, goalId) =>
  GOALS.filter((g) => g.id !== goalId && g.ladder.includes(stateId))

// Reached-ness reads her live record. Anything the system genuinely cannot see
// returns false rather than guessing — an unearned tick is worse than a blank rung.
export function evidence(data, careerData) {
  const ev = careerData?.career_evidence || {}
  const shows = (data?.career_position?.exhibitions || []).length
  return {
    g_publication: (ev.publications_confirmed || 0) > 0,
    g_group: (ev.confirmed_group_shows || 0) >= 3,
    g_institutional: !!ev.has_institutional_show,
    g_solo: !!ev.has_solo_show,
    g_international: !!ev.has_international_show,
    g_press: false,
    g_representation: !!ev.has_representation,
    g_fairs: false,

    a_cadence: true,
    a_look: shows > 0,
    a_found: true,
    a_series: false,
    a_motion: false,
    a_borrowed: false,
    a_second: false,
    a_inbound: false,

    l_reproduces: true,
    l_inprint: (ev.publications_confirmed || 0) > 0,
    l_lookbook: false,
    l_findable: false,
    l_first: false,
    l_repeat: false,
    l_inbound: false,
  }
}
