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
// SECOND person (Scott, 2026-09-08). recurring_calendar_engine's docstring says
// third — "the page describes; it does not talk to anyone" — but the rest of this
// page speaks to her directly, and describing someone in the third person to
// their face reads as a case file. Second person here is still descriptive, not
// instructive: "you have about 27,000 followers" states a fact.

// UI is Chinese and English only — LANGUAGES is ['zh','en'], so a `ja` string
// here could never render. Japanese belongs in the outreach email engines,
// which write to Japanese venues, and nowhere in this app's interface.
const T = (en, zh) => ({ en, zh })

export const STATES = {
  // ── gallery ────────────────────────────────────────────────────────────────
  g_publication: {
    label: T('First publication', '第一本出版物'),
    detail: T('Colour Diary (2021), grown out of the daily diary practice. The publishing half of the CV is established.', '《色彩日记》（2021），从每日日记的实践里长出来。履历里出版的那一半已经成立。'),
  },
  g_group: {
    label: T('Group shows across China and Japan', '中国与日本的联展'),
    detail: T('8 confirmed, from Shanghai and Guangzhou to Tokyo — a real exhibition history rather than a first outing.', '已确认 8 场，从上海、广州到东京——是一段真正的展览史，而不是一次初登场。'),
  },
  g_institutional: {
    label: T('Museum and institutional exhibitions', '美术馆与机构展览'),
    detail: T('Mian Art Museum in Tianjin and Hengdu Art Museum in Taizhou. Institutions vouch in a way a commercial room cannot — they have no stock to sell.', '天津的缅艺术馆与台州的横渡美术馆。机构的背书是商业空间给不了的：它们没有货要卖。'),
  },
  g_solo: {
    label: T('Solo shows, including in Tokyo', '个展，包括在东京'),
    detail: T('Three on record, most recently Light and Shadows and Cats at Galerie LE MONDE in Harajuku, closed 6 September 2026. The work has carried a room alone.', '记录中有三场，最近一次是原宿 Galerie LE MONDE 的《光与影与猫》，2026 年 9 月 6 日结束。作品已经能独自撑起一个空间。'),
  },
  g_international: {
    label: T('First international showing', '第一次国际展出'),
    detail: T('A London showing in December 2025 took the work beyond China and Japan — the start of an international record.', '2025 年 12 月的伦敦展出，把作品带出了中国和日本——国际记录由此开始。'),
  },
  g_press: {
    label: T('Written about, rather than reproduced', '被评论，而不只是被转载'),
    detail: T('Three features on record — Bored Panda twice, Design You Trust once. All reproduce the pictures; none makes an argument about them, and criticism is what a curator can cite.', '记录中有三篇报道——Bored Panda 两次，Design You Trust 一次。都是把图放上去，没有一篇在论述；而策展人能引用的，恰恰是论述。'),
  },
  g_representation: {
    label: T('A gallery that sells on your behalf', '一家代理你销售的画廊'),
    detail: T('The largest structural step available now, and it grows from the shows already on record. Representation moves the price of a single painting, not only the number sold, because a gallery introduces collectors it intends to keep.', '目前可走的最大一步，而且是从已有的展览记录里长出来的。代理抬的是单张画的价格，不只是卖出的张数——因为画廊介绍的是它打算长期留住的藏家。'),
  },
  g_fairs: {
    label: T('Stronger solo venues and art fairs', '更强的个展场地与艺博会'),
    detail: T('Established commercial galleries, institutional solos, and the fairs where collectors gather — Art Fair Tokyo, Tokyo Gendai. Usually reached through a representing gallery rather than before one.', '成熟的商业画廊、机构个展，以及藏家聚集的艺博会——东京艺术博览会、Tokyo Gendai。通常是通过代理画廊到达，而不是在那之前。'),
  },

  // ── audience ───────────────────────────────────────────────────────────────
  a_cadence: {
    label: T('A daily practice that does not stop', '不停下来的每日实践'),
    detail: T('A watercolour diary kept daily since 2020. Everything further up this ladder assumes a steady supply of work, and this is the rung most practices never clear.', '自 2020 年起每天不断的水彩日记。这条阶梯往上的一切都建立在稳定的作品产出之上，而这一级是多数创作者始终没跨过的。'),
  },
  a_look: {
    label: T('A look recognisable at thumbnail size', '缩略图大小也认得出的面貌'),
    detail: T('Urban architecture, interior light, watercolour transparency — consistent for six years. In a feed, recognition happens before the name is read, so the look has to work alone.', '城市建筑、室内光线、水彩的透明感——已经稳定了六年。在信息流里，认出来发生在读到名字之前，所以那种面貌必须自己撑住。'),
  },
  a_found: {
    label: T('An audience that found you', '一群自己找上来的读者'),
    detail: T('About 27,000 on the Instagram diary and about 44,000 on Xiaohongshu, built without advertising on either. That is an audience, and it is the base the rest of this ladder multiplies.', 'Instagram 日记大约 27,000 人，小红书大约 44,000 人，两边都没有投过广告。这已经是一群受众，也是这条阶梯往上乘算的基数。'),
  },
  a_series: {
    label: T('Work that continues rather than accumulates', '会延续的作品，而不是堆积的作品'),
    detail: T('A diary is watched; a named, numbered, continuing series is followed, because it gives a reason to come back for the next one. You already group work this way — 一天和四季, 彩色日记翻翻乐 and 365日永恒如新 are all named and numbered.', '日记是被看的；一个有名字、有编号、还在继续的系列是被追的——因为它给人回来看下一张的理由。你其实已经这样归类过作品了：《一天和四季》《彩色日记翻翻乐》《365日永恒如新》都是有名字、有编号的。'),
  },
  a_motion: {
    label: T('The work seen in motion', '被看见的作画过程'),
    detail: T('Already yours: you film the painting and the recordings go up on Bilibili, where about 7,500 people follow you for them. Watercolour spreading into wet paper is one of the very few things a still image cannot show, and you are the only person who can film yours.', '这一级你已经做到了：你会拍作画过程，成片发在 B 站，那边大约有 7,500 人是为此关注你的。水彩在湿纸上化开，是静止图像几乎唯一拍不到的东西——而你的过程，只有你拍得出来。'),
    treatment: {
      open: T('What having this already is worth', '已经有了这一级，意味着什么'),
      hide: T('Close', '收起'),
      blocks: [
        { label: T('What it changes', '它改变了什么'),
          text: T('A finished painting competes with every other finished painting. A painting being made competes with almost nothing, because the moment pigment hits wet paper cannot be screenshotted, described, or reproduced by anyone else. It is the one thing in your practice that is structurally yours.', '一张画完的画，要和所有画完的画竞争。一张正在被画的画几乎没有对手——颜料落在湿纸上的那一瞬间，没法截图、没法转述，也没有别人能复制。这是你的实践里，结构上唯一属于你自己的东西。'),
        },
        { label: T('What it already cost you', '你已经付出的成本'),
          text: T('Nothing extra, which is the point. Every other state on this ladder asks for something new — a series to invent, a platform to learn, a person to write to. This one is a by-product of a desk you already sit at daily, and you have been generating it for a while.', '没有额外成本，而这正是关键。这条阶梯上其它每一级都要求一件新的事——想一个系列、学一个平台、给一个人写信。这一级只是你每天都要坐的那张桌子的副产品，而且你已经产出了一阵子了。'),
        },
        { label: T('What is worth filming', '值得拍的是什么'),
          text: T('Not the whole painting. The moments where the medium does something a viewer cannot predict — a wash spreading into damp paper, salt or a dry brush breaking a flat area, the first dark going into a pale one, lifting colour back out with a clean brush. Architecture gives you hard edges to cut against soft ones, which is the contrast that holds attention.', '不是整张画。是媒介做出观众预料不到的事的那些瞬间——一片洗染在潮纸上化开、盐或干笔破开一块平涂、第一笔重色落进浅色里、用干净笔把颜色再吸出来。建筑给了你硬边，去和软边形成对比——留住注意力的正是这种反差。'),
        },
        { label: T('Where else the same file goes', '同一个文件还能去哪里'),
          text: T('Bilibili has them. The same file needs no re-editing and no translation to sit on the Instagram side too, because nobody needs language to watch paint move — so the one thing that already crosses both your audiences unchanged is currently only being shown to one of them.', 'B 站上已经有了。同一个文件不用重剪、也不用翻译，就能同样放在 Instagram 那边——因为看颜料流动不需要语言。也就是说，唯一一样在你两群读者之间原样成立的东西，眼下只给其中一边看。'),
        },
        { label: T('Where this sits', '它在什么位置'),
          text: T('It is not only an audience state. A named series becomes far easier to sustain when each entry has a second life as a recording, and a brand deciding whether to license a look is reassured by seeing it made by hand.', '它不只属于受众这一条。当每一张画都还有「一段录像」这第二次生命时，一个有名字的系列会容易维持得多；而正在考虑授权的品牌，看到这种面貌是手工做出来的，会更放心。'),
        },
      ],
    },
  },
  // Filming is necessary, not sufficient (Scott, 2026-09-08: "just because she
  // does process videos isn't enough if she only does them on bilibili"). The
  // rung above is a real 'yes' — she films, and 7,500 people on Bilibili follow
  // her for it. This one is the distribution, and it is a real 'no': the two
  // audiences that don't get them are the ones that would move a career.
  a_weekly: {
    label: T('The painting videos reaching the audiences that never see them',
             '让作画影片抵达那些从没看过的人'),
    detail: T('You have already done this once and it worked better than anything else on your record: six weekly flip-throughs in 2023 that reached 55,000, 49,000 and 16,000 people. None of it is on Instagram or X, where the 27,000 have never seen any of it.',
              '这件事你已经做成过一次，而且成绩比你记录里的任何东西都好：2023 年连续六周的翻翻乐，触达了 55,000、49,000、16,000 人。这些一条都没有发到 Instagram 或 X——那边的 27,000 人从来没看过。'),
    treatment: {
      open: T('What your own channel already proved', '你自己的频道已经证明了什么'),
      hide: T('Close', '收起'),
      blocks: [
        { label: T('Short beats long by 8.5x — on your channel, not in general', '短片是长片的 8.5 倍——这是你自己频道的数字，不是通则'),
          text: T('Of your 33 measurable videos, the ones under two and a half minutes have a median of about 9,975 views. The ones over it: about 1,172. Eight of your top nine are short. The long real-time sessions — the 14 to 21 minute ones — sit around 1,200 to 5,400 for far more work.',
                  '你有 33 条能看到数据的影片：两分半以内的，播放中位数约 9,975；超过两分半的，约 1,172。你最好的九条里有八条是短片。那些 14 到 21 分钟的实时录制，播放大多在 1,200 到 5,400 之间——付出多得多，回报少得多。'),
        },
        { label: T('But it was never just the length', '但起作用的从来不只是长度'),
          text: T('Your recent short ones did not repeat it — 0:36 last August got 139. What the 2023 run had was a hook: a finished 365-day book, numbered episodes, released one a week. People came back for the next one. That is the part worth keeping, and it is not a filming technique.',
                  '你最近的短片没有重现那个结果——去年八月那条 0:36 的只有 139 播放。2023 年那一轮有的是一个「钩子」：一本画完的 365 天日记、编好号的集数、每周一条。人们是回来看下一集的。值得保留的是这件事，而它跟拍摄技巧无关。'),
        },
        { label: T('Once a week, and you have done it', '每周一条，而且你做到过'),
          text: T('Those six went out weekly for six weeks straight. That cadence is not a thing to learn; it is a thing to repeat. The 55,000 one reached about seven times your follower count there, which means it travelled well past the people who already follow you.',
                  '那六条是连续六周、每周一条发出去的。这个节奏不需要学，只需要再做一次。播放 55,000 的那条，大约是你在那边粉丝数的七倍——也就是说，它远远走出了已经关注你的人。'),
        },
        { label: T('Not stories', '不要只发限时动态'),
          text: T('When these do go to Instagram: a story is gone in 24 hours, so it reaches whoever opened the app that day and leaves nothing for the curator who finds you in March. A feed post or a reel stays. If it has to be a story, save it to Highlights afterwards. Timelapse is fine — the spread of pigment often reads better sped up than in real time.',
                  '等这些真的发到 Instagram 时：限时动态 24 小时就没了，只触达那天打开 App 的人，三月份才找到你的策展人什么也看不到。发在主页或做成 Reels，它会留下；如果只能发限时动态，事后存进精选。延时完全可以——颜料化开的过程，压缩过往往比实时更好看。'),
        },
        { label: T('The files already exist', '这些文件本来就有'),
          text: T('Thirty-eight of them. They need no re-editing and no translation to go up in the other two places, because watching paint move needs no language. Posting them to one place is the only reason they reach one place.',
                  '三十八条。它们不用重剪、也不用翻译就能发到另外两个地方——因为看颜料流动不需要语言。它们现在只触达一边，唯一的原因就是只发了一边。'),
        },
      ],
    },
  },
  a_borrowed: {
    label: T('Appearing inside other audiences', '出现在别人的受众里'),
    detail: T('The fastest growth is borrowed rather than built — a shared zine, a two-person show, a trade of features. Twelve artists working in adjacent territory are already mapped; none approached.', '增长最快的方式是借来的，而不是攒出来的——一本合印的 zine、一个双人展、互相介绍。已经梳理出十二位在相邻领域创作的艺术家，尚未接触任何一位。'),
  },
  a_second: {
    label: T('An audience in Chinese as well as on Instagram',
             '中文世界里也有读者，不只是 Instagram'),
    detail: T('You already hold both, and the Chinese side is the bigger one: about 44,000 on Xiaohongshu against about 27,000 on the Instagram diary. Two audiences, in two languages, for one body of work.',
              '这两边你都已经有了，而且中文这边更大：小红书大约 44,000 人，Instagram 上的日记大约 27,000 人。两种语言，两群读者，同一批画。'),
    treatment: {
      open: T('What having both is worth', '同时有这两边，意味着什么'),
      hide: T('Close', '收起'),
      blocks: [
        { label: T('Why Xiaohongshu suits this work', '为什么小红书适合这些画'),
          text: T('City scenes, interiors, daily life and Japan are among the most-read things on it, and the captions are in your first language rather than a second one. A Chinese artist living in Tokyo painting the city is a genre people already follow there — it needs no explaining.',
                  '城市街景、室内、日常生活、日本，本来就是那上面阅读量最高的几类，而且配文用的是你的母语，不是第二语言。一个住在东京、画这座城市的中国画家，在那边本身就是有人在追的题材——不需要解释。'),
        },
        { label: T('What two audiences give that one does not', '两群读者比一群多出什么'),
          text: T('They buy in different currencies, are found by different algorithms, and do not disappear together when one platform changes how it shows work. A print run priced for one market can be sold into the other without making anything new.',
                  '他们用不同的货币买东西、被不同的算法找到，而且不会因为某一个平台改了推荐方式就一起消失。为一个市场定价印出来的东西，不用再做新的，就能卖进另一个。'),
        },
        { label: T('Where the video fits', '影片放在这里的位置'),
          text: T('You already film the painting, and about 7,500 people follow those recordings on Bilibili. The same file needs no re-editing and no translation to play on the English side too — watching paint move needs no language at all, so it is the one thing that travels across every audience unchanged.',
                  '你已经在拍作画过程了，B 站上大约有 7,500 人是为这些影片关注你的。同一个文件不用重剪、也不用翻译，就能同样发到英文那边——看颜料流动完全不需要语言，所以它是唯一一样在所有受众之间都原样成立的东西。'),
        },
        { label: T('Which one is actually bigger', '究竟哪一边更大'),
          text: T('Xiaohongshu, by a wide margin — about 44,000 there against about 27,000 on Instagram. Worth knowing because every outreach email this system writes still names Instagram and only Instagram, which means the platform being shown to galleries is the smaller half of your reach.',
                  '小红书，而且差得不少——那边大约 44,000 人，Instagram 大约 27,000 人。值得知道，是因为这个系统写的每一封对外邮件里，提到的平台仍然只有 Instagram；也就是说，摆到画廊面前的，是你影响力里较小的那一半。'),
        },
        { label: T('What is still not known', '还不知道的部分'),
          text: T('How much the three overlap. Counting Bilibili as well, about 78,500 follows are on record across the Chinese and English sides — but that is a ceiling on reach, not a count of people.',
                  '三边有多少是同一批人。把 B 站也算进来，中文与英文两侧合计记录在案的关注大约 78,500——但这是触达的上限，不是真实的人数。'),
        },
      ],
    },
  },
  a_inbound: {
    label: T('An audience that arrives without being asked', '不用去找、自己会来的受众'),
    detail: T('The state the rest of this ladder is for. At scale a print run stops being a gamble — your best route breaks even at 109 copies, which is one follower in 240 on the Instagram diary alone, one in 650 if both audiences are counted, and one in 4,600 at half a million.', '这条阶梯上其余的一切，都是为了到达这个状态。到了这个规模，印一版书不再是赌博——你最好的印制方案 109 本回本：只按 Instagram 日记算是 240 人里有 1 人，两边一起算是 650 人里有 1 人，到五十万时是 4,600 人里有 1 人。'),
  },

  // ── licensing ──────────────────────────────────────────────────────────────
  l_reproduces: {
    label: T('A subject that survives reproduction', '经得起复制的题材'),
    detail: T('Watercolour architecture and interior light hold up printed small and in quantity, and they suit the categories licensing actually buys — stationery, calendars, covers, interiors.', '水彩的建筑与室内光线，缩小、量产地印出来依然成立，也正好落在授权真正会买的品类里——文具、日历、书封、室内。'),
  },
  l_inprint: {
    label: T('Work already in print', '已经印出来的作品'),
    detail: T('Eight zines and two publications. A commissioner can see the work has been through production before, which is a different question from whether it is good.', '八本 zine，两本出版物。委托方能看到这些作品已经走过一次生产流程——这和作品好不好，是两个问题。'),
  },
  l_lookbook: {
    label: T('A portfolio that can be sent the same day', '当天就能发出去的作品集'),
    detail: T('Ten to twenty works shown as product mockups, one PDF. An art director cannot picture a painting on a notebook cover; a mockup does it for them. Nothing in your record is one.', '十到二十件作品做成产品效果图，一份 PDF。美术总监没法凭空想象一张画印在笔记本封面上是什么样，效果图替他想。你的记录里还没有这样一份东西。'),
  },
  l_findable: {
    label: T('Listed where commissioners search', '出现在委托方检索的地方'),
    detail: T('Licensing is mostly inbound, so being on the files and libraries art directors search is the difference between pitching and being found. Not listed on any of the four routes the app has verified.', '授权大多是对方找上门，所以出现在美术总监会检索的档案库和图库里，就是「主动去投」和「被找到」之间的差别。应用已核实的四条渠道里，都还没有登记。'),
  },
  l_first: {
    label: T('A first paid usage', '第一笔付费授权'),
    detail: T('Worth more as a precedent than as money: a published rate to quote and a client who can be asked again. Magazine illustration starts around ¥5,000, a book cover around ¥70,000.', '它作为先例，比作为收入更值钱：一个可以引用的价格，和一个可以再问一次的客户。杂志插图大约从 5,000 日元起，书封大约 70,000 日元。'),
  },
  l_repeat: {
    label: T('Repeat clients and a rate you set', '回头客，和一个由你定的价'),
    detail: T('One licence is a job; three from the same category is a rate. Published Japanese figures run to ¥100,000 for a magazine cover and ¥800,000 for a calendar, with copyright transfer priced at two to three times a normal licence.', '一笔授权是一份工作；同一品类里的三笔，就是一个价位。日本已公开的价格，杂志封面到 100,000 日元，日历到 800,000 日元，而买断版权的定价是普通授权的两到三倍。'),
  },
  l_inbound: {
    label: T('Brands arriving unprompted', '品牌自己找上门'),
    detail: T('The state this ladder is for. Hobonichi hand-picks illustrators whose work has a distinct voice rather than reading submissions — at this end of the ladder you are found rather than pitching.'),
  },
}

