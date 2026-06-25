import { useState, useEffect, useMemo, Component, createContext, useContext } from 'react'
import './SaffronPage.css'
import { CalendarMonth } from './DeadlineCalendar'
import { parseDeadline, keyOf } from '../utils/calendarDates'
import './DeadlineCalendar.css'
import { saffronHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb } from '../i18n/translations'
import {
  LICENSING_LANDSCAPE,
  PRESS_PITCH_MAP,
  GRANT_LANDSCAPE,
  REVENUE_STREAMS,
  CAREER_DEPENDENCY_MAP,
  PRICING_INTELLIGENCE,
  COLLABORATION_MAP,
  COLLECTOR_ECOSYSTEM,
  PRESS_KIT,
} from '../data/saffron_insights'

// Saffron's analysis body is authored in English in api.py. When the viewer is
// reading in Chinese, we translate every served string client-side via this map
// (unmapped strings pass through unchanged — graceful partial coverage).
// localizeDeep — for the static saffron_insights constants (CAREER_TIMELINE,
// PRICING_INTELLIGENCE): return a copy where every field that has a `<field>_zh`
// / `<field>_ja` sibling (including parallel arrays like had_zh) is swapped for
// the active language. The _zh/_ja sibling keys are dropped from the output.
function localizeDeep(node, lang) {
  const suf = lang === 'zh' ? '_zh' : lang === 'ja' ? '_ja' : null
  if (!suf || node == null || typeof node !== 'object') return node
  if (Array.isArray(node)) return node.map(x => localizeDeep(x, lang))
  const out = {}
  for (const k in node) {
    if (k.endsWith('_zh') || k.endsWith('_ja')) continue
    const sib = node[k + suf]
    out[k] = localizeDeep(sib !== undefined ? sib : node[k], lang)
  }
  return out
}

function deepTranslate(obj, map) {
  if (typeof obj === 'string') return map[obj] || obj
  if (Array.isArray(obj)) return obj.map(x => deepTranslate(x, map))
  if (obj && typeof obj === 'object') {
    const out = {}
    for (const k in obj) out[k] = deepTranslate(obj[k], map)
    return out
  }
  return obj
}

const SF_ZH = {
  // ── Open questions (she reads + answers these) ──
  "What's your current Instagram posting frequency?": "你目前在 Instagram 上的发布频率是多少？",
  "With an established, growing Instagram following, the account is already a working portfolio. Cadence is the most controllable variable for maximising reach on the platform galleries, publishers, and curators actually use for discovery. Without knowing current frequency, no posting strategy can be recommended.": "你已有稳固且持续增长的 Instagram 受众，账号本身就是一份运转中的作品集。发布节奏是提升触及最可控的变量——而画廊、出版社与策展人正是用这个平台来发掘新人。在不知道当前频率的情况下，无法给出任何发布策略建议。",
  "Where is your audience located geographically?": "你的受众主要分布在哪些地区？",
  "A primarily Chinese-language following changes the geographic expansion strategy entirely — it suggests China reentry before European expansion.": "如果粉丝以中文受众为主，整个地域拓展策略都会不同——这意味着应先重返中国市场，再考虑欧洲。",
  "Have you sold work, and through which channels?": "你卖出过作品吗？通过哪些渠道？",
  "Sales history reveals which formats and price points convert — this shapes which fairs and platforms are worth prioritising.": "销售记录能揭示哪些形式与价位真正能成交——这决定了哪些博览会与平台值得优先投入。",
  "Is a new publication or zine in progress?": "你目前是否在筹备新的出版物或独立刊物？",
  "If you're already planning one, this should support it — not pitch it as a new idea.": "如果你已经在筹备，系统应当支持它——而不是把它当作一个全新的点子来推荐。",
  "Do you have a current artist statement in any language?": "你是否已有一份（任意语言的）现行艺术家自述？",
  "Most open calls and gallery submissions require one. If none exists, this is the most urgent gap before any submissions.": "大多数公开征集与画廊投递都需要它。如果还没有，这是你开始任何投递前最紧迫的空缺。",
  "Are you still in contact with your Tide from China co-exhibitors?": "你和「潮自中国」联展的其他参展者还有联系吗？",
  "If those 5 artists are Tokyo-based and active, they are the most natural group show partners. If they've dispersed, that network is dormant.": "如果那 5 位艺术家身在东京且仍活跃，他们就是最自然的联展伙伴。如果已各奔东西，这个人脉网络便处于休眠状态。",
  "Do you have a second Japan exhibition in progress?": "你目前是否在筹备第二场日本展览？",
  "There's one show on record, so the read assumes 2–3 more group shows would help — but you may already have one underway. If so, tell me here.": "记录在册的只有一场展览，因此分析假设再参与 2–3 场联展会有帮助——但你也许已经有一场在进行中。如果是，请在这里告诉我。",
  "What price points do you use for originals and prints?": "你的原作和印刷品定价大约是多少？",
  "Pricing determines which collector tier and which fairs are appropriate. Under-pricing is common at this stage and affects how galleries perceive the work.": "定价决定了适合哪一层级的藏家与哪些博览会。在这个阶段定价偏低很常见，并会影响画廊对作品的看法。",

  // ── Career paths (long-term scenarios) ──
  "Gallery Track": "画廊路线",
  "Primary identity as a gallery artist.": "以画廊艺术家为主要身份。",
  "Solo shows, institutional open calls, gallery representation over the next few years.": "个展、机构公开征集，在未来几年里获得画廊代理。",
  "Exhibition history is thin. 2–3 more group shows are required before any gallery will discuss a solo show.": "展览经历尚浅。在任何画廊愿意谈个展之前，还需要 2–3 场联展。",
  "Right if you're primarily motivated by the physical exhibition experience and gallery community.": "如果你最看重实体展览的体验与画廊圈子，这条路最适合你。",
  "Publication Track": "出版路线",
  "Primary identity as an illustrator and artist-book maker.": "以插画家与艺术书创作者为主要身份。",
  "Second solo book, international distribution, major book fairs over the next few years.": "在未来几年里完成第二本个人作品集、国际发行、参与重要书展。",
  "No new publication since 2021. The content exists — it needs packaging.": "自 2021 年以来没有新出版物。内容已经具备——只差整理成册。",
  "Right if you're motivated by the book as object and the publishing community. Your formation already points here.": "如果你着迷于书作为实体，以及出版社群，这条路最适合你。你的成长背景本就指向这里。",
  "Hybrid Track": "复合路线",
  "Artist-publisher: books and gallery shows running in parallel.": "艺术家兼出版者：书与画廊展览并行。",
  "The book practice feeds the gallery presence and vice versa. Bookshop gallery shows bridge both worlds.": "出版实践滋养画廊呈现，反之亦然。书店画廊展览连接两个世界。",
  "Requires more energy and time management than either single track.": "比任何单一路线都更考验精力与时间管理。",
  "The most natural fit given your existing practice. The daily diary is simultaneously publication material and gallery-worthy work.": "鉴于你现有的实践，这是最自然的选择。每日水彩日记既是出版素材，也是值得展出的作品。",
  "The Hybrid Track is the best structural fit. The bookshop gallery show is the single highest-leverage action — it advances both tracks with one move.": "复合路线在结构上最契合。书店画廊展览是单一杠杆最高的行动——一步同时推进两条路线。",
  // Age/countdown framing retired (Scott: companions may use what she tells
  // them, never parade inferred personal facts). Horizon is now a neutral
  // "next few years" — matching the backend's new English.
  "The next few years": "未来几年",

  // ── Instagram ──
  "Primary visual portfolio platform — an established, growing following built through daily watercolor diary practice since 2020. The platform galleries, publishers, and curators use for discovery.": "你主要的视觉作品集平台——自 2020 年起通过每日水彩日记积累了稳固且持续增长的受众。也是画廊、出版社与策展人用来发掘新人的平台。",
  "Instagram is an established strength — an established, growing following, already a working portfolio and the surface galleries and publishers use to discover you. Growth from here is a bonus, not a requirement.": "Instagram 已是你确立的优势——稳固且持续增长的受众，本身就是一份运转中的作品集，也是画廊与出版社发掘你的入口。继续增长是加分项，而非必需。",
  "A years-long watercolor diary since 2020. The material is already there; nothing about visibility asks you to paint more.": "自 2020 年起、持续多年的水彩日记。素材已经现成；提升曝光并不要求你画得更多。",
  "Urban environments, cats, domestic life, travel fragments — subjects that already do well on Instagram": "城市环境、猫、日常生活、旅行片段——这些题材在 Instagram 上本就表现不错。",

  // ── Pathway steps ──
  "Artist-run spaces are the natural path: 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN. Each show builds credibility and introduces your work to gallery directors.": "艺术家自营空间是最自然的路径：3331 Arts Chiyoda、Design Festa Gallery、Gallery IYN。每一场展览都积累信誉，并把你的作品介绍给画廊主理人。",
  "UTRECHT, Book and Sons, or flotsam books. Bridges illustration community into gallery context — a natural fit given your publication background.": "UTRECHT、Book and Sons 或 flotsam books。把插画社群引入画廊语境——鉴于你的出版背景，这是自然的契合。",
  "Builds presence in the Tokyo zine and book ecosystem. Creates a natural entrypoint for bookshop gallery conversations and strengthens the publication half of your CV.": "在东京独立刊物与书籍生态中建立存在感。为书店画廊的洽谈创造自然的切入口，并强化你简历中出版的那一半。",

  // ── Press / collaboration / audience / collector ──
  "Domestic interiors and everyday life — directly aligned with your subject matter": "家居室内与日常生活——与你的题材直接契合",
  "Large illustration/photography community; annual book prize you could enter": "庞大的插画／摄影社群；有可投递的年度书籍奖项",
  "The 5 co-exhibitors from Tide from China are your strongest existing collaboration seeds. Their current Tokyo presence and active practice is unconfirmed — tell Saffron whether you've stayed in contact with any of them.": "「潮自中国」联展的 5 位共同参展者，是你现有最强的合作种子。他们目前是否在东京、是否仍活跃尚未确认——请告诉山楂你是否还和其中任何人保持联系。",
  "Whether your established Instagram following is concentrated in China, Japan, or distributed internationally determines which geographic markets to prioritise — for exhibitions, fairs, and publishers. A primarily Chinese audience suggests a different expansion path than a globally distributed one.": "你那稳固的 Instagram 受众究竟集中在中国、日本，还是分布于全球，决定了该优先经营哪些地域市场——展览、博览会与出版社皆然。以中文受众为主，意味着与全球分布截然不同的拓展路径。",
  "Knowing who buys illustration and watercolor work at your price point determines which fairs, platforms, and venues are commercially worthwhile — not just aesthetically aligned.": "了解在你的价位上谁会购买插画与水彩作品，决定了哪些博览会、平台与场地在商业上值得投入——而不仅仅是审美上契合。",

  // ── Comparable artists ──
  "Taiwan": "台湾", "Japan / USA": "日本／美国", "USA": "美国", "UK": "英国",
  "USA (Chinese-American)": "美国（华裔）", "Japan": "日本", "Uruguay / Australia": "乌拉圭／澳大利亚",
  "atmospheric urban and interior watercolor, quiet scenes, strong tonal control. Built international credibility from a Taiwan base through IWS competitions.": "氛围感的城市与室内水彩，安静的场景，扎实的色调掌控。从台湾出发，通过 IWS 赛事建立了国际信誉。",
  "Primary career-path reference for building international watercolor credibility from an Asian base.": "从亚洲根基出发建立国际水彩信誉的首要事业路径参照。",
  "Japanese watercolor painter, urban and travel subjects, light and understated atmosphere. Has exhibited with AWS and NWS — Japan-rooted identity with international visibility.": "日本水彩画家，城市与旅行题材，轻盈而含蓄的氛围。曾参与 AWS 与 NWS 展览——扎根日本而具国际能见度的身份。",
  "Reference for Japan-origin watercolor career with international reach.": "以日本为出身、具国际影响力的水彩事业参照。",
  "Architectural watercolor — buildings, urban light, atmosphere, quiet structural observation. Large-format architectural studies with dramatic mood.": "建筑水彩——楼宇、城市光线、氛围、安静的结构观察。富戏剧性情绪的大尺幅建筑习作。",
  "Primary reference for architectural watercolor practice and aesthetic.": "建筑水彩实践与美学的首要参照。",
  "British architectural watercolorist known for Edinburgh and UK urban scenes. Has exhibited in London and internationally.": "英国建筑水彩画家，以爱丁堡及英国城市场景著称。曾在伦敦及国际展出。",
  "Reference for building an architectural watercolor career with direct-to-collector sales.": "以直接面向藏家销售来建立建筑水彩事业的参照。",
  "Chinese-born watercolorist integrating Chinese ink painting sensibility with Western watercolor technique. AWS member.": "出生于中国的水彩画家，将中国水墨的感性与西方水彩技法融合。AWS 会员。",
  "Reference for cross-cultural watercolor identity — Chinese training meeting international exhibition contexts.": "跨文化水彩身份的参照——中国训练背景与国际展览语境的交汇。",
  "Annual national exhibition — Tier 3 credibility target. Contemporary Japanese watercolor practitioners working at the level she is building toward.": "年度全国性展览——第三层级的信誉目标。当代日本水彩从业者所处的水平，正是你正在努力达到的。",
  "Reference ecosystem for Japan active watercolor exhibition community.": "日本活跃水彩展览社群的参照生态。",
  "Urban watercolor with loose, atmospheric style; strong international exhibition record built from a non-Western base. AWS signature member.": "城市水彩，风格松动而富氛围；从非西方根基建立了扎实的国际展览记录。AWS 签名会员。",
  "Reference for building international watercolor exhibition record through society competitions.": "通过协会赛事建立国际水彩展览记录的参照。",
  "Prominent UK watercolor practitioner and author. Style is loose and expressive — very different from GEGYjiji's quiet urban register. Community reference only.": "英国知名水彩从业者与作者。风格松动而富表现力——与你安静的城市气质截然不同。仅作社群参照。",
  "Community reference only. Do NOT use as stylistic reference or aesthetic comparison.": "仅作社群参照。请勿用作风格参照或审美比较。",
  "atmospheric watercolor": "氛围水彩", "quiet observation": "安静的观察", "Asia-based career": "立足亚洲的事业", "architectural subjects": "建筑题材",
  "Japan-connected identity": "与日本相连的身份", "urban and travel watercolor": "城市与旅行水彩", "quiet atmospheric palette": "安静的氛围色调", "watercolor societies": "水彩协会",
  "architecture and urban environments": "建筑与城市环境", "atmospheric light": "氛围光线", "watercolor medium": "水彩媒材", "mood-first approach": "以情绪为先的手法",
  "architecture and urban buildings": "建筑与城市楼宇", "observation-based practice": "基于观察的实践", "structural and atmospheric balance": "结构与氛围的平衡",
  "Chinese artistic formation": "中国艺术训练背景", "Western watercolor practice": "西方水彩实践", "cross-cultural career": "跨文化的事业",
  "Japan-based": "立足日本", "annual exhibition culture": "年度展览文化", "national institutional credibility": "国家机构层面的信誉",
  "urban scenes": "城市场景", "atmospheric loose watercolor": "氛围松动的水彩", "international career from non-Western base": "从非西方根基发展的国际事业",
  "international watercolor community": "国际水彩社群", "publishing and teaching path": "出版与教学路径",

  // ── Your record (career position) ──
  "February 2023": "2023 年 2 月",
  "Group show — 6 Chinese illustrators": "联展——6 位中国插画师",
  "First Japan exhibition": "首次日本展览",
  "Solo illustration collection": "个人插画作品集",
  "Group publication, contributor": "群体出版物，供稿者",
  "Beijing Fashion Institute": "北京服装学院",
  "Illustration & design": "插画与设计",
  "Illustration & design background": "插画与设计背景",
  "Tokyo, Japan / Beijing, China": "日本东京／中国北京",
  "Zines & Books": "独立刊物与书籍", "Galleries": "画廊", "Residencies": "驻地",
  "Open Calls & Fairs": "公开征集与博览会", "Cafés & Bookshop Spaces": "咖啡馆与书店空间", "Other": "其他",
  "Immediate Best Moves": "当下最佳行动", "Publication Targets": "出版目标",
  "Relationship Builders": "关系建立", "Stretch Targets": "进阶目标", "Needs Research": "需要调研",

  // ── Benchmarks ──
  "Group exhibitions": "联展", "Publications": "出版物", "Instagram followers": "Instagram 粉丝",
  "1 confirmed": "1 场已确认", "2 (1 solo, 1 group)": "2（1 本个人，1 本群体）",
  "below_typical": "低于典型", "on_track": "处于正轨",
  "Expected at this stage — but the gap needs closing before gallery conversations are realistic": "这个阶段属于正常——但在画廊洽谈变得现实之前，需要补上这个差距",
  "Solid for this stage, especially with a solo collection so early": "对这个阶段而言相当扎实，尤其是很早就有了第一本个人作品集",
  "Right in the typical band for illustrators at this stage — a solid, real audience for print and zine discovery, with room to grow toward the 50k market-viability signal": "正处于这个阶段插画师的典型区间——一个扎实而真实的受众群，利于印刷品与独立刊物被发掘，并有空间向 5 万这一市场可行性信号增长",
  "Exhibition history is the weakest dimension. An established, growing Instagram following is a solid, real asset at this career stage but not yet a standout — it sits in the typical peer range. The near-term work is converting audience into exhibition and publication credits.": "展览经历是最薄弱的一环。稳固且持续增长的 Instagram 受众在这个事业阶段是扎实而真实的资产，但还算不上突出——它落在同侪的典型区间内。近期的功课是把受众转化为展览与出版的履历。",
  "~6 (daily practice from 2020, first publication 2021)": "约 6 年（2020 年起每日创作，2021 年首次出版）",

  // ── Month names ──
  "January": "一月", "February": "二月", "March": "三月", "April": "四月",
  "May": "五月", "June": "六月", "July": "七月", "August": "八月",
  "September": "九月", "October": "十月", "November": "十一月", "December": "十二月",

  // ── Readiness (careerData) ──
  // Level labels (from career_strategy_engine, flow through deepTranslate)
  "Ambient Visibility": "环境可见度",
  "Networking & Foundation": "人脉与根基",
  "Credibility": "专业公信力",
  "Prestige": "声望",
  "Foundation complete — building Tier 4 body of work": "根基已成——正在积累第四级的作品体系",
  "Tier 1-2 foundation building": "第 1–2 层级的基础建设",
  "Complete 2 more Tokyo group show(s) to reach the 3-show minimum that opens Tier 3 conversations.": "再完成 2 场东京联展，达到开启第 3 层级洽谈所需的 3 场最低门槛。",
  // Gap titles + details — opportunity framing (positive reinforcement)
  // NOTE: readiness gap/detail/action strings are now localized at the source —
  // career_strategy_engine emits *_zh siblings with the live counts, and
  // CareerReadiness reads them via locF. No baked-count sentences live here
  // anymore (they leaked English the moment a count changed).
  "A first solo show is within reach": "首次个展，已经触手可及",
  "A first solo show is a real leap in credibility for Tier 3 calls — and it's an achievable next step. Even a small bookshop-gallery or café solo counts.": "首次个展会让你在第三级征集中的公信力实现真正的飞跃——而且这是可以达成的下一步。哪怕是书店画廊或咖啡馆里的小型个展，也算数。",
  "Target bookshop gallery solo show: UTRECHT, Book and Sons, flotsam books, 日記屋 月日": "争取书店画廊个展：UTRECHT、Book and Sons、flotsam books、日記屋 月日",
  "An institutional show is the next door to open": "机构展览，是下一扇待你推开的门",
  "An arts-council or public-gallery show is the next credibility door to open. TOKAS, BankART1929, and Youkobo are realistic near-term entries for where you are now.": "在艺术委员会或公立画廊办展，是下一扇值得推开的公信力之门。TOKAS、BankART1929 与 Youkobo，都是以你现在的位置切实可及的近期入口。",
  "Watch TOKAS open calls and Youkobo artist-in-residence programs": "关注 TOKAS 公开征集与 Youkobo 驻地项目",
  "International reach, whenever you want it": "国际舞台，随时为你敞开",
  "Your shows so far are in Japan and China — a strong base. Adding an international showing, even a remote open call, opens residencies and fellowships when you want them.": "你目前的展览集中在日本与中国——这是坚实的根基。再添一次国际展出，哪怕是一次远程公开征集，就能在你想要的时候打开驻地与奖助的大门。",
  "Consider global watercolor open calls or table at Offprint Paris / London Art Book Fair": "考虑国际水彩公开征集，或在 Offprint Paris／London Art Book Fair 设展位",
  "The Japan Watercolor Society is open to you": "日本水彩画会，正向你敞开",
  "The Japan Watercolor Society annual exhibition is a Tier 3 credibility marker for watercolor artists in Japan — and non-members can enter the juried calls. An open door whenever you're ready.": "日本水彩画会的年度展览，是日本水彩艺术家第三级公信力的标志——而且非会员也可以参加评审征集。这扇门，随时为你敞开。",
  "Research Japan Watercolor Society (公益社団法人日本水彩画会) annual entry process": "了解日本水彩画会（公益社団法人日本水彩画会）的年度参展流程",

  // ── Geographic reach ──
  "Japan / Tokyo": "日本／东京", "Europe (UK, France, etc.)": "欧洲（英国、法国等）",
  "North America": "北美", "Global / International (open calls)": "全球／国际（公开征集）",
  "primary_base": "主要根据地", "medium_term": "中期", "active": "活跃",
  "Core operating territory. The question here is depth, not entry.": "核心经营区域。这里的问题是深度，而非进入。",
  "Strong art book and zine fair ecosystem — Offprint Paris and London are the natural entry points.": "强大的艺术书与独立刊物展会生态——Offprint Paris 与伦敦是自然的切入口。",
  "NYC zine culture (Printed Matter) and LA illustration scene. Already in pipeline.": "纽约的独立刊物文化（Printed Matter）与洛杉矶的插画圈。已在跟进之中。",
  "International open calls and online platforms that accept globally. Actionable now without travel.": "面向全球开放的国际公开征集与线上平台。无需出行，现在即可行动。",
  "Offprint Paris or London — low barrier, direct access to European curators and collectors who buy artist books": "Offprint Paris 或伦敦——门槛低，可直接接触购买艺术书的欧洲策展人与藏家",
  "Printed Matter NY Art Book Fair — the highest-profile artist book platform in North America": "Printed Matter 纽约艺术书展——北美最具知名度的艺术书平台",

  // ── Publication landscape ──
  "First solo published work, grew from daily diary practice": "首部个人出版作品，由每日日记实践发展而来",
  "Participation confirmed, publication details unverified": "参与已确认，出版细节尚未核实",
  "unknown": "未知",
  "Self-publish / zine": "自出版／独立刊物", "Bookshop gallery": "书店画廊",
  "Art book fairs": "艺术书展", "Major publishers": "大型出版社",
  "low": "低", "medium": "中", "high": "高",
  "Tokyo zine culture is active and illustrator-friendly. Fastest route to a new publication credit.": "东京的独立刊物文化活跃且对插画师友好。这是获得新出版履历最快的途径。",
  "Accept work from illustrators without gallery representation. Bridges publication and gallery worlds.": "接受没有画廊代理的插画师作品。连接出版与画廊两个世界。",
  "Table fees required but direct access to collectors and curators who buy artist books.": "需缴展位费，但能直接接触购买艺术书的藏家与策展人。",
  "Relationship-first. Cold submissions rarely land at this level — build toward these over 2–3 years.": "以关系为先。在这个层级冷投稿很少成功——用 2–3 年逐步靠近。",

  // ── Timing ──
  "Most opportunities have rolling or unspecified deadlines — check each one individually.": "大多数机会的截止日期是滚动或未指定的——请逐一查看。",

  // ── Opportunity gap ──
  "Café Galleries": "咖啡馆画廊", "Editorial / Magazines": "编辑约稿／杂志",
  "Competitions & Awards": "竞赛与奖项", "Watercolor Open Calls": "水彩公开征集",
  "Zines & Print": "独立刊物与印刷", "Grants & Fellowships": "资助与奖学金",
  "Residencies & Grants": "驻地与资助", "Cafes & Bookshop Spaces": "咖啡馆与书店空间",
  "gap": "缺口", "strength": "强项",
  "Core relationship-building venues for a Tokyo-based painter.": "对一位东京画家而言，建立关系的核心场地。",
  "Low-barrier first exhibition venues; common for emerging Tokyo artists.": "门槛低的首展场地；东京新晋艺术家的常见选择。",
  "Production time + institutional credibility; peers typically track 5–10.": "创作时间＋机构信誉；同侪通常会跟进 5–10 个。",
  "Most watercolor illustrators this stage have 5–15 editorial leads tracked.": "这个阶段的水彩插画师大多会跟进 5–15 条编辑约稿线索。",
  "Competition wins appear on every peer's early CV.": "竞赛获奖出现在每位同侪早期的简历上。",
  "Juried watercolor calls are the fastest route to international credibility.": "评审制的水彩征集是通往国际信誉最快的途径。",
  "The most accessible first-presence format for illustration-adjacent artists.": "对插画相关的艺术家而言，最易上手的首次亮相形式。",
  "Most peers at this stage track 3–8 grants even when not yet eligible.": "这个阶段的多数同侪即便尚不符合资格，也会跟进 3–8 个资助。",

  // ── Strategic pathway ──
  "First Solo Show in Tokyo": "在东京举办首次个展",
  "18–36 months from mid-2026": "自 2026 年中起 18–36 个月",
  "First publication credit": "首个出版履历",
  "First group show in Japan": "在日本的首次联展",
  "2–3 more Tokyo group shows": "再参与 2–3 场东京联展",
  "Bookshop gallery exhibition": "书店画廊展览",
  "Second publication or new zine": "第二本出版物或新的独立刊物",
  "Gallery relationship building": "建立画廊关系",
  "Solo show application or invitation": "个展申请或邀请",
  "Colour Diary (2021) and contribution to defined Definition 02. Publication history established.": "《Colour Diary》（2021）以及为 defined Definition 02 供稿。出版经历已确立。",
  "Tide from China Part 1, ACG_Labo Harajuku, February 2023. First confirmed Japan exhibition on record.": "《潮自中国 第一部》，ACG_Labo 原宿，2023 年 2 月。记录在册的首次日本展览。",
  "Attend openings at target venues consistently. The invitation to a solo show comes from a relationship, not a cold submission — this step runs in parallel with everything else.": "持续出席目标场地的开幕活动。个展的邀请来自关系，而非冷投稿——这一步与其他所有步骤并行。",
  "Target: an intimate Tokyo gallery with a track record of solo shows by international artists at similar career stages. Youkobo Art Space, Gallery Denn, or a bookshop gallery context are realistic first targets.": "目标：一家私密的东京画廊，有为相似事业阶段的国际艺术家举办个展的记录。Youkobo Art Space、Gallery Denn，或书店画廊语境，是现实的首选目标。",
  "Only 1 confirmed group show in Japan. Most Tokyo galleries expect 3–4 group exhibition credits before a solo conversation — so 2–3 more group shows needed. The next group show is the highest-leverage move right now.": "在日本仅有 1 场已确认的联展。多数东京画廊期望在谈个展前先有 3–4 项联展履历——因此还需要 2–3 场联展。眼下，下一场联展是杠杆最高的行动。",
  "Apply for a second group show at a Tokyo artist-run space. 3331 Arts Chiyoda open calls, Design Festa Gallery curated shows, and Gallery IYN open submissions are the realistic near-term entries. Any of these, confirmed and attended, advances the pathway.": "申请在东京某艺术家自营空间参与第二场联展。3331 Arts Chiyoda 的公开征集、Design Festa Gallery 的策展群展，以及 Gallery IYN 的公开投稿，都是现实的近期切入口。其中任何一项，只要确认并参与，都会推进这条路径。",

  // ── Mediums / countries (market stats) ──
  "watercolor": "水彩", "photography": "摄影", "illustration": "插画", "mixed_media": "综合媒材",
  "painting": "绘画", "printmaking": "版画", "drawing": "素描", "any": "不限",
  "United States": "美国", "United Kingdom": "英国", "France": "法国", "Germany": "德国",
  "Singapore": "新加坡", "China": "中国", "Australia": "澳大利亚", "Online": "线上",

  // ── Press features ──
  "Work feature": "作品报道", "Work feature (part 2)": "作品报道（第二部分）",
  "Visual feature of watercolor work — large general audience, no biographical depth": "水彩作品的视觉报道——受众广泛，但无人物深度",
  "Follow-up feature of the same body of work": "对同一批作品的后续报道",
  "Japan's most significant contemporary art publication": "日本最重要的当代艺术刊物",
  "Design and art, illustration-friendly, Tokyo readership": "设计与艺术，对插画友好，东京读者群",
  "Primary English-language illustrator discovery platform globally": "全球首屈一指的英语插画师发掘平台",

  // ── Collaboration ──
  "Tide from China Part 1, Tokyo 2023": "《潮自中国 第一部》，东京 2023",

  // ── Scenario requires-now steps + stragglers ──
  "3–5 Tokyo group shows by 2027 — artist-run spaces first (3331, Design Festa Gallery, Gallery IYN)": "到 2027 年参与 3–5 场东京联展——先从艺术家自营空间开始（3331、Design Festa Gallery、Gallery IYN）",
  "One institutional open call (TOKAS, Youkobo, BankART) by 2028": "到 2028 年投递一次机构公开征集（TOKAS、Youkobo、BankART）",
  "Consistent gallery attendance — build relationships before cold submissions": "持续看展——在冷投递之前先建立关系",
  "Artist statement developed and refined": "完善并打磨艺术家自述",
  "New self-published zine or small book within 12 months — the daily diary content already exists": "12 个月内自出版一本新的独立刊物或小书——每日日记的内容已经现成",
  "Table at Tokyo Art Book Fair 2026 or 2027": "在 2026 或 2027 年东京艺术书展设展位",
  "Submission to Offprint or NY Art Book Fair by 2028": "到 2028 年投递 Offprint 或纽约艺术书展",
  "Publisher relationship with torch press or equivalent — start with introduction, not submission": "与 torch press 或同类出版社建立关系——先从引荐开始，而非投稿",
  "All Publication Track steps": "出版路线的全部步骤",
  "2–3 Tokyo group shows in parallel": "同时参与 2–3 场东京联展",
  "Bookshop gallery show as the bridge (UTRECHT or Book and Sons) — satisfies both tracks simultaneously": "以书店画廊展览作为桥梁（UTRECHT 或 Book and Sons）——同时满足两条路线",
}

