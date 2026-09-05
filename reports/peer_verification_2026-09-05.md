# Peer verification — the named artists in `futures_engine.py`

Date: 2026-09-05. Research only; no code was changed.

Scope: the four "someone living it" slots in `engines/futures_engine.py`, plus a
spot-check of the comparable-artist list shown on Saffron's page.

**Method note.** Every claim below is sourced to the artist's own site, their
gallery's own site, or the National Diet Library bibliographic record. Where a
summariser paraphrased rather than quoted, the page was refetched and the raw
text read — this mattered: an early automated summary of Urbanowicz's books page
asserted "self-published" for four titles, and the NDL records show the exact
opposite. Nothing in this report rests on a secondary source's assumption.

**Headline:** two of the three named artists are described in a way that is
factually wrong, and both errors are the kind she would catch. One is a
publishing fact; one is a career-scale fact. The licensing slot should stay
empty.

---

## 1. Mateusz Urbanowicz — **needs correction (two places)**

### What we currently claim

`futures_engine.py:73` (future `no_gatekeepers`):
> Mateusz Urbanowicz — Tokyo streets in watercolor, self-published books, a large direct audience, no gallery.

`futures_engine.py:181` (future `between_covers`):
> Urbanowicz again — his city books outsell most gallery careers.

The surrounding copy frames the whole future as: *"No gallery takes a cut, no
publisher decides your next book, no client sends notes."*

### What is actually true

**The books are not self-published.** Every major title is from a commercial
Japanese publisher. From the National Diet Library catalogue:

| Title | Publisher | Date | ISBN |
|---|---|---|---|
| 東京店構え / Tokyo Storefronts | エムディエヌコーポレーション (MdN Corporation), dist. インプレス | 2018.5 | 978-4-8443-6734-5 |
| 東京夜行 / Tokyo at Night | MdN Corporation / Impress | 2019.9 | 978-4-8443-6856-4 |
| お蔵出し 2010–2021 | MdN Corporation / Impress | 2022.9 | 978-4-295-20352-0 |
| 空想店構え (Imaginary Storefronts) | MdN Corporation / Impress | 2025.3 | 978-4-295-20549-4 |
| 見えるものを描かず、見えないものを描く | 玄光社 (Genkosha) | 2024.10 | 978-4-7683-1954-3 |

His own biography page lists MdN Corp under a heading "Clients / Cooperation →
Publishers 出版社", alongside Poplar, Kinnohoshi, Kodansha and X-Knowledge.

**He is not free of clients either.** Verbatim from his biography page: *"Since
2013 I have been working as a full-time background artist in the Comix Wave
Films animation studio in Tokyo. Taking part in making of TV commercials,
animated TV series (for example, 'Space Dandy'), and feature-length animated
movies (like 'Your Name.'). I moved to a freelance artist career to focus on my
original projects in 2017."* His own client list names Studio Colorido, Studio
Bones, Hakuhodo, Dentsu, NHK, Nippon Television, Japan Airlines, Otsuka
Pharmaceutical, Ezaki Glico, Kuretake, Celsys and Savage Interactive.

**"No gallery" is accurate.** No commercial gallery represents him. He sells
originals and prints himself through mateuszurbanowicz.bigcartel.com, and his
solo shows are in bookshops and brand spaces rather than galleries: TENOHA
Milano (2022), Ogaki Bookstore Azabudai Hills (2025 and again Feb–Mar 2026),
HIS Paris store (Nov 2025, with the Tokyo Convention & Visitors Bureau). Group
appearances include the Kadokawa Culture Museum, O Museum and the Sumida Hokusai
Museum — museum group shows, not gallery representation.

**"Outsell most gallery careers" is not verifiable.** The one real figure is
the Ogaki Bookstore exhibition announcement quoted on his own front page: *"this
collection of works by Mateusz Urbanowicz, whose series of books has sold over
100,000 copies in Japan alone…"* That is a bookstore/publisher promotional
figure, not audited, and it says nothing about gallery careers. The comparison
should go.

### Verdict

**Needs correction in both places.** He is a genuinely good example of an artist
with no gallery and a direct audience — the "no gatekeepers" half is real. The
"self-published" and "no client sends notes" half is false, and it is false
about a Tokyo-based watercolour painter of storefronts, i.e. the single person
in this list she is most likely to already follow.

### Corrected sentences — drop straight in

