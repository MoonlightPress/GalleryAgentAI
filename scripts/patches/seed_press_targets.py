import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"

press_targets = [
    {
        "title": "美術手帖 (Bijutsu Techo) — Artist Feature",
        "name": "美術手帖 (Bijutsu Techo)",
        "organization": "美術出版社",
        "category": "press_target",
        "opportunity_type": "press_target",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://bijutsutecho.com/",
        "official_website": "https://bijutsutecho.com/",
        "deadline": "ongoing",
        "fees": "Free",
        "overall_score": 8.5,
        "differentiated_score": 9.0,
        "one_sentence": "Japan's leading fine art magazine. Artist features for emerging Tokyo-based painters. Discovers via Instagram + gallery shows.",
        "why_this_fits_short": "Flagship fine art publication for the Japanese art world. An editorial feature here is a career-defining visibility event.",
        "quick_action": "Prepare press kit (bio, statement, 10–15 high-res images). Tag #美術手帖 on strong work. Build Instagram archive.",
        "contact": "editorial@bijutsutecho.com or Instagram DM @bijutsutecho",
        "action_type": "pitch",
        "native_medium": "painting",
        "verification_status": "verified",
        "verification_bucket": "relationship_builders",
        "exclusive_primary_bucket": "press_target",
        "tags": ["press", "fine_art", "japan", "tokyo", "emerging_artist", "editorial"],
        "discovery_group": "PRESS",
        "added_by": "press_seed",
        "research_priority": "high",
        "relationship_note": "Discovery path: consistent Instagram posting + Tokyo gallery shows + tag #美術手帖. Editorial team actively scouts. Press kit should lead with the 'Chinese artist documenting Tokyo' angle — strong editorial hook.",
    },
    {
        "title": "Pen Magazine — Artist Spotlight",
        "name": "Pen Magazine",
        "organization": "CCCメディアハウス",
        "category": "press_target",
        "opportunity_type": "press_target",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://pen-online.jp/",
        "official_website": "https://pen-online.jp/",
        "deadline": "ongoing",
        "fees": "Free",
        "overall_score": 7.5,
        "differentiated_score": 8.0,
        "one_sentence": "Tokyo lifestyle/design magazine. Artist features for creatives with distinct visual identity. Urban architecture angle is on-brand.",
        "why_this_fits_short": "Tokyo's design-literate audience. Urban watercolor + Tokyo documentation = strong editorial angle for Pen readers.",
        "quick_action": "Frame pitch as 'artist documenting Tokyo's changing architecture' — not just 'I paint'. Contact via pen-online.jp or editorial DM.",
        "contact": "Via pen-online.jp contact or editorial DM",
        "action_type": "pitch",
        "native_medium": "painting",
        "verification_status": "verified",
        "verification_bucket": "relationship_builders",
        "exclusive_primary_bucket": "press_target",
        "tags": ["press", "lifestyle", "japan", "tokyo", "design", "editorial"],
        "discovery_group": "PRESS",
        "added_by": "press_seed",
        "research_priority": "medium",
        "relationship_note": "Discovers primarily via Instagram and design community word-of-mouth. Having a gallery show or book project helps. Lead with the architectural/urban documentation angle.",
    },
    {
        "title": "It's Nice That — Illustration Feature",
        "name": "It's Nice That",
        "organization": "It's Nice That",
        "category": "press_target",
        "opportunity_type": "press_target",
        "city": "London",
        "country": "UK",
        "source_url": "https://www.itsnicethat.com/",
        "official_website": "https://www.itsnicethat.com/",
        "deadline": "ongoing",
        "fees": "Free",
        "overall_score": 8.0,
        "differentiated_score": 8.5,
        "one_sentence": "International design/illustration publication with 2M+ readers. Actively scouts illustrators via Instagram. Daily practice format is exactly what they cover.",
        "why_this_fits_short": "Biggest international platform for illustrators at her level. A feature here reaches the global illustration community and attracts licensing and commission inquiries.",
        "quick_action": "Submit via itsnicethat.com/submit. Lead with the daily watercolor diary format — they love systematic creative disciplines.",
        "contact": "itsnicethat.com/submit",
        "action_type": "pitch",
        "native_medium": "painting",
        "verification_status": "verified",
        "verification_bucket": "relationship_builders",
        "exclusive_primary_bucket": "press_target",
        "tags": ["press", "illustration", "international", "uk", "editorial"],
        "discovery_group": "PRESS",
        "added_by": "press_seed",
        "research_priority": "high",
        "relationship_note": "Can happen quickly if work resonates. Low barrier — submit directly online. Frame around daily practice discipline, not just 'I'm a watercolor artist'.",
    },
    {
        "title": "Apartamento — Artist Feature",
        "name": "Apartamento Magazine",
        "organization": "Apartamento",
        "category": "press_target",
        "opportunity_type": "press_target",
        "city": "Barcelona",
        "country": "Spain",
        "source_url": "https://apartamentomagazine.com/",
        "official_website": "https://apartamentomagazine.com/",
        "deadline": "ongoing",
        "fees": "Free",
        "overall_score": 7.0,
        "differentiated_score": 7.5,
        "one_sentence": "International lifestyle/culture magazine with warm everyday-life aesthetic. Discovers via Instagram and community. Not submission-based — relationship path.",
        "why_this_fits_short": "Her intimate urban interiors and everyday Tokyo documentation is perfectly on-brand for Apartamento's audience. The 'foreigner observing Tokyo' angle is strong.",
        "quick_action": "Not pitch-based. Be visible at Tokyo Art Book Fair and book events. Connect with artists they already feature. Build presence in the right spaces.",
        "contact": "Via Instagram relationship and art book fair connections",
        "action_type": "relationship",
        "native_medium": "painting",
        "verification_status": "verified",
        "verification_bucket": "relationship_builders",
        "exclusive_primary_bucket": "press_target",
        "tags": ["press", "lifestyle", "international", "relationship_based", "editorial"],
        "discovery_group": "PRESS",
        "added_by": "press_seed",
        "research_priority": "medium",
        "relationship_note": "Long-term relationship play. Physical presence at art book fairs (Tokyo Art Book Fair, Offprint) is the path. They feature artists who are embedded in the creative community, not cold-pitch applicants.",
    },
    {
        "title": "Casa Brutus — Architecture/Art Feature",
        "name": "Casa Brutus",
        "organization": "マガジンハウス",
        "category": "press_target",
        "opportunity_type": "press_target",
        "city": "Tokyo",
        "country": "Japan",
        "source_url": "https://casabrutus.com/",
        "official_website": "https://casabrutus.com/",
        "deadline": "ongoing",
        "fees": "Free",
        "overall_score": 7.5,
        "differentiated_score": 8.0,
        "one_sentence": "Japanese architecture/design/lifestyle magazine. Artist features when work intersects with architecture or space. Her Tokyo building documentation is directly relevant.",
        "why_this_fits_short": "Urban watercolor documenting Tokyo architecture is an exact fit for Casa Brutus's editorial coverage of space and design.",
        "quick_action": "Email or DM @casabrutus. Position work as architectural documentation, not just art. Strong angle: 'watercolor record of Tokyo's disappearing buildings'.",
        "contact": "Via casabrutus.com contact or Instagram @casabrutus",
        "action_type": "pitch",
        "native_medium": "painting",
        "verification_status": "verified",
        "verification_bucket": "relationship_builders",
        "exclusive_primary_bucket": "press_target",
        "tags": ["press", "architecture", "japan", "tokyo", "editorial"],
        "discovery_group": "PRESS",
        "added_by": "press_seed",
        "research_priority": "medium",
        "relationship_note": "Architecture angle is the editorial hook — not 'I'm an artist' but 'I document Tokyo's changing buildings in watercolor'. Photographer and architect connections can introduce to editors.",
    },
    {
        "title": "ILOVETOYS / neuprint — Chinese Illustration Feature",
        "name": "Chinese Illustration Publications (ILOVETOYS, neuprint)",
        "organization": "ILOVETOYS / neuprint",
        "category": "press_target",
        "opportunity_type": "press_target",
        "city": "Shanghai",
        "country": "China",
        "source_url": "https://www.instagram.com/ilovetoys_magazine/",
        "official_website": "",
        "deadline": "ongoing",
        "fees": "Free",
        "overall_score": 8.0,
        "differentiated_score": 8.5,
        "one_sentence": "Chinese illustration magazines actively looking for overseas Chinese artists. She's Chinese, in Tokyo, with 90k followers — strong story for Chinese art audiences.",
        "why_this_fits_short": "She's Chinese. 'Chinese artist documenting Tokyo through watercolor' is exactly the cross-cultural story these publications want. Near-term opportunity with lower competition than Japanese press.",
        "quick_action": "Pitch via WeChat DM or Weibo. Chinese-language pitch. Lead with the Beijing/Chinese-artist-in-Tokyo angle.",
        "contact": "Via WeChat official accounts, Weibo DM, or Instagram DM @ilovetoys_magazine",
        "action_type": "pitch",
        "native_medium": "painting",
        "verification_status": "strong_partial",
        "verification_bucket": "relationship_builders",
        "exclusive_primary_bucket": "press_target",
        "tags": ["press", "illustration", "chinese", "diaspora", "editorial"],
        "discovery_group": "PRESS",
        "added_by": "press_seed",
        "research_priority": "high",
        "relationship_note": "Near-term realistic target. Chinese publications are actively expanding international coverage of overseas Chinese artists. Pitch in Chinese. Story: '90k followers watercolorist in Tokyo documenting the city for Chinese audiences'.",
    },
]


def main():
    data = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("items", [])

    existing_titles = {
        (o.get("title") or o.get("name") or "").strip().lower()
        for o in items
    }

    added = []
    skipped = []
    for pt in press_targets:
        key = pt["title"].strip().lower()
        if key in existing_titles:
            skipped.append(pt["title"])
        else:
            items.append(pt)
            existing_titles.add(key)
            added.append(pt["title"])

    # Save back — preserve list format
    out = items if isinstance(data, list) else {**data, "items": items}
    OPP_PATH.write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Added {len(added)} press targets:")
    for t in added:
        print(f"  + {t}")
    if skipped:
        print(f"Skipped {len(skipped)} (already exist):")
        for t in skipped:
            print(f"  = {t}")


if __name__ == "__main__":
    main()
