# Saffron Chinese audit — all strategy ladder copy

Source: [strategy_ladders.js](C:/ScottStuff/GalleryAgentAI/frontend/src/data/strategy_ladders.js). Exact object paths are stable locators. Every Chinese leaf was reviewed, including all expanded treatments. These prose proposals accompany a structural recommendation to replace scored ladders with evidence and optional sequences; changing labels alone does not correct the evidence rules.


## STATES.g_publication.label — Retain

**Current:** 第一本出版物


## STATES.g_publication.detail — Rewrite

**Current:** 《色彩日记》（2021），从每日日记的实践里长出来。履历里出版的那一半已经成立。


**Replace with:** 《Colour Diary》由持续的水彩日记整理而来，已成为你的出版经历之一。

**Reason:** Avoid unverified translated title/date and awkward 出版的那一半成立.


## STATES.g_group.label — Retain

**Current:** 中国与日本的联展


## STATES.g_group.detail — Rewrite

**Current:** 已确认 8 场，从上海、广州到东京——是一段真正的展览史，而不是一次初登场。


**Replace with:** 已有 8 场已确认联展，展出地点包括上海、广州和东京。

**Reason:** Count should be derived; no faint praise about first outing.


## STATES.g_institutional.label — Retain

**Current:** 美术馆与机构展览


## STATES.g_institutional.detail — Rewrite

**Current:** 天津的棉美术馆与台州的横渡美术馆。机构的背书是商业空间给不了的：它们没有货要卖。


**Replace with:** 曾在天津棉美术馆和台州横渡美术馆参加展览。这些经历可以连同项目介绍与现场资料一起收入作品集。

**Reason:** Institution != no commerce; do not demean commercial venues.


## STATES.g_solo.label — Rewrite

**Current:** 个展，包括在东京


**Replace with:** 已举办个展

**Reason:** Remove 包括在东京 as dangling translation.


## STATES.g_solo.detail — Rewrite

**Current:** 记录中有三场，最近一次是原宿 Galerie LE MONDE 的《光与影与猫》，2026 年 9 月 6 日结束。作品已经能独自撑起一个空间。


**Replace with:** 已有三场个展记录，最近一场在原宿 Galerie LE MONDE，于 2026 年 9 月 6 日结束。可用展览介绍和现场照片呈现这一组作品。

**Reason:** Recognition plus usable evidence; preserve official title separately, no invented translation.


## STATES.g_international.label — Rewrite

**Current:** 第一次国际展出


**Replace with:** 在更多地区展出

**Reason:** Chinese artist in Japan already international; London is not start of all international work.


## STATES.g_international.detail — Rewrite

**Current:** 2025 年 12 月的伦敦展出，把作品带出了中国和日本——国际记录由此开始。


**Replace with:** 2025 年 12 月曾在伦敦展出，作品也由此接触到中日之外的展览环境。

**Reason:** Precise geographic claim.


## STATES.g_press.label — Rewrite

**Current:** 被评论，而不只是被转载


**Replace with:** 关于作品的采访与评论

**Reason:** Positive name; not downgrade existing press.


## STATES.g_press.detail — Rewrite

**Current:** 记录中有三篇报道——Bored Panda 两次，Design You Trust 一次。都是把图放上去，没有一篇在论述；而策展人能引用的，恰恰是论述。


**Replace with:** 已有报道以作品介绍为主。未来如有围绕创作展开的采访或评论，可以与现有报道一起整理，帮助读者了解作品的背景。

**Reason:** No single mandatory next rung or unsupported curator requirement. Count mismatch 2 vs 3 must be reconciled.


## STATES.g_representation.label — Rewrite

**Current:** 一家代理你销售的画廊


**Replace with:** 持续的画廊合作

**Reason:** Representation is an option, not universal goal.


## STATES.g_representation.detail — Rewrite

**Current:** 目前可走的最大一步，而且是从已有的展览记录里长出来的。代理抬的是单张画的价格，不只是卖出的张数——因为画廊介绍的是它打算长期留住的藏家。


**Replace with:** 可以比较画廊提供的展览、销售和藏家联络支持，再判断合作范围是否适合自己的创作安排。

**Reason:** Remove largest possible step and guaranteed price rise.