`no_gatekeepers` example (replaces line 73–74):

> **en:** Mateusz Urbanowicz — Tokyo storefronts in watercolor. No gallery
> represents him; he sells originals and prints himself, and the audience came
> before the books did.
>
> **zh:** Mateusz Urbanowicz——用水彩画东京的店铺门面。没有画廊代理他，原作和版画都由他自己卖；观众是先于书出现的。

`between_covers` example (replaces line 181–182):

> **en:** Urbanowicz again — four watercolor collections with the publisher MdN.
> The announcement for his 2026 Tokyo exhibition puts the series past 100,000
> copies sold in Japan.
>
> **zh:** 还是 Urbanowicz——四本水彩作品集，都由出版社 MdN 出版。2026 年东京展的公告写道，这个系列在日本已售出超过十万册。

One further note on the `no_gatekeepers` body copy at lines 47–54: *"no publisher
decides your next book, no client sends notes"* is a fair description of the
*kind of life*, but it now sits directly above an example who has both a
publisher and a client list. Either the example moves or that clause softens.

### Sources

- https://ndlsearch.ndl.go.jp/api/opensearch?creator=ウルバノヴィチ (National Diet Library, bibliographic records — publisher and ISBN for every title)
- https://mateuszurbanowicz.com/biography/ (biography, exhibition list, "Clients / Cooperation" list, verbatim)
- https://mateuszurbanowicz.com/animation-work/ ("Your Name – backgrounds 君の名は。背景美術")
- https://mateuszurbanowicz.com/ (Ogaki Bookstore announcement, 100,000-copies figure)
- https://mateuszurbanowicz.bigcartel.com (his own shop, originals and drawings)

---

## 2. Keita Morimoto (森本啓太) — **needs correction**

### What we currently claim

`futures_engine.py:111`:
> Keita Morimoto — nocturnal Tokyo streets, at a Tokyo gallery that sells for him.

### What is actually true

**The gallery is right.** KOTARO NUKAGA (Tokyo) lists 森本啓太 on its represented
artists roster, and held his solo *"what we told ourselves"* there
17 Jan – 7 Mar 2026. Earlier solos there: *"A Little Closer"* (2023),
*"After Dark"* (2021).

**But it is nowhere near the whole picture.** He is also represented by
Nicholas Metivier Gallery (Toronto) and by **Almine Rech**, whose roster carries
Jeff Koons, James Turrell and the Picasso estate; he had a solo *"To Nowhere and
Back"* at Almine Rech New York in 2025. Other solos: Night Gallery (Los Angeles,
2023), Kunsthal n (Copenhagen, 2025), and a solo — *"what has escaped us"* —
at the **21st Century Museum of Contemporary Art, Kanazawa** in 2025.

**He is in public collections**, per his gallery page: the National Gallery of
Canada, ICA Miami, the High Museum of Art (Atlanta), Peabody Essex Museum, the
Fondazione Sandretto Re Rebaudengo (Turin), Urban Nation (Berlin), Kyoto
Municipal Kyocera Museum of Art, Shiga Prefectural Museum of Art, Arts Maebashi.
KOTARO NUKAGA shows him at Art Basel Hong Kong, Frieze Seoul and Tokyo Gendai.
Editions of his work sell through AVANT ARTE.

**He is Tokyo-based — but not a lifelong Tokyo painter.** Born Osaka 1990, moved
to Canada in 2006, graduated OCAD University (Toronto) 2012, returned to Japan
in 2021. A decade of the night-scene work was painted in Toronto.

**"Nocturnal Tokyo streets" is loose.** His gallery describes the work as drawing
on Baroque painting and early-20th-century American Realism, turning ordinary
urban scenes into narrative through light. Night-time urban scenes: yes. "Tokyo
streets" specifically: not reliably.

### Verdict

**Needs correction.** "At a Tokyo gallery that sells for him" describes a painter
one step ahead of her. He is a museum-collected, art-fair-circuit painter on a
blue-chip international roster. To someone working in Tokyo, describing him as
"someone living it" at that scale reads as either uninformed or faintly absurd,
which is exactly the failure mode this section can't afford. The fix is not to
drop him — the path is real and he is on the end of it — but to say where on the
path he stands.

### Corrected sentence — drop straight in

Replaces line 111–112:

