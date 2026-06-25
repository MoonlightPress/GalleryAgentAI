# Comparable Artists — Expansion Pass

**For:** GEGYjiji (@gegyjiji) — Saffron / "You're in Good Company"
**Date:** 2026-06-26
**Researcher pass:** append-only. The existing 8 peers stay. This document proposes **9 additional, verified artists** weighted toward her *actual* practice — the daily watercolor diary (since 2020), domestic interiors, cats, interior light, Tokyo quiet life, and the illustration / artist-book ecosystem she's rooted in.

---

## Why these, and how they're weighted

The current list does its job for the **architectural / loose-watercolor masters** half of her (Schaller, Castagnet, Chien Chung-Wei, Jean Haines) and the **cross-cultural watercolor-career** half (Keiko Tanabe, Lian Quan Zhen). What it under-serves is the half of her that is most *her*: an **illustration-community daily-diary practice** that turns ordinary domestic life into watercolor, posted online, and gathered into books.

So the new entries are deliberately weighted that way. The highest `fit_score`s go to true daily-diary, domestic-life watercolorists (Samantha Dion Baker, Liz Steel, Ohn Mar Win). The architectural masters in the live list should **not** outrank these — these are closer to what she actually does every day. Lower (but still well above the architectural masters) are the **career-path / thematic** comps: artists whose *medium* or *subject* differs but whose *path* — online audience → art books → exhibitions, often as an Asian illustrator — is the road she's on. Each of those carries an honest note saying so.

Tone note for the section copy: these are companions on the same road, not a ladder she's behind on. Every fit reason describes a genuine overlap; where the overlap is career/community rather than style, it says so plainly.

---

## The proposed additions

Each block gives: the verified link, an honest fit note, the exact `peer_artists.json` object, and the Simplified-Chinese for every localized string.

---

### 1. Samantha Dion Baker — daily watercolor sketch journal → books *(closest comp)*

- **Verified:** Instagram **@sdionbakerdesign** (~113k) · https://www.instagram.com/sdionbakerdesign/ · site https://www.sdionbaker.com/
- **Honest fit:** As close as the list gets. A Brooklyn illustrator who has drawn her day — home, neighborhood, meals, small domestic moments — every day in watercolor and pen, and grew that exact daily-diary habit into a series of published books (*Draw Your Day*). This is GEGYjiji's practice and her stated publishing direction, in one person. Genuine stylistic *and* path overlap.

```json
{
  "name": "Samantha Dion Baker",
  "region": "USA",
  "medium": "watercolor and ink",
  "fit_reason": "Keeps a daily illustrated sketch journal of ordinary life — her home, her neighborhood, meals, small domestic moments — painted in watercolor and pen, the same daily-diary practice GEGYjiji has kept since 2020. Her journal grew directly into a series of published books (Draw Your Day), the publication path GEGYjiji is building toward.",
  "shared_traits": [
    "daily illustrated diary practice",
    "domestic and everyday-life subjects",
    "watercolor and ink on paper",
    "diary that grew into published books",
    "audience built on Instagram"
  ],
  "use_as": "Closest model for turning a daily watercolor diary into published books and a sustaining illustration career.",
  "fit_score": 0.83,
  "overlap_terms": []
}
```

---

### 2. Liz Steel — daily watercolor sketchbook, her cat, teacups, rooms

- **Verified:** Instagram **@lizsteelart** (~93k) · https://www.instagram.com/lizsteelart/ · site https://www.lizsteel.com/
- **Honest fit:** A Sydney artist whose whole practice is a daily watercolor sketchbook of her own life — her cat, her teacups, the rooms she sits in, buildings she passes — and who built a following and a teaching business around the habit itself. The everyday-domestic register and the recurring cat are a direct echo of GEGYjiji's diary. Real stylistic overlap; the architecture she also paints is incidental, not the core.

```json
{
  "name": "Liz Steel",
  "region": "Australia",
  "medium": "watercolor",
  "fit_reason": "A daily watercolor sketchbook artist from Sydney who paints her own life — her cat, teacups, the rooms she sits in, the buildings she passes — and has built a large following and a teaching practice around that habit. The everyday-domestic register and the cat as a recurring anchor closely echo GEGYjiji's diary.",
  "shared_traits": [
    "daily watercolor sketchbook habit",
    "cats and domestic life as subjects",
    "intimate everyday observation",
    "self-built audience and teaching career"
  ],
  "use_as": "Reference for sustaining a daily watercolor practice and turning the habit itself into a community and income.",
  "fit_score": 0.79,
  "overlap_terms": []
}
```