// A goal is a name plus an ORDER of states. `why` overrides the detail where a
// shared state earns its place for a different reason in this ladder.
export const GOALS = [
  {
    id: 'gallery_success',
    name: T('Gallery success', '画廊这条路'),
    ladder: ['g_publication', 'g_group', 'g_institutional', 'g_solo',
             'g_international', 'g_press', 'g_representation', 'g_fairs'],
    why: {},
  },
  {
    id: 'a_following',
    name: T('A following', '一群固定的读者'),
    ladder: ['a_cadence', 'a_look', 'a_found', 'a_series',
             'a_motion', 'a_weekly', 'a_borrowed', 'a_second', 'a_inbound'],
    why: {},
  },
  {
    id: 'intl_licensing',
    name: T('International licensing', '国际授权'),
    ladder: ['l_reproduces', 'a_look', 'l_inprint', 'a_series',
             'l_lookbook', 'l_findable', 'l_first', 'l_repeat', 'l_inbound'],
    why: {
      a_look: T('Brands license a look they can put across a product line, so it has to survive being reproduced small and in quantity — the same consistency that earns recognition in a feed.', '品牌买的是一种能铺成产品线的面貌，所以它必须经得起被缩小、被大量复制——和在信息流里被认出来，靠的是同一种稳定。'),
      a_series: T('A range needs several related pieces at once, so a named series licenses more easily than a strong single image.', '一个产品系列一次要用好几件相关的作品，所以有名字的系列，比一张强的单图更容易授权。'),
    },
  },
]