> **en:** Keita Morimoto — night-time urban scenes, painted in Tokyo. KOTARO
> NUKAGA represents him there, and galleries in Toronto and New York do the same
> abroad. This is the far end of the road, not the next step on it.
>
> **zh:** 森本启太——在东京画夜晚的城市景象。东京由 KOTARO NUKAGA 代理他，多伦多和纽约也各有画廊。这是这条路最远处的样子，不是下一步。

If a nearer-stage Tokyo example is wanted instead, that needs its own research
pass — I did not find one I could verify, and I'd rather say so than name
someone on a hunch.

### Sources

- https://kotaronukaga.com/artist/ (represented-artist roster, 森本啓太 listed)
- https://kotaronukaga.com/artist/keita-morimoto/ (biography, solo/group exhibition list, collections, 2026 solo, AVANT ARTE editions)
- https://www.alminerech.com/artists (Almine Rech roster, Keita Morimoto listed)

---

## 3. Tatsuro Kiuchi (木内達朗) — **needs correction (one phrase)**

### What we currently claim

`futures_engine.py:213`:
> Tatsuro Kiuchi — atmospheric spaces, covers and editorial, one of the most-commissioned illustrators in Japan.

### What is actually true

**Editorial and commercial illustration: confirmed, comprehensively.** From his
own About page: born in Tokyo, biology degree from International Christian
University, then graduated with distinction from ArtCenter College of Design in
Pasadena. He began with children's books for US and Japanese publishers and
*"eventually branch[ed] into editorial work for magazines, book jacket
illustrations, and advertising commissions."*

**Book covers: confirmed, and they are major ones.** His Japanese bio names
書籍装画 for 池井戸潤's *Hanzawa Naoki* (半沢直樹) and *Shitamachi Rocket*
(下町ロケット) series — among the most widely read novels in Japan. His site's own
navigation has a dedicated "Book Covers" section alongside Penguin Books, The
Folio Society and Criterion.

**Client list, from his own site's project index:** The New York Times, The New
Yorker, Penguin Books, The Folio Society, Criterion, NHK, JRA, Uniqlo, Google,
Suntory, Royal Mail, Starbucks, All Nippon Airways, Airbnb, Omega, Hyundai,
Ritz-Carlton, FIFA, AARP, *Turning Red*, *Forza Horizon 6*.

**Awards, from his own About page:** 講談社出版文化賞さしえ賞 (Kodansha Publishing
Culture Award, Illustration), Society of Illustrators gold and silver medals,
selections at the Bologna and Bratislava illustration exhibitions, Tokyo
Illustrators Society Bronze Award 2001. Member of the Tokyo Illustrators Society;
teaches at Aoyamajuku.

**"One of the most-commissioned illustrators in Japan": unverified.** No source
supports a ranking claim, and none plausibly could. It is the one sentence here
that cannot be stood behind.

**No agent.** His contact page routes work to him directly. He runs
PEN STILL WRITES, which its own front page describes as a portal site he
operates listing illustrators he has a connection with, with commissions going
directly to each illustrator — a collective and a shop window, not an agency
representing him.

### Verdict

**Accurate except for the superlative**, which should be replaced with the
concrete facts — which are more persuasive anyway. Worth noting for the
surrounding copy: the `on_assignment` money section says *"An agent takes 25–30%
and brings work you would not otherwise see."* The example named directly
beneath it has no agent. That is not a contradiction, but the step "An agent
comes after there's work to manage, not before" reads better if the example
demonstrates it.

### Corrected sentence — drop straight in

Replaces line 213–214:

> **en:** Tatsuro Kiuchi — atmospheric spaces, book jackets and editorial. Covers
> for Ikeido Jun's novels, illustration for the New York Times and Penguin,
> campaigns for Uniqlo and Royal Mail. No agent — the work comes to him directly.
>
> **zh:** 木内达朗——画有氛围的空间，做书籍装帧与杂志插画。池井户润小说的封面、《纽约时报》与企鹅出版社的插图、优衣库与英国皇家邮政的广告。他没有经纪人，工作直接找上门。

### Sources

- https://scrapbox.io/api/pages/tatsurokiuchi/About (About page, English and Japanese bios verbatim, awards list)
- https://tatsurokiuchi.com/ and https://tatsurokiuchi.com/contact/ (project index / client list, direct contact, no agent listed)
- https://penstillwrites.com/ (self-description: portal run by Kiuchi, commissions go direct to each illustrator)
- https://www.commarts.com/features/tatsuro-kiuchi (Communication Arts feature, "Tokyo-based illustrator")