---

### 3. Ohn Mar Win — Burmese-British watercolor sketchbooks, domestic still life

- **Verified:** Instagram **@ohn_mar_win** (~207k) · https://www.instagram.com/ohn_mar_win/ · site https://ohnmarwin.com
- **Honest fit:** A Burmese-British watercolorist who fills sketchbooks with domestic still life — coffee, food, the quiet objects of home — shares them daily on Instagram, and has a self-published book and a large following. An Asian-heritage illustrator whose career rests on watercolor sketchbooks plus an online audience, much like GEGYjiji's. Real subject and medium overlap; her palette runs warmer/brighter than GEGYjiji's muted greys.

```json
{
  "name": "Ohn Mar Win",
  "region": "UK (Burmese-British)",
  "medium": "watercolor",
  "fit_reason": "A Burmese-British watercolorist who fills sketchbooks with domestic still life — coffee, food, the quiet objects of home — and shares them daily on Instagram, where she has built a large following and a self-published book. An Asian-heritage artist whose career rests on watercolor sketchbooks and an online audience, much like GEGYjiji's.",
  "shared_traits": [
    "watercolor sketchbook practice",
    "domestic still life and home objects",
    "Asian-heritage illustrator",
    "audience and books built online"
  ],
  "use_as": "Reference for building an illustration career on watercolor sketchbooks, an online following, and self-published books.",
  "fit_score": 0.72,
  "overlap_terms": []
}
```

---

### 4. Tatsuro Kiuchi (木内達朗) — Tokyo, quiet domestic stillness *(medium differs)*

- **Verified:** Instagram **@tatsurokiuchi** (~63k) · https://www.instagram.com/tatsurokiuchi/ · site https://tatsurokiuchi.com/main
- **Honest fit:** A Tokyo illustrator whose quiet scenes — cafés, apartments, interior light, a figure alone in domestic space — share GEGYjiji's stillness and attention to ordinary moments almost exactly. The catch: he paints *digitally*, not in watercolor. So this is a thematic/tonal kinship, not a material one — but very few artists match her register of calm domestic observation this closely, which is why he earns a high score despite the medium gap.

```json
{
  "name": "Tatsuro Kiuchi (木内達朗)",
  "region": "Japan",
  "medium": "digital painting (illustration)",
  "fit_reason": "A Tokyo illustrator whose quiet scenes — cafes, apartments, interior light, figures alone in domestic space — share GEGYjiji's stillness and attention to ordinary moments. He works digitally rather than in watercolor, so this is a thematic and tonal kinship more than a material one, but few artists match her register of calm domestic observation so closely.",
  "shared_traits": [
    "quiet domestic and interior scenes",
    "stillness and everyday calm",
    "Tokyo-based illustrator",
    "atmosphere over incident"
  ],
  "use_as": "Stylistic and tonal reference for quiet, domestic, interior-light storytelling; note the medium is digital, not watercolor.",
  "fit_score": 0.70,
  "overlap_terms": []
}
```

---

### 5. Felicia Chiao — introspective domestic sketchbook diary, online-built *(medium differs)*

- **Verified:** Instagram **@feliciachiao** (~685k) · https://www.instagram.com/feliciachiao/ · gallery https://www.harmanprojects.com/artists/454-felicia-chiao/
- **Honest fit:** A Taiwanese-American illustrator who keeps a deeply personal sketchbook diary of interior, introspective domestic scenes, and built an audience of hundreds of thousands from that practice alone — moving from a day job into a full illustration-and-gallery career. Her medium is marker/ink on toned paper, not watercolor, so the kinship is the diary practice, the domestic-interior subject, and the online-built path — not the surface look.