## STATES.g_fairs.label — Rewrite

**Current:** 更强的个展场地与艺博会


**Replace with:** 进一步的展览与艺博会机会

**Reason:** 更强 describes prestige as personal score.


## STATES.g_fairs.detail — Rewrite

**Current:** 成熟的商业画廊、机构个展，以及藏家聚集的艺博会——东京艺术博览会、Tokyo Gendai。通常是通过代理画廊到达，而不是在那之前。


**Replace with:** 不同艺博会和机构展览有各自的参与方式。有些通过画廊，有些接受独立申请，需要分别核对。

**Reason:** Not a fixed ladder dependency.


## STATES.a_cadence.label — Rewrite

**Current:** 不停下来的每日实践


**Replace with:** 持续的水彩日记

**Reason:** No obligation never to stop.


## STATES.a_cadence.detail — Rewrite

**Current:** 自 2020 年起每天不断的水彩日记。这条阶梯往上的一切都建立在稳定的作品产出之上，而这一级是多数创作者始终没跨过的。


**Replace with:** 从 2020 年开始的水彩日记，已经积累成可用于展览、出版和作品介绍的素材。

**Reason:** Avoid unsupported most artists fail comparison.


## STATES.a_look.label — Rewrite

**Current:** 缩略图大小也认得出的面貌


**Replace with:** 逐渐清晰的画面风格

**Reason:** Less mechanical thumbnail criterion.


## STATES.a_look.detail — Rewrite

**Current:** 城市建筑、室内光线、水彩的透明感——已经稳定了六年。在信息流里，认出来发生在读到名字之前，所以那种面貌必须自己撑住。


**Replace with:** 城市建筑、室内光线和水彩的透明感，在你的作品中持续出现。这些关联可以帮助整理作品系列与对外介绍。

**Reason:** Specific appreciation; recognize not guaranteed audience response.


## STATES.a_found.label — Rewrite

**Current:** 一群自己找上来的读者


**Replace with:** 多个平台上的关注者

**Reason:** No assumptions about acquisition.


## STATES.a_found.detail — Rewrite

**Current:** X 上大约 89,300 人，微博 65,000 人，小红书 44,000 人，Instagram 日记 27,000 人，B 站 7,500 人——合计大约 233,000 个关注，没有一个是买来的。这已经是一群受众，也是这条阶梯往上乘算的基数。


**Replace with:** 你在 X、微博、小红书、Instagram 和 B 站都有关注者。各平台数量可分别展示，并注明记录日期；跨平台关注会重叠，不能直接当作独立人数或实际触达。

**Reason:** No claim none paid; followers not reach.


## STATES.a_series.label — Rewrite

**Current:** 会延续的作品，而不是堆积的作品


**Replace with:** 已有名称的作品系列

**Reason:** Remove negation and belittling accumulation.


## STATES.a_series.detail — Rewrite

**Current:** 日记是被看的；一个有名字、有编号、还在继续的系列是被追的——因为它给人回来看下一张的理由。你其实已经这样归类过作品了：《一天和四季》《彩色日记翻翻乐》《365日永恒如新》都是有名字、有编号的。


**Replace with:** 《一天和四季》《彩色日记翻翻乐》《365日永恒如新》已有名称与编号，可以继续用于整理视频、出版选题或系列介绍。

**Reason:** Concrete recognition without claiming proven retention.


## STATES.a_motion.label — Rewrite

**Current:** 被看见的作画过程


**Replace with:** 已记录的作画过程

**Reason:** Grounded possession rather than audience mind reading.


## STATES.a_motion.detail — Rewrite

**Current:** 这一级你已经做到了：你会拍作画过程，成片发在 B 站，那边大约有 7,500 人是为此关注你的。水彩在湿纸上化开，是静止图像几乎唯一拍不到的东西——而你的过程，只有你拍得出来。


**Replace with:** 你已经拍摄并在 B 站发布作画过程。视频保留了成画之外的变化，例如水分、颜料和笔触如何逐步形成画面。

**Reason:** Do not infer every follower’s reason.


## STATES.a_motion.treatment.open — Rewrite

**Current:** 已经有了这一级，意味着什么


**Replace with:** 这些视频还可以怎样使用

**Reason:** Remove levels.


