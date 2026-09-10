"""
outreach_kit_engine.py

The first letter — an actual email, not advice about emails.

Tokyo galleries do not run submission boxes; the researched route in is showing
up as a viewer and then writing. But "build relationships with galleries" is the
kind of instruction that never becomes an action. A draft she can change the
name on does.

The governing idea is Scott's (2026-09-04) and it is the strongest thing to come
out of that whole session: **the first contact asks for nothing.** There is
therefore nothing in it to refuse, and whatever comes back is a specification
she can go and build toward. A silence costs nothing either. It converts a
gatekeeper from a yes/no into a source of information.

The draft below is adapted from the outreach kit in
reports/design_saffron_career_trio.md, with one correction: that version had her
subject as "light and cats" (光と猫). Cats appear in her work but are not her
subject — it is architecture and space, and a first email to a gallery is the
last place to get that wrong.

She reads Chinese by default and works in Japanese, so the letter itself is
Japanese and the surrounding explanation is Chinese.
"""


def _t(en: str, zh: str) -> dict:
    return {"en": en, "zh": zh}


# Addressed to HAGI ART (Yanaka). Was Gallery Kogure, chosen in the 2026-09-04
# research as the closest roster match — but the 2026-09-07 pass checked that
# roster venue by venue and ruled Kogure out in writing (~35 artists in
# lacquer, mixed media, photography and sculpture, no watercolour or
# architectural specialism). The letter went on pointing there for three more
# days, so she was being handed a ready-to-send email to a gallery this system
# had already decided was wrong. Retargeted 2026-09-10. The body still works
# for any of them with the first paragraph changed.
# Japanese business-letter conventions this had been breaking (cold read,
# 2026-09-10). In order of how much they cost:
#   1. No closing. It ended at the signature with no 何卒よろしくお願い申し上げます,
#      which is close to mandatory and reads foreign by its absence.
#   2. The politeness level flipped mid-paragraph — 開催しました (丁寧語) and then
#      開催いたしました (謙譲語) two sentences apart, about the same shows.
#   3. The exhibition count read as 1 + 3 = 4. "This year at LE MONDE" followed
#      by "three solo shows to date" gave no way to tell the LE MONDE show was
#      one of the three. It is. Stated as three, with LE MONDE as the most
#      recent, which is also how the ladder states it.
#   4. The request never arrived: 実物をお持ちしてご覧いただければ幸いです chains
#      two humble forms without asking for the occasion.
#   5. Subject line was a question. Japanese subject lines are noun phrases, and
#      見ていただけますでしょうか is the doubled-polite form besides.
# 御中 vs ご担当者様: ご担当者様 is right here — the letter is addressed to a
# person at the gallery, not to the organisation as an entity.
LETTER_JA = """件名：作品ご高覧のお願い（水彩画家 GEGYjiji）

HAGI ART ご担当者様

はじめまして。東京で水彩を描いております GEGYjiji と申します。
先日、貴廊の「［拝見した展覧会名］」を拝見し、
若い作家の作品を丁寧に紹介されている場だと感じ、ご連絡いたしました。

2020年から毎日一枚の水彩を描き続けており、東京の街角や室内、
建築とそこに射す光を主題にしております。これまでに上海と東京で
個展を三度開催しており、直近は今年、原宿の Galerie LE MONDE での
個展です。天津・台州の美術館でのグループ展にも参加しております。

作品5点を下記にまとめております。

［リンク］

お忙しいところ恐れ入りますが、もしご興味をお持ちいただけましたら、
実物をご覧いただく機会を頂戴できましたら幸いです。

何卒よろしくお願い申し上げます。

--
GEGYjiji（水彩画家）
Instagram: https://www.instagram.com/gegyjiji/"""


# Stated as conventions rather than instructions (Scott, 2026-09-05). These are
# facts about how Tokyo galleries read a cold letter; written as commands they
# turned into advice she did not ask for.
RULES = [
    _t("One link — Instagram, or a single web album. Attachments from an unknown sender routinely go unopened.",
       "一个链接——Instagram，或者一个网页相册。陌生人发来的附件，通常不会被打开。"),
    _t("Five images from one series, rather than a selection across the practice. The judgement being made is whether the work holds a wall, not how many kinds of thing it can be.",
       "五张，来自同一个系列，而不是从整个创作里东挑一张西挑一张。对方要判断的是这批作品能不能撑起一面墙，而不是它能有多少种面貌。"),
    _t("The sentence naming which of their shows was attended is the one part of the letter that cannot be fabricated, and the part that gets read twice.",
       "写明去看过他们哪一场展的那句话，是整封信里唯一无法伪造的部分，也是会被读两遍的部分。"),
    _t("The first letter asks for a viewing, not a show. A request for a show is a proposal, and a proposal is something that can be declined.",
       "第一封信请求的是“看一下”，不是一次展览。请求展览就成了提案，而提案是可以被回绝的。"),
    _t("Silence at ten days indicates the letter was not seen rather than refused. A second letter three months later, at the next opening, comes from someone who has by then been twice.",
       "十天没有回音，通常意味着信没有被看到，而不是被拒绝。三个月后下一场展开幕时写第二封，寄信人已经是“来过两次的人”。"),
    _t("Sizes and prices are left out until they are asked for. Included unprompted, the letter becomes a quote sheet.",
       "尺寸和价格在对方问起之前不写。没被问就写上，信就变成了一份报价单。"),
]


def build() -> dict:
    return {
        "title": _t("The first letter", "第一封信"),
        "intro": _t(
            "Tokyo galleries do not run submission boxes; the route in is attendance and then a "
            "letter. A first letter that works is short — the show attended, three sentences of "
            "introduction, one link, five paintings. It contains no request, so there is nothing "
            "in it to refuse, and a reply of any kind is already the conversation.",
            "东京的画廊不设投稿箱；进入的方式是先到场，然后写信。"
            "有效的第一封信很短——去看过的那场展、三句话的自我介绍、一个链接、五张画。"
            "信里没有任何请求，所以没有什么可以被拒绝；而对方只要回一句话，就已经是在往下谈了。"),
        "letter_ja": LETTER_JA,
        "letter_note": _t(
            "Addressed to HAGI ART, whose own remit is young artists' solo and group shows and which charges no venue fee. The body holds for any of them with the first paragraph changed.",
            "这封写给 HAGI ART——它自己写明的方向就是年轻创作者的个展与联展，而且不收场地费。换掉第一段，其余的内容对任何一家都适用。"),
        "rules": RULES,
        "rules_label": _t("Six things that are true in Tokyo specifically",
                          "在东京，这六件事是真的"),
    }