// zh for the 2026-06-26 comparable-artist expansion (9 new peers). Kept as a
// SEPARATE object merged into the zh txMap below, so the region keys it shares
// with SF_ZH (USA / Japan / China / Australia) override cleanly instead of
// tripping no-dupe-keys. ja for these peers is a known gap (filled later via the
// translate script); zh is her default and is fully covered here.
const SF_ZH_PEERS = {
  "USA": "美国",
  "Australia": "澳大利亚",
  "UK (Burmese-British)": "英国（缅甸裔英国人）",
  "Japan": "日本",
  "USA (Taiwanese-American)": "美国（台湾裔美国人）",
  "Japan (Polish, Tokyo-based)": "日本（波兰裔，常驻东京）",
  "South Korea": "韩国",
  "China": "中国",

  "Keeps a daily illustrated sketch journal of ordinary life — her home, her neighborhood, meals, small domestic moments — painted in watercolor and pen, the same daily-diary practice GEGYjiji has kept since 2020. Her journal grew directly into a series of published books (Draw Your Day), the publication path GEGYjiji is building toward.": "她坚持每天画一本描绘平凡生活的插画速写日记——自己的家、街区、餐食、细小的居家时刻——用水彩和钢笔记录，正是 GEGYjiji 自 2020 年起延续的那种每日日记式创作。她的日记直接发展成了一系列出版图书（《Draw Your Day》），也正是 GEGYjiji 正在努力走向的出版路径。",
  "Closest model for turning a daily watercolor diary into published books and a sustaining illustration career.": "把每日水彩日记转化为出版图书并维系插画事业的最贴近范本。",
  "daily illustrated diary practice": "每日插画日记的创作习惯",
  "domestic and everyday-life subjects": "居家与日常生活题材",
  "watercolor and ink on paper": "纸本水彩与墨水",
  "diary that grew into published books": "由日记发展为出版图书",
  "audience built on Instagram": "在 Instagram 上积累的受众",

  "A daily watercolor sketchbook artist from Sydney who paints her own life — her cat, teacups, the rooms she sits in, the buildings she passes — and has built a large following and a teaching practice around that habit. The everyday-domestic register and the cat as a recurring anchor closely echo GEGYjiji's diary.": "一位来自悉尼的每日水彩速写本画家，描绘自己的生活——她的猫、茶杯、所处的房间、路过的建筑——并围绕这一习惯建立起庞大的关注群体和教学事业。其日常居家的气质，以及作为反复出现之锚点的猫，都与 GEGYjiji 的日记十分呼应。",
  "Reference for sustaining a daily watercolor practice and turning the habit itself into a community and income.": "维系每日水彩创作、并把这一习惯本身转化为社群与收入的参照。",
  "daily watercolor sketchbook habit": "每日水彩速写本的习惯",
  "cats and domestic life as subjects": "以猫与居家生活为题材",
  "intimate everyday observation": "亲密的日常观察",
  "self-built audience and teaching career": "自我建立的受众与教学事业",

  "A Burmese-British watercolorist who fills sketchbooks with domestic still life — coffee, food, the quiet objects of home — and shares them daily on Instagram, where she has built a large following and a self-published book. An Asian-heritage artist whose career rests on watercolor sketchbooks and an online audience, much like GEGYjiji's.": "一位缅甸裔英国水彩画家，用速写本描绘居家静物——咖啡、食物、家中安静的物件——并每天在 Instagram 上分享，由此积累了庞大的关注者，并出版了自费图书。一位以水彩速写本与线上受众为事业根基的亚裔背景艺术家，与 GEGYjiji 颇为相似。",
  "Reference for building an illustration career on watercolor sketchbooks, an online following, and self-published books.": "以水彩速写本、线上关注与自费出版图书建立插画事业的参照。",
  "watercolor sketchbook practice": "水彩速写本的创作",
  "domestic still life and home objects": "居家静物与家中物件",
  "Asian-heritage illustrator": "亚裔背景的插画家",
  "audience and books built online": "在线上建立的受众与图书",

  "A Tokyo illustrator whose quiet scenes — cafes, apartments, interior light, figures alone in domestic space — share GEGYjiji's stillness and attention to ordinary moments. He works digitally rather than in watercolor, so this is a thematic and tonal kinship more than a material one, but few artists match her register of calm domestic observation so closely.": "一位东京插画家，他笔下安静的场景——咖啡馆、公寓、室内光线、独处于居家空间中的人物——与 GEGYjiji 的静谧和对平凡时刻的注视相通。他以数字绘画而非水彩创作，因此这更是一种题材与气质上的亲缘，而非材料上的相同；但鲜有艺术家能如此贴近她那种平静的居家观察。",
  "Stylistic and tonal reference for quiet, domestic, interior-light storytelling; note the medium is digital, not watercolor.": "用于安静、居家、室内光线叙事的风格与气质参照；请注意其媒介是数字绘画，而非水彩。",
  "quiet domestic and interior scenes": "安静的居家与室内场景",
  "stillness and everyday calm": "静谧与日常的平和",
  "Tokyo-based illustrator": "常驻东京的插画家",
  "atmosphere over incident": "重氛围而非情节",

  "A Taiwanese-American illustrator who keeps a deeply personal sketchbook diary of interior, introspective domestic scenes and built an audience of hundreds of thousands from that practice alone — moving from a day job into a full illustration and gallery career. Her medium is marker rather than watercolor, so the kinship is the diary practice, the domestic-interior subject, and the online-built path, not the surface look.": "一位台湾裔美国插画家，坚持画一本极为私人的速写本日记，描绘室内、内省的居家场景，并仅凭这一创作就积累了数十万受众——从一份正职转向全职插画与画廊事业。她的媒介是马克笔而非水彩，因此这份亲缘在于日记式创作、居家室内题材，以及由线上建立的路径，而非表面的样貌。",
  "Reference for how a private daily sketchbook diary can grow into a full illustration and exhibition career; note medium is marker, not watercolor.": "参照一本私人的每日速写日记如何成长为全职插画与展览事业；请注意其媒介是马克笔，而非水彩。",
  "personal sketchbook diary practice": "私人速写本日记的创作",
  "domestic interior and introspective subjects": "居家室内与内省题材",
  "career built from an online audience": "由线上受众建立的事业",

  "A Tokyo-based painter whose watercolor series of ordinary Tokyo storefronts and streets grew from Instagram into published art books and a sustaining independent career — almost exactly the trajectory GEGYjiji is on. He is Polish rather than Asian, so the overlap is the practice and path: watercolor, quiet Tokyo, online audience to art books.": "一位常驻东京的画家，他以水彩描绘平凡东京店面与街道的系列，从 Instagram 发展为出版画集与可持续的独立事业——几乎正是 GEGYjiji 所走的轨迹。他是波兰人而非亚洲人，因此重合之处在于创作方式与路径：水彩、安静的东京、由线上受众走向画集。",
  "Direct career-path model: watercolor of everyday Tokyo, built from Instagram into published art books and self-sustaining practice.": "直接的事业路径范本：以水彩描绘日常东京，从 Instagram 发展为出版画集与自给自足的创作。",
  "watercolor of ordinary Tokyo": "描绘平凡东京的水彩",
  "quiet urban atmosphere": "安静的城市氛围",
  "online audience grown into art books": "由线上受众发展为画集",
  "independent Tokyo-based career": "常驻东京的独立事业",

  "A Korean illustrator who built the long-running 'Forest Girl's Diary' from a personal blog — a soft, watercolor-style daily diary of a girl's quiet life, updated several times a week — and turned it into bestselling published books. The subject is a fairy-tale forest rather than a Tokyo apartment, so the kinship is the daily-diary engine and the online-to-books path, not the setting.": "一位韩国插画家，她从个人博客起步，创作了长期连载的《森林女孩日记》——一部柔和、水彩风格、描绘一个女孩安静生活的每日日记，每周更新数次——并将其发展为畅销出版图书。题材是童话般的森林而非东京公寓，因此这份亲缘在于每日日记的引擎与由线上走向图书的路径，而非场景本身。",
  "Reference for sustaining a named daily-diary project over years and turning it into a publishing career; the diary format, not the fairy-tale content, is the parallel.": "参照如何将一个具名的每日日记项目维系多年、并发展成出版事业；与之相通的是日记的形式，而非童话的内容。",
  "daily diary as ongoing project": "作为长期项目的每日日记",
  "quiet everyday-life subjects": "安静的日常生活题材",
  "Asian illustrator built from online audience": "由线上受众建立的亚洲插画家",
  "diary grown into published books": "由日记发展为出版图书",

  "A Tokyo painter whose work centers on cats, rendered in watercolor and ink, and who has built a prolific publishing practice — art books, picture books, a gallery-shop of her own — alongside a large following. Her world is surreal and fantastical rather than quiet-domestic, so the kinship is the cat-centered subject and the art-book/publishing career, not the realist register.": "一位东京画家，其作品以猫为核心，以水彩与墨水绘成，并在庞大关注群体之外建立了高产的出版事业——画集、绘本，以及她自己的画廊兼店铺。她的世界超现实而奇幻，而非安静的居家，因此这份亲缘在于以猫为核心的题材与画集／出版事业，而非写实的气质。",
  "Reference for a cats-centered Tokyo painter building a deep art-book and publishing career; note the style is surreal/fantasy, not realist domestic.": "参照一位以猫为核心的东京画家如何建立深厚的画集与出版事业；请注意其风格为超现实／奇幻，而非写实的居家。",
  "cats as central subject": "以猫为核心题材",
  "watercolor and ink medium": "水彩与墨水媒介",
  "prolific art-book and picture-book publishing": "高产的画集与绘本出版",
  "Tokyo-based with own gallery-shop": "常驻东京并拥有自己的画廊店铺",

  "A self-taught Chinese illustrator from Guangdong who built her audience on a Weibo blog from 2010 and turned it into internationally published art books (Song of Sylvan, Ink of Wild) and gallery shows abroad — a Chinese artist who reached an international career through ink-and-watercolor work and an online following. Her imagery is folkloric and fantastical, so the kinship is the Chinese-artist-online-to-art-books path, not the subject.": "一位来自广东的自学成才的中国插画家，自 2010 年起在微博博客上积累受众，并将其发展为在国际出版的画集（《松风》《野作》）以及海外画廊展览——一位通过水墨与水彩作品及线上关注走向国际事业的中国艺术家。她的图像富有民俗与奇幻色彩，因此这份亲缘在于中国艺术家由线上走向画集的路径，而非题材。",
  "Reference for a Chinese illustrator building from an online following to internationally published art books and overseas exhibitions; the path, not the fantasy subject, is the parallel.": "参照一位中国插画家如何从线上关注走向在国际出版的画集与海外展览；与之相通的是路径，而非奇幻题材。",
  "Chinese illustrator": "中国插画家",
  "ink and watercolor medium": "水墨与水彩媒介",
  "audience built online then published": "先在线上建立受众，后获出版",
  "international art-book and gallery career": "国际画集与画廊事业",
}