## STATES.a_motion.treatment.hide — Retain

**Current:** 收起


## STATES.a_motion.treatment.blocks.0.label — Rewrite

**Current:** 它改变了什么


**Replace with:** 视频能补充什么

**Reason:** Useful heading.


## STATES.a_motion.treatment.blocks.0.text — Rewrite

**Current:** 一张画完的画，要和所有画完的画竞争。一张正在被画的画几乎没有对手——颜料落在湿纸上的那一瞬间，没法截图、没法转述，也没有别人能复制。这是你的实践里，结构上唯一属于你自己的东西。


**Replace with:** 过程视频可以呈现水彩在纸面上的变化，也让读者看到作品如何完成。它与成画可以互相补充。

**Reason:** Remove no competition, impossible screenshot, only uniquely hers claims.


## STATES.a_motion.treatment.blocks.1.label — Rewrite

**Current:** 你已经付出的成本


**Replace with:** 已有素材，可以少做哪些准备

**Reason:** Recognize existing labor.


## STATES.a_motion.treatment.blocks.1.text — Rewrite

**Current:** 没有额外成本，而这正是关键。这条阶梯上其它每一级都要求一件新的事——想一个系列、学一个平台、给一个人写信。这一级只是你每天都要坐的那张桌子的副产品，而且你已经产出了一阵子了。


**Replace with:** 已有录像可以减少重新拍摄的工作。整理时仍需确认文件、画幅、声音和字幕，再决定哪些适合直接使用。

**Reason:** Zero additional cost erases effort.


## STATES.a_motion.treatment.blocks.2.label — Rewrite

**Current:** 值得拍的是什么


**Replace with:** 可以选取的片段

**Reason:** Optional selection, not technique lesson.


## STATES.a_motion.treatment.blocks.2.text — Rewrite

**Current:** 不是整张画。是媒介做出观众预料不到的事的那些瞬间——一片洗染在潮纸上化开、盐或干笔破开一块平涂、第一笔重色落进浅色里、用干净笔把颜色再吸出来。建筑给了你硬边，去和软边形成对比——留住注意力的正是这种反差。


**Replace with:** 可以从已经拍好的片段中，选取画面变化清楚的部分，例如颜色扩散、明暗形成或建筑细节逐渐出现。是否保留完整过程，取决于这条视频想呈现什么。

**Reason:** Do not invent salt/drybrush as her technique or promise attention.


## STATES.a_motion.treatment.blocks.3.label — Rewrite

**Current:** 同一个文件还能去哪里


**Replace with:** 用于其他平台前，需要检查什么

**Reason:** Replace same-file magical portability.


## STATES.a_motion.treatment.blocks.3.text — Rewrite

**Current:** B 站上已经有了。同一个文件不用重剪、也不用翻译，就能同样放在 Instagram 那边——因为看颜料流动不需要语言。也就是说，唯一一样在你两群读者之间原样成立的东西，眼下只给其中一边看。


**Replace with:** 以画面为主的片段可以减少语言转换工作。用于其他平台前，仍需检查画幅、时长、字幕、音乐使用范围与封面。

**Reason:** No platform reach guarantees.


## STATES.a_motion.treatment.blocks.4.label — Rewrite

**Current:** 它在什么位置


**Replace with:** 放进作品介绍

**Reason:** Replace vague position.


## STATES.a_motion.treatment.blocks.4.text — Rewrite

**Current:** 它不只属于受众这一条。当每一张画都还有「一段录像」这第二次生命时，一个有名字的系列会容易维持得多；而正在考虑授权的品牌，看到这种面貌是手工做出来的，会更放心。


**Replace with:** 过程片段也可以放在系列介绍或作品集旁边，帮助编辑、合作方和读者了解创作方式。

**Reason:** No assertion buyers reassured or series easier to maintain.


## STATES.a_weekly.label — Rewrite

**Current:** 让作画影片抵达那些从没看过的人


**Replace with:** 尝试跨平台发布过程片段

**Reason:** No inference nobody has seen videos.


## STATES.a_weekly.detail — Rewrite

**Current:** 这件事你已经做成过一次，而且成绩比你记录里的任何东西都好：2023 年连续六周的翻翻乐，播放量分别是 55,000、49,000、16,000。那些作画影片一条都没有发到 X 或 Instagram——那边的 89,300 和 27,000 位关注者从来没看过。