---

## 4. The licensing example — **leave blank**

`futures_engine.py:144` currently reads *"(No example named yet — this one needs
research before a name goes here.)"* After this pass, that should stay.

### What I looked for

An illustrator or painter, working in architecture / cityscape / interiors,
whose living comes substantially from **licensing** — images placed on
stationery, homeware, packaging, brand collaborations — rather than from gallery
sales or per-job commissions.

### What I found, and why each one fails

**Michael Storrings** — the closest subject match anywhere: two decades painting
New York's streets and seasons in ink and watercolour, with his cityscapes
licensed onto Galison jigsaw puzzles, greeting cards, playing cards, bookmarks,
tote bags, and NYPL merchandise. **Disqualified:** Galison's own artist bio
describes him as Senior Vice President and Executive Creative Director at
Macmillan Publishers. The licensing sits beside a senior corporate salary, so it
cannot be presented as a life made from licensing. (Single-sourced — his own site
was unreachable behind a Wordfence block — but it is disqualifying either way,
and I would not name him on one source.)

**Ohn Mar Win** — already in our peer map. A real 20-year licensing and
surface-design practice: fruit and vegetable watercolours on branding and
packaging for Marks & Spencer, John Lewis, Next, Heal's, Unilever, Arla, Shell's
Deli2Go, UNICEF, BBC Worldwide. **Disqualified twice over.** First, subject:
food and botanicals, not architecture. Second, and more usefully, she publishes
her actual income breakdown, and for 2022/23 it was: teaching online 63.4%,
teaching in person 13.7%, illustration 9.6%, book 6%, image library 3.1%, **art
licensing 3%**, brand collaborations 0.8%. Licensing is roughly 7% of her income
including the passive image library. She is not a licensing example.

### Verdict

**Leave it blank.** Naming Storrings would be a false claim about how a living
person earns; naming anyone else would be a guess. The category is real — but the
people who live in it are structurally invisible, which is the whole point of it
and also why an example is hard to find. That is worth saying out loud rather
than papering over.

### Suggested copy for the empty slot — drop straight in

Replaces line 144–145:

> **en:** (No name here yet. This is the one path built to keep the artist out of
> sight — the image is on the shelf, the name isn't — and nothing checked out.
> Left blank rather than guessed at.)
>
> **zh:** （这里还没有名字。这条路本来就是让作者隐身的——图像在货架上，名字不在——目前没有找到能够确证的人。宁可留白，也不猜。）

### One related flag in the same section

`futures_engine.py:127–135` says a royalty is *"ongoing and unbounded — which is
why this category can quietly outpace every other one here."* That is asserted,
not evidenced, and the one artist in this report who publishes real numbers shows
licensing as a single-digit share of her income. It may well be true for a
licensing-led career; it is not currently supported. Consider softening to what
the mechanism guarantees ("a royalty keeps paying after the work is done")
rather than what it is claimed to beat.

### Sources

- https://www.galison.com/collections/michael-storrings-collection (Storrings bio, Macmillan role, product list)
- https://www.ohnmarwin.com/about (client list verbatim)
- https://www.ohnmarwin.com/ ("I like to illustrate artwork for brands, art licensing, and giftware")
- https://ohnmarwin.com/illustrationsouljourney/2024/6/18/how-i-made-money-as-an-artist-and-illustrator-202223-version (income breakdown by percentage)

---

## 5. A useful by-product: an evidenced example for future 1

The `no_gatekeepers` money copy claims a course is *"the one that turns an
audience into a living."* That claim is currently unevidenced in the app.
**Ohn Mar Win** evidences it precisely: 20+ Skillshare classes, 80,000+ students,
and a published breakdown putting teaching at **77.1%** of a self-described
six-figure annual income, against 9.6% from illustration commissions. She also
states it took her over eleven years to reach that point.

She is not a cityscape painter and shouldn't be presented as a stylistic peer.
But if that section ever wants a name attached to the course layer, she is the
best-documented one available, because she published the numbers herself.

---

## 6. Wider peer list — spot check

Files: `frontend/src/components/SaffronPage.jsx` (`PEER_IG` at line 682,
`PEER_LINK` at line 703), `memory/peer_artists.json`, generated by
`engines/peer_artist_engine.py` from `artist_intelligence_seed_data.json`.