```json
{
  "name": "Felicia Chiao",
  "region": "USA (Taiwanese-American)",
  "medium": "marker and ink (sketchbook illustration)",
  "fit_reason": "A Taiwanese-American illustrator who keeps a deeply personal sketchbook diary of interior, introspective domestic scenes and built an audience of hundreds of thousands from that practice alone — moving from a day job into a full illustration and gallery career. Her medium is marker rather than watercolor, so the kinship is the diary practice, the domestic-interior subject, and the online-built path, not the surface look.",
  "shared_traits": [
    "personal sketchbook diary practice",
    "domestic interior and introspective subjects",
    "Asian-heritage illustrator",
    "career built from an online audience"
  ],
  "use_as": "Reference for how a private daily sketchbook diary can grow into a full illustration and exhibition career; note medium is marker, not watercolor.",
  "fit_score": 0.66,
  "overlap_terms": []
}
```

---

### 6. Mateusz Urbanowicz — watercolor of ordinary Tokyo, online → art books *(career path)*

- **Verified:** Instagram **@mateusz_urbanowicz** (~163k) · https://www.instagram.com/mateusz_urbanowicz/ · site https://mateuszurbanowicz.com/
- **Honest fit:** A Tokyo-based painter whose watercolor series of ordinary Tokyo storefronts and streets grew from Instagram into published art books and a self-sustaining independent career — almost exactly GEGYjiji's trajectory. He's Polish, not Asian, so the overlap is the *practice and path*: watercolor, quiet everyday Tokyo, online audience converted into art books. A near-perfect career-path model even though he isn't a daily-diary artist.

```json
{
  "name": "Mateusz Urbanowicz",
  "region": "Japan (Polish, Tokyo-based)",
  "medium": "watercolor",
  "fit_reason": "A Tokyo-based painter whose watercolor series of ordinary Tokyo storefronts and streets grew from Instagram into published art books and a sustaining independent career — almost exactly the trajectory GEGYjiji is on. He is Polish rather than Asian, so the overlap is the practice and path: watercolor, quiet Tokyo, online audience to art books.",
  "shared_traits": [
    "watercolor of ordinary Tokyo",
    "quiet urban atmosphere",
    "online audience grown into art books",
    "independent Tokyo-based career"
  ],
  "use_as": "Direct career-path model: watercolor of everyday Tokyo, built from Instagram into published art books and self-sustaining practice.",
  "fit_score": 0.64,
  "overlap_terms": []
}
```

---

### 7. Aeppol (애뽈) — Korean daily "diary" from blog → bestselling books *(career path)*

- **Verified:** Instagram **@_aeppol** · https://www.instagram.com/_aeppol · Facebook https://www.facebook.com/illust.aeppol/ · publisher page https://www.simonandschuster.com/books/The-Forest-Girls-Coloring-Book/Aeppol/9781646047321
- **Honest fit:** A Korean illustrator who built the long-running *Forest Girl's Diary* from a personal blog — a soft, watercolor-style daily diary of a girl's quiet life, updated several times a week — and turned it into bestselling published books. The subject is a fairy-tale forest, not a Tokyo apartment, so the kinship is the **daily-diary engine** and the **online-to-books** path, not the setting. A clean model for sustaining a *named* diary project over years.

```json
{
  "name": "Aeppol (애뽈)",
  "region": "South Korea",
  "medium": "watercolor-style illustration",
  "fit_reason": "A Korean illustrator who built the long-running 'Forest Girl's Diary' from a personal blog — a soft, watercolor-style daily diary of a girl's quiet life, updated several times a week — and turned it into bestselling published books. The subject is a fairy-tale forest rather than a Tokyo apartment, so the kinship is the daily-diary engine and the online-to-books path, not the setting.",
  "shared_traits": [
    "daily diary as ongoing project",
    "quiet everyday-life subjects",
    "Asian illustrator built from online audience",
    "diary grown into published books"
  ],
  "use_as": "Reference for sustaining a named daily-diary project over years and turning it into a publishing career; the diary format, not the fairy-tale content, is the parallel.",
  "fit_score": 0.62,
  "overlap_terms": []
}
```

---

### 8. Yuko Higuchi (ヒグチユウコ) — cats, watercolor, deep art-book career *(cats + book path)*