**Replace with:** 2023 年连续发布的翻页视频中，有几条取得较高播放量。这组内容可以作为研究样本，比较主题、编排与发布时间，再判断哪些部分值得重新使用。

**Reason:** Remove best achievement ever and cross-platform unseen claim.


## STATES.a_weekly.treatment.open — Rewrite

**Current:** 你自己的频道已经证明了什么


**Replace with:** 看看这组视频的数据

**Reason:** Observation not proof.


## STATES.a_weekly.treatment.hide — Retain

**Current:** 收起


## STATES.a_weekly.treatment.blocks.0.label — Rewrite

**Current:** 短片是长片的 8.5 倍——这是你自己频道的数字，不是通则


**Replace with:** 这批样本中，短视频的播放中位数较高

**Reason:** Metric attached to comparison.


## STATES.a_weekly.treatment.blocks.0.text — Rewrite

**Current:** 你有 33 条能看到数据的影片：两分半以内的，播放中位数约 9,975；超过两分半的，约 1,172。你最好的九条里有八条是短片。那些 14 到 21 分钟的实时录制，播放大多在 1,200 到 5,400 之间——付出多得多，回报少得多。


**Replace with:** 在目前记录的 33 条视频中，时长不足两分半的视频播放中位数约为 9,975，较长视频约为 1,172，相差约 8.5 倍。这是该批样本的差异；题材、发布时间和传播条件也可能影响结果。

**Reason:** Specify sample and measure; do not equate views with reward or effort.


## STATES.a_weekly.treatment.blocks.1.label — Rewrite

**Current:** 但起作用的从来不只是长度


**Replace with:** 系列编排也值得比较

**Reason:** Hypothesis, not causal claim.


## STATES.a_weekly.treatment.blocks.1.text — Rewrite

**Current:** 你最近的短片没有重现那个结果——去年八月那条 0:36 的只有 139 播放。2023 年那一轮有的是一个「钩子」：一本画完的 365 天日记、编好号的集数、每周一条。人们是回来看下一集的。值得保留的是这件事，而它跟拍摄技巧无关。


**Replace with:** 2023 年这组视频围绕完成的日记、编号和连续发布展开。可以把这些特点与其他视频比较；仅凭播放量，还不能确定观众是否为了下一集回来。

**Reason:** Avoid 钩子 and invented repeat-viewing motivation; remove humiliating 139-view contrast from headline.


## STATES.a_weekly.treatment.blocks.2.label — Rewrite

**Current:** 粉丝数是怎么涨起来的


**Replace with:** 播放量还不能说明什么

**Reason:** Useful uncertainty.


## STATES.a_weekly.treatment.blocks.2.text — Rewrite

**Current:** 受众会涨，是因为有东西触到了还没关注你的人；否则就是把同样的作品，反复放给同一屋子人看。在唯一能看到数字的那个频道上，你 33 条影片里有 9 条的播放量超过了你在那边的粉丝数，其中 8 条都在两分半以内，最好的一条是 7.3 倍。那六周是连续每周一条发出去的。这个节奏不需要学，只需要再做一次。


**Replace with:** 播放次数可能包含重复观看。把历史播放量与今天的关注数量相除，也无法推算当时有多少新观众或新增关注。若要判断这一点，需要对应时期的后台数据。

**Reason:** No views > followers => discovery proof.


## STATES.a_weekly.treatment.blocks.3.label — Rewrite

**Current:** 不要只发限时动态


**Replace with:** 让作品介绍便于日后查看

**Reason:** No scolding not-stories title.


## STATES.a_weekly.treatment.blocks.3.text — Rewrite

**Current:** 等这些真的发到 Instagram 时：限时动态 24 小时就没了，只触达那天打开 App 的人，三月份才找到你的策展人什么也看不到。发在主页或做成 Reels，它会留下；如果只能发限时动态，事后存进精选。延时完全可以——颜料化开的过程，压缩过往往比实时更好看。


**Replace with:** 如果希望日后进入主页的人也能找到，可以选择便于长期查看的发布方式，并按当前平台功能整理作品。

