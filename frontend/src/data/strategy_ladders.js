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
    detail: T('About 26,000 on the daily-diary account, built without advertising. That is an audience, and it is the base the rest of this ladder multiplies.', '每日日记账号上大约 26,000 人，没有投过广告。这已经是一群受众，也是这条阶梯往上乘算的基数。'),
  },
  a_series: {
    label: T('Work that continues rather than accumulates', '会延续的作品，而不是堆积的作品'),
    detail: T('A diary is watched; a named, numbered, continuing series is followed, because it gives a reason to come back for the next one. Six years of work with no named body inside it.', '日记是被看的；一个有名字、有编号、还在继续的系列是被追的——因为它给人回来看下一张的理由。六年的作品里，还没有一个被命名的系列。'),
  },
  a_motion: {
    label: T('The work seen in motion', '被看见的作画过程'),
    detail: T('Watercolour spreading into wet paper is one of the very few things a still image cannot show, and it is the single change on this ladder that asks for no extra painting — the camera watches work already being done.', '水彩在湿纸上化开，是静止图像几乎唯一拍不到的东西；而且这是这条阶梯上唯一不要求你多画一张的改变——镜头拍的，是本来就在做的事。'),
    treatment: {
      open: T('Why this one matters more than the rest', '为什么这一级比其它几级都重要'),
      hide: T('Close', '收起'),
      blocks: [
        { label: T('What it changes', '它改变了什么'),
          text: T('A finished painting competes with every other finished painting. A painting being made competes with almost nothing, because the moment pigment hits wet paper cannot be screenshotted, described, or reproduced by anyone else. It is the one thing in your practice that is structurally yours.', '一张画完的画，要和所有画完的画竞争。一张正在被画的画几乎没有对手——颜料落在湿纸上的那一瞬间，没法截图、没法转述，也没有别人能复制。这是你的实践里，结构上唯一属于你自己的东西。'),
        },
        { label: T('Why it costs nothing', '为什么它没有额外成本'),
          text: T('Every other state on this ladder asks for something new — a series to invent, a platform to learn, a person to write to. This one asks for a phone on a stand pointing at a desk you are already sitting at, for work you are already doing daily. The material is a by-product.', '这条阶梯上其它每一级都要求一件新的事——想一个系列、学一个平台、给一个人写信。这一级只要求一部架好的手机，对着你本来就坐着的桌子，拍你本来每天都在做的事。素材是副产品。'),
        },
        { label: T('What is worth filming', '值得拍的是什么'),
          text: T('Not the whole painting. The moments where the medium does something a viewer cannot predict — a wash spreading into damp paper, salt or a dry brush breaking a flat area, the first dark going into a pale one, lifting colour back out with a clean brush. Architecture gives you hard edges to cut against soft ones, which is the contrast that holds attention.', '不是整张画。是媒介做出观众预料不到的事的那些瞬间——一片洗染在潮纸上化开、盐或干笔破开一块平涂、第一笔重色落进浅色里、用干净笔把颜色再吸出来。建筑给了你硬边，去和软边形成对比——留住注意力的正是这种反差。'),
        },
        { label: T('Where it goes', '它发到哪里'),
          text: T('The same file works everywhere without re-editing, which is what makes it the natural partner to a second audience elsewhere — one recording, several places, no translation, because nobody needs language to watch paint move.', '同一个文件到哪儿都能用，不用重剪——所以它天然是「在别处的第二群受众」那一级的搭档：拍一次，发几个地方，不需要翻译，因为看颜料流动不需要语言。'),
        },
        { label: T('Where this sits', '它在什么位置'),
          text: T('It is not only an audience state. A named series becomes far easier to sustain when each entry has a second life as a recording, and a brand deciding whether to license a look is reassured by seeing it made by hand.', '它不只属于受众这一条。当每一张画都还有「一段录像」这第二次生命时，一个有名字的系列会容易维持得多；而正在考虑授权的品牌，看到这种面貌是手工做出来的，会更放心。'),
        },
      ],
    },
  },
  a_borrowed: {
    label: T('Appearing inside other audiences', '出现在别人的受众里'),
    detail: T('The fastest growth is borrowed rather than built — a shared zine, a two-person show, a trade of features. Twelve artists working in adjacent territory are already mapped; none approached.', '增长最快的方式是借来的，而不是攒出来的——一本合印的 zine、一个双人展、互相介绍。已经梳理出十二位在相邻领域创作的艺术家，尚未接触任何一位。'),
  },
  a_second: {
    label: T('An audience in Chinese, not only on Instagram',
             '中文世界里的读者，而不只是 Instagram 上的'),
    detail: T('Everything the system knows about your audience is one Instagram account with about 27,000 followers. The obvious second one is Chinese — your first language, and a market where "a Chinese artist living in Tokyo, painting the city" is a genre people already follow rather than a thing that needs explaining.',
              '系统知道的关于你受众的一切，就只有一个大约 27,000 人的 Instagram 账号。第二群显而易见是中文的——那是你的母语，而且在那个市场里，「一个住在东京、画这座城市的中国画家」本身就是有人在追的题材，不需要额外解释。'),
    treatment: {
      open: T('Which platforms, and why that one first', '具体是哪些平台，为什么先是那一个'),
      hide: T('Close', '收起'),
      blocks: [
        { label: T('Xiaohongshu first', '先是小红书'),
          text: T('It is the closest match to what you already make: city scenes, interiors, daily life, and travel in Japan are among the most-read things on it, and the captions would be in your own language rather than a second one. Nothing here has to be made — the paintings exist, and the cost is the posting.',
                  '它和你已经在做的东西最贴近：城市街景、室内、日常生活、在日本的旅行，本来就是那上面阅读量最高的几类内容，而且配文可以用你自己的语言写，而不是第二语言。这一级不需要新画什么——画都在，成本只是「发」这个动作。'),
        },
        { label: T('Then wherever the video goes', '然后是影片能去的地方'),
          text: T('Once painting is being filmed, the same file plays on Bilibili and on short-video feeds without re-editing. Watching paint move needs no language at all, which is why this state and the one about filming are worth doing in that order.',
                  '一旦开始拍作画过程，同一个文件不用重剪就能发到 B 站和短影片流里。看颜料流动完全不需要语言——所以「被看见的作画过程」和这一级，值得按这个顺序做。'),
        },
        { label: T('What it is actually for', '它到底是为了什么'),
          text: T('Not a bigger number. A second audience buys in a different currency, is found by a different algorithm, and does not disappear if one platform changes how it shows work. It is the difference between one audience and a practice that has readers.',
                  '不是为了数字更大。第二群读者用另一种货币买东西、被另一套算法找到，而且不会因为某一个平台改了推荐方式就一起消失。这是「有一个账号的受众」和「有读者的创作」之间的差别。'),
        },
        { label: T('What the system does not know', '系统不知道的部分'),
          text: T('Whether you are already posting there. The profile records one platform and one follower count, so this state is marked unreached because nothing contradicts it — not because anyone checked.',
                  '你是不是已经在那边发了。档案里只记着一个平台、一个粉丝数，所以这一级被标成未达成，只是因为没有任何信息与之相反——不是因为有人去核实过。'),
        },
      ],
    },
  },
  a_inbound: {
    label: T('An audience that arrives without being asked', '不用去找、自己会来的受众'),
    detail: T('The state the rest of this ladder is for. At scale a print run stops being a gamble — your best route breaks even at 109 copies, which is one follower in 240 today and one in 4,600 at half a million.', '这条阶梯上其余的一切，都是为了到达这个状态。到了这个规模，印一版书不再是赌博——你最好的印制方案 109 本回本，按今天的受众是 240 人里有 1 人，到五十万时是 4,600 人里有 1 人。'),
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
             'a_motion', 'a_borrowed', 'a_second', 'a_inbound'],
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