- **Verified:** Instagram **@yukohiguchi3** (~338k) · https://www.instagram.com/yukohiguchi3/ · Linktree https://linktr.ee/higuchiyuko
- **Honest fit:** A Tokyo painter whose work centers on cats in watercolor and ink, with a prolific publishing practice — art books, picture books, her own gallery-shop (Boris) — and a cult following. Her world is surreal and fantastical, not quiet-domestic, so the kinship is the **cat-centered subject** and the **art-book/publishing career**, not the realist register. Useful as a "how far the cats-and-books road can go" reference.

```json
{
  "name": "Yuko Higuchi (ヒグチユウコ)",
  "region": "Japan",
  "medium": "watercolor and ink",
  "fit_reason": "A Tokyo painter whose work centers on cats, rendered in watercolor and ink, and who has built a prolific publishing practice — art books, picture books, a gallery-shop of her own — alongside a large following. Her world is surreal and fantastical rather than quiet-domestic, so the kinship is the cat-centered subject and the art-book/publishing career, not the realist register.",
  "shared_traits": [
    "cats as central subject",
    "watercolor and ink medium",
    "prolific art-book and picture-book publishing",
    "Tokyo-based with own gallery-shop"
  ],
  "use_as": "Reference for a cats-centered Tokyo painter building a deep art-book and publishing career; note the style is surreal/fantasy, not realist domestic.",
  "fit_score": 0.58,
  "overlap_terms": []
}
```

---

### 9. Zao Dao (早稻) — Chinese illustrator, Weibo blog → international art books *(career path)*

- **Verified:** X/Twitter **@tataka510** · https://x.com/tataka510 · Facebook https://www.facebook.com/zaodaoComic/ · art books via KEKO Creative / TOA Graphic Books (e.g. https://toagraphicbooks.com/product/song-of-sylvan-zao-dao-artbook/)
- **Honest fit:** A self-taught Chinese illustrator from Guangdong who built her audience on a Weibo blog from 2010 and turned it into internationally published art books (*Song of Sylvan*, *Ink of Wild*) and gallery shows abroad — a Chinese artist who reached an international career through ink-and-watercolor work and an online following. Her imagery is folkloric and fantastical, so the kinship is the **Chinese-artist-online-to-art-books** path, not the subject. (Note: her cleanest public links are X and Facebook, not Instagram.)

```json
{
  "name": "Zao Dao (早稻)",
  "region": "China",
  "medium": "ink and watercolor",
  "fit_reason": "A self-taught Chinese illustrator from Guangdong who built her audience on a Weibo blog from 2010 and turned it into internationally published art books (Song of Sylvan, Ink of Wild) and gallery shows abroad — a Chinese artist who reached an international career through ink-and-watercolor work and an online following. Her imagery is folkloric and fantastical, so the kinship is the Chinese-artist-online-to-art-books path, not the subject.",
  "shared_traits": [
    "Chinese illustrator",
    "ink and watercolor medium",
    "audience built online then published",
    "international art-book and gallery career"
  ],
  "use_as": "Reference for a Chinese illustrator building from an online following to internationally published art books and overseas exhibitions; the path, not the fantasy subject, is the parallel.",
  "fit_score": 0.52,
  "overlap_terms": []
}
```

---

## Considered and dropped (anti-fabrication log)

These came up in research and were **deliberately not included**, to keep the honesty bar:

- **Sili Chen** — could not confirm a stable artist identity/link in search; omitted rather than guess.
- **Ya Mai Xiao Ju** — Chinese watercolor-cat illustrator surfaced only via a listicle; no clean, verifiable primary link found. Omitted.
- **Hiroki Takeda / Yutaka Murakami** — real Japanese watercolor-cat painters, but decorative-floral / older-generation respectively; weaker daily-diary/domestic fit, so left out to avoid padding.
- **Anna-Laura Sullivan** — real, verifiable (@annalaurasullivan, Brooklyn watercolor comics), but the register is cute-critter comics, a meaningfully different style; held back so the list stays honestly close.
- **Subikiawa** — real Japanese daily-life illustrator (@subikiawa), but the path is tableware/stationery goods, not artist-books/zines; off the requested categories.

---

## Career-stage spread (so it's not all famous masters)