// zh for her real exhibition CV (Career Position): the exhibition type,
// significance and dates leaked English on the Profile tab (Lore, 2026-06-26).
// zh only — ja isn't selectable in the UI and en is the source. Separate object
// (merged into the zh txMap below) so any key it shares with SF_ZH overrides
// cleanly instead of tripping no-dupe-keys.
const SF_ZH_CV = {
  "Group show": "联展",
  "Solo show": "个展",
  "Exhibition (group/solo not specified on source)": "展览（来源未注明个展或联展）",
  "Group show (official festival poster artists)": "联展（官方节庆海报艺术家）",
  "Group show (6 Chinese illustrators)": "联展（6 位中国插画师）",
  "Group show (museum)": "联展（美术馆）",
  "First exhibition in Japan (stated explicitly in exhibition materials)": "首次在日本展出（展览资料中明确说明）",
  "Institutional (museum) group exhibition": "机构（美术馆）联展",
  "First solo gallery exhibition on record": "记录在册的首次画廊个展",
  "First international (UK) showing on record": "记录在册的首次国际（英国）展出",
  "Solo show in Tokyo — most recent on record": "东京个展——记录在册的最新一场",
  "March–April 2021": "2021 年 3–4 月",
  "March 2021": "2021 年 3 月",
  "March–May 2021": "2021 年 3–5 月",
  "August 2021": "2021 年 8 月",
  "February 4–13, 2023": "2023 年 2 月 4–13 日",
  "October 2024": "2024 年 10 月",
  "November 2024 – February 2025": "2024 年 11 月 – 2025 年 2 月",
  "February–March 2025": "2025 年 2–3 月",
  "December 2025": "2025 年 12 月",
  "January 2026": "2026 年 1 月",
  "April 2026": "2026 年 4 月",
}

// Japanese overrides for the same age/horizon strings (her ja siblings come from
// the backend's _i18n.ja, which can't carry the new neutral-horizon English yet).
// Kept inline (NOT translations.js) and merged into the ja txMap below so the ja
// view also drops the age/countdown framing. Only the strings the review touched.
const SF_JA = {
  "The next few years": "これからの数年",
  "Solo shows, institutional open calls, gallery representation over the next few years.": "個展、公募展、そしてこれからの数年でのギャラリー専属。",
  "Second solo book, international distribution, major book fairs over the next few years.": "これからの数年で2冊目の個人作品集、海外流通、主要なブックフェアへ。",
  "Solid for this stage, especially with a solo collection so early": "この段階としては堅実——とりわけ、早くから初の個人作品集を出していることは大きい",
}

class SectionErrorBoundary extends Component {
  constructor(props) { super(props); this.state = { error: null } }
  static getDerivedStateFromError(err) { return { error: err } }
  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: '12px 16px', background: '#fff8ee', border: '1px solid #e8c97a', borderRadius: 6, margin: '8px 0', fontFamily: 'Georgia, serif', fontSize: 13, color: '#7a4a1a' }}>
          A section failed to render: <code style={{ fontSize: 11 }}>{String(this.state.error)}</code>
        </div>
      )
    }
    return this.props.children
  }
}

// ── Shared primitives ──────────────────────────────────────────────────────

// Each Saffron tab shows its first section open and the rest collapsed to their
// summary — one consistent rule across every tab (Scott: inconsistency is worse
// than either choice). A section's own defaultOpen prop still wins when set; a
// section with no prop inherits this context (true outside any provider, so
// nothing changes for surfaces that don't opt in).
const SectionOpenContext = createContext(true)

function SectionShell({ title, subtitle, summary, defaultOpen, children }) {
  const ctxDefault = useContext(SectionOpenContext)
  const initialOpen = defaultOpen !== undefined ? defaultOpen : ctxDefault
  const [open, setOpen] = useState(initialOpen)
  return (
    <section className={`sf-section${open ? '' : ' sf-section--closed'}`}>
      <button className="sf-toggle-header" onClick={() => setOpen(o => !o)}>
        <div className="sf-toggle-text">
          <h2 className="sf-section-title">{title}</h2>
          {open
            ? subtitle && <p className="sf-section-subtitle">{subtitle}</p>
            : summary  && <p className="sf-section-summary">{summary}</p>
          }
        </div>
        <span className={`sf-chevron${open ? ' sf-chevron--open' : ''}`}>▾</span>
      </button>
      {open && <div className="sf-section-body">{children}</div>}
    </section>
  )
}

function EmptyState({ message }) {
  return <p className="sf-empty-state">{message}</p>
}

// Any external name (venue, outlet) → a search link so she can look it up.
function sfSearch(name) {
  return `https://www.google.com/search?q=${encodeURIComponent(name || '')}`
}

// A grant's link: its own application/info page when we can find one, otherwise a
// name search. The `apply` field often leads with a bare domain ("acc.org — …"),
// so pull the first domain-looking token; fall back to website/url, then search.
function grantHref(grant) {
  if (grant.website) return grant.website
  if (grant.url) return grant.url
  const apply = String(grant.apply || '')
  const m = apply.match(/([a-z0-9-]+\.)+[a-z]{2,}(\/[^\s]*)?/i)
  if (m) {
    const dom = m[0]
    return dom.startsWith('http') ? dom : `https://${dom}`
  }
  return sfSearch(grant.name)
}

// A revenue stream only gets a link when it points at a real, specific resource
// — a known platform actually named in the stream. Concept rows (commissions,
// sharing originals, consignment) have no single URL, so they render as plain
// text rather than a useless web-search link (Scott, 2026-06-26: "if it's not a
// specific resource, don't have a link").
const REVENUE_PLATFORM_URL = { 'SUZURI': 'https://suzuri.jp/', 'Booth.pm': 'https://booth.pm/' }
function revenueHref(item) {
  if (item.website) return item.website
  if (item.url) return item.url
  const hay = `${item.stream || ''} ${item.description || ''}`
  const hit = Object.keys(REVENUE_PLATFORM_URL).find(p => hay.includes(p))
  return hit ? REVENUE_PLATFORM_URL[hit] : null
}