### Clear problem 1 — most of `PEER_IG` is dead code

`artist_intelligence_seed_data.json` contains exactly **8** peer artists, and
`memory/peer_artists.json` mirrors them:

> Chien Chung-Wei (簡忠威), Keiko Tanabe, Thomas W. Schaller, Cathy Read,
> Lian Quan Zhen, Japan Watercolor Society (日本水彩画会) exhibitors,
> Alvaro Castagnet, Jean Haines

The block in `PEER_IG` commented `// 2026-06-26 expansion (verified handles)` maps
**eight names that do not exist in the data**: Samantha Dion Baker, Liz Steel,
Ohn Mar Win, Tatsuro Kiuchi, Felicia Chiao, Mateusz Urbanowicz, Aeppol,
Yuko Higuchi. The same is true of both `PEER_LINK` entries' companion — Zao Dao
(早稻) has no peer record either. None of these ever render. Either the peer
expansion was reverted from the seed data and the map was left behind, or the
seed data was never updated. Worth deciding which, since several of those names
(Felicia Chiao's interiors, Liz Steel's architectural sketching, Samantha Dion
Baker's urban diary) are much closer fits to architecture-and-space than half the
list that does render.

### Clear problem 2 — one live peer produces a junk link

`"Japan Watercolor Society (日本水彩画会) exhibitors"` is in the rendered data but
has no `PEER_IG` or `PEER_LINK` entry, so line 726 falls through to
`sfSearch('Japan Watercolor Society (日本水彩画会) exhibitors instagram')`. It is an
exhibition ecosystem, not a person, and has no Instagram to find. It should get
an explicit link to the society (or be excluded from the card grid).

### Clear problem 3 — Cathy Read's description is wrong in a checkable detail

`peer_artists.json` says *"British architectural watercolorist known for
Edinburgh and UK urban scenes."* Her site describes "Vibrant Metropolitan
Perspectives" and contemporary architecture work, from a studio at Arts Central,
Milton Keynes; she appeared on Sky Arts *Landscape Artist of the Year* in 2016.
Edinburgh is not supported anywhere I could find. Her medium is also mixed —
watercolour with acrylic ink — not watercolour alone.

Suggested replacement `fit_reason`: *"British architectural artist — contemporary
buildings and metropolitan scenes in watercolour and acrylic ink. Sells direct
from her own studio and shop."*

### Checked and fine

- **Jean Haines** — alive, site live, actively teaching and selling; her own
  galleries are animals, flowers, landscapes and portraits, with no architecture
  at all. The record already says "community reference only. Do NOT use as
  stylistic reference," and the card shows that text, so it's honest as it
  stands. Flagging only that she is the weakest fit on a short list.
- **Lian Quan Zhen** — `PEER_LINK` target lianspainting.com resolves and is his
  real site; latest content is a 2021 China painting trip, so the site is dated
  but not dead.
- **Zao Dao's** X account (x.com/tataka510) resolves, though her peer record
  doesn't exist so the link is unreachable in the UI (see problem 1).
- **Tatsuro Kiuchi's** handle `tatsurokiuchi` and **Ohn Mar Win's**
  `ohn_mar_win` are both confirmed correct — each artist links that exact handle
  from their own site.
- No deceased artists among the eight that render.

### Could not verify

Instagram is fully login-walled to unauthenticated requests: every handle,
including a deliberately invented control handle, returns HTTP 200 with identical
markup. The remaining handles in `PEER_IG` could not be independently confirmed
this pass. Confirming them needs either a logged-in browser session or each
artist's own site linking the handle, as was done above for Kiuchi and Ohn Mar Win.

---

## Summary table

| Person | Slot | Verdict |
|---|---|---|
| Mateusz Urbanowicz | `no_gatekeepers` | Correct — "self-published" is false; the books are MdN Corporation. He also has a long client list. |
| Mateusz Urbanowicz | `between_covers` | Correct — "outsell most gallery careers" is unverifiable; use the 100,000-copies figure and name the publisher. |
| Keita Morimoto | `someone_else_sells` | Correct — the gallery is right but the scale is badly understated; he is museum-collected and on Almine Rech's roster. |
| Tatsuro Kiuchi | `on_assignment` | Correct one phrase — "one of the most-commissioned in Japan" is unverifiable; the concrete facts are stronger. |
| — | `work_goes_out` | Leave blank. No defensible licensing example found. |