**Reason:** Avoid brittle claims about stories and curator arrival month.


## STATES.a_weekly.treatment.blocks.4.label — Rewrite

**Current:** 这些文件本来就有


**Replace with:** 先检查一条已有视频

**Reason:** Small optional step.


## STATES.a_weekly.treatment.blocks.4.text — Rewrite

**Current:** 作画的素材早就拍好、剪好了——积了好几年。它们不用重剪、也不用翻译就能发到另外两个地方——因为看颜料流动不需要语言。它们现在只触达一边，唯一的原因就是只发了一边。


**Replace with:** 可以先选一条已有片段，检查画幅、字幕、音乐和文件质量，再判断是否适合用于另一个平台。

**Reason:** No only-reason blame or claim files definitely retained.


## STATES.a_borrowed.label — Rewrite

**Current:** 出现在别人的受众里


**Replace with:** 与其他创作者共同呈现作品

**Reason:** People not audience assets to borrow.


## STATES.a_borrowed.detail — Rewrite

**Current:** 增长最快的方式是借来的，而不是攒出来的——一本合印的 zine、一个双人展、互相介绍。已经梳理出十二位在相邻领域创作的艺术家。


**Replace with:** 合印 zine、共同展览或互相介绍作品，都是可能的合作方式。对象是否适合，需要看作品、双方意愿与实际联系；这份资料不代表合作已经成立。

**Reason:** No fastest growth claim; referenced 12-person map is unmounted.


## STATES.a_second.label — Rewrite

**Current:** 中文世界里也有读者，不只是 Instagram


**Replace with:** 不同平台上的读者

**Reason:** Platform not language.


## STATES.a_second.detail — Rewrite

**Current:** 这两边你都已经有了，而且中文这边现在明显更大：微博大约 65,000 人，小红书大约 44,000 人，Instagram 上的日记大约 27,000 人，再加上 B 站 7,500 人。两种语言，不止一群读者，同一批画。


**Replace with:** 微博、小红书、B 站、Instagram 和 X 上的作品呈现，可以按各平台的内容与读者反馈分别研究。关注数量、读者语言和购买情况是不同的信息。

**Reason:** Avoid false Chinese/English split.


## STATES.a_second.treatment.open — Rewrite

**Current:** 同时有这两边，意味着什么


**Replace with:** 比较不同平台能提供什么

**Reason:** Plain label.


## STATES.a_second.treatment.hide — Retain

**Current:** 收起


## STATES.a_second.treatment.blocks.0.label — Rewrite

**Current:** 为什么小红书适合这些画


**Replace with:** 小红书上的现有内容

**Reason:** Not unsupported platform-wide popularity.


## STATES.a_second.treatment.blocks.0.text — Rewrite

**Current:** 城市街景、室内、日常生活、日本，本来就是那上面阅读量最高的几类，而且配文用的是你的母语，不是第二语言。一个住在东京、画这座城市的中国画家，在那边本身就是有人在追的题材——不需要解释。


**Replace with:** 可以从已经发布的街景、室内与日常题材中，比较读者对哪些内容有回应。语言、配文和选图都可作为观察条件。

**Reason:** No invented top content categories or nationality = genre.


## STATES.a_second.treatment.blocks.1.label — Rewrite

**Current:** 两群读者比一群多出什么


**Replace with:** 分别了解读者与购买条件

**Reason:** Remove two-room metaphor.


## STATES.a_second.treatment.blocks.1.text — Rewrite

**Current:** 他们用不同的货币买东西、被不同的算法找到，而且不会因为某一个平台改了推荐方式就一起消失。为一个市场定价印出来的东西，不用再做新的，就能卖进另一个。


**Replace with:** 不同平台的读者可能重叠。判断销售机会时，需要分别了解可用的购买渠道、配送范围和实际订单，不能只比较关注数量。

**Reason:** No assumed currencies, no shared collapse claim.


## STATES.a_second.treatment.blocks.2.label — Rewrite

**Current:** 影片放在这里的位置


**Replace with:** 视频素材的其他用途

**Reason:** Natural heading.


## STATES.a_second.treatment.blocks.2.text — Rewrite