// Which OTHER goals a state also belongs to. Derived from the ladders, so it can
// never disagree with them.
export const alsoServes = (stateId, goalId) =>
  GOALS.filter((g) => g.id !== goalId && g.ladder.includes(stateId))

// Three states, not two. The first version returned a bare boolean, so "we
// checked and the answer is no" and "nobody has ever looked" both rendered as an
// empty circle — and the page then advised her to go and do things she was
// already doing. That is exactly what happened with Xiaohongshu: the profile
// tracked Instagram alone, the state read as unreached, and the treatment told
// her to start an account that exists (Scott, 2026-09-08).
//
//   'yes'     — her record says so
//   'no'      — her record says so, and it is a real absence
//   'unknown' — the system has never measured this. NOT a gap, and never advice.
//
// Most of the audience and licensing ladders are honestly 'unknown', because the
// system has never tracked a lookbook, a series name, a video, or a licence. The
// engine specced in docs/NEXT_PHASE_strategies.md inherits this contract.
export function evidence(data, careerData) {
  const ev = careerData?.career_evidence || {}
  const shows = (data?.career_position?.exhibitions || []).length
  const yn = (b) => (b ? 'yes' : 'no')
  return {
    // Gallery — the career engine measures all of this, so yes/no are both real.
    g_publication: yn((ev.publications_confirmed || 0) > 0),
    g_group: yn((ev.confirmed_group_shows || 0) >= 3),
    g_institutional: yn(!!ev.has_institutional_show),
    g_solo: yn(!!ev.has_solo_show),
    g_international: yn(!!ev.has_international_show),
    // A real 'no': three features are on record and all three reproduce.
    g_press: 'no',
    // A real 'no': the profile records gallery_representation as none confirmed.
    g_representation: yn(!!ev.has_representation),
    // Nobody tracks fair participation anywhere in the system.
    g_fairs: 'unknown',

    a_cadence: 'yes',
    a_look: yn(shows > 0),
    a_found: 'yes',
    // Third instance of the same bug in one session, and the worst of the three:
    // this was 'unknown' while its copy asserted "six years of work with no
    // named body inside it" — an unmeasured state rendered as an absence, in the
    // one file that carries the rule against exactly that. It is also false. Her
    // Bilibili channel groups work into three named, numbered collections
    // (一天和四季 / 彩色日记翻翻乐 / 365日永恒如新), read 2026-09-08.
    a_series: 'yes',
    // Reached. She films the painting and posts it to Bilibili (Scott,
    // 2026-09-08). Second time in one session that a state this file called
    // unmeasured turned out to be something she had been doing for years — the
    // first was Xiaohongshu. When a state is 'unknown', ask before writing
    // anything that reads as "you could start".
    a_motion: 'yes',
    // A real 'no', and the reason a_motion's 'yes' is not the end of it: Scott
    // looked for these on Instagram and X before finding them on Bilibili, and
    // they are not there ("just because she does process videos isn't enough if
    // she only does them on bilibili"). Being a real 'no' is what lets this one
    // be offered as the next step.
    a_weekly: 'no',
    a_borrowed: 'unknown',
    // Reached. She has been on Xiaohongshu all along; the profile recorded
    // Instagram alone, so this rendered as a gap and the page advised her to
    // start an account she already had (Scott, 2026-09-08).
    a_second: 'yes',
    a_inbound: 'unknown',

    l_reproduces: 'yes',
    l_inprint: yn((ev.publications_confirmed || 0) > 0),
    // Never measured: no lookbook field, no directory listing check, no licence
    // log. Rendering these as gaps was the bug.
    l_lookbook: 'unknown',
    l_findable: 'unknown',
    l_first: 'unknown',
    l_repeat: 'unknown',
    l_inbound: 'unknown',
  }
}
