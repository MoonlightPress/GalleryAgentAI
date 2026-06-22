import { useState, useEffect, useMemo, Component } from 'react'
import './SaffronPage.css'
import { saffronHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'
import {
  LICENSING_LANDSCAPE,
  PRESS_PITCH_MAP,
  GRANT_LANDSCAPE,
  REVENUE_STREAMS,
  CAREER_DEPENDENCY_MAP,
  CAREER_TIMELINE,
  PRICING_INTELLIGENCE,
} from '../data/saffron_insights'

// Saffron's analysis body is authored in English in api.py. When the viewer is
// reading in Chinese, we translate every served string client-side via this map
// (unmapped strings pass through unchanged — graceful partial coverage).
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
  "With a 26k Instagram following, the account is established and growing. Cadence is the most controllable variable for maximising reach on the platform galleries, publishers, and curators actually use for discovery. Without knowing current frequency, no posting strategy can be recommended.": "你已有 2.6 万 Instagram 粉丝，账号已确立并在增长。发布节奏是提升触及最可控的变量——而画廊、出版社与策展人正是用这个平台来发掘新人。在不知道当前频率的情况下，无法给出任何发布策略建议。",
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
  "Solo shows, institutional open calls, gallery representation by 30.": "个展、机构公开征集，30 岁前获得画廊代理。",
  "Exhibition history is thin. 2–3 more group shows are required before any gallery will discuss a solo show.": "展览经历尚浅。在任何画廊愿意谈个展之前，还需要 2–3 场联展。",
  "Right if you're primarily motivated by the physical exhibition experience and gallery community.": "如果你最看重实体展览的体验与画廊圈子，这条路最适合你。",
  "Publication Track": "出版路线",
  "Primary identity as an illustrator and artist-book maker.": "以插画家与艺术书创作者为主要身份。",
  "Second solo book, international distribution, major book fairs by 30.": "30 岁前完成第二本个人作品集、国际发行、参与重要书展。",
  "No new publication since 2021. The content exists — it needs packaging.": "自 2021 年以来没有新出版物。内容已经具备——只差整理成册。",
  "Right if you're motivated by the book as object and the publishing community. Your formation already points here.": "如果你着迷于书作为实体，以及出版社群，这条路最适合你。你的成长背景本就指向这里。",
  "Hybrid Track": "复合路线",
  "Artist-publisher: books and gallery shows running in parallel.": "艺术家兼出版者：书与画廊展览并行。",
  "The book practice feeds the gallery presence and vice versa. Bookshop gallery shows bridge both worlds.": "出版实践滋养画廊呈现，反之亦然。书店画廊展览连接两个世界。",
  "Requires more energy and time management than either single track.": "比任何单一路线都更考验精力与时间管理。",
  "The most natural fit given your existing practice. The daily diary is simultaneously publication material and gallery-worthy work.": "鉴于你现有的实践，这是最自然的选择。每日水彩日记既是出版素材，也是值得展出的作品。",
  "The Hybrid Track is the best structural fit. The bookshop gallery show is the single highest-leverage action — it advances both tracks with one move.": "复合路线在结构上最契合。书店画廊展览是单一杠杆最高的行动——一步同时推进两条路线。",
  "Age 30 (approximately 4 years from now)": "30 岁（大约从现在起 4 年后）",

  // ── Instagram ──
  "Primary visual portfolio platform — 26k followers built through daily watercolor diary practice since 2020. The platform galleries, publishers, and curators use for discovery.": "你主要的视觉作品集平台——自 2020 年起通过每日水彩日记积累了 2.6 万粉丝。也是画廊、出版社与策展人用来发掘新人的平台。",
  "Instagram is an established strength — 26k followers, already a working portfolio and the surface galleries and publishers use to discover you. Growth from here is a bonus, not a requirement.": "Instagram 已是你确立的优势——2.6 万粉丝，本身就是一份运转中的作品集，也是画廊与出版社发掘你的入口。继续增长是加分项，而非必需。",
  "A years-long watercolor diary since 2020. The material is already there; nothing about visibility asks you to paint more.": "自 2020 年起、持续多年的水彩日记。素材已经现成；提升曝光并不要求你画得更多。",
  "Urban environments, cats, domestic life, travel fragments — subjects that already do well on Instagram": "城市环境、猫、日常生活、旅行片段——这些题材在 Instagram 上本就表现不错。",
  "A low-effort way to deepen your reach without painting more: short process videos — a time-lapse, or a clip of a piece coming together. They travel well on Instagram and Reels, suit a slow studio practice, and turn work you're already doing into something to share.": "一种省力、又能扩大触及的方式，且无需多画：短的创作过程视频——延时摄影，或一幅作品逐渐成形的片段。它们在 Instagram 和 Reels 上传播力强，契合慢节奏的工作室创作，把你本就在做的事变成可以分享的内容。",

  // ── Pathway steps ──
  "Artist-run spaces are the natural path: 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN. Each show builds credibility and introduces your work to gallery directors.": "艺术家自营空间是最自然的路径：3331 Arts Chiyoda、Design Festa Gallery、Gallery IYN。每一场展览都积累信誉，并把你的作品介绍给画廊主理人。",
  "UTRECHT, Book and Sons, or flotsam books. Bridges illustration community into gallery context — a natural fit given your publication background.": "UTRECHT、Book and Sons 或 flotsam books。把插画社群引入画廊语境——鉴于你的出版背景，这是自然的契合。",
  "Builds presence in the Tokyo zine and book ecosystem. Creates a natural entrypoint for bookshop gallery conversations and strengthens the publication half of your CV.": "在东京独立刊物与书籍生态中建立存在感。为书店画廊的洽谈创造自然的切入口，并强化你简历中出版的那一半。",

  // ── Press / collaboration / audience / collector ──
  "Domestic interiors and everyday life — directly aligned with your subject matter": "家居室内与日常生活——与你的题材直接契合",
  "Large illustration/photography community; annual book prize you could enter": "庞大的插画／摄影社群；有可投递的年度书籍奖项",
  "The 5 co-exhibitors from Tide from China are your strongest existing collaboration seeds. Their current Tokyo presence and active practice is unconfirmed — tell Saffron whether you've stayed in contact with any of them.": "「潮自中国」联展的 5 位共同参展者，是你现有最强的合作种子。他们目前是否在东京、是否仍活跃尚未确认——请告诉红雀你是否还和其中任何人保持联系。",
  "Whether your 26k Instagram following is concentrated in China, Japan, or distributed internationally determines which geographic markets to prioritise — for exhibitions, fairs, and publishers. A primarily Chinese audience suggests a different expansion path than a globally distributed one.": "你那 2.6 万 Instagram 粉丝究竟集中在中国、日本，还是分布于全球，决定了该优先经营哪些地域市场——展览、博览会与出版社皆然。以中文受众为主，意味着与全球分布截然不同的拓展路径。",
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
  "Not a classical fine arts track": "非传统纯艺路径",
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
  "Solid for this stage, especially with a solo collection at 21": "对这个阶段而言相当扎实，尤其是 21 岁就有了个人作品集",
  "Right in the typical band for illustrators at this stage — a solid, real audience for print and zine discovery, with room to grow toward the 50k market-viability signal": "正处于这个阶段插画师的典型区间——一个扎实而真实的受众群，利于印刷品与独立刊物被发掘，并有空间向 5 万这一市场可行性信号增长",
  "Exhibition history is the weakest dimension. The 26k Instagram following is a solid, real asset at this career stage but not yet a standout — it sits in the typical peer range. The near-term work is converting audience into exhibition and publication credits.": "展览经历是最薄弱的一环。2.6 万 Instagram 粉丝在这个事业阶段是扎实而真实的资产，但还算不上突出——它落在同侪的典型区间内。近期的功课是把受众转化为展览与出版的履历。",
  "~6 (daily practice from 2020, first publication 2021)": "约 6 年（2020 年起每日创作，2021 年首次出版）",

  // ── Month names ──
  "January": "一月", "February": "二月", "March": "三月", "April": "四月",
  "May": "五月", "June": "六月", "July": "七月", "August": "八月",
  "September": "九月", "October": "十月", "November": "十一月", "December": "十二月",

  // ── Readiness (careerData) ──
  "Tier 1-2 foundation building": "第 1–2 层级的基础建设",
  "Complete 2 more Tokyo group show(s) to reach the 3-show minimum that opens Tier 3 conversations.": "再完成 2 场东京联展，达到开启第 3 层级洽谈所需的 3 场最低门槛。",
  "Insufficient group show history": "联展经历不足",
  "Apply to open calls at 3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN": "向 3331 Arts Chiyoda、Design Festa Gallery、Gallery IYN 的公开征集投递",
  "No solo show on CV": "简历上尚无个展",
  "Target bookshop gallery solo show: UTRECHT, Book and Sons, flotsam books, 日記屋 月日": "争取书店画廊个展：UTRECHT、Book and Sons、flotsam books、日記屋 月日",
  "No institutional exhibition history": "尚无机构展览经历",
  "Watch TOKAS open calls and Youkobo artist-in-residence programs": "关注 TOKAS 公开征集与 Youkobo 驻地项目",
  "No international exhibition outside Japan/China": "在日本／中国之外尚无国际展览",
  "Consider global watercolor open calls or table at Offprint Paris / London Art Book Fair": "考虑国际水彩公开征集，或在 Offprint Paris／London Art Book Fair 设展位",
  "No Japan Watercolor Society membership or exhibition": "尚无日本水彩画会会员资格或展览",
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

function SectionShell({ title, subtitle, summary, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen)
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

// Humanize a raw activity status (e.g. "in_contact") into a readable label.
function actStatusLabel(status, t) {
  const key = `sf.actStatus.${status}`
  const v = t(key)
  if (v && v !== key) return v
  return String(status || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}


// ── Original four sections ─────────────────────────────────────────────────

function CareerPosition({ data, t }) {
  const ig = data.social.find(s => s.platform === 'Instagram')
  const summary = `${data.exhibitions.length} · ${data.publications.length} · Instagram ${ig?.followers ?? '—'} · ${data.base}`

  const igStr = ig?.followers || '26k'
  const m     = String(igStr).toLowerCase().match(/([\d.]+)\s*k/)
  const igNum = m ? parseFloat(m[1]) * 1000 : (parseInt(String(igStr).replace(/[^\d]/g, ''), 10) || 26000)
  const rings = [
    { id: 'ig',    label: t('sf.mile.followers'), current: igStr,                            target: '50k', pct: igNum / 50000,                color: '#c47a35' },
    { id: 'shows', label: t('sf.mile.shows'),     current: String(data.exhibitions.length),  target: '3',   pct: data.exhibitions.length / 3,  color: '#7a9e7e' },
    { id: 'pub',   label: t('sf.mile.pubs'),      current: String(data.publications.length), target: '3',   pct: data.publications.length / 3, color: '#c49a3e' },
  ]

  return (
    <SectionShell
      title={t('sf.sec.careerPosition')}
      subtitle={t('sf.sub.careerPosition')}
      summary={summary}
      defaultOpen={true}
    >
      <div className="sf-rings">
        {rings.map(rg => <MilestoneRing key={rg.id} {...rg} />)}
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
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.social')}</div>
          <table className="sf-social-table">
            <tbody>
              {data.social.map((s, i) => (
                <tr key={i}>
                  <td className="sf-social-platform">{s.platform}</td>
                  <td className="sf-social-handle">{s.handle}</td>
                  <td className="sf-social-followers">{s.followers}</td>
                  {s.posts != null ? <td className="sf-social-posts">{s.posts} {t('sf.label.posts')}</td> : <td />}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.education')}</div>
          <div className="sf-row-title">{data.education.institution}</div>
          <div className="sf-row-meta">{data.education.field} · {data.education.note}</div>
          <div className="sf-block-label" style={{ marginTop: '18px' }}>{t('sf.label.base')}</div>
          <div className="sf-row-title">{data.base}</div>
        </div>
      </div>
    </SectionShell>
  )
}

function MarketLandscape({ data, t }) {
  const maxCat  = Math.max(...data.category_breakdown.map(c => c.count), 1)
  const geoTotal = data.tokyo_vs_international.tokyo + data.tokyo_vs_international.international
  const tokyoPct = Math.round((data.tokyo_vs_international.tokyo / (geoTotal || 1)) * 100)
  const summary  = `${data.total} — ${data.tokyo_vs_international.tokyo} ${t('sf.label.tokyo')}, ${data.tokyo_vs_international.international} ${t('sf.label.international')}`

  return (
    <SectionShell
      title={t('sf.sec.market')}
      subtitle={t('sf.sub.market', { n: data.total })}
      summary={summary}
    >
      <div className="sf-market-grid">
        <div className="sf-market-block">
          <div className="sf-block-label">{t('sf.label.byCategory')}</div>
          <div className="sf-bars">
            {data.category_breakdown.map((cat, i) => (
              <div key={i} className="sf-bar-row">
                <span className="sf-bar-label">{cat.label}</span>
                <div className="sf-bar-track">
                  <div className="sf-bar-fill" style={{ width: `${(cat.count / maxCat) * 100}%` }} />
                </div>
                <span className="sf-bar-count">{cat.count}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="sf-market-block">
          <div className="sf-block-label">{t('sf.label.tokyoVsIntl')}</div>
          <div className="sf-geo-bar">
            <div className="sf-geo-tokyo" style={{ width: `${tokyoPct}%` }} />
            <div className="sf-geo-intl"  style={{ width: `${100 - tokyoPct}%` }} />
          </div>
          <div className="sf-geo-legend">
            <span className="sf-geo-label sf-geo-label-tokyo">{t('sf.label.tokyo')} — {data.tokyo_vs_international.tokyo}</span>
            <span className="sf-geo-label sf-geo-label-intl">{t('sf.label.international')} — {data.tokyo_vs_international.international}</span>
          </div>
          <div className="sf-block-label" style={{ marginTop: '28px' }}>{t('sf.label.byAction')}</div>
          <div className="sf-action-list">
            {data.actionability.map((a, i) => (
              <div key={i} className={`sf-action-row sf-action-${a.tier}`}>
                <span className="sf-action-label">{a.label}</span>
                <span className="sf-action-count">{a.count}</span>
              </div>
            ))}
          </div>
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
}

function ComparableArtists({ artists, t }) {
  const top     = artists.slice(0, 4)
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

function StrategicPathway({ data, t }) {
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
      </div>
    </SectionShell>
  )
}

// ── New sections ───────────────────────────────────────────────────────────

function InstagramStrategy({ data, t }) {
  const ig = data.platforms.find(p => p.name === 'Instagram')
  const postingFreq = data.known?.posting_frequency

  return (
    <SectionShell
      title={t('sf.sec.instagram')}
      subtitle={t('sf.sub.instagram')}
      summary={`Instagram ${ig?.followers ?? '—'}`}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('pp.ig.platform')}</div>
          {data.platforms.map((p, i) => (
            <div key={i} className="sf-platform-row">
              <div className="sf-platform-name">{p.name}</div>
              <div className="sf-platform-handle">{p.handle}</div>
              <div className="sf-platform-followers">{p.followers ?? '—'}{p.posts != null ? ` · ${p.posts} ${t('sf.label.posts')}` : ''}</div>
              <div className="sf-platform-note">{p.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">{t('pp.ig.known')}</div>
          <div className="sf-row-title" style={{ marginBottom: 6 }}>{data.known.diary_practice}</div>
          <div className="sf-row-meta">{data.known.content_type}</div>

          {data.strategy && (
            <div style={{ marginTop: 16 }}>
              <div className="sf-block-label">{t('sf.ig.strategy')}</div>
              <p className="sf-info-text">{data.strategy}</p>
            </div>
          )}

          {postingFreq && (
            <div className="sf-peppercorn-answer" style={{ marginTop: 16 }}>
              <div className="sf-block-label">{t('sf.label.postingFreq')}</div>
              <div className="sf-answer-bubble">{postingFreq}</div>
            </div>
          )}
        </div>
      </div>
    </SectionShell>
  )
}

function AudienceGeography({ data, t }) {
  // Only show when there's a real audience report — no "what's missing" meta.
  if (!data.available || !data.artist_report) return null
  return (
    <SectionShell
      title={t('sf.sec.audienceGeo')}
      subtitle={t('sf.sub.audienceGeo')}
      summary={t('sf.sum.audienceGeo.live')}
    >
      <div className="sf-info-block">
        <div className="sf-block-label">{t('sf.label.artistReport')}</div>
        <div className="sf-answer-bubble sf-answer-bubble--geo">{data.artist_report}</div>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.whyMatters')}</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
      </div>
    </SectionShell>
  )
}

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

function CareerBenchmarks({ data, t }) {
  const rec = data.artist_record
  const summary = `${rec.exhibitions} · ${rec.publications} · Instagram ${rec.instagram ?? '—'}`
  return (
    <SectionShell
      title={t('sf.sec.benchmarks')}
      subtitle={t('sf.sub.benchmarks')}
      summary={summary}
    >
      <p className="sf-peers-caveat">{data.summary}</p>
      <div className="sf-benchmark-grid">
        {data.peer_range.map((row, i) => {
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

function SeasonalCalendar({ data, t }) {
  const known = data.months.reduce((n, m) => n + m.opportunities.length, 0)
  const summary = t('sf.sum.calendarUnknown', { known, n: data.unknown_deadline_count, s: data.unknown_deadline_count !== 1 ? 's' : '' })
  return (
    <SectionShell
      title={t('sf.sec.calendar')}
      subtitle={t('sf.sub.calendar')}
      summary={summary}
    >
      {data.months.length === 0 ? (
        <EmptyState message={t('sf.empty.calendar')} />
      ) : (
        <div className="sf-calendar">
          {data.months.map((m, i) => (
            <div key={i} className="sf-cal-month">
              <div className="sf-cal-month-name">{m.month}</div>
              <div className="sf-cal-opps">
                {m.opportunities.map((o, j) => (
                  <div key={j} className="sf-cal-opp">
                    <span className="sf-cal-cat">{o.category}</span>
                    <span className="sf-cal-name">{o.name}</span>
                    <span className="sf-cal-dl">{o.deadline}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      {data.rolling.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <div className="sf-block-label">{t('sf.label.rolling', { n: data.rolling.length })}</div>
          <div className="sf-cal-rolling">
            {data.rolling.map((o, i) => (
              <div key={i} className="sf-cal-opp sf-cal-opp--rolling">
                <span className="sf-cal-cat">{o.category}</span>
                <span className="sf-cal-name">{o.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      <div className="sf-cal-note">{data.coverage_note}</div>
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

function CollectorEcosystem({ data, t }) {
  return (
    <SectionShell
      title={t('sf.sec.collector')}
      subtitle={t('sf.sub.collector')}
      summary={t('sf.sum.collector')}
    >
      <div className="sf-info-block">
        <div className="sf-block-label">{t('sf.label.whyMatters')}</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.fairsPipeline')}</div>
        <div className="sf-tag-list">
          {data.fairs_in_pipeline.map((f, i) => <span key={i} className="sf-trait">{f}</span>)}
        </div>
      </div>
    </SectionShell>
  )
}

function CollaborationMap({ data, t }) {
  const summary = t('sf.sum.coExhibitors', { n: data.known_co_exhibitors.length, s: data.known_co_exhibitors.length !== 1 ? 's' : '' })
  return (
    <SectionShell
      title={t('sf.sec.collab')}
      subtitle={t('sf.sub.collab')}
      summary={summary}
    >
      <div className="sf-block-label">{t('sf.label.knownCoExhib')}</div>
      {data.known_co_exhibitors.map((a, i) => (
        <div key={i} className="sf-collab-row">
          <span className="sf-collab-name">{a.name}</span>
          <span className="sf-collab-context">{a.context}</span>
          <span className="sf-collab-status">{t('sf.label.currentStatus')} {a.current_status}</span>
        </div>
      ))}
      <p className="sf-info-text" style={{ marginTop: 14 }}>{data.note}</p>
    </SectionShell>
  )
}

function GeographicExpansion({ data, t }) {
  const summary = t('sf.label.primaryBase')
  return (
    <SectionShell
      title={t('sf.sec.geoExpansion')}
      subtitle={t('sf.sub.geoExpansion')}
      summary={summary}
    >
      <div className="sf-geo-regions">
        {data.regions.map((r, i) => (
          <div key={i} className={`sf-geo-region sf-geo-region--${r.status}`}>
            <div className="sf-geo-region-header">
              <span className="sf-geo-region-name">{r.name}</span>
              <span className="sf-geo-region-count">
                {r.pipeline_count > 0 ? t('sf.inPipeline', { n: r.pipeline_count }) : ''}
              </span>
              <span className="sf-geo-status-tag">{t(`sf.geo.${r.status}`) || r.status.replace(/_/g, ' ')}</span>
            </div>
            <p className="sf-geo-region-note">{r.note}</p>
            {r.entry_point && (
              <div className="sf-geo-entry">{t('sf.label.entryPoint')} {r.entry_point}</div>
            )}
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

function PublicationLandscape({ data, t }) {
  const summary = `${data.pipeline_count} · ${data.artist_publications.length}`
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
                  {t(`sf.barrier.${tier.barrier}`) || tier.barrier}
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
  const PROB_COLORS = { high: '#5a7a30', moderate: '#c47a35', low: '#b03020' }
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
                style={{ color: PROB_COLORS[s.probability] || '#7a5030' }}
              >
                {t(`sf.prob.${s.probability}`) || s.probability}
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

const STATUS_KEYS = {
  ready_to_review:  'sf.status.readyReview',
  ready_to_contact: 'sf.status.readyContact',
  contacted:        'sf.status.contacted',
  not_contacted:    'sf.status.notContacted',
}
const STATUS_COLORS = {
  ready_to_review: '#c47a35', ready_to_contact: '#5a7a30',
  contacted: '#3a6a20', not_contacted: '#9a7040',
}

function VenueTracker({ data, t }) {
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
          {data.tracked.map((v, i) => {
            const color = STATUS_COLORS[v.status] || '#9a7040'
            const label = t(STATUS_KEYS[v.status] || 'sf.status.notContacted')
            return (
              <div key={i} className="sf-venue-row">
                <div className="sf-venue-header">
                  <a className="sf-venue-name sf-ext-link" href={sfSearch(`${v.name} ${v.city || ''}`)} target="_blank" rel="noreferrer">{v.name} ↗</a>
                  <span className="sf-venue-type">{v.type} · {v.city}</span>
                  <span className="sf-venue-status" style={{ color }}>{label}</span>
                  {v.priority && <span className="sf-venue-priority">{t('sf.venue.priority', { n: v.priority })}</span>}
                </div>
                <div className="sf-venue-last">
                  {v.last_contacted
                    ? t('sf.venue.lastContacted', { date: v.last_contacted })
                    : t('sf.venue.notContacted')}
                </div>
                {v.next_action && (
                  <div className="sf-venue-next">{v.next_action}</div>
                )}
              </div>
            )
          })}
        </div>
      )}
      {data.gap_note && (
        <div className="sf-insight-callout" style={{ marginTop: 20 }}>{data.gap_note}</div>
      )}
    </SectionShell>
  )
}

// Open questions map 1:1 (in order) to the saffron_answers slots in api.py.
const SF_ANSWER_KEYS = [
  'posting_frequency', 'audience_geography', 'has_sold_work', 'new_publication_planned',
  'has_artist_statement', 'tide_china_contact', 'second_exhibition_planned', 'price_points',
]

function QuestionRow({ q, index, t }) {
  const [value, setValue] = useState('')
  const [saved, setSaved] = useState(false)
  const key = SF_ANSWER_KEYS[index]

  function save() {
    const v = value.trim()
    if (!v || !key) return
    setSaved(true)
    fetch('/api/saffron_answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key, value: v }),
    }).catch(() => {})
  }

  return (
    <div className="sf-question-row">
      <div className="sf-question-number">{index + 1}</div>
      <div className="sf-question-body">
        <div className="sf-question-text">{q.question}</div>
        <div className="sf-question-why">{q.why_it_matters}</div>
        {saved ? (
          <div className="sf-question-saved">{t('sf.oq.saved')}</div>
        ) : (
          <div className="sf-question-answer">
            <input
              className="sf-question-input"
              value={value}
              onChange={e => setValue(e.target.value)}
              placeholder={t('sf.oq.placeholder')}
              onKeyDown={e => { if (e.key === 'Enter') save() }}
            />
            <button className="sf-question-save" onClick={save} disabled={!value.trim()}>
              {t('sf.oq.save')}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function OpenQuestions({ data, t }) {
  return (
    <SectionShell
      title={t('sf.sec.openQs')}
      subtitle={t('sf.sub.openQs')}
      summary={`${data.count}`}
    >
      <p className="sf-info-text" style={{ marginBottom: 24 }}>{t('sf.label.openQNote')}</p>
      <div className="sf-questions">
        {data.questions.map((q, i) => <QuestionRow key={i} q={q} index={i} t={t} />)}
      </div>
    </SectionShell>
  )
}

// ── Licensing Landscape ────────────────────────────────────────────────────

const TIER_COLORS = { now: '#16a34a', near_term: '#d97706', medium_term: '#9ca3af' }

function locF(item, field, lang) {
  if (lang === 'zh' && item[field + '_zh']) return item[field + '_zh']
  if (lang === 'ja' && item[field + '_ja']) return item[field + '_ja']
  return item[field] || ''
}

function LicensingLandscape({ t, lang }) {
  const d = LICENSING_LANDSCAPE
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      {d.items.map((group, gi) => (
        <div key={gi} className="sf-insight-group">
          <div className="sf-block-label">{locF(group, 'category', lang)}</div>
          <div className="sf-licensing-entries">
            {group.entries.map((entry, ei) => (
              <div key={ei} className="sf-licensing-entry">
                <div className="sf-licensing-entry-header">
                  <span className="sf-licensing-name">{entry.name}</span>
                  <span className="sf-tier-badge" style={{ color: TIER_COLORS[entry.tier] || '#9ca3af' }}>
                    {t(`sf.tier.${entry.tier}`) || entry.tier}
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

function PressPitchMap({ t, lang }) {
  const d = PRESS_PITCH_MAP
  const outlets = d.items.filter(item => item.name)
  const discoveryNote = d.items.find(item => item.category_note)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-press-pitch-list">
        {outlets.map((item, i) => (
          <div key={i} className="sf-press-pitch-row">
            <div className="sf-press-pitch-header">
              <span className="sf-press-pitch-name">{item.name}</span>
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
                  {item.contact}
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
  const d = GRANT_LANDSCAPE
  const grants = d.items.filter(item => item.name)
  const strategyNote = d.items.find(item => item.category_note)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-grant-list">
        {grants.map((grant, i) => (
          <div key={i} className="sf-grant-row">
            <div className="sf-grant-header">
              <span className="sf-grant-name">{grant.name}</span>
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
  const d = REVENUE_STREAMS
  const streams = d.items.filter(item => item.stream !== 'Summary assessment')
  const summary_item = d.items.find(item => item.stream === 'Summary assessment')
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-revenue-list">
        {streams.map((item, i) => (
          <div key={i} className={`sf-revenue-row${item.leaving_on_table ? ' sf-revenue-row--gap' : ''}`}>
            <div className="sf-revenue-header">
              <span className="sf-revenue-stream">{locF(item, 'stream', lang)}</span>
              {item.realistic_monthly && (
                <span className="sf-revenue-range">{item.realistic_monthly}</span>
              )}
              {item.leaving_on_table && (
                <span className="sf-revenue-gap-tag">{t('sf.label.gapTag')}</span>
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
              {mi < d.milestones.length - 1 && (
                <div className="sf-depmap-connector" />
              )}
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
  stalling:     '#b03020',
}

function CareerMomentum({ data, t }) {
  const { totals, response_rate, trajectory, monthly_chart } = data
  const [activity, setActivity] = useState(data.recent_activity || [])
  const maxBar = Math.max(...monthly_chart.map(m => m.submissions + m.contacts), 1)

  async function removeEvent(id) {
    setActivity(a => a.filter(x => x.id !== id))
    try { await fetch(`/api/career_events/${id}`, { method: 'DELETE' }) } catch { /* no-op */ }
  }
  const trajColor = TRAJECTORY_COLORS[trajectory] || '#9a7040'
  const summary = t('sf.sum.momentum', { submissions: totals.submissions, venues: totals.venues_in_crm, rate: response_rate })

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
            {t(`sf.mom.traj.${trajectory}`) || trajectory}
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

function TimingIntelligence({ data, t }) {
  const maxCount = Math.max(...data.monthly_counts.map(m => m.count), 1)
  const summary  = t('sf.sum.timing', { peaks: data.peak_months.slice(0, 2).join(' · '), dated: data.with_parsed_deadline })

  return (
    <SectionShell
      title={t('sf.sec.timing')}
      subtitle={t('sf.sub.timing')}
      summary={summary}
    >
      <div className="sf-insight-callout">{data.key_insight}</div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.timing.deadlinesByMonth')}</div>
      <div className="sf-timing-grid">
        {data.monthly_counts.map((m, i) => (
          <div key={i} className="sf-timing-month">
            <div className="sf-timing-month-name">{m.month.slice(0, 3)}</div>
            <div className="sf-timing-bar-track">
              <div
                className={`sf-timing-bar${data.peak_months.includes(m.month) ? ' sf-timing-bar--peak' : ''}`}
                style={{ height: `${Math.round((m.count / maxCount) * 100)}%` }}
              />
            </div>
            <div className="sf-timing-count">{m.count || ''}</div>
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

function CareerTimeline({ t }) {
  const d = CAREER_TIMELINE
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-insight-callout">{d.overall_assessment}</div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.timeline.artistStage')}</div>
      <div className="sf-timeline-stage">
        <span className="sf-trait">{t('sf.timeline.age', { n: d.artist_stage.age })}</span>
        <span className="sf-trait">{t('sf.timeline.groupShow', { n: d.artist_stage.group_shows, s: d.artist_stage.group_shows !== 1 ? 's' : '' })}</span>
        <span className="sf-trait">{t('sf.timeline.publications', { n: d.artist_stage.publications, s: d.artist_stage.publications !== 1 ? 's' : '' })}</span>
        {d.artist_stage.instagram && <span className="sf-trait">Instagram {d.artist_stage.instagram}</span>}
      </div>

      <div className="sf-peers-grid" style={{ marginTop: 24 }}>
        {d.peers.map((peer, i) => (
          <div key={i} className="sf-peer-card">
            <a
              className="sf-peer-name sf-peer-link"
              href={PEER_IG[peer.name] ? `https://www.instagram.com/${PEER_IG[peer.name]}/` : sfSearch(`${peer.name} instagram`)}
              target="_blank"
              rel="noreferrer"
            >
              {peer.name} ↗
            </a>
            <div className="sf-peer-region">{peer.region} · {peer.comparable_age}</div>
            <div className="sf-block-label" style={{ marginTop: 12, fontSize: '0.72rem' }}>{t('sf.timeline.hadAtStage')}</div>
            <ul className="sf-timeline-had-list">
              {peer.at_stage.had.map((h, j) => <li key={j}>{h}</li>)}
            </ul>
            <div className="sf-peer-use" style={{ marginTop: 10 }}>{peer.comparison}</div>
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

// ── Pricing Intelligence ───────────────────────────────────────────────────

const IMPACT_COLORS = { high: '#5a7a30', medium: '#c47a35', low: '#9ca3af' }

function PricingIntelligence({ t }) {
  const d = PRICING_INTELLIGENCE
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
                {t(`sf.pricing.impact.${f.impact}`) || f.impact}
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

// ── Opportunity Gap Analysis ───────────────────────────────────────────────

function OpportunityGap({ data, t }) {
  const summary = `${data.gaps.length} gaps · ${data.strengths.length} strengths`
  return (
    <SectionShell
      title={t('sf.sec.oppGap')}
      subtitle={t('sf.sub.oppGap')}
      summary={summary}
    >
      <div className="sf-insight-callout">{data.summary}</div>

      {data.gaps.length > 0 && (
        <>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.gap.underrepresented')}</div>
          <div className="sf-gap-list">
            {data.gaps.map((g, i) => (
              <div key={i} className="sf-gap-row sf-gap-row--gap">
                <div className="sf-gap-row-header">
                  <span className="sf-gap-label">{g.label}</span>
                  <span className="sf-gap-counts">
                    {g.actual_count} {t('sf.gap.vs')} ~{g.expected_count} {t('sf.gap.expected')}
                  </span>
                </div>
                <p className="sf-gap-note">{g.note}</p>
              </div>
            ))}
          </div>
        </>
      )}

      {data.strengths.length > 0 && (
        <>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.gap.strengths')}</div>
          <div className="sf-gap-list">
            {data.strengths.map((g, i) => (
              <div key={i} className="sf-gap-row sf-gap-row--strength">
                <div className="sf-gap-row-header">
                  <span className="sf-gap-label">{g.label}</span>
                  <span className="sf-gap-counts">
                    {g.actual_count} {t('sf.gap.tracked')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.gap.portfolioFocus')}</div>
      <div className="sf-tag-list">
        {data.top_actual_categories.map((c, i) => (
          <span key={i} className="sf-trait">{c.category.replace(/_/g, ' ')} ({c.count})</span>
        ))}
      </div>
    </SectionShell>
  )
}

// ── Career Readiness ───────────────────────────────────────────────────────

const GAP_DOT_COLORS = {
  HIGH:   '#c47a35',
  MEDIUM: '#d4a855',
  LOW:    '#b0a080',
}

function MilestoneRing({ pct, current, target, label, color }) {
  const r = 30
  const circ = 2 * Math.PI * r
  const p = Math.max(0, Math.min(pct || 0, 1))
  return (
    <div className="sf-ring">
      <svg viewBox="0 0 76 76" className="sf-ring-svg">
        <circle cx="38" cy="38" r={r} className="sf-ring-track" />
        <circle
          cx="38" cy="38" r={r} className="sf-ring-fill"
          transform="rotate(-90 38 38)"
          style={{ stroke: color, strokeDasharray: circ, strokeDashoffset: circ * (1 - p) }}
        />
        <text x="38" y="37" className="sf-ring-current">{current}</text>
        <text x="38" y="50" className="sf-ring-target">/ {target}</text>
      </svg>
      <div className="sf-ring-label">{label}</div>
    </div>
  )
}

function ReadinessBar({ label, sublabel, pct, color }) {
  return (
    <div className="sf-readiness-bar-row">
      <div className="sf-readiness-bar-header">
        <span className="sf-readiness-bar-label">{label}</span>
        <span className="sf-readiness-bar-pct">{Math.round(pct)}%</span>
      </div>
      <div className="sf-readiness-track">
        <div className="sf-readiness-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <div className="sf-readiness-sublabel">{sublabel}</div>
    </div>
  )
}

const CAT_LABELS = {
  'Open Calls & Fairs':      'Open Calls & Fairs',
  'Galleries':               'Galleries',
  'Zines & Books':           'Zines & Books',
  'Residencies & Grants':    'Residencies & Grants',
  'Competitions & Awards':   'Competitions & Awards',
  'Cafes & Bookshop Spaces': 'Cafes & Bookshop Spaces',
  'Other':                   'Other',
}

const MEDIUM_LABELS = {
  watercolor:  'Watercolor',
  painting:    'Painting',
  illustration:'Illustration',
  book_arts:   'Book Arts',
  mixed:       'Mixed / Multi-medium',
  photography: 'Photography',
  unknown:     'Medium unspecified',
}

function MarketStats({ data }) {
  const { t } = useLanguage()
  if (!data) return null
  const cats   = Object.entries(data.by_category || {})
  const maxCat = Math.max(...cats.map(([, v]) => v), 1)
  const { top_tier = 0, mid_tier = 0, lower_tier = 0 } = data.score_distribution || {}
  const scoreTotal = (top_tier + mid_tier + lower_tier) || 1
  const dp = data.deadline_pressure || {}
  const total = data.total_opportunities || 0
  const summary = t('sf.ms.summary', { total, top: top_tier, deadlines: dp.this_month || 0 })
  return (
    <SectionShell title={t('sf.ms.title')} subtitle={t('sf.ms.subtitle')} summary={summary}>
      <div className="sf-block-label">{t('sf.ms.byType')}</div>
      <div className="sf-bars sf-ms-bars">
        {cats.map(([label, count]) => (
          <div key={label} className="sf-bar-row">
            <span className="sf-bar-label">{CAT_LABELS[label] || label}</span>
            <div className="sf-bar-track"><div className="sf-bar-fill sf-ms-bar-fill" style={{ width: `${(count / maxCat) * 100}%` }} /></div>
            <span className="sf-bar-count">{count}</span>
          </div>
        ))}
      </div>
      <div className="sf-ms-two-col" style={{ marginTop: 32 }}>
        <div>
          <div className="sf-block-label">{t('sf.ms.deadlinePressure')}</div>
          <div className="sf-ms-pressure-list">
            <div className="sf-ms-pressure-row sf-ms-pressure--hot"><span className="sf-ms-pressure-num">{dp.this_month || 0}</span><span className="sf-ms-pressure-label">{t('sf.ms.thisMonth')}</span></div>
            <div className="sf-ms-pressure-row sf-ms-pressure--warm"><span className="sf-ms-pressure-num">{dp.next_3_months || 0}</span><span className="sf-ms-pressure-label">{t('sf.ms.next3months')}</span></div>
            <div className="sf-ms-pressure-row sf-ms-pressure--cool"><span className="sf-ms-pressure-num">{dp.open_ongoing || 0}</span><span className="sf-ms-pressure-label">{t('sf.ms.rollingOngoing')}</span></div>
          </div>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.ms.mediumFit')}</div>
          <div className="sf-ms-medium-list">
            {Object.entries(data.by_medium || {}).map(([med, cnt]) => (
              <div key={med} className="sf-ms-medium-row">
                <span className={`sf-ms-medium-label${med === 'watercolor' ? ' sf-ms-medium--wc' : ''}`}>{MEDIUM_LABELS[med] || med}</span>
                <span className="sf-ms-medium-count">{cnt}</span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="sf-block-label">{t('sf.ms.scoreDistrib')}</div>
          <div className="sf-ms-score-tiers">
            <div className="sf-ms-score-row sf-ms-score--high"><div className="sf-ms-score-bar-wrap"><div className="sf-ms-score-bar" style={{ width: `${(top_tier / scoreTotal) * 100}%` }} /></div><span className="sf-ms-score-num">{top_tier}</span><span className="sf-ms-score-label">{t('sf.ms.scoreHigh')}</span></div>
            <div className="sf-ms-score-row sf-ms-score--mid"><div className="sf-ms-score-bar-wrap"><div className="sf-ms-score-bar" style={{ width: `${(mid_tier / scoreTotal) * 100}%` }} /></div><span className="sf-ms-score-num">{mid_tier}</span><span className="sf-ms-score-label">{t('sf.ms.scoreMid')}</span></div>
            <div className="sf-ms-score-row sf-ms-score--low"><div className="sf-ms-score-bar-wrap"><div className="sf-ms-score-bar" style={{ width: `${(lower_tier / scoreTotal) * 100}%` }} /></div><span className="sf-ms-score-num">{lower_tier}</span><span className="sf-ms-score-label">{t('sf.ms.scoreLow')}</span></div>
          </div>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.ms.top5')}</div>
          <div className="sf-ms-top-list">
            {(data.top_scored || []).map((opp, i) => (
              <div key={i} className="sf-ms-top-row"><span className="sf-ms-top-rank">{i + 1}</span><span className="sf-ms-top-name">{opp.name}</span><span className="sf-ms-top-score">{opp.score}</span></div>
            ))}
          </div>
        </div>
      </div>
    </SectionShell>
  )
}

function ReadinessCorrection({ t }) {
  const [title, setTitle] = useState('')
  const [venue, setVenue] = useState('')
  const [year,  setYear]  = useState('')
  const [saved, setSaved] = useState(false)

  async function addShow() {
    if (!title.trim()) return
    const body = { title: title.trim(), venue: venue.trim(), date: year.trim() }
    setTitle(''); setVenue(''); setYear(''); setSaved(true)
    setTimeout(() => setSaved(false), 3200)
    try {
      await fetch('/api/exhibition_log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
    } catch { /* no-op on network failure */ }
  }

  return (
    <div className="sf-readiness-hedge">
      <p className="sf-readiness-hedge-text">{t('sf.cr.hedge')}</p>
      <div className="sf-readiness-addshow">
        <input className="sf-hedge-input" value={title} onChange={e => setTitle(e.target.value)} placeholder={t('sf.cr.addShow.title')} />
        <input className="sf-hedge-input" value={venue} onChange={e => setVenue(e.target.value)} placeholder={t('sf.cr.addShow.venue')} />
        <input className="sf-hedge-input sf-hedge-input--year" value={year} onChange={e => setYear(e.target.value)} onKeyDown={e => e.key === 'Enter' && addShow()} placeholder={t('sf.cr.addShow.year')} />
        <button className="sf-hedge-add" onClick={addShow} disabled={!title.trim()}>{t('sf.cr.addShow.btn')}</button>
      </div>
      {saved && <p className="sf-readiness-hedge-saved">{t('sf.cr.addShow.saved')}</p>}
    </div>
  )
}

function CareerReadiness({ data }) {
  const { t } = useLanguage()
  if (!data) return null

  const tier3Pct = (data.readiness_scores?.tier_3_readiness ?? 0) * 100
  const tier4Pct = (data.readiness_scores?.tier_4_readiness ?? 0) * 100
  const gaps     = data.blocking_gaps ?? []
  const actNow   = (data.immediate_priorities ?? []).slice(0, 3)
  const build    = data.build_toward ?? []
  const watch    = data.watch_list   ?? []
  const months   = data.months_to_tier3

  const summary = data.current_phase
    ? `${data.current_phase}${months ? ` · ${t('sf.cr.monthsToTier3', { n: months })}` : ''}`
    : t('sf.cr.title')

  return (
    <SectionShell
      title={t('sf.cr.title')}
      subtitle={t('sf.cr.subtitle')}
      summary={summary}
    >
      {/* Four-tier ladder */}
      <p className="sf-tiers-intro">{t('sf.cr.tiersIntro')}</p>
      <div className="sf-readiness-bars">
        <div className="sf-tier-done">
          <span className="sf-tier-check">✓</span>
          <span className="sf-tier-name">{t('sf.cr.tier1')}</span>
          <span className="sf-tier-status">{t('sf.cr.tierComplete')}</span>
        </div>
        <div className="sf-tier-done">
          <span className="sf-tier-check">✓</span>
          <span className="sf-tier-name">{t('sf.cr.tier2')}</span>
          <span className="sf-tier-status">{t('sf.cr.tierComplete')}</span>
        </div>
        <ReadinessBar
          label={t('sf.cr.tier3')}
          sublabel={t('sf.cr.tier3Sublabel')}
          pct={tier3Pct}
          color="#c47a35"
        />
        <ReadinessBar
          label={t('sf.cr.tier4')}
          sublabel={t('sf.cr.tier4Sublabel')}
          pct={tier4Pct}
          color="#d4b87a"
        />
      </div>

      {/* Timeline pill + next milestone */}
      <div className="sf-readiness-milestone-row">
        {months != null && (
          <span className="sf-readiness-timeline-pill">{t('sf.cr.monthsToTier3', { n: months })}</span>
        )}
      </div>
      {data.next_milestone && (
        <p className="sf-readiness-milestone">{data.next_milestone}</p>
      )}

      {/* Blocking gaps */}
      {gaps.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <div className="sf-block-label">{t('sf.cr.blockingGaps')}</div>
          <div className="sf-readiness-gaps">
            {gaps.map((g, i) => (
              <div key={i} className="sf-readiness-gap-row">
                <span
                  className="sf-readiness-gap-dot"
                  style={{ background: GAP_DOT_COLORS[g.priority] ?? '#b0a080' }}
                />
                <div className="sf-readiness-gap-body">
                  <span className="sf-readiness-gap-text">{g.gap}</span>
                  {g.action && (
                    <span className="sf-readiness-gap-action">{g.action}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <ReadinessCorrection t={t} />

      {/* Three columns */}
      <div className="sf-readiness-columns" style={{ marginTop: 28 }}>
        <div className="sf-readiness-col">
          <div className="sf-block-label">{t('sf.cr.actNow')}</div>
          {actNow.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : actNow.map((o, i) => (
              <div key={i} className="sf-readiness-col-item">
                <span className="sf-readiness-col-name">{o.name ?? o.title ?? o}</span>
                {o.score != null && (
                  <span className="sf-readiness-col-score">{Math.round(o.score * 10) / 10}</span>
                )}
              </div>
            ))
          }
        </div>
        <div className="sf-readiness-col">
          <div className="sf-block-label">{t('sf.cr.buildToward')}</div>
          {build.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : build.map((o, i) => (
              <div key={i} className="sf-readiness-col-item">
                <span className="sf-readiness-col-name">{o.name ?? o.title ?? o}</span>
              </div>
            ))
          }
        </div>
        <div className="sf-readiness-col sf-readiness-col--watch">
          <div className="sf-block-label">{t('sf.cr.watchList')}</div>
          {watch.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : watch.map((o, i) => (
              <div key={i} className="sf-readiness-col-item sf-readiness-col-item--muted">
                <span className="sf-readiness-col-name">{o.name ?? o.title ?? o}</span>
              </div>
            ))
          }
        </div>
      </div>
    </SectionShell>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function SaffronPage({ nav }) {
  const [rawData,    setRawData]    = useState(null)
  const [rawCareer,  setRawCareer]  = useState(null)
  const [error,      setError]      = useState(null)
  const [tab,        setTab]        = useState('profile')
  const { t, lang } = useLanguage()

  useEffect(() => {
    fetch('/api/saffron')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setRawData)
      .catch(e => setError(e.message))
  }, [])

  useEffect(() => {
    fetch('/api/career_strategy')
      .then(r => { if (!r.ok) throw null; return r.json() })
      .then(setRawCareer)
      .catch(() => {})
  }, [])

  // Translate the served (English) analysis into Chinese for 中文 viewers.
  // Translator map: dynamic opportunity strings come from the payload's own
  // _i18n (rebuilt from live data every run, so it survives pipeline updates);
  // the static authored prose comes from SF_ZH (zh only).
  const txMap = useMemo(() => {
    if (lang === 'zh') return { ...(rawData?._i18n?.zh || {}), ...SF_ZH }
    if (lang === 'ja') return rawData?._i18n?.ja || null
    return null
  }, [rawData, lang])
  const data       = useMemo(() => (txMap ? deepTranslate(rawData,   txMap) : rawData),   [rawData,   txMap])
  const careerData = useMemo(() => (txMap ? deepTranslate(rawCareer, txMap) : rawCareer), [rawCareer, txMap])

  const SF_TABS = [
    ['profile',       t('sf.cat.profile')],
    ['landscape',     t('sf.cat.landscape')],
    ['strategy',      t('sf.cat.strategy')],
    ['calendar',      t('sf.cat.calendar')],
    ['relationships', t('sf.cat.relationships')],
    ['money',         t('sf.cat.money')],
  ]
  function goTab(key) {
    setTab(key)
    // Reset to the top of the content so the new section starts at its beginning —
    // scrollIntoView on an already-pinned sticky bar does nothing, so scroll the
    // window to the content's top instead.
    requestAnimationFrame(() => {
      const el = document.querySelector('.sf-content')
      if (el) {
        const top = el.getBoundingClientRect().top + window.scrollY - 4
        window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
      }
    })
  }

  return (
    <div className="saffron-page">
      <section className="saffron-hero">
        <img src={saffronHero} alt="Saffron's wide view" className="saffron-hero-img" />
      </section>
      {nav}

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

          <SectionErrorBoundary key={tab}>
            {tab === 'profile' && (
              <>
                {careerData && <CareerReadiness data={careerData} />}
                <CareerPosition     data={data.career_position}    t={t} />
                <CareerBenchmarks   data={data.career_benchmarks}  t={t} />
                <CareerTimeline     t={t} />
                <ComparableArtists  artists={data.peer_artists}    t={t} />
                <InstagramStrategy  data={data.instagram_strategy} t={t} />
                <AudienceGeography  data={data.audience_geography} t={t} />
                <CareerMomentum     data={data.career_momentum}    t={t} />
              </>
            )}
            {tab === 'landscape' && (
              <>
                <MarketStats         data={data.market_stats} />
                <MarketLandscape     data={data.market_landscape}     t={t} />
                <OpportunityGap      data={data.opportunity_gap}      t={t} />
                <GeographicExpansion data={data.geographic_expansion} t={t} />
              </>
            )}
            {tab === 'strategy' && (
              <>
                <StrategicPathway    data={data.pathway}             t={t} />
                <LongTermScenarios   data={data.long_term_scenarios} t={t} />
                <CareerDependencyMap t={t} lang={lang} />
                <OpenQuestions       data={data.open_questions}      t={t} />
              </>
            )}
            {tab === 'calendar' && (
              <>
                <SeasonalCalendar   data={data.seasonal_calendar}   t={t} />
                <TimingIntelligence data={data.timing_intelligence} t={t} />
              </>
            )}
            {tab === 'relationships' && (
              <>
                <PressFeatures      data={data.press_features}      t={t} />
                <PressPitchMap      t={t} lang={lang} />
                <CollaborationMap   data={data.collaboration_map}   t={t} />
                <CollectorEcosystem data={data.collector_ecosystem} t={t} />
                <VenueTracker       data={data.venue_tracker}       t={t} />
              </>
            )}
            {tab === 'money' && (
              <>
                <RevenueStreams       t={t} lang={lang} />
                <PricingIntelligence  t={t} />
                <GrantLandscape       t={t} lang={lang} />
                <LicensingLandscape   t={t} lang={lang} />
                <PublicationLandscape data={data.publication_landscape} t={t} />
              </>
            )}
          </SectionErrorBoundary>
        </div>
      )}
    </div>
  )
}