**Current:** 你已经在拍作画过程了，B 站上大约有 7,500 人是为这些影片关注你的。同一个文件不用重剪、也不用翻译，就能同样发到其他账号——看颜料流动完全不需要语言，所以它是唯一一样能在中文和英文两边原样成立的东西。


**Replace with:** 已有过程视频可以作为跨平台尝试的素材。以画面为主的片段可能减少翻译工作，仍需检查发布规格与声音使用范围。

**Reason:** Remove unique language-free medium, unsupported follower intent.


## STATES.a_second.treatment.blocks.3.label — Rewrite

**Current:** 究竟哪个账号最大


**Replace with:** 对外介绍时选哪个账号

**Reason:** Utility without ranking people.


## STATES.a_second.treatment.blocks.3.text — Rewrite

**Current:** 既不是 Instagram，也不是小红书——是 X，大约 89,300 人，是 Instagram 日记的三倍多。微博第二，65,000 人，然后是小红书，44,000 人。值得知道，是因为它决定了自我介绍里该放哪个账号：你最大的那间屋子，是英文的那一间。


**Replace with:** 选择便于对方查看作品、且内容完整的账号。关注数量可以单独记录，但不必决定每一次介绍使用哪个平台。

**Reason:** Do not infer X audience English; respect Instagram-only outreach instruction.


## STATES.a_second.treatment.blocks.4.label — Rewrite

**Current:** 还不知道的部分


**Replace with:** 还需要哪些信息

**Reason:** Avoid internal bookkeeping story.


## STATES.a_second.treatment.blocks.4.text — Rewrite

**Current:** 五个账号之间有多少是同一批人——所以大约 233,000 这个总数是触达的上限，而不是真实人数。按语言分倒是清楚的，而微博改变了这个格局：大约 116,500 人用中文看你的作品（微博、小红书、B 站），现在几乎追平了大约 116,300 人用英文看你的作品（X、Instagram）——在算上微博之前，这个比例是英文侧两倍于中文侧。


**Replace with:** 目前不能从公开关注数确认跨平台重叠、读者语言、实际触达或购买意愿。后续有相应记录时，再补充这些判断。

**Reason:** Follower sum not ceiling on reach: nonfollowers may view too.


## STATES.a_inbound.label — Rewrite

**Current:** 不用去找、自己会来的受众


**Replace with:** 逐步了解实际购买需求

**Reason:** Inbound attention not guaranteed purchasability.


## STATES.a_inbound.detail — Rewrite

**Current:** 这条阶梯上其余的一切，都是为了到达这个状态。到了这个规模，印一版书不再是赌博——你最好的印制方案 109 本回本：只按 Instagram 日记算是 250 人里有 1 人；把你已经拥有的全部算进来，是 2,100 人里有 1 人。


**Replace with:** 已有关注可以帮助新产品被看见，是否购买仍需通过实际订单了解。印量可以结合试卖或预订情况来安排，避免直接用关注数量预测销量。

**Reason:** Remove gambling reassurance and flawed 109/follower arithmetic.


## STATES.l_reproduces.label — Rewrite

**Current:** 经得起复制的题材


**Replace with:** 适合印制的作品文件

**Reason:** Print fidelity is testable, not inherent in subject.


## STATES.l_reproduces.detail — Rewrite

**Current:** 水彩的建筑与室内光线，缩小、量产地印出来依然成立，也正好落在授权真正会买的品类里——文具、日历、书封、室内。


**Replace with:** 现有作品可以通过样品检查缩放、裁切和色彩还原，再判断适合哪些印刷产品。

**Reason:** No automatic reproduction suitability.


## STATES.l_inprint.label — Retain

**Current:** 已经印出来的作品


## STATES.l_inprint.detail — Rewrite

**Current:** 八本 zine，两本出版物。委托方能看到这些作品已经走过一次生产流程——这和作品好不好，是两个问题。


**Replace with:** 已有 zine 和出版物，可以作为作品印制效果的样本。授权使用前仍需确认图像文件与相关权利。

**Reason:** No quality vs production lecture; rights may differ.


## STATES.l_lookbook.label — Rewrite

**Current:** 当天就能发出去的作品集


**Replace with:** 可供合作方查看的授权作品集

**Reason:** No same-day completion promise.


## STATES.l_lookbook.detail — Rewrite