Rough follower scale at time of research, smallest first: Tatsuro Kiuchi ~63k · Liz Steel ~93k · Samantha Dion Baker ~113k · Mateusz Urbanowicz ~163k · Ohn Mar Win ~207k · Yuko Higuchi ~338k · Felicia Chiao ~685k (Aeppol and Zao Dao are large but harder to pin to one number). GEGYjiji sits at ~26k, so Kiuchi / Liz Steel / Samantha Dion Baker are the nearest in reach, and the larger names show how far the same daily-diary / online-to-books road can run. None are positioned as a deficit — they're further along the same path she's already on.

---

## Append-ready: full JSON array of the 9 new peers

```json
[
  {
    "name": "Samantha Dion Baker",
    "region": "USA",
    "medium": "watercolor and ink",
    "fit_reason": "Keeps a daily illustrated sketch journal of ordinary life — her home, her neighborhood, meals, small domestic moments — painted in watercolor and pen, the same daily-diary practice GEGYjiji has kept since 2020. Her journal grew directly into a series of published books (Draw Your Day), the publication path GEGYjiji is building toward.",
    "shared_traits": [
      "daily illustrated diary practice",
      "domestic and everyday-life subjects",
      "watercolor and ink on paper",
      "diary that grew into published books",
      "audience built on Instagram"
    ],
    "use_as": "Closest model for turning a daily watercolor diary into published books and a sustaining illustration career.",
    "fit_score": 0.83,
    "overlap_terms": []
  },
  {
    "name": "Liz Steel",
    "region": "Australia",
    "medium": "watercolor",
    "fit_reason": "A daily watercolor sketchbook artist from Sydney who paints her own life — her cat, teacups, the rooms she sits in, the buildings she passes — and has built a large following and a teaching practice around that habit. The everyday-domestic register and the cat as a recurring anchor closely echo GEGYjiji's diary.",
    "shared_traits": [
      "daily watercolor sketchbook habit",
      "cats and domestic life as subjects",
      "intimate everyday observation",
      "self-built audience and teaching career"
    ],
    "use_as": "Reference for sustaining a daily watercolor practice and turning the habit itself into a community and income.",
    "fit_score": 0.79,
    "overlap_terms": []
  },
  {
    "name": "Ohn Mar Win",
    "region": "UK (Burmese-British)",
    "medium": "watercolor",
    "fit_reason": "A Burmese-British watercolorist who fills sketchbooks with domestic still life — coffee, food, the quiet objects of home — and shares them daily on Instagram, where she has built a large following and a self-published book. An Asian-heritage artist whose career rests on watercolor sketchbooks and an online audience, much like GEGYjiji's.",
    "shared_traits": [
      "watercolor sketchbook practice",
      "domestic still life and home objects",
      "Asian-heritage illustrator",
      "audience and books built online"
    ],
    "use_as": "Reference for building an illustration career on watercolor sketchbooks, an online following, and self-published books.",
    "fit_score": 0.72,
    "overlap_terms": []
  },
  {
    "name": "Tatsuro Kiuchi (木内達朗)",
    "region": "Japan",
    "medium": "digital painting (illustration)",
    "fit_reason": "A Tokyo illustrator whose quiet scenes — cafes, apartments, interior light, figures alone in domestic space — share GEGYjiji's stillness and attention to ordinary moments. He works digitally rather than in watercolor, so this is a thematic and tonal kinship more than a material one, but few artists match her register of calm domestic observation so closely.",
    "shared_traits": [
      "quiet domestic and interior scenes",
      "stillness and everyday calm",
      "Tokyo-based illustrator",
      "atmosphere over incident"
    ],
    "use_as": "Stylistic and tonal reference for quiet, domestic, interior-light storytelling; note the medium is digital, not watercolor.",
    "fit_score": 0.70,
    "overlap_terms": []
  },
  {
    "name": "Felicia Chiao",
    "region": "USA (Taiwanese-American)",
    "medium": "marker and ink (sketchbook illustration)",
    "fit_reason": "A Taiwanese-American illustrator who keeps a deeply personal sketchbook diary of interior, introspective domestic scenes and built an audience of hundreds of thousands from that practice alone — moving from a day job into a full illustration and gallery career. Her medium is marker rather than watercolor, so the kinship is the diary practice, the domestic-interior subject, and the online-built path, not the surface look.",
    "shared_traits": [
      "personal sketchbook diary practice",
      "domestic interior and introspective subjects",
      "Asian-heritage illustrator",
      "career built from an online audience"
    ],
    "use_as": "Reference for how a private daily sketchbook diary can grow into a full illustration and exhibition career; note medium is marker, not watercolor.",
    "fit_score": 0.66,
    "overlap_terms": []
  },
  {
    "name": "Mateusz Urbanowicz",
    "region": "Japan (Polish, Tokyo-based)",
    "medium": "watercolor",
    "fit_reason": "A Tokyo-based painter whose watercolor series of ordinary Tokyo storefronts and streets grew from Instagram into published art books and a sustaining independent career — almost exactly the trajectory GEGYjiji is on. He is Polish rather than Asian, so the overlap is the practice and path: watercolor, quiet Tokyo, online audience to art books.",
    "shared_traits": [
      "watercolor of ordinary Tokyo",
      "quiet urban atmosphere",
      "online audience grown into art books",
      "independent Tokyo-based career"
    ],
    "use_as": "Direct career-path model: watercolor of everyday Tokyo, built from Instagram into published art books and self-sustaining practice.",
    "fit_score": 0.64,
    "overlap_terms": []
  },
  {
    "name": "Aeppol (애뽈)",
    "region": "South Korea",
    "medium": "watercolor-style illustration",
    "fit_reason": "A Korean illustrator who built the long-running 'Forest Girl's Diary' from a personal blog — a soft, watercolor-style daily diary of a girl's quiet life, updated several times a week — and turned it into bestselling published books. The subject is a fairy-tale forest rather than a Tokyo apartment, so the kinship is the daily-diary engine and the online-to-books path, not the setting.",
    "shared_traits": [
      "daily diary as ongoing project",
      "quiet everyday-life subjects",
      "Asian illustrator built from online audience",
      "diary grown into published books"
    ],
    "use_as": "Reference for sustaining a named daily-diary project over years and turning it into a publishing career; the diary format, not the fairy-tale content, is the parallel.",
    "fit_score": 0.62,
    "overlap_terms": []
  },
  {
    "name": "Yuko Higuchi (ヒグチユウコ)",
    "region": "Japan",
    "medium": "watercolor and ink",
    "fit_reason": "A Tokyo painter whose work centers on cats, rendered in watercolor and ink, and who has built a prolific publishing practice — art books, picture books, a gallery-shop of her own — alongside a large following. Her world is surreal and fantastical rather than quiet-domestic, so the kinship is the cat-centered subject and the art-book/publishing career, not the realist register.",
    "shared_traits": [
      "cats as central subject",
      "watercolor and ink medium",
      "prolific art-book and picture-book publishing",
      "Tokyo-based with own gallery-shop"
    ],
    "use_as": "Reference for a cats-centered Tokyo painter building a deep art-book and publishing career; note the style is surreal/fantasy, not realist domestic.",
    "fit_score": 0.58,
    "overlap_terms": []
  },
  {
    "name": "Zao Dao (早稻)",
    "region": "China",
    "medium": "ink and watercolor",
    "fit_reason": "A self-taught Chinese illustrator from Guangdong who built her audience on a Weibo blog from 2010 and turned it into internationally published art books (Song of Sylvan, Ink of Wild) and gallery shows abroad — a Chinese artist who reached an international career through ink-and-watercolor work and an online following. Her imagery is folkloric and fantastical, so the kinship is the Chinese-artist-online-to-art-books path, not the subject.",
    "shared_traits": [
      "Chinese illustrator",
      "ink and watercolor medium",
      "audience built online then published",
      "international art-book and gallery career"
    ],
    "use_as": "Reference for a Chinese illustrator building from an online following to internationally published art books and overseas exhibitions; the path, not the fantasy subject, is the parallel.",
    "fit_score": 0.52,
    "overlap_terms": []
  }
]
```

---

## Append-ready: zh translation map (exact-match)

Every English `fit_reason`, `use_as`, `region`, and `shared_traits` string above, mapped to Simplified Chinese. Keys are the exact English strings, so this can merge straight into the localization map.

```json
{
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
  "international art-book and gallery career": "国际画集与画廊事业"
}
```