// Humanize a raw activity status (e.g. "in_contact") into a readable label.
function actStatusLabel(status, t) {
  const key = `sf.actStatus.${status}`
  const v = t(key)
  if (v && v !== key) return v
  return String(status || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}


// ── Original four sections ─────────────────────────────────────────────────

// A real "where you stand" read for Career Position — authored copy (not a
// count), truthful to her record and stable as counts change. Opens the section
// so it actually tells her her position instead of only listing what she's done.
const CAREER_SYNOPSIS = {
  en: "You're an actively exhibiting artist — solo and group shows across China, Japan and abroad, including museum group shows and a Tokyo solo — with a first solo publication and an established, growing audience. The foundation is real. From here it's less about adding credits and more about depth: gallery relationships, a representation conversation if you ever want one, and the book practice your daily work already feeds.",
  zh: "你是一位持续在办展的艺术家——个展与联展遍及中国、日本及海外，其中包括美术馆群展，以及一场东京个展——还有首部个人出版物，和一群稳定、持续增长的受众。根基是扎实的。接下来与其说是再添履历，不如说是往深处走：画廊关系、（如果你愿意）一次代理的洽谈，以及你的日常创作本就在滋养的那条出版之路。",
  ja: "あなたは継続的に発表を続けているアーティストです——中国・日本・海外での個展とグループ展、美術館でのグループ展、そして東京での個展まで——さらに初の個人作品集と、確立された、伸び続けるオーディエンスがあります。土台は確かです。ここから先は、実績を足すことよりも深さです——ギャラリーとの関係、望むなら専属の話、そして日々の制作がすでに育てている本の実践。",
}
const CAREER_SUMMARY = {
  en: 'Actively exhibiting — solo, group, museum & international shows, a first book, an established audience.',
  zh: '持续办展——个展、联展、美术馆与海外展，首部作品集，稳定的受众。',
  ja: '継続的に発表——個展・グループ展・美術館・海外展、初の作品集、確立されたオーディエンス。',
}

function CareerPosition({ data, t }) {
  const { lang } = useLanguage()
  const ig = data.social.find(s => s.platform === 'Instagram')
  // Her record is the exhibitions + publications. Social handles, education, and
  // home base are things she already knows — they were removed from this section
  // (no value to her). Instagram now lives ONCE in the app as the audience fact.
  const summary = CAREER_SUMMARY[lang] || CAREER_SUMMARY.en

  const igStr = ig?.followers || '26k'
  // "You're here" markers — NOT progress-to-target rings. The old rings rendered
  // a strength half-empty (e.g. an established count shown as "52% to 50k"), which contradicts the app's own
  // "growth is a bonus, not a requirement." A marker states where she stands; it
  // never fills a fraction of a goal she didn't set.
  const markers = [
    { id: 'ig',    label: t('sf.mile.followers'), current: igStr,                            color: '#c47a35' },
    { id: 'shows', label: t('sf.mile.shows'),     current: String(data.exhibitions.length),  color: '#7a9e7e' },
    { id: 'pub',   label: t('sf.mile.pubs'),      current: String(data.publications.length), color: '#c49a3e' },
  ]

  return (
    <SectionShell
      title={t('sf.sec.careerPosition')}
      subtitle={t('sf.sub.careerPosition')}
      summary={summary}
    >
      <p className="sf-career-synopsis">{CAREER_SYNOPSIS[lang] || CAREER_SYNOPSIS.en}</p>
      <div className="sf-rings">
        {markers.map(mk => <MilestoneMarker key={mk.id} {...mk} />)}
      </div>

      <div className="sf-career-grid">
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.exhibitions')}</div>
          {data.exhibitions.map((ex, i) => (
            <div key={i} className="sf-career-row">
              <span className="sf-check">✓</span>
              <div className="sf-career-row-body">
                <div className="sf-row-title">{ex.title}</div>
                <div className="sf-row-sub">{ex.venue} · {ex.date}</div>
                <div className="sf-row-meta">{ex.type} · {ex.note}</div>
              </div>
            </div>
          ))}
        </div>
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.publications')}</div>
          {data.publications.map((pub, i) => (
            <div key={i} className="sf-career-row">
              <span className="sf-check">✓</span>
              <div className="sf-career-row-body">
                <div className="sf-row-title">{pub.title}{pub.year ? ` (${pub.year})` : ''}</div>
                <div className="sf-row-meta">{pub.type}</div>
              </div>
            </div>
          ))}
        </div>
        {/* Social handles, education, and home base removed — she already knows
            her own handles, where she studied, and where she lives. Instagram is
            stated ONCE here, as the audience fact ("an established, growing
            following"), not repeated as a handle row / benchmark / geo line. */}
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.audience')}</div>
          <div className="sf-row-title">{t('sf.audience.fact')}</div>
        </div>
      </div>
    </SectionShell>
  )
}

// Confirmed Instagram handles for the comparable artists (verified Jun 2026).
// Anyone not listed falls back to a name search.
const PEER_IG = {
  'Chien Chung-Wei (簡忠威)': 'chien_chung_wei',
  'Keiko Tanabe':            'keikotanabewatercolor',
  'Thomas W. Schaller':      'thomaswschaller',
  'Cathy Read':              'cathyreadart',
  'Alvaro Castagnet':        'alvaro.castagnet',
  'Jean Haines':             'jeanhaines',
  // 2026-06-26 expansion (verified handles). Zao Dao has no clean Instagram —
  // she falls through to a name search.
  'Samantha Dion Baker':     'sdionbakerdesign',
  'Liz Steel':               'lizsteelart',
  'Ohn Mar Win':             'ohn_mar_win',
  'Tatsuro Kiuchi (木内達朗)': 'tatsurokiuchi',
  'Felicia Chiao':           'feliciachiao',
  'Mateusz Urbanowicz':      'mateusz_urbanowicz',
  'Aeppol (애뽈)':            '_aeppol',
  'Yuko Higuchi (ヒグチユウコ)': 'yukohiguchi3',
}

function ComparableArtists({ artists, t }) {
  // Show a generous set (Scott, 2026-06-26: "needs more people"). With the new
  // verified peers sorted ahead by fit, this keeps her existing good comps AND
  // the closer daily-diary / illustration-community ones.
  const top     = artists.slice(0, 13)
  const summary = t('sf.sum.peers', { n: top.length })
  return (
    <SectionShell
      title={t('sf.sec.peers')}
      subtitle={t('sf.sub.peers')}
      summary={summary}
    >
      <p className="sf-peers-caveat">{t('sf.label.peersCaveat')}</p>
      <div className="sf-peers-grid">
        {top.map((a, i) => (
          <div key={i} className="sf-peer-card">
            <a
              className="sf-peer-name sf-peer-link"
              href={PEER_IG[a.name] ? `https://www.instagram.com/${PEER_IG[a.name]}/` : sfSearch(`${a.name} instagram`)}
              target="_blank"
              rel="noreferrer"
            >
              {a.name} ↗
            </a>
            <div className="sf-peer-region">{a.region}</div>
            <div className="sf-peer-reason">{a.fit_reason}</div>
            <div className="sf-peer-traits">
              {a.shared_traits.map((tr, j) => <span key={j} className="sf-trait">{tr}</span>)}
            </div>
            <div className="sf-peer-use">{t('sf.label.useAs')} {a.use_as}</div>
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

// "more / 具体怎么做" toggle labels for the shy-friendly concrete-tactics
// disclosure on the strategy steps. Permission-framed, never a script.
const SHY_TIPS_MORE = { zh: '具体怎么做 ▾', ja: '具体的にどうする ▾', en: 'More — what this looks like ▾' }
const SHY_TIPS_HIDE = { zh: '收起', ja: '閉じる', en: 'Hide' }

// Render the multi-line tips string as an intro line + bullet list (lines that
// start with "•"). Keeps the warm, optional register; no markdown artifacts.
function ShyTips({ text, lang }) {
  const [open, setOpen] = useState(false)
  if (!text) return null
  const lines = String(text).split('\n').map(l => l.trim()).filter(Boolean)
  const intro = lines.filter(l => !l.startsWith('•'))
  const bullets = lines.filter(l => l.startsWith('•')).map(l => l.replace(/^•\s*/, ''))
  return (
    <div className="sf-shy-tips">
      <button className="sf-shy-tips-toggle" onClick={() => setOpen(o => !o)}>
        {open ? (SHY_TIPS_HIDE[lang] || SHY_TIPS_HIDE.en) : (SHY_TIPS_MORE[lang] || SHY_TIPS_MORE.en)}
      </button>
      {open && (
        <div className="sf-shy-tips-body">
          {intro[0] && <p className="sf-shy-tips-intro">{intro[0]}</p>}
          {bullets.length > 0 && (
            <ul className="sf-shy-tips-list">
              {bullets.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          )}
          {intro.slice(1).map((p, i) => <p key={i} className="sf-shy-tips-outro">{p}</p>)}
        </div>
      )}
    </div>
  )
}

function StrategicPathway({ data, t }) {
  const { lang } = useLanguage()
  const done    = data.steps.filter(s => s.done).length
  const summary = `${data.goal} · ${done} / ${data.steps.length}`
  return (
    <SectionShell
      title={t('sf.sec.pathway', { goal: data.goal })}
      subtitle={t('sf.sub.pathway', { timeline: data.timeline_estimate })}
      summary={summary}
    >
      <div className="sf-steps">
        {data.steps.map((step) => (
          <div key={step.n} className={`sf-step ${step.done ? 'sf-step--done' : step.blocking ? 'sf-step--blocking' : 'sf-step--pending'}`}>
            <div className="sf-step-marker">{step.done ? '✓' : step.blocking ? '▶' : '○'}</div>
            <div className="sf-step-body">
              <div className="sf-step-label">{step.label}</div>
              <div className="sf-step-detail">{step.detail}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="sf-pathway-callout sf-pathway-blocking">
        <div className="sf-callout-label">{t('sf.label.whatBlocking')}</div>
        <p className="sf-callout-text">{data.blocking_now}</p>
      </div>
      <div className="sf-pathway-callout sf-pathway-next">
        <div className="sf-callout-label">{t('sf.label.nextMove')}</div>
        <p className="sf-callout-text">{data.next_move}</p>
        {data.shy_tips && <ShyTips text={data.shy_tips} lang={lang} />}
      </div>
    </SectionShell>
  )
}

// ── New sections ───────────────────────────────────────────────────────────

// (InstagramStrategy and AudienceGeography sections removed 2026-06-25 — the
//  Profile tab no longer repeats Instagram across multiple panels. Instagram is
//  stated once, as the audience fact in CareerPosition; the panel's one useful
//  bit, the weekly-rhythm cadence tip, was salvaged into Career Readiness.)

const ASSESSMENT_KEYS = {
  strong:        'sf.assess.strong',
  on_track:      'sf.assess.on_track',
  below_typical: 'sf.assess.below_typical',
  weak:          'sf.assess.weak',
  unknown:       'sf.assess.unknown',
}
const ASSESSMENT_COLORS = {
  strong: '#5a7a30', on_track: '#7a9a40', below_typical: '#c47a35', weak: '#b03020',
  unknown: '#9a8a70',
}

const BENCHMARKS_SUMMARY = {
  en: 'Where you sit at or above the typical range for your stage — your strongest dimensions.',
  zh: '在你这个阶段，你处于或高于典型区间的那几项——你最强的维度。',
  ja: 'あなたの段階で、典型的な範囲と同等か上にある面——あなたの強み。',
}
function CareerBenchmarks({ data, t }) {
  const { lang } = useLanguage()
  // Never compare her unfavorably (Scott): show only the dimensions where she's
  // at or above the typical band. Growth areas live — positively — in Career
  // Readiness, not as a peer deficit here. If nothing is favorable yet, the
  // section simply doesn't appear.
  // Filter on the API's stable `favorable` boolean (the assessment string gets
  // deep-translated in zh, so matching on it would wrongly hide everything).
  // Also drop the pure-Instagram-followers dimension: Instagram is now stated
  // ONCE, as the audience fact in CareerPosition — it shouldn't reappear here as
  // a benchmark row. `peer_high === '100k+'` uniquely + translation-stably tags
  // that row (numbers/symbols don't get deep-translated).
  const favorable = (data.peer_range || []).filter(r => r.favorable && r.peer_high !== '100k+')
  if (favorable.length === 0) return null
  // Collapsed summary: a readable synopsis, not raw counts (Scott, 2026-06-26).
  const summary = BENCHMARKS_SUMMARY[lang] || BENCHMARKS_SUMMARY.en
  return (
    <SectionShell
      title={t('sf.sec.benchmarks')}
      subtitle={t('sf.sub.benchmarks')}
      summary={summary}
    >
      <p className="sf-peers-caveat">{t('sf.cr.peerStrengths')}</p>
      <div className="sf-benchmark-grid">
        {favorable.map((row, i) => {
          const color = ASSESSMENT_COLORS[row.assessment] || ASSESSMENT_COLORS.on_track
          const label = t(ASSESSMENT_KEYS[row.assessment] || 'sf.assess.on_track')
          return (
            <div key={i} className="sf-benchmark-row">
              <div className="sf-benchmark-dimension">{row.dimension}</div>
              <div className="sf-benchmark-artist">{row.artist_value}</div>
              <div className="sf-benchmark-range">
                <span className="sf-range-label">{t('sf.label.peers')} </span>
                {row.peer_low} → {row.peer_typical} → {row.peer_high}
              </div>
              <div className="sf-benchmark-tag" style={{ color }}>{label}</div>
              <div className="sf-benchmark-note">{row.note}</div>
            </div>
          )
        })}
      </div>
    </SectionShell>
  )
}

const SF_MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December']

// A "缺口/gap" tag reads as quantified failure to a sensitive user; reframe any
// hard-coded deficit label in this component as an opportunity ("机会/opportunity").
const OPP_LABEL = { zh: '机会', ja: 'チャンス', en: 'opportunity' }

// ── Recurrence / rolling-deadline phrase localization ──────────────────────
// Many opportunities carry a recurrence phrase instead of a date ("Rolling",
// "Twice-yearly (spring/autumn)"). The calendar rendered `o.deadline` raw, so
// these English phrases leaked into the zh (and ja) view — the last real zh
// leak on the most-scanned surface. This maps the known recurrence phrases (and
// common leading tokens) to localized equivalents. Date-only strings and
// anything unmapped pass through unchanged (graceful partial coverage).
const RECURRENCE_PHRASES = {
  zh: {
    'Rolling': '常年开放',
    'Rolling applications': '常年开放',
    'Rolling consignment': '常年寄售',
    'Twice-yearly': '每年两次',
    'Twice-yearly (spring/autumn)': '每年两次（春/秋）',
    'Annual': '每年一次',
    'Quarterly': '每季度一次',
    'Monthly': '每月一次',
    'Ongoing': '持续开放',
    'ongoing': '持续开放',
    'No fixed deadline': '无固定截止日期',
    'No fixed deadline — ongoing, proposal-based': '无固定截止日期 — 持续开放，提案制',
    'No fixed deadline — rotating exhibitions ongoing': '无固定截止日期 — 轮换展览持续进行',
    'Seasonal': '季节性',
    'Varies': '时间不定',
    'TBD': '待定',
  },
  ja: {
    'Rolling': '通年受付',
    'Rolling applications': '通年受付',
    'Rolling consignment': '通年委託',
    'Twice-yearly': '年2回',
    'Twice-yearly (spring/autumn)': '年2回（春/秋）',
    'Annual': '年1回',
    'Quarterly': '四半期ごと',
    'Monthly': '毎月',
    'Ongoing': '随時',
    'ongoing': '随時',
    'No fixed deadline': '締切なし',
    'No fixed deadline — ongoing, proposal-based': '締切なし — 随時、提案制',
    'No fixed deadline — rotating exhibitions ongoing': '締切なし — 巡回展示を随時開催',
    'Seasonal': '季節限定',
    'Varies': '時期未定',
    'TBD': '未定',
  },
}

// Localize a deadline/recurrence string for the current language. Tries a whole-
// string match first, then the part before an em/en-dash, then the leading word.
// Anything still unmatched (dates, proper nouns) returns unchanged.
function localizeDeadline(raw, lang) {
  if (!raw || lang === 'en') return raw
  const map = RECURRENCE_PHRASES[lang]
  if (!map) return raw
  const s = String(raw).trim()
  if (map[s]) return map[s]
  // "Rolling (multiple deadlines: ...)" / "Annual — 2026 cycle closed ..." etc.
  const lead = s.split(/\s*[—–-]\s*|\s*\(/)[0].trim()
  if (lead && map[lead]) {
    const rest = s.slice(s.indexOf(lead) + lead.length)
    return map[lead] + rest
  }
  const firstWord = s.split(/[\s(]/)[0]
  if (firstWord && map[firstWord]) {
    return map[firstWord] + s.slice(firstWord.length)
  }
  return raw
}

function SeasonalCalendar({ data, t, lang }) {
  const known = data.months.reduce((n, m) => n + m.opportunities.length, 0)
  const summary = t('sf.sum.calendarUnknown', { known, n: data.unknown_deadline_count, s: data.unknown_deadline_count !== 1 ? 's' : '' })
  const calMonths = t('cal.months')
  const calWeekdays = t('cal.weekdays')
  const [monthOffset, setMonthOffset] = useState(0)
  const [selectedKey, setSelectedKey] = useState(null)

  const locName = (o) =>
    (lang === 'zh' && o.name_zh) ? o.name_zh : (lang === 'ja' && o.name_ja) ? o.name_ja : o.name
  const catLabel = (c) => tfb(t, `cat.${c}`, c)
  const monthLabel = (m) => {
    const idx = SF_MONTHS_EN.indexOf(m)
    return idx >= 0 && Array.isArray(calMonths) ? calMonths[idx] : m
  }

  // Build the byDate map that drives the literal month grid.
  const now = new Date(); now.setHours(0, 0, 0, 0)
  const todayKey = keyOf(now)
  const byDate = new Map()
  for (const m of data.months) {
    for (const o of m.opportunities) {
      let d = o.date ? new Date(o.date + 'T00:00:00') : null
      if (!d || isNaN(d.getTime())) d = parseDeadline(o.deadline)
      if (!d) continue
      const key = keyOf(d)
      if (!byDate.has(key)) byDate.set(key, { date: d, opps: [] })
      byDate.get(key).opps.push(o)
    }
  }
  const monthBase = new Date(now.getFullYear(), now.getMonth() + monthOffset, 1)
  const selectedOpps = selectedKey ? (byDate.get(selectedKey)?.opps || []) : null

  // Every entry links out — its own page when we have a URL, otherwise a web
  // search for the name (same fallback Saffron's press rows use). A list with no
  // way to act on any row isn't useful.
  const oppRow = (o, i, withDeadline = true) => (
    <div key={i} className={`sf-cal-opp${withDeadline ? '' : ' sf-cal-opp--rolling'}`}>
      <span className="sf-cal-cat">{catLabel(o.category)}</span>
      <a className="sf-cal-name sf-ext-link" href={o.url || sfSearch(locName(o))} target="_blank" rel="noreferrer">{locName(o)} ↗</a>
      {withDeadline && o.deadline && <span className="sf-cal-dl">{localizeDeadline(o.deadline, lang)}</span>}
    </div>
  )

  return (
    <SectionShell
      title={t('sf.sec.calendar')}
      subtitle={t('sf.sub.calendar')}
      summary={summary}
    >
      {/* The literal calendar: a real month grid; click a marked day to filter the list. */}
      {byDate.size > 0 && (
        <CalendarMonth
          byDate={byDate}
          base={monthBase}
          calMonths={calMonths}
          calWeekdays={calWeekdays}
          todayKey={todayKey}
          selectedKey={selectedKey}
          onSelect={setSelectedKey}
          onShift={(dir) => { setSelectedKey(null); setMonthOffset(o => Math.max(0, o + dir)) }}
          canGoBack={monthOffset > 0}
        />
      )}
      {selectedKey && (
        <button className="cal-clear-sel" onClick={() => setSelectedKey(null)}>{t('cal.showAll')}</button>
      )}

      {/* The comprehensive list (Scott: keep it — now with links + localized names). */}
      {data.months.length === 0 ? (
        <EmptyState message={t('sf.empty.calendar')} />
      ) : selectedOpps ? (
        <div className="sf-calendar">
          <div className="sf-cal-month">
            <div className="sf-cal-opps">{selectedOpps.map((o, j) => oppRow(o, j))}</div>
          </div>
        </div>
      ) : (
        <div className="sf-calendar">
          {data.months.map((m, i) => (
            <div key={i} className="sf-cal-month">
              <div className="sf-cal-month-name">{monthLabel(m.month)}</div>
              <div className="sf-cal-opps">{m.opportunities.map((o, j) => oppRow(o, j))}</div>
            </div>
          ))}
        </div>
      )}

      {data.rolling.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <div className="sf-block-label">{t('sf.label.rolling', { n: data.rolling.length })}</div>
          <div className="sf-cal-rolling">
            {data.rolling.map((o, i) => oppRow(o, i, false))}
          </div>
        </div>
      )}
      <div style={{ marginTop: 24 }}>
        <div className="sf-block-label">{t('sf.label.prepLeadTimes')}</div>
        <div className="sf-lead-times">
          {Object.entries(data.preparation_lead_times).map(([k, v], i) => (
            <div key={i} className="sf-lead-row">
              <span className="sf-lead-type">{k.replace(/_/g, ' ')}</span>
              <span className="sf-lead-time">{v}</span>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function PressFeatures({ data, t }) {
  const total   = data.confirmed.length
  const summary = t('sf.sum.pressFeatures', { n: total, s: total !== 1 ? 's' : '' })
  return (
    <SectionShell
      title={t('sf.sec.press')}
      subtitle={t('sf.sub.press')}
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('sf.label.confirmed')}</div>
          {data.confirmed.map((f, i) => (
            <div key={i} className="sf-press-row">
              <a className="sf-press-outlet sf-ext-link" href={sfSearch(f.outlet)} target="_blank" rel="noreferrer">{f.outlet} ↗</a>
              <div className="sf-press-type">{f.type}</div>
              <div className="sf-press-note">{f.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">{t('sf.label.pitchTargets')}</div>
          {data.pitch_targets.map((pt, i) => (
            <div key={i} className="sf-pitch-row">
              <a className="sf-pitch-outlet sf-ext-link" href={sfSearch(pt.outlet)} target="_blank" rel="noreferrer">{pt.outlet} ↗</a>
              <div className="sf-pitch-why">{pt.why}</div>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

const COLLECTOR_FIT_LABEL   = { zh: '对你而言：', ja: 'あなたにとって：', en: 'For you:' }
const COLLECTOR_HOWTO_LABEL = { zh: '怎么开始（都可选）', ja: '始め方（すべて任意）', en: 'Where to start (all optional)' }

// Rebuilt 2026-06-26: real, verified channels where collectors of her kind of
// work gather + a low-pressure how-to, replacing the old "the pipeline tracks
// opportunities, not buyers" non-answer. Reuses the collaboration card styling.
function CollectorEcosystem({ lang }) {
  const d = localizeDeep(COLLECTOR_ECOSYSTEM, lang)
  return (
    <SectionShell title={d.title} summary={d.summary}>
      <p className="sf-info-text" style={{ marginTop: 0, marginBottom: 18 }}>{d.intro}</p>
      <div className="sf-collab-entries">
        {d.channels.map((c, i) => (
          <div key={i} className="sf-collab-entry">
            <a className="sf-collab-link sf-ext-link" href={c.link} target="_blank" rel="noreferrer">{c.name} ↗</a>
            <p className="sf-collab-who">{c.what}</p>
            <div className="sf-collab-try">
              <span className="sf-collab-try-label">{COLLECTOR_FIT_LABEL[lang] || COLLECTOR_FIT_LABEL.en}</span>
              {c.fit_for_her}
            </div>
          </div>
        ))}
      </div>
      <div className="sf-collab-howto">
        <div className="sf-block-label">{COLLECTOR_HOWTO_LABEL[lang] || COLLECTOR_HOWTO_LABEL.en}</div>
        <ol className="sf-collab-howto-list">
          {d.how_to.map((s, i) => <li key={i}>{s.step}</li>)}
        </ol>
      </div>
    </SectionShell>
  )
}

// ── Press Kit ──────────────────────────────────────────────────────────────
// A real, ready-to-use press kit generated from her profile + a how-to, because
// the app tells her to "have a press kit ready" (Scott, 2026-06-26). Fields carry
// {en,zh,ja}; the full draft is behind a disclosure so the section stays calm.
const PK_USE_LABEL    = { zh: '怎么用', ja: '使い方', en: 'How to use it' }
const PK_UPDATE_LABEL = { zh: '怎么保持更新', ja: '更新の仕方', en: 'Keeping it updated' }
const PK_SHOW = { zh: '看一份可直接用的样本 ▾', ja: 'そのまま使えるサンプルを見る ▾', en: 'See a ready-to-use sample ▾' }
const PK_HIDE = { zh: '收起样本', ja: 'サンプルを閉じる', en: 'Hide sample' }
const PK_F = {
  oneLine:   { zh: '一句话简介', ja: '一行プロフィール', en: 'One-line bio' },
  shortBio:  { zh: '简短简介', ja: 'ショートバイオ', en: 'Short bio' },
  longBio:   { zh: '完整简介', ja: 'ロングバイオ', en: 'Long bio' },
  statement: { zh: '艺术家自述', ja: 'アーティストステートメント', en: 'Artist statement' },
  factSheet: { zh: '资料速览', ja: 'ファクトシート', en: 'Fact sheet' },
  works:     { zh: '代表作 / 系列', ja: '代表作・シリーズ', en: 'Selected works' },
  images:    { zh: '配图建议', ja: '画像のガイド', en: 'Image guidance' },
  press:     { zh: '媒体报道', ja: 'メディア掲載', en: 'Press' },
}
const pkPick = (f, lang) => (f && (f[lang] || f.en)) || ''
const pkList = (f, lang) => (f && (f[lang] || f.en)) || []

function PressKit({ lang }) {
  const [open, setOpen] = useState(false)
  return (
    <SectionShell title={pkPick(PRESS_KIT.title, lang)} summary={pkPick(PRESS_KIT.summary, lang)}>
      <p className="sf-info-text" style={{ marginTop: 0 }}>{pkPick(PRESS_KIT.intro, lang)}</p>

      <div className="sf-block-label" style={{ marginTop: 16 }}>{PK_USE_LABEL[lang] || PK_USE_LABEL.en}</div>
      <ol className="sf-collab-howto-list">
        {pkList(PRESS_KIT.how_to_use, lang).map((s, i) => <li key={i}>{s}</li>)}
      </ol>
      <div className="sf-block-label" style={{ marginTop: 14 }}>{PK_UPDATE_LABEL[lang] || PK_UPDATE_LABEL.en}</div>
      <ol className="sf-collab-howto-list">
        {pkList(PRESS_KIT.how_to_update, lang).map((s, i) => <li key={i}>{s}</li>)}
      </ol>

      <button className="sf-pk-toggle" onClick={() => setOpen(o => !o)}>
        {open ? (PK_HIDE[lang] || PK_HIDE.en) : (PK_SHOW[lang] || PK_SHOW.en)}
      </button>
      {open && (
        <div className="sf-pk-sample">
          {[
            ['oneLine', PRESS_KIT.one_line, 'text'],
            ['shortBio', PRESS_KIT.short_bio, 'text'],
            ['longBio', PRESS_KIT.long_bio, 'text'],
            ['statement', PRESS_KIT.statement, 'text'],
            ['factSheet', PRESS_KIT.fact_sheet, 'list'],
            ['works', PRESS_KIT.selected_works, 'list'],
            ['images', PRESS_KIT.image_guidance, 'list'],
          ].map(([key, field, kind]) => (
            <div key={key} className="sf-pk-field">
              <div className="sf-pk-label">{PK_F[key][lang] || PK_F[key].en}</div>
              {kind === 'text'
                ? <p className="sf-pk-text">{pkPick(field, lang)}</p>
                : <ul className="sf-pk-ul">{pkList(field, lang).map((s, i) => <li key={i}>{s}</li>)}</ul>}
            </div>
          ))}
          <div className="sf-pk-field">
            <div className="sf-pk-label">{PK_F.press[lang] || PK_F.press.en}</div>
            <ul className="sf-pk-ul">
              {PRESS_KIT.press.map((p, i) => (
                <li key={i}><a className="sf-ext-link" href={p.url} target="_blank" rel="noreferrer">{p.outlet} — {p.type} ↗</a></li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </SectionShell>
  )
}

const COLLAB_TRY_LABEL  = { zh: '可以一起做：', ja: '一緒にできること：', en: 'You could try:' }
const COLLAB_HOWTO_LABEL = { zh: '如何开启一次合作', ja: 'コラボの始め方', en: 'How to approach a collaboration' }

// Rebuilt 2026-06-26: real, verified collaboration targets (named, linked, with
// a concrete collab form) in three honest groups, plus a low-pressure how-to —
// replacing the old "5 strangers with status: unknown" list. Authored content
// from saffron_insights.js, localized via localizeDeep (zh baked, ja → en).
function CollaborationMap({ lang }) {
  const d = localizeDeep(COLLABORATION_MAP, lang)
  return (
    <SectionShell title={d.title} summary={d.summary}>
      {d.lead && <p className="sf-info-text" style={{ marginTop: 0, marginBottom: 18 }}>{d.lead}</p>}
      {d.groups.map((g, gi) => (
        <div key={gi} className="sf-collab-group">
          <div className="sf-block-label">{g.label}</div>
          <div className="sf-collab-entries">
            {g.entries.map((e, ei) => (
              <div key={ei} className="sf-collab-entry">
                <a className="sf-collab-link sf-ext-link" href={e.link} target="_blank" rel="noreferrer">{e.name} ↗</a>
                <p className="sf-collab-who">{e.who}</p>
                <p className="sf-collab-why">{e.why_fit}</p>
                <div className="sf-collab-try">
                  <span className="sf-collab-try-label">{COLLAB_TRY_LABEL[lang] || COLLAB_TRY_LABEL.en}</span>
                  {e.collab_form}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <div className="sf-collab-howto">
        <div className="sf-block-label">{COLLAB_HOWTO_LABEL[lang] || COLLAB_HOWTO_LABEL.en}</div>
        <ol className="sf-collab-howto-list">
          {d.how_to.map((s, i) => <li key={i}>{s}</li>)}
        </ol>
      </div>
    </SectionShell>
  )
}

// (GeographicExpansion removed 2026-06-25 with the Landscape tab.)

const PUBLICATION_SUMMARY = {
  en: 'Where to publish next — from zines to art books — and the two titles you already have.',
  zh: '下一步去哪出版——从独立刊物到艺术书——以及你已有的两部作品。',
  ja: '次にどこで出すか——zineからアートブックまで——そして、すでにある2冊。',
}
function PublicationLandscape({ data, t }) {
  const { lang } = useLanguage()
  const summary = PUBLICATION_SUMMARY[lang] || PUBLICATION_SUMMARY.en
  return (
    <SectionShell
      title={t('sf.sec.publication')}
      subtitle={t('sf.sub.publication')}
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('sf.label.herPubs')}</div>
          {data.artist_publications.map((p, i) => (
            <div key={i} className="sf-press-row">
              <div className="sf-press-outlet">{p.title}{p.year ? ` · ${p.year}` : ''}</div>
              <div className="sf-press-type">{p.type}</div>
              <div className="sf-press-note">{p.note}</div>
            </div>
          ))}

          {data.artist_intent && (
            <div className="sf-peppercorn-answer" style={{ marginTop: 16 }}>
              <div className="sf-block-label">{t('sf.label.pubIntent')}</div>
              <div className="sf-answer-bubble">{data.artist_intent}</div>
            </div>
          )}

          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.label.pubTiers')}</div>
          {data.tiers.map((tier, i) => (
            <div key={i} className="sf-pub-tier">
              <div className="sf-pub-tier-header">
                <span className="sf-pub-tier-name">{tier.tier}</span>
                <span className={`sf-pub-barrier sf-pub-barrier--${tier.barrier}`}>
                  {tfb(t, `sf.barrier.${tier.barrier}`, tier.barrier)}
                </span>
              </div>
              <div className="sf-pub-examples">{tier.examples.join(' · ')}</div>
              <div className="sf-pub-note">{tier.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">{t('sf.label.topTargets', { n: data.top_targets.length })}</div>
          {data.top_targets.map((o, i) => (
            <div key={i} className="sf-pub-target">
              <span className="sf-pub-target-name">{o.name}</span>
              <span className="sf-pub-target-cat">{o.category}</span>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function LongTermScenarios({ data, t }) {
  // These are her three possible LIVES, not bets. We label them by FIT/alignment,
  // never probability — and no dream-path gets a red "unlikely" tag. Red (#b03020)
  // is retired here; the lowest band is a warm neutral, not a warning.
  const FIT_COLORS = { high: '#5a7a30', moderate: '#c47a35', low: '#a07a45' }
  // fit/alignment relabel: 高→最契合, 中→契合, 低→可选 (most-fitting / fitting /
  // an option) — kept local so it overrides the en/ja/zh "probability" strings
  // without touching the shared translations file.
  const FIT_LABELS = {
    zh: { high: '最契合', moderate: '契合', low: '可选' },
    ja: { high: '最も合う', moderate: '合う', low: '選択肢' },
    en: { high: 'best fit', moderate: 'good fit', low: 'an option' },
  }
  const { lang } = useLanguage()
  const fitLabel = (p) => (FIT_LABELS[lang] || FIT_LABELS.en)[p] || (FIT_LABELS.en[p] || p)
  const summary = `3 paths · ${data.horizon}`
  return (
    <SectionShell
      title={t('sf.sec.longTerm')}
      subtitle={t('sf.sub.longTerm', { horizon: data.horizon })}
      summary={summary}
    >
      <div className="sf-scenarios">
        {data.scenarios.map((s, i) => (
          <div key={i} className="sf-scenario">
            <div className="sf-scenario-header">
              <div>
                <div className="sf-scenario-name">{s.name}</div>
                <div className="sf-scenario-tagline">{s.tagline}</div>
              </div>
              <span
                className="sf-scenario-prob"
                style={{ color: FIT_COLORS[s.probability] || '#7a5030' }}
              >
                {fitLabel(s.probability)}
              </span>
            </div>
            <p className="sf-scenario-desc">{s.description}</p>
            <div className="sf-block-label" style={{ marginTop: 14 }}>{t('sf.label.requiresNow')}</div>
            <ul className="sf-scenario-requires">
              {s.requires_now.map((r, j) => <li key={j}>{r}</li>)}
            </ul>
            <div className="sf-scenario-footer">
              <div className="sf-scenario-bottleneck">
                <strong>{t('sf.label.bottleneck')}</strong> {s.bottleneck}
              </div>
              <div className="sf-scenario-signal">
                <strong>{t('sf.label.rightIf')}</strong> {s.best_fit_signal}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="sf-pathway-callout sf-pathway-next" style={{ marginTop: 28 }}>
        <div className="sf-callout-label">{t('sf.label.saffronView')}</div>
        <p className="sf-callout-text">{data.saffron_view}</p>
      </div>
    </SectionShell>
  )
}

// A real tracker, not a list (Scott, 2026-06-26): each venue's status, last-
// contacted date and a note are editable and persist to contact_memory.json via
// PATCH /api/contacts/{name} — the same store Peppercorn writes to, so the two
// surfaces stay in sync. Status set matches Peppercorn's CRM values.
const VENUE_STATUS_OPTS = [
  { value: 'cold',            color: '#9a8a70', zh: '尚未联系',   ja: '未連絡',       en: 'Not yet contacted' },
  { value: 'researching',     color: '#c47a35', zh: '了解中',     ja: '調べている',   en: 'Looking into it' },
  { value: 'ready_to_review', color: '#c47a35', zh: '可以联系了', ja: '連絡してよい', en: 'Ready to reach out' },
  { value: 'in_contact',      color: '#c4a03a', zh: '联系中',     ja: 'やり取り中',   en: 'In contact' },
  { value: 'contacted',       color: '#5a7a30', zh: '已联系',     ja: '連絡した',     en: 'Reached out' },
  { value: 'sent_inquiry',    color: '#5a7a30', zh: '已发出问询', ja: '問い合わせ済み', en: 'Inquiry sent' },
  { value: 'submitted',       color: '#5a7a30', zh: '已投递',     ja: '応募済み',     en: 'Submitted' },
  { value: 'responded',       color: '#3a6a20', zh: '已回复',     ja: '返信あり',     en: 'They replied' },
  { value: 'ongoing',         color: '#3a6a20', zh: '进行中',     ja: '進行中',       en: 'Ongoing' },
  { value: 'relationship',    color: '#7a5cc0', zh: '保持往来',   ja: '関係構築',     en: 'Ongoing relationship' },
  { value: 'not_a_fit',       color: '#9a8a70', zh: '不太合适',   ja: '合わない',     en: 'Not a fit' },
]
const venueStatusOpt = (status) => VENUE_STATUS_OPTS.find(o => o.value === status)
const venueStatusLabel = (status, lang) => {
  const o = venueStatusOpt(status)
  if (o) return o[lang] || o.en
  if (!status) return ({ zh: '尚未联系', ja: '未連絡', en: 'Not yet contacted' })[lang] || 'Not yet contacted'
  return String(status).replace(/_/g, ' ')
}
const venueStatusColor = (status) => (venueStatusOpt(status) || {}).color || '#9a7040'

const VENUE_EDIT    = { zh: '更新', ja: '更新', en: 'Update' }
const VENUE_CANCEL  = { zh: '取消', ja: 'キャンセル', en: 'Cancel' }
const VENUE_SAVE    = { zh: '保存', ja: '保存', en: 'Save' }
const VENUE_SAVED   = { zh: '已保存', ja: '保存しました', en: 'Saved' }
const VENUE_NOTE_PH = { zh: '一句备注（可选）', ja: 'メモ（任意）', en: 'A note (optional)' }

function VenueTrackerRow({ v, lang, t }) {
  const [editing, setEditing] = useState(false)
  const [cur, setCur] = useState({ status: v.status || 'cold', last_contacted: v.last_contacted || '', notes: v.notes || '' })
  const [status, setStatus] = useState(cur.status)
  const [date, setDate]     = useState(cur.last_contacted)
  const [note, setNote]     = useState(cur.notes)
  const [saved, setSaved]   = useState(false)
  const [busy, setBusy]     = useState(false)

  async function save() {
    setBusy(true)
    try {
      const r = await fetch(`/api/contacts/${encodeURIComponent(v.name)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, last_contacted: date, notes: note }),
      })
      if (r.ok) {
        const c = (await r.json()).contact || {}
        setCur({ status: c.status ?? status, last_contacted: c.last_contacted ?? date, notes: c.notes ?? note })
        setSaved(true); setTimeout(() => setSaved(false), 2500)
        setEditing(false)
      }
    } catch { /* leave the row as-is on network failure */ }
    setBusy(false)
  }

  return (
    <div className="sf-venue-row">
      <div className="sf-venue-header">
        <a className="sf-venue-name sf-ext-link" href={sfSearch(`${v.name} ${v.city || ''}`)} target="_blank" rel="noreferrer">{v.name} ↗</a>
        <span className="sf-venue-type">{v.type} · {v.city}</span>
        <span className="sf-venue-status" style={{ color: venueStatusColor(cur.status) }}>{venueStatusLabel(cur.status, lang)}</span>
        {v.priority && <span className="sf-venue-priority">{t('sf.venue.priority', { n: v.priority })}</span>}
        <button className="sf-venue-edit" onClick={() => setEditing(e => !e)}>
          {editing ? (VENUE_CANCEL[lang] || VENUE_CANCEL.en) : (VENUE_EDIT[lang] || VENUE_EDIT.en)}
        </button>
      </div>
      <div className="sf-venue-last">
        {cur.last_contacted ? t('sf.venue.lastContacted', { date: cur.last_contacted }) : t('sf.venue.notContacted')}
      </div>
      {cur.notes && !editing && <div className="sf-venue-note">{cur.notes}</div>}
      {v.next_action && !editing && <div className="sf-venue-next">{v.next_action}</div>}
      {editing && (
        <div className="sf-venue-edit-form">
          <select className="sf-hedge-input" value={status} onChange={e => setStatus(e.target.value)}>
            {VENUE_STATUS_OPTS.map(o => <option key={o.value} value={o.value}>{o[lang] || o.en}</option>)}
          </select>
          <input className="sf-hedge-input sf-hedge-input--year" type="date" value={date} onChange={e => setDate(e.target.value)} />
          <input className="sf-hedge-input" value={note} onChange={e => setNote(e.target.value)} placeholder={VENUE_NOTE_PH[lang] || VENUE_NOTE_PH.en} />
          <button className="sf-hedge-add" onClick={save} disabled={busy}>{VENUE_SAVE[lang] || VENUE_SAVE.en}</button>
        </div>
      )}
      {saved && <div className="sf-venue-saved">{VENUE_SAVED[lang] || VENUE_SAVED.en}</div>}
    </div>
  )
}

function VenueTracker({ data, t }) {
  const { lang } = useLanguage()
  const summary = t('sf.sum.venues', { n: data.total, s: data.total !== 1 ? 's' : '', active: data.active ?? 0 })
  return (
    <SectionShell
      title={t('sf.sec.venues')}
      subtitle={t('sf.sub.venues')}
      summary={summary}
    >
      {data.tracked.length === 0 ? (
        <EmptyState message={t('sf.empty.venues')} />
      ) : (
        <div className="sf-venue-list">
          {data.tracked.map((v, i) => <VenueTrackerRow key={v.name || i} v={v} lang={lang} t={t} />)}
        </div>
      )}
      {data.gap_note && (
        <div className="sf-insight-callout" style={{ marginTop: 20 }}>{data.gap_note}</div>
      )}
    </SectionShell>
  )
}

// (Open-questions block removed from the Profile tab 2026-06-25 — those
//  questions live in Peppercorn now, as its Saffron-questions section. The
//  ProfileOpenQuestions / QuestionRow components and their constants
//  (SF_ANSWER_KEYS, PROFILE_OQ_*) were deleted with it.)

// ── Licensing Landscape ────────────────────────────────────────────────────

const TIER_COLORS = { now: '#16a34a', near_term: '#d97706', medium_term: '#9ca3af' }

// One scannable first move at the top of a path section — the content already
// lives in the entries; this just surfaces the starting line so it isn't buried.
function WhereToStart({ d, t, lang }) {
  const text = lang === 'zh' && d.where_to_start_zh ? d.where_to_start_zh : d.where_to_start
  if (!text) return null
  return (
    <div className="sf-start-here">
      <span className="sf-start-label">{t('sf.label.whereToStart')}</span>
      <p className="sf-start-text">{text}</p>
    </div>
  )
}

function locF(item, field, lang) {
  if (lang === 'zh' && item[field + '_zh']) return item[field + '_zh']
  if (lang === 'ja' && item[field + '_ja']) return item[field + '_ja']
  return item[field] || ''
}

function LicensingLandscape({ t, lang }) {
  const d = localizeDeep(LICENSING_LANDSCAPE, lang)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      {/* The "what your work suits + partners" detail lives in the card now, not
          in the collapsed subheader (Scott, 2026-06-26: that was real card info,
          and the subheader should just say what the card is for). */}
      {d.lead && <p className="sf-info-text" style={{ marginTop: 0, marginBottom: 16 }}>{d.lead}</p>}
      <WhereToStart d={d} t={t} lang={lang} />
      {d.items.map((group, gi) => (
        <div key={gi} className="sf-insight-group">
          <div className="sf-block-label">{locF(group, 'category', lang)}</div>
          <div className="sf-licensing-entries">
            {group.entries.map((entry, ei) => (
              <div key={ei} className="sf-licensing-entry">
                <div className="sf-licensing-entry-header">
                  {/* Only link a real outlet; explainer rows render as plain text
                      rather than a useless name-search (Scott's rule). */}
                  {entry.website || entry.url
                    ? <a className="sf-licensing-name sf-ext-link" href={entry.website || entry.url} target="_blank" rel="noreferrer">{entry.name} ↗</a>
                    : <span className="sf-licensing-name">{entry.name}</span>}
                  <span className="sf-tier-badge" style={{ color: TIER_COLORS[entry.tier] || '#9ca3af' }}>
                    {tfb(t, `sf.tier.${entry.tier}`, entry.tier)}
                  </span>
                </div>
                <p className="sf-licensing-note">{locF(entry, 'note', lang)}</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </SectionShell>
  )
}

// ── Press & Pitch Map ──────────────────────────────────────────────────────

// Each press/pitch outlet links to its real site so she can go read it and judge
// fit herself (Scott, 2026-06-26). Confident official sites here; anything not
// listed falls back to a name search.
const PRESS_OUTLET_SITE = {
  '美術手帖 (Bijutsu Techo)': 'https://bijutsutecho.com/',
  'Pen Magazine':            'https://www.pen-online.jp/',
  "It's Nice That":          'https://www.itsnicethat.com/',
  'Apartamento':             'https://www.apartamentomagazine.com/',
  'Casa Brutus':             'https://casabrutus.com/',
}

function PressPitchMap({ t, lang }) {
  const d = PRESS_PITCH_MAP
  const outlets = d.items.filter(item => item.name)
  const discoveryNote = d.items.find(item => item.category_note)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <WhereToStart d={d} t={t} lang={lang} />
      <div className="sf-press-pitch-list">
        {outlets.map((item, i) => (
          <div key={i} className="sf-press-pitch-row">
            <div className="sf-press-pitch-header">
              <a
                className="sf-press-pitch-name sf-ext-link"
                href={PRESS_OUTLET_SITE[item.name] || sfSearch(item.name)}
                target="_blank"
                rel="noreferrer"
              >{item.name} ↗</a>
              <span className="sf-press-pitch-type">{locF(item, 'type', lang)}</span>
            </div>
            <p className="sf-press-pitch-why">{locF(item, 'why_fits', lang)}</p>
            <div className="sf-press-pitch-meta">
              {item.how_to_pitch && (
                <div className="sf-press-pitch-how">
                  <span className="sf-press-pitch-meta-label">{t('sf.label.pitchColon')}</span>
                  {locF(item, 'how_to_pitch', lang)}
                </div>
              )}
              {item.contact && (
                <div className="sf-press-pitch-contact">
                  <span className="sf-press-pitch-meta-label">{t('sf.label.contactColon')}</span>
                  {locF(item, 'contact', lang)}
                </div>
              )}
              {item.timeline && (
                <div className="sf-press-pitch-timeline">
                  <span className="sf-press-pitch-meta-label">{t('sf.label.timelineColon')}</span>
                  {locF(item, 'timeline', lang)}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      {discoveryNote && (
        <div className="sf-insight-callout" style={{ marginTop: 24 }}>
          <div className="sf-block-label">{locF(discoveryNote, 'category_note', lang)}</div>
          <p className="sf-info-text">{locF(discoveryNote, 'how_discovered', lang)}</p>
        </div>
      )}
    </SectionShell>
  )
}

// ── Grant Landscape ────────────────────────────────────────────────────────

function GrantLandscape({ t, lang }) {
  const d = localizeDeep(GRANT_LANDSCAPE, lang)
  const grants = d.items.filter(item => item.name)
  const strategyNote = d.items.find(item => item.category_note)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <WhereToStart d={d} t={t} lang={lang} />
      <div className="sf-grant-list">
        {grants.map((grant, i) => (
          <div key={i} className="sf-grant-row">
            <div className="sf-grant-header">
              <a
                className="sf-grant-name sf-ext-link"
                href={grantHref(grant)}
                target="_blank"
                rel="noreferrer"
              >{grant.name} ↗</a>
              <span className="sf-grant-country">{grant.country}</span>
            </div>
            <div className="sf-grant-amount">{grant.amount}</div>
            <p className="sf-grant-why">{locF(grant, 'why_apply', lang)}</p>
            <div className="sf-grant-meta">
              {grant.eligibility && (
                <div className="sf-grant-meta-row">
                  <span className="sf-grant-meta-label">{t('sf.label.eligibilityColon')}</span>
                  {locF(grant, 'eligibility', lang)}
                </div>
              )}
              {grant.deadline && (
                <div className="sf-grant-meta-row">
                  <span className="sf-grant-meta-label">{t('sf.label.deadlineColon')}</span>
                  {grant.deadline}
                </div>
              )}
              {grant.competition && (
                <div className="sf-grant-meta-row">
                  <span className="sf-grant-meta-label">{t('sf.label.competitionColon')}</span>
                  {locF(grant, 'competition', lang)}
                </div>
              )}
              {grant.tip && (
                <div className="sf-grant-tip">{t('sf.label.tipColon')}{locF(grant, 'tip', lang)}</div>
              )}
            </div>
          </div>
        ))}
      </div>
      {strategyNote && (
        <div className="sf-insight-callout" style={{ marginTop: 24 }}>
          <div className="sf-block-label">{locF(strategyNote, 'category_note', lang)}</div>
          <p className="sf-info-text">{locF(strategyNote, 'note', lang)}</p>
        </div>
      )}
    </SectionShell>
  )
}

// ── Revenue Streams ────────────────────────────────────────────────────────

function RevenueStreams({ t, lang }) {
  const d = localizeDeep(REVENUE_STREAMS, lang)
  const streams = d.items.filter(item => item.stream !== 'Summary assessment')
  const summary_item = d.items.find(item => item.stream === 'Summary assessment')
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <WhereToStart d={d} t={t} lang={lang} />
      <div className="sf-revenue-list">
        {streams.map((item, i) => (
          <div key={i} className={`sf-revenue-row${item.leaving_on_table ? ' sf-revenue-row--gap' : ''}`}>
            <div className="sf-revenue-header">
              {(() => {
                const href = revenueHref(item)
                const label = locF(item, 'stream', lang)
                return href
                  ? <a className="sf-revenue-stream sf-ext-link" href={href} target="_blank" rel="noreferrer">{label} ↗</a>
                  : <span className="sf-revenue-stream">{label}</span>
              })()}
              {item.realistic_monthly && (
                <span className="sf-revenue-range">{item.realistic_monthly}</span>
              )}
              {item.leaving_on_table && (
                <span className="sf-revenue-gap-tag">{OPP_LABEL[lang] || OPP_LABEL.en}</span>
              )}
            </div>
            <p className="sf-revenue-desc">{locF(item, 'description', lang)}</p>
            {item.pricing && (
              <div className="sf-revenue-pricing">{locF(item, 'pricing', lang)}</div>
            )}
            {item.why_now && (
              <div className="sf-revenue-why">{locF(item, 'why_now', lang)}</div>
            )}
            {item.action && (
              <div className="sf-revenue-action">
                <span className="sf-revenue-action-label">{t('sf.label.actionColon')}</span>
                {locF(item, 'action', lang)}
              </div>
            )}
          </div>
        ))}
      </div>
      {summary_item && (
        <div className="sf-pathway-callout sf-pathway-blocking" style={{ marginTop: 24 }}>
          <div className="sf-callout-label">{t('sf.label.assessmentTitle')}</div>
          <p className="sf-callout-text">{locF(summary_item, 'description', lang)}</p>
        </div>
      )}
    </SectionShell>
  )
}

// ── Career Dependency Map ──────────────────────────────────────────────────

const MILESTONE_DOT_COLORS = {
  current: '#16a34a',
  next:    '#d97706',
  future:  '#9ca3af',
  horizon: '#9ca3af',
}

function CareerDependencyMap({ t, lang }) {
  const d = CAREER_DEPENDENCY_MAP
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-depmap">
        {d.milestones.map((milestone, mi) => {
          const dotColor = MILESTONE_DOT_COLORS[milestone.status] || '#9ca3af'
          const phaseKey = `sf.depmap.${milestone.status}`
          const phaseLabel = t(phaseKey) || milestone.label
          return (
            <div key={mi} className={`sf-depmap-milestone sf-depmap-milestone--${milestone.status}`}>
              <div className="sf-depmap-milestone-header">
                <span className="sf-depmap-dot" style={{ background: dotColor }} />
                <span className="sf-depmap-phase-label">{phaseLabel}</span>
              </div>
              <div className="sf-depmap-items">
                {milestone.items.map((item, ii) => (
                  <div key={ii} className="sf-depmap-item">
                    <div className="sf-depmap-complete">
                      <span className="sf-depmap-complete-label">{t('sf.depmap.completes')}</span>
                      {locF(item, 'complete', lang)}
                    </div>
                    <div className="sf-depmap-unlocks">
                      <span className="sf-depmap-unlocks-label">{t('sf.depmap.unlocks')}</span>
                      <ul className="sf-depmap-unlocks-list">
                        {(locF(item, 'unlocks', lang) || item.unlocks || []).map((unlock, ui) => (
                          <li key={ui}>{unlock}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </SectionShell>
  )
}

// ── Career Momentum Tracker ────────────────────────────────────────────────

const TRAJECTORY_COLORS = {
  early:        '#9a7040',
  accelerating: '#5a7a30',
  steady:       '#3a6a80',
  stalling:     '#8a7563',
}

const MOMENTUM_SUMMARY = {
  en: 'Your outreach over time — submissions, venue contacts and replies, as you log them.',
  zh: '你随时间的对外联系——提交、场馆联系与回复，随你记录而更新。',
  ja: '時間に沿ったあなたの動き——応募・会場への連絡・返信が、記録するごとに反映されます。',
}
function CareerMomentum({ data, t }) {
  const { lang } = useLanguage()
  const { totals, trajectory, monthly_chart } = data
  const [activity, setActivity] = useState(data.recent_activity || [])
  const maxBar = Math.max(...monthly_chart.map(m => m.submissions + m.contacts), 1)

  async function removeEvent(id) {
    setActivity(a => a.filter(x => x.id !== id))
    try { await fetch(`/api/career_events/${id}`, { method: 'DELETE' }) } catch { /* no-op */ }
  }
  const trajColor = TRAJECTORY_COLORS[trajectory] || '#9a7040'
  const summary = MOMENTUM_SUMMARY[lang] || MOMENTUM_SUMMARY.en

  return (
    <SectionShell
      title={t('sf.sec.momentum')}
      subtitle={t('sf.sub.momentum')}
      summary={summary}
      defaultOpen={false}
    >
      <div className="sf-momentum-stats">
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number">{totals.submissions}</div>
          <div className="sf-momentum-label">{t('sf.mom.totalSubmissions')}</div>
        </div>
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number">{totals.venues_in_crm}</div>
          <div className="sf-momentum-label">{t('sf.mom.venuesInCRM')}</div>
        </div>
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number">{totals.responses_received}</div>
          <div className="sf-momentum-label">{t('sf.mom.responses')}</div>
        </div>
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number" style={{ color: trajColor }}>
            {tfb(t, `sf.mom.traj.${trajectory}`, trajectory)}
          </div>
          <div className="sf-momentum-label">{t('sf.mom.trajectory')}</div>
        </div>
      </div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.mom.activityChart')}</div>
      <div className="sf-mom-chart">
        {monthly_chart.map((m, i) => {
          const total = m.submissions + m.contacts
          return (
            <div key={i} className="sf-mom-bar-col">
              <div className="sf-mom-bar-track">
                <div className="sf-mom-bar-subs"
                  style={{ height: `${Math.round((m.submissions / maxBar) * 100)}%` }} />
                <div className="sf-mom-bar-contacts"
                  style={{ height: `${Math.round((m.contacts / maxBar) * 100)}%` }} />
              </div>
              <div className="sf-mom-bar-label">{m.month.slice(5)}</div>
              <div className="sf-mom-bar-total">{total || ''}</div>
            </div>
          )
        })}
      </div>
      <div className="sf-mom-legend">
        <span className="sf-mom-legend-subs">{t('sf.mom.submissions')}</span>
        <span className="sf-mom-legend-contacts">{t('sf.mom.contacts')}</span>
      </div>

      {activity.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <div className="sf-block-label">{t('sf.mom.recentActivity')}</div>
          <div className="sf-mom-activity">
            {activity.map((item, i) => (
              <div key={item.id || i} className="sf-mom-activity-row">
                <span className={`sf-mom-type sf-mom-type--${item.type}`}>
                  {item.type === 'submission' ? '📤' : '📋'}
                </span>
                <span className="sf-mom-activity-name">{item.name}</span>
                <span className="sf-mom-activity-status">{actStatusLabel(item.status, t)}</span>
                <span className="sf-mom-activity-date">{item.date?.slice(0, 10)}</span>
                {item.type === 'career_event' && item.id && (
                  <button className="sf-mom-activity-del" onClick={() => removeEvent(item.id)} title={t('sf.mom.removeEvent')}>×</button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {totals.submissions === 0 && (
        <div className="sf-insight-callout" style={{ marginTop: 20 }}>
          {t('sf.mom.noSubmissionsYet')}
        </div>
      )}
    </SectionShell>
  )
}

// ── Timing Intelligence ────────────────────────────────────────────────────

// A real reading of the timing, built from the live counts: how much of the
// board is a fixed date vs. rolling/open, so she sees the calendar pressure is
// concentrated and the rest is approachable any time (Scott: add real insight).
const TIMING_READING = {
  en: (dated, flexible) => `Of everything on your radar, ${dated} have a fixed date and ${flexible} are rolling or open — so most of the calendar pressure sits on a handful of dates, and the rest you can approach whenever you're ready.`,
  zh: (dated, flexible) => `在你关注的机会里，${dated} 个有固定截止日期，${flexible} 个是常年开放或没有固定截止——也就是说，真正要盯日历的只有少数几天，其余的你随时准备好了再去都行。`,
  ja: (dated, flexible) => `あなたが見ている中で、${dated} 件は締切が決まっていて、${flexible} 件は通年・随時です——つまりカレンダー上のプレッシャーはごく一部の日付に集中していて、残りは準備ができたときにいつでも動けます。`,
}
function TimingIntelligence({ data, t }) {
  const { lang } = useLanguage()
  const maxCount = Math.max(...data.monthly_counts.map(m => m.count), 1)
  const summary  = t('sf.sum.timing', { peaks: data.peak_months.slice(0, 2).join(' · '), dated: data.with_parsed_deadline })
  const dated    = data.with_parsed_deadline ?? 0
  const flexible = (data.rolling_count ?? 0) + (data.no_deadline_count ?? 0)
  const timingReading = (TIMING_READING[lang] || TIMING_READING.en)(dated, flexible)

  return (
    <SectionShell
      title={t('sf.sec.timing')}
      subtitle={t('sf.sub.timing')}
      summary={summary}
    >
      <div className="sf-insight-callout">{data.key_insight}</div>
      <p className="sf-info-text" style={{ marginTop: 12 }}>{timingReading}</p>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.timing.deadlinesByMonth')}</div>
      <div className="sf-timing-grid">
        {data.monthly_counts.map((m, i) => (
          <div key={i} className="sf-timing-month">
            <div className="sf-timing-count">{m.count || ''}</div>
            <div className="sf-timing-bar-track">
              <div
                className={`sf-timing-bar${data.peak_months.includes(m.month) ? ' sf-timing-bar--peak' : ''}`}
                style={{ height: `${Math.round((m.count / maxCount) * 100)}%` }}
              />
            </div>
            <div className="sf-timing-month-name">{m.month.slice(0, 3)}</div>
          </div>
        ))}
      </div>

      <div className="sf-two-col" style={{ marginTop: 28 }}>
        <div>
          <div className="sf-block-label">{t('sf.timing.peakMonths')}</div>
          {data.peak_months.map((m, i) => (
            <div key={i} className="sf-timing-peak-row">
              <span className="sf-timing-peak-dot" />
              <span>{m}</span>
              <span className="sf-timing-peak-count">{t('sf.timing.deadlineCount', { n: data.monthly_counts.find(x => x.month === m)?.count ?? 0 })}</span>
            </div>
          ))}
          {data.quiet_months.length > 0 && (
            <>
              <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.timing.quietMonths')}</div>
              {data.quiet_months.map((m, i) => (
                <div key={i} className="sf-timing-quiet-row">{m} — {t('sf.timing.quietNote')}</div>
              ))}
            </>
          )}
        </div>
        <div>
          <div className="sf-block-label">{t('sf.timing.coverage')}</div>
          <div className="sf-timing-stats">
            <div className="sf-timing-stat-row">
              <span>{t('sf.timing.withDeadline')}</span>
              <span className="sf-timing-stat-val">{data.with_parsed_deadline}</span>
            </div>
            <div className="sf-timing-stat-row">
              <span>{t('sf.timing.rolling')}</span>
              <span className="sf-timing-stat-val">{data.rolling_count}</span>
            </div>
            <div className="sf-timing-stat-row">
              <span>{t('sf.timing.noDeadline')}</span>
              <span className="sf-timing-stat-val">{data.no_deadline_count}</span>
            </div>
          </div>
          <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.timing.prepWindow')}</div>
          <p className="sf-info-text">{t('sf.timing.prepWindowNote')}</p>
        </div>
      </div>
    </SectionShell>
  )
}

// ── Comparative Career Timeline ────────────────────────────────────────────

// CareerTimeline (peer-at-stage "what they had at your age" comparison) was
// removed from the UI — it's the textbook unfavorable comparison for an early-
// career artist (Scott: never compare her to others unless it's favorable).
// Restore from git history if a favorable reframe is ever wanted.

// ── Pricing Intelligence ───────────────────────────────────────────────────

const IMPACT_COLORS = { high: '#5a7a30', medium: '#c47a35', low: '#9ca3af' }

function PricingIntelligence({ t, lang }) {
  const d = localizeDeep(PRICING_INTELLIGENCE, lang)
  const { originals, prints, zines } = d.current_range
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <p className="sf-peers-caveat">{d.source_note}</p>

      <div className="sf-block-label" style={{ marginTop: 16 }}>{t('sf.pricing.currentRanges')}</div>
      <div className="sf-pricing-ranges">
        {[originals, prints, zines].map((range, i) => (
          <div key={i} className="sf-pricing-range-card">
            <div className="sf-pricing-range-label">{range.label}</div>
            <div className="sf-pricing-range-value">
              ¥{range.low.toLocaleString()} – ¥{range.high.toLocaleString()}
            </div>
            <p className="sf-pricing-range-note">{range.note}</p>
            {range.sweet_spot && (
              <div className="sf-pricing-sweet-spot">{range.sweet_spot}</div>
            )}
          </div>
        ))}
      </div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.pricing.whatAffectsPrice')}</div>
      <div className="sf-pricing-factors">
        {d.what_affects_price.map((f, i) => (
          <div key={i} className="sf-pricing-factor">
            <div className="sf-pricing-factor-header">
              <span className="sf-pricing-factor-name">{f.factor}</span>
              <span className="sf-pricing-impact" style={{ color: IMPACT_COLORS[f.impact] }}>
                {tfb(t, `sf.pricing.impact.${f.impact}`, f.impact)}
              </span>
            </div>
            <p className="sf-pricing-factor-note">{f.note}</p>
          </div>
        ))}
      </div>

      <div className="sf-pathway-callout sf-pathway-blocking" style={{ marginTop: 24 }}>
        <div className="sf-callout-label">{t('sf.pricing.editionDiscipline')}</div>
        <p className="sf-callout-text">{d.edition_discipline.rule}</p>
        <p className="sf-callout-text" style={{ marginTop: 8, fontStyle: 'italic' }}>
          {d.edition_discipline.current_gap}
        </p>
      </div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.pricing.credibilitySignals')}</div>
      <ul className="sf-pricing-signals">
        {d.credibility_signals.map((s, i) => <li key={i}>{s}</li>)}
      </ul>
    </SectionShell>
  )
}

// (OpportunityGap removed 2026-06-25 with the Landscape tab.)

// ── Career Readiness ───────────────────────────────────────────────────────

const GAP_DOT_COLORS = {
  HIGH:   '#c47a35',
  MEDIUM: '#d4a855',
  LOW:    '#b0a080',
}

// A neutral "you're here" marker — a value and its label, no target, no fill
// fraction. It states where she stands without grading it against a goal she
// never set. (Replaced the old progress ring that showed a strength half-empty.)
function MilestoneMarker({ current, label, color }) {
  return (
    <div className="sf-marker">
      <div className="sf-marker-value">{current}</div>
      <div className="sf-marker-accent" style={{ background: color }} />
      <div className="sf-marker-label">{label}</div>
    </div>
  )
}


// (Landscape tab removed 2026-06-25 — MarketStats / MarketLandscape /
//  OpportunityGap / GeographicExpansion and their label/constant helpers are
//  gone; the app already surfaces the field on the Discover side.)

function ReadinessCorrection({ t, onChanged }) {
  const [venue, setVenue] = useState('')
  const [date,  setDate]  = useState('')
  const [city,  setCity]  = useState('')
  const [country, setCountry] = useState('')
  const [type,  setType]  = useState('group')
  const [confidence, setConfidence] = useState('confirmed')
  const [saved, setSaved] = useState(false)

  async function addShow() {
    if (!venue.trim()) return
    const body = {
      type, venue: venue.trim(), date: date.trim(),
      city: city.trim(), country: country.trim(),
      confidence, outcome: 'shown',
    }
    setVenue(''); setDate(''); setCity(''); setCountry(''); setSaved(true)
    setTimeout(() => setSaved(false), 3200)
    try {
      await fetch('/api/exhibition_log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      onChanged?.()  // refetch so the readiness reflects it
    } catch { /* no-op on network failure */ }
  }

  return (
    <div className="sf-readiness-hedge">
      <p className="sf-readiness-hedge-text">{t('sf.cr.hedge')}</p>
      <div className="sf-readiness-addshow">
        <input className="sf-hedge-input" value={venue} onChange={e => setVenue(e.target.value)} placeholder={t('sf.cr.addShow.venue')} />
        <input className="sf-hedge-input sf-hedge-input--year" value={date} onChange={e => setDate(e.target.value)} placeholder={t('sf.cr.addShow.year')} />
        <input className="sf-hedge-input" value={city} onChange={e => setCity(e.target.value)} placeholder={t('sf.cr.city')} />
        <input className="sf-hedge-input" value={country} onChange={e => setCountry(e.target.value)} placeholder={t('sf.cr.country')} />
        <select className="sf-hedge-input" value={type} onChange={e => setType(e.target.value)}>
          <option value="group">{t('sf.cr.type.group')}</option>
          <option value="solo">{t('sf.cr.type.solo')}</option>
          <option value="institutional">{t('sf.cr.type.institutional')}</option>
          <option value="international">{t('sf.cr.type.international')}</option>
        </select>
        <select className="sf-hedge-input" value={confidence} onChange={e => setConfidence(e.target.value)}>
          <option value="confirmed">{t('sf.cr.confirmed')}</option>
          <option value="mentioned">{t('sf.cr.mentioned')}</option>
        </select>
        <button className="sf-hedge-add" onClick={addShow} disabled={!venue.trim()}>{t('sf.cr.addShow.btn')}</button>
      </div>
      {saved && <p className="sf-readiness-hedge-saved">{t('sf.cr.addShow.saved')}</p>}
    </div>
  )
}

// Which exhibition `type` satisfies each readiness gap (jws is handled separately).
const GAP_TYPE = {
  group_shows:        'group',
  solo_show:          'solo',
  institutional_show: 'institutional',
  international_show: 'group',
}

// "I already did this" — a per-gap form that records the evidence that clears
// the gap (a show via /api/exhibition_log, or society membership via
// /api/membership), then refetches so the readiness updates immediately.
function GapCorrectionForm({ gap, onChanged }) {
  const { t } = useLanguage()
  const [open, setOpen] = useState(false)
  const [venue, setVenue] = useState('')
  const [date, setDate] = useState('')
  const [city, setCity] = useState('')
  const [country, setCountry] = useState('')
  const [confidence, setConfidence] = useState('confirmed')
  const [year, setYear] = useState('')
  const [busy, setBusy] = useState(false)
  const isJws = gap.gap_id === 'jws'

  async function submit() {
    setBusy(true)
    try {
      if (isJws) {
        await fetch('/api/membership', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'Japan Watercolor Society', year: year.trim() || null }),
        })
      } else {
        await fetch('/api/exhibition_log', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: GAP_TYPE[gap.gap_id] || 'group',
            venue: venue.trim(), date: date.trim(),
            city: city.trim(), country: country.trim(),
            confidence, outcome: 'shown',
          }),
        })
      }
      setOpen(false)
      onChanged?.()
    } catch { /* no-op on network failure */ }
    setBusy(false)
  }

  if (!open) {
    return (
      <button className="sf-gap-done-btn" onClick={() => setOpen(true)}>
        {t('sf.cr.alreadyDid')}
      </button>
    )
  }

  return (
    <div className="sf-gap-correction">
      {isJws ? (
        <input className="sf-hedge-input sf-hedge-input--year" value={year}
          onChange={e => setYear(e.target.value)} placeholder={t('sf.cr.jwsYear')} />
      ) : (
        <>
          <input className="sf-hedge-input" value={venue} onChange={e => setVenue(e.target.value)} placeholder={t('sf.cr.addShow.venue')} />
          <input className="sf-hedge-input sf-hedge-input--year" value={date} onChange={e => setDate(e.target.value)} placeholder={t('sf.cr.addShow.year')} />
          <input className="sf-hedge-input" value={city} onChange={e => setCity(e.target.value)} placeholder={t('sf.cr.city')} />
          <input className="sf-hedge-input" value={country} onChange={e => setCountry(e.target.value)} placeholder={t('sf.cr.country')} />
          <select className="sf-hedge-input" value={confidence} onChange={e => setConfidence(e.target.value)}>
            <option value="confirmed">{t('sf.cr.confirmed')}</option>
            <option value="mentioned">{t('sf.cr.mentioned')}</option>
          </select>
        </>
      )}
      <div className="sf-gap-correction-actions">
        <button className="sf-hedge-add" onClick={submit} disabled={busy || (!isJws && !venue.trim())}>{t('sf.cr.addShow.btn')}</button>
        <button className="sf-gap-cancel" onClick={() => setOpen(false)}>{t('sf.cr.cancel')}</button>
      </div>
    </div>
  )
}

// (LevelUpBanner removed — the level-up celebration is exactly the videogame
// framing the review flagged; the profile no longer has a numeric level to cross.)

// Column headers for the three opportunity buckets — plain "now / getting
// closer / keep an eye on", NEVER tier numbers. (Domino: the readiness columns
// should not read as a ranked ladder.)
const COL_LABELS = {
  now:    { zh: '现在',     ja: '今',         en: 'Now' },
  near:   { zh: '正在靠近', ja: '近づいている', en: 'Getting closer' },
  watch:  { zh: '留意',     ja: '気に留める',   en: 'Keep an eye on' },
}
const colLabel = (which, lang) => (COL_LABELS[which][lang] || COL_LABELS[which].en)

// ONE warm status line for the profile — a sentence, no number/bar/%/level/
// celebration. Built from her real evidence so it stays truthful and updates
// when she logs a show; the closing clause hedges ("if you want it") so it never
// prescribes representation. (Replaces the five contradicting level widgets.)
function careerStatusLine(ev, lang) {
  const shows = ev.confirmed_group_shows ?? 0
  const solos = ev.solo_shows ?? (ev.has_solo_show ? 1 : 0)
  const intl  = !!ev.has_international_show
  if (lang === 'ja') {
    const parts = []
    if (shows) parts.push(`${shows}回のグループ展`)
    if (solos) parts.push(`${solos}回の個展`)
    if (intl)  parts.push('海外での展示')
    const built = parts.length ? `——${parts.join('、')}` : ''
    return `しっかりとした土台ができています${built}。次に向かう先は、ギャラリーとの関係づくりや専属です（望むなら、ですが）。`
  }
  if (lang === 'en') {
    const parts = []
    if (shows) parts.push(`${shows} group shows`)
    if (solos) parts.push(`${solos} solo show${solos > 1 ? 's' : ''}`)
    if (intl)  parts.push('an international showing')
    const built = parts.length ? ` — ${parts.join(', ')}` : ''
    return `You've built a solid foundation${built}. The direction from here is gallery relationships and representation, if you want it.`
  }
  // zh (her default)
  const parts = []
  if (shows) parts.push(`${shows} 场联展`)
  if (solos) parts.push(`${solos} 场个展`)
  if (intl)  parts.push('海外的展出')
  const built = parts.length ? `——${parts.join('、')}` : ''
  return `你已经建立了扎实的根基${built}。接下来的方向是画廊关系与代理（如果你想要的话）。`
}

// One readiness-column row: the opportunity name as a real link out (its own
// page when we have one, otherwise a name search). The field is `website` —
// NOT `url`. No numeric score is ever shown to her.
function ReadinessColItem({ o, muted }) {
  const name = (o && typeof o === 'object') ? (o.name ?? o.title ?? '') : o
  const href = (o && typeof o === 'object' && o.website) ? o.website : sfSearch(name)
  return (
    <div className={`sf-readiness-col-item${muted ? ' sf-readiness-col-item--muted' : ''}`}>
      <a className="sf-readiness-col-name sf-ext-link" href={href} target="_blank" rel="noreferrer">{name} ↗</a>
    </div>
  )
}

// Plainer "next step" labels — no "level up / unlock / advance a tier" framing.
const NEXT_STEP_LABEL = { zh: '下一步', ja: '次の一歩', en: 'Next step' }
// The optional, no-pressure hint under the next-step card.
const NEXT_STEP_HINT = {
  zh: '没有截止日期，也不催你——想做的时候再做。',
  ja: '締切も急かしもありません——やりたくなったときで大丈夫です。',
  en: 'No deadline, no pressure — only when you feel like it.',
}
// "More directions" toggle (was "还有 N 个进阶目标" / advance-a-tier language).
const MORE_DIRS = {
  zh: (n) => `还有 ${n} 个方向 ▾`,
  ja: (n) => `あと ${n} 件 ▾`,
  en: (n) => `${n} more ▾`,
}
const HIDE_DIRS = { zh: '收起', ja: '閉じる', en: 'Hide' }

// Small "want a gentle posting rhythm?" line — the ONE bit salvaged from the
// deleted InstagramStrategy panel. Optional, collapsible, never a quota.
const CADENCE_TIP_MORE = { zh: '想要一个温和的发布节奏？▾', ja: '穏やかな投稿リズムは？▾', en: 'Want a gentle posting rhythm? ▾' }
const CADENCE_TIP_HIDE = { zh: '收起', ja: '閉じる', en: 'Hide' }

function CadenceTip({ text, lang }) {
  const [open, setOpen] = useState(false)
  if (!text) return null
  return (
    <div className="sf-cadence-tip">
      <button className="sf-cadence-tip-toggle" onClick={() => setOpen(o => !o)}>
        {open ? (CADENCE_TIP_HIDE[lang] || CADENCE_TIP_HIDE.en) : (CADENCE_TIP_MORE[lang] || CADENCE_TIP_MORE.en)}
      </button>
      {open && <p className="sf-cadence-tip-text">{text}</p>}
    </div>
  )
}

function CareerReadiness({ data, cadenceTip, onChanged }) {
  const { t, lang } = useLanguage()
  const [showMore, setShowMore] = useState(false)
  if (!data) return null

  const ev       = data.career_evidence || {}
  const level    = data.level || null
  const gaps     = data.blocking_gaps ?? []
  const actNow   = (data.immediate_priorities ?? []).slice(0, 3)
  const build    = data.build_toward ?? []
  const watch    = data.watch_list   ?? []

  // ONE next step (engine picks the highest-priority gap, or a positive
  // advanced-state line when every gap is closed). The rest collapse away.
  const nextStep  = level?.next_unlock || gaps[0] || null
  const otherGaps = nextStep ? gaps.filter(g => g.gap_id !== nextStep.gap_id) : gaps
  const stepActionable = nextStep && nextStep.gap_id !== 'advanced'

  // Summary line: the warm status sentence, not a rank.
  const summary = careerStatusLine(ev, lang)

  return (
    <SectionShell
      title={t('sf.cr.title')}
      subtitle={t('sf.cr.subtitle')}
      summary={summary}
    >
      {/* ONE warm status line — a sentence, no number/bar/%/level/celebration.
          (Replaced the five contradicting level widgets: level-up banner,
          numeric badge, ladder, tier3/tier4 bars, months-to-tier.) */}
      <p className="sf-status-line">{careerStatusLine(ev, lang)}</p>

      {/* ONE next-step card — the single thing to look at next, with its inline
          "I already did this" form. No "level up / unlock a tier" language. */}
      {nextStep && (
        <div className="sf-next-unlock">
          <div className="sf-next-unlock-label">{NEXT_STEP_LABEL[lang] || NEXT_STEP_LABEL.en}</div>
          <div className="sf-next-unlock-gap">{locF(nextStep, 'gap', lang)}</div>
          {nextStep.detail && <p className="sf-next-unlock-detail">{locF(nextStep, 'detail', lang)}</p>}
          {nextStep.action && <p className="sf-next-unlock-action">{locF(nextStep, 'action', lang)}</p>}
          {stepActionable && (
            <>
              <p className="sf-next-unlock-hint">{NEXT_STEP_HINT[lang] || NEXT_STEP_HINT.en}</p>
              <GapCorrectionForm gap={nextStep} onChanged={onChanged} />
            </>
          )}
          {/* The one bit salvaged from the deleted Instagram panel: a gentle
              weekly-rhythm cadence tip, folded in here as a small optional line. */}
          <CadenceTip text={cadenceTip} lang={lang} />
        </div>
      )}

      {/* Remaining directions — collapsed by default, never a wall */}
      {otherGaps.length > 0 && (
        <div className="sf-more-gaps">
          <button className="sf-more-gaps-toggle" onClick={() => setShowMore(s => !s)}>
            {showMore ? (HIDE_DIRS[lang] || HIDE_DIRS.en) : (MORE_DIRS[lang] || MORE_DIRS.en)(otherGaps.length)}
          </button>
          {showMore && (
            <div className="sf-readiness-gaps" style={{ marginTop: 12 }}>
              {otherGaps.map((g, i) => (
                <div key={i} className="sf-readiness-gap-row">
                  <span
                    className="sf-readiness-gap-dot"
                    style={{ background: GAP_DOT_COLORS[g.priority] ?? '#b0a080' }}
                  />
                  <div className="sf-readiness-gap-body">
                    <span className="sf-readiness-gap-text">{locF(g, 'gap', lang)}</span>
                    {g.action && <span className="sf-readiness-gap-action">{locF(g, 'action', lang)}</span>}
                    <GapCorrectionForm gap={g} onChanged={onChanged} />
                  </div>
                </div>
              ))}
              <ReadinessCorrection t={t} onChanged={onChanged} />
            </div>
          )}
        </div>
      )}

      {/* Three opportunity columns — now / getting closer / keep an eye on.
          NOT tier numbers. Every name links out (its own page when we have a
          URL, else a name search). No numeric scores, no "newly in reach". */}
      <div className="sf-readiness-columns" style={{ marginTop: 28 }}>
        <div className="sf-readiness-col">
          <div className="sf-block-label">{colLabel('now', lang)}</div>
          {actNow.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : actNow.map((o, i) => <ReadinessColItem key={i} o={o} />)
          }
        </div>
        <div className="sf-readiness-col">
          <div className="sf-block-label">{colLabel('near', lang)}</div>
          {build.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : build.map((o, i) => <ReadinessColItem key={i} o={o} />)
          }
        </div>
        <div className="sf-readiness-col sf-readiness-col--watch">
          <div className="sf-block-label">{colLabel('watch', lang)}</div>
          {watch.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : watch.map((o, i) => <ReadinessColItem key={i} o={o} muted />)
          }
        </div>
      </div>
    </SectionShell>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

function SaffronIntro() {
  const { t } = useLanguage()
  const [dismissed, setDismissed] = useState(() => {
    try { return localStorage.getItem('sf_intro_dismissed') === '1' } catch { return false }
  })
  if (dismissed) return null
  function close() {
    setDismissed(true)
    try { localStorage.setItem('sf_intro_dismissed', '1') } catch { /* localStorage unavailable */ }
  }
  return (
    <div className="companion-intro">
      <button className="companion-intro-close" onClick={close} title={t('intro.dismiss')}>×</button>
      <p className="companion-intro-text">{t('sf.intro.body')}</p>
    </div>
  )
}

export default function SaffronPage({ nav }) {
  const [rawData,    setRawData]    = useState(null)
  const [rawCareer,  setRawCareer]  = useState(null)
  const [error,      setError]      = useState(null)
  const [tab,        setTab]        = useState('strategy')
  const { t, lang } = useLanguage()

  const loadSaffron = () => {
    fetch('/api/saffron')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setRawData)
      .catch(e => setError(e.message))
  }
  useEffect(() => { loadSaffron() }, [])

  const loadCareer = () => {
    fetch('/api/career_strategy')
      .then(r => { if (!r.ok) throw null; return r.json() })
      .then(setRawCareer)
      .catch(() => {})
  }
  useEffect(() => { loadCareer() }, [])

  // After an edit that changes her career data (logging a show, marking a gap
  // done), refresh BOTH the career-strategy report (readiness bars/gaps) AND the
  // saffron payload (career-position counts) so every readiness display updates
  // live instead of only when the section is remounted.
  const refreshCareer = () => { loadCareer(); loadSaffron() }

  // Translate the served (English) analysis into Chinese for 中文 viewers.
  // Translator map: dynamic opportunity strings come from the payload's own
  // _i18n (rebuilt from live data every run, so it survives pipeline updates);
  // the static authored prose comes from SF_ZH (zh only).
  const txMap = useMemo(() => {
    if (lang === 'zh') return { ...(rawData?._i18n?.zh || {}), ...SF_ZH, ...SF_ZH_PEERS, ...SF_ZH_CV }
    if (lang === 'ja') return { ...(rawData?._i18n?.ja || {}), ...SF_JA }
    return null
  }, [rawData, lang])
  const data       = useMemo(() => (txMap ? deepTranslate(rawData,   txMap) : rawData),   [rawData,   txMap])
  const careerData = useMemo(() => (txMap ? deepTranslate(rawCareer, txMap) : rawCareer), [rawCareer, txMap])

  // Saffron is the big-picture companion — Mochi and Peppercorn are the specific
  // ones, so Saffron opens broad (landscape → strategy) and only then narrows to
  // her profile, which is also the most personal/self-comparing tab.
  const SF_TABS = [
    ['strategy',      t('sf.cat.strategy')],
    ['profile',       t('sf.cat.profile')],
    ['calendar',      t('sf.cat.calendar')],
    ['relationships', t('sf.cat.relationships')],
    ['money',         t('sf.cat.money')],
  ]
  function goTab(key) {
    setTab(key)
    // Land the new tab's FIRST section just below the sticky nav + tab bar — not
    // behind them. Scrolling to sf-content's raw top tucked the section header
    // under the sticky stack and cut off the top of the content.
    requestAnimationFrame(() => {
      const content = document.querySelector('.sf-content')
      const tabs = document.querySelector('.sf-tabs')
      if (!content) return
      const target = content.querySelector('.sf-section') || content
      // sticky tab bar sits at top:54px (below the nav); offset by its full height.
      const stickyOffset = 54 + (tabs ? tabs.offsetHeight : 48) + 10
      const top = target.getBoundingClientRect().top + window.scrollY - stickyOffset
      window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
    })
  }

  return (
    <div className="saffron-page">
      <section className="saffron-hero">
        <img src={saffronHero} alt="Saffron's wide view" className="saffron-hero-img" />
      </section>
      {nav}

      <SaffronIntro />

      {!data && !error && <div className="sf-loading">{t('sf.loading')}</div>}

      {error && (
        <div className="sf-error">
          {t('sf.error')} — <code>python api.py</code>
        </div>
      )}

      {data && (
        <div className="sf-content">
          <div className="sf-tabs">
            {SF_TABS.map(([key, label]) => (
              <button
                key={key}
                className={`sf-tab${tab === key ? ' sf-tab--active' : ''}`}
                onClick={() => goTab(key)}
              >
                {label}
              </button>
            ))}
          </div>

          {/* Each section gets its OWN error boundary so one throwing section
              shows a small inline notice instead of blanking the whole tab.
              `key={tab}` resets a failed boundary when she switches tabs.
              SB() wraps one child; the first section of a tab is open, the rest
              collapse to their summary (via SectionOpenContext). */}
          {(() => {
            const SB = (k, node) => <SectionErrorBoundary key={`${tab}-${k}`}>{node}</SectionErrorBoundary>
            return (
              <>
                {tab === 'strategy' && (
                  <>
                    {SB('pathway', <StrategicPathway data={data.pathway} t={t} />)}
                    <SectionOpenContext.Provider value={false}>
                      {SB('longterm', <LongTermScenarios data={data.long_term_scenarios} t={t} />)}
                      {SB('depmap',   <CareerDependencyMap t={t} lang={lang} />)}
                      {/* Open questions moved to the profile tab (compact, opt-in). */}
                    </SectionOpenContext.Provider>
                  </>
                )}
                {/* The Landscape tab was removed entirely (Scott, 2026-06-25):
                    the whole app already shows the landscape, so the tab and all
                    its sections (market stats, market landscape, gap analysis,
                    geographic expansion) were deleted — no salvage. */}
                {tab === 'profile' && (
                  <>
                    {careerData && SB('readiness', <CareerReadiness data={careerData} cadenceTip={data.instagram_strategy?.strategy} onChanged={refreshCareer} />)}
                    <SectionOpenContext.Provider value={false}>
                      {/* Open questions moved to Peppercorn (they live there as the
                          Saffron-questions section). Standalone InstagramStrategy
                          and audience-geography panels removed — Instagram is now
                          stated once, as the audience fact in CareerPosition; only
                          the weekly-rhythm cadence tip was salvaged (into the
                          next-step area of Career Readiness above). */}
                      {/* The peer/record COMPARISON sections stay collapsed (opt-in)
                          — the most self-comparing, least-needed-at-a-glance part. */}
                      {SB('careerpos',  <CareerPosition data={data.career_position} t={t} />)}
                      {SB('benchmarks', <CareerBenchmarks data={data.career_benchmarks} t={t} />)}
                      {SB('peers',      <ComparableArtists artists={data.peer_artists} t={t} />)}
                      {SB('momentum',   <CareerMomentum data={data.career_momentum} t={t} />)}
                    </SectionOpenContext.Provider>
                  </>
                )}
                {tab === 'calendar' && (
                  <>
                    {SB('calendar', <SeasonalCalendar data={data.seasonal_calendar} t={t} lang={lang} />)}
                    <SectionOpenContext.Provider value={false}>
                      {SB('timing', <TimingIntelligence data={data.timing_intelligence} t={t} />)}
                    </SectionOpenContext.Provider>
                  </>
                )}
                {tab === 'relationships' && (
                  <>
                    {SB('press', <PressFeatures data={data.press_features} t={t} />)}
                    <SectionOpenContext.Provider value={false}>
                      {SB('presspitch', <PressPitchMap t={t} lang={lang} />)}
                      {SB('presskit',   <PressKit lang={lang} />)}
                      {SB('collab',     <CollaborationMap lang={lang} />)}
                      {SB('collectors', <CollectorEcosystem lang={lang} />)}
                      {SB('venues',     <VenueTracker data={data.venue_tracker} t={t} />)}
                    </SectionOpenContext.Provider>
                  </>
                )}
                {tab === 'money' && (
                  <>
                    {SB('revenue', <RevenueStreams t={t} lang={lang} />)}
                    <SectionOpenContext.Provider value={false}>
                      {SB('pricing',  <PricingIntelligence t={t} lang={lang} />)}
                      {SB('grants',   <GrantLandscape t={t} lang={lang} />)}
                      {SB('licensing',<LicensingLandscape t={t} lang={lang} />)}
                      {SB('publand',  <PublicationLandscape data={data.publication_landscape} t={t} />)}
                    </SectionOpenContext.Provider>
                  </>
                )}
              </>
            )
          })()}
        </div>
      )}
    </div>
  )
}
