import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
D={
'where_to_start_zh':('TOKAS-Emerging 可作为机构个展的研究对象。2027 年度报名已截止；下面保留当届条件供准备时参考，下一轮以官方新公告为准。','Remove 最合适 and premature eligibility assurance; closed opportunity is not immediate start.'),
'items.0.amount_zh':('2027 年度：免费展览空间与 15 万日元制作支持，另有部分布展、运输及宣传支持。','Official page says partial assistance; note date and tax treatment in detail.'),
'items.0.eligibility_zh':('2027 年度要求在日本居住，且于 1991 年 4 月 1 日及以后出生，并能承担准备、实施与撤展等责任。其他条件见官方要项。','2026-09-10 official check: 1991, not 1990. Do not carry fixed birth cutoff into later cycles.'),
'items.0.why_apply_zh':('入选后可在 TOKAS 本乡举办个展，并获得制作与展示方面的支持。','Do not continually frame Chinese identity as barrier or personal exemption.'),
'items.0.tip_zh':('TOKAS 与 Arts Council Tokyo 的项目分别申请，各自的时间、材料和支持范围需要单独核对。','Remove defensive response to imaginary 合并申请 misunderstanding.'),
'items.1.amount_zh':('个人申请最高 30 万日元；实际额度及可计入的费用，以当轮指南为准。','Plain language; source refresh required for current cycle.'),
'items.1.eligibility_zh':('需要核对东京都内居住、艺术活动经历及项目实施等要求。涉及个人情况的部分，可向主办方确认。','Do not invent special doubt that a student visa is not residence or assert she has that status.'),
'items.1.why_apply_zh':('可用于符合条件的自主策划艺术活动，例如展览项目。','Remove unique-on-page claim and preserve project-cost purpose.'),
'items.1.tip_zh':('准备预算时，按指南分别列出可补助与需自行承担的费用。','Useful, specific action without bureaucratic redundancy.'),
'items.2.country_zh':('亚洲及美国的文化交流','Not simply United States for Asian artists; destinations governed by program.'),
'items.2.amount_zh':('个人奖助的金额、期限和支付安排，以 2027 年度官方指南为准。','Hold unsupported lump-sum claim; do not translate guessed payout mechanism.'),
'items.2.eligibility_zh':('中国大陆属于当届资格名单中的地区。国籍或永久居留只是条件之一，还需核对年龄、目的地及学习和工作安排。奖助期间的课程与教学限制，见官方指南。','Remove “这一关你过” and unsupported universal five-year rule; applicant eligibility cannot be inferred from nationality alone.'),
'items.2.why_apply_zh':('适合研究与文化交流计划，可以比较目的地、交流对象和所需时间。','Neither biggest nor only nationality fit is decision-worthy or established.'),
'items.2.tip_zh':('申请内容应围绕研究与文化交流展开，并说明希望了解的问题、交流对象和计划活动。作品制作经费或办展经费需另找适用项目。','Replace 去看/去做 slogan and prediction of rejection with accurate program purpose.'),
'items.3.amount_zh':('支持金额与类别，以当届项目指南为准。','Verify exact category, not overall foundation.'),
'items.3.eligibility_zh':('需按具体资助类别核对国籍、户籍、推荐材料及作品要求。','Current text collapses category-specific rules; hold for verification.'),
'items.3.why_apply_zh':('可作为国内创作资助的研究对象，先比较作品要求与自己的项目是否相符。','No only-China-route overclaim.'),
'items.3.tip_zh':('作品尺寸、材料、成果提交及收藏安排，会影响项目准备量，需先按对应类别核对。','“这和你现在的画法是两回事” judges practice; dimensions need exact applicable guide.'),
}

data=json.loads((OUT/'grants_snapshot.json').read_text(encoding='utf-8'))
rows=[]
def walk(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():
            q=p+'.'+k if p else k
            if k.endswith('_zh'):rows.append((q,v))
            elif isinstance(v,(dict,list)):walk(v,q)
    elif isinstance(o,list):
        for i,v in enumerate(o):walk(v,p+'.'+str(i))
walk(data)
parts=['# Saffron Chinese audit — grant detail\n\nSource: `frontend/src/data/saffron_insights.js`, `GRANT_LANDSCAPE`. All Chinese leaves in this object were read. Current Saffron renders only named items (0–3); item 4 is internal research, not visible copy. Dates/amounts retained for wording are still time-sensitive and require the source checks in the brief. No claim is made that every grant has been independently reverified.\n\nTOKAS 2027 correction: [official call](https://www.tokyoartsandspace.jp/archive/application/2026/20260616-331.html). ACC purpose/eligibility: [official 2027 guidelines](https://www.asianculturalcouncil.org/grant-opportunities).\n']
for path,old in rows:
    dec=D.get(path)
    status='Out of current UI' if path.startswith('items.4.') else ('Rewrite / verify conditions' if dec else 'Retain wording; recheck dated facts')
    parts.append(f'\n## {path} — {status}\n\n**Current:** {old}\n')
    if dec:parts.append(f'\n**Replace with:** {dec[0]}\n\n**Reason:** {dec[1]}\n')
(OUT/'04-Chinese-grants.md').write_text('\n'.join(parts),encoding='utf-8')
print(f'{len(rows)} grant fields reviewed; {len(D)} replacement entries')