**Current:** 十到二十件作品做成产品效果图，一份 PDF。美术总监没法凭空想象一张画印在笔记本封面上是什么样，效果图替他想。


**Replace with:** 可将选定作品与少量产品排版样例放进一份 PDF，并附上联系方式和授权说明。样例用于说明用途，不代表已有商业合作。

**Reason:** Do not insult art director imagination; remove arbitrary 10–20 demand.


## STATES.l_findable.label — Rewrite

**Current:** 出现在委托方检索的地方


**Replace with:** 可被检索的作品资料

**Reason:** Plain purpose.


## STATES.l_findable.detail — Rewrite

**Current:** 授权大多是对方找上门，所以出现在美术总监会检索的档案库和图库里，就是「主动去投」和「被找到」之间的差别。已经核实过四条这样的渠道确实存在；至于你的名字在不在上面，这个系统没有查过。


**Replace with:** 可以查看相关作品目录和图库的收录要求、费用与合同。是否已经收录你的资料，需要另外确认。

**Reason:** No “most licensing inbound” claim or measured gap inference.


## STATES.l_first.label — Retain

**Current:** 第一笔付费授权


## STATES.l_first.detail — Rewrite

**Current:** 它作为先例，比作为收入更值钱：一个可以引用的价格，和一个可以再问一次的客户。杂志插图大约从 5,000 日元起，书封大约 70,000 日元。


**Replace with:** 如果已有付费授权，可以记录使用范围、期限、费用和结算方式，供下一次报价参考。这里尚未确认相关记录。

**Reason:** Unknown is not absence; remove commission rates misused as license fees.


## STATES.l_repeat.label — Rewrite

**Current:** 回头客，和一个由你定的价


**Replace with:** 再次合作与追加使用

**Reason:** Three jobs do not determine a market price.


## STATES.l_repeat.detail — Rewrite

**Current:** 一笔授权是一份工作；同一品类里的三笔，就是一个价位。日本已公开的价格，杂志封面到 100,000 日元，日历到 800,000 日元，而买断版权的定价是普通授权的两到三倍。


**Replace with:** 持续合作可以积累更具体的报价依据。再次使用作品时，需按新增用途、范围和期限商议。

**Reason:** Remove pseudo pricing rules and detached 800k calendar example.


## STATES.l_inbound.label — Rewrite

**Current:** 品牌自己找上门


**Replace with:** 品牌主动询问合作

**Reason:** Neutral optional outcome.


## STATES.l_inbound.detail — Rewrite

**Current:** 这条阶梯就是为了到达这个状态。ほぼ日有常设的「アーティストコレクション」手账封面系列，上面写着插画师的名字；而他们完全没有公开任何投稿入口——最后一次公开征集是 2010 年。这样的门，只会从另一边打开。


**Replace with:** ほぼ日的插画合作系列可作为研究案例。未找到公开投稿入口，只能说明目前可确认的渠道有限，不能据此判断合作只能怎样开始。

**Reason:** No-door metaphor is determinism; lack of public route not proof only inbound.


## GOALS.0.name — Rewrite

**Current:** 画廊这条路


**Replace with:** 画廊合作与展览

**Reason:** Clear goal without game.


## GOALS.1.name — Rewrite

**Current:** 一群固定的读者


**Replace with:** 作品传播与读者

**Reason:** Her audience already established.


## GOALS.2.name — Rewrite

**Current:** 国际授权


**Replace with:** 国际图像授权

**Reason:** Distinguish image rights from broad licensing.


## GOALS.2.why.a_look — Rewrite

**Current:** 品牌买的是一种能铺成产品线的面貌，所以它必须经得起被缩小、被大量复制——和在信息流里被认出来，靠的是同一种稳定。


**Replace with:** 产品系列需要在不同尺寸和版式下保持画面的一致性，可以通过样例和打样来检查。

**Reason:** Remove 面貌铺成产品线 translation.


## GOALS.2.why.a_series — Rewrite

**Current:** 一个产品系列一次要用好几件相关的作品，所以有名字的系列，比一张强的单图更容易授权。


**Replace with:** 相关作品便于展示一个产品系列的可能性，是否采用仍取决于具体需求。

**Reason:** Named series not inherently easier sale than strong single image.
