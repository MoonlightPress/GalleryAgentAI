import json
import os
import hashlib


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def make_id(name, url):
    return hashlib.md5(f"{name}|{url}".encode("utf-8")).hexdigest()[:12]


def opp(name, org, category, city, url, notes="", friction="low"):
    return {
        "id": make_id(name, url),
        "name": name,
        "organization": org,
        "type": category,
        "category": category,
        "city": city,
        "country": "Japan",
        "official_website": url,
        "submission_page": url,
        "source_url": url,
        "source_link": url,
        "source_status": "verified_link_present",
        "deadline": "Check current schedule",
        "fees": "Check source",
        "status": "needs_review",
        "visibility": "secondary",
        "priority": "C",
        "friction_level": friction,
        "notes": notes
    }


opportunities = [
    opp("MOUNT ZINE", "MOUNT ZINE", "zine_print", "Tokyo", "https://zine.mount.co.jp/", "Zine shop / zine events / artist publishing ecosystem."),
    opp("Book and Sons", "Book and Sons", "bookstore_gallery", "Tokyo", "https://bookandsons.com/", "Art/design bookstore with exhibitions and publishing-adjacent audience."),
    opp("UTRECHT", "UTRECHT", "bookstore_gallery", "Tokyo", "https://utrecht.jp/", "Independent art book / zine ecosystem."),
    opp("NADiff a/p/a/r/t", "NADiff", "bookstore_gallery", "Tokyo", "https://www.nadiff.com/", "Art bookstore/gallery; useful for art book ecosystem mapping."),
    opp("flotsam books", "flotsam books", "bookstore_gallery", "Tokyo", "https://www.flotsambooks.com/", "Photography/art bookshop with artist-facing audience."),
    opp("POST", "POST", "bookstore_gallery", "Tokyo", "https://post-books.info/", "Art bookshop/gallery; publishing-oriented audience."),
    opp("TOKYO ART BOOK FAIR", "TOKYO ART BOOK FAIR", "fair_popup", "Tokyo", "https://tokyoartbookfair.com/", "Major art book fair; zine/book/publishing opportunity.", "medium"),
    opp("Design Festa", "Design Festa", "fair_popup", "Tokyo", "https://designfesta.com/", "Large creator booth event; direct sales / visibility.", "medium"),
    opp("Comitia", "COMITIA", "fair_popup", "Tokyo", "https://www.comitia.co.jp/", "Original self-published comics/illustration event.", "medium"),
    opp("HandMade In Japan Fes", "Creema", "fair_popup", "Tokyo", "https://hmj-fes.jp/", "Handmade/art goods booth event.", "medium"),
    opp("Aoyama Farmers Market", "Farmer's Market @ UNU", "fair_popup", "Tokyo", "https://farmersmarkets.jp/", "Recurring weekend market; possible artist goods testing."),
    opp("RAW TOKYO", "RAW TOKYO", "fair_popup", "Tokyo", "https://rawtokyo.jp/", "Market/pop-up ecosystem; check vendor fit."),
    opp("3331 Arts Chiyoda", "3331 Arts Chiyoda", "artist_space", "Tokyo", "https://www.3331.jp/", "Artist-run / exhibition ecosystem reference."),
    opp("Tokyo Arts and Space", "Tokyo Arts and Space", "institutional", "Tokyo", "https://www.tokyoartsandspace.jp/en/", "Institutional open calls and residencies.", "high"),
    opp("Youkobo Art Space", "Youkobo Art Space", "residency", "Tokyo", "https://www.youkobo.co.jp/en/", "Artist residency / local art ecosystem.", "medium"),
    opp("AIT Residency", "Arts Initiative Tokyo", "residency", "Tokyo", "https://www.a-i-t.net/en/", "Contemporary art residency/programming ecosystem.", "high"),
    opp("SCAI The Bathhouse", "SCAI The Bathhouse", "gallery", "Tokyo", "https://www.scaithebathhouse.com/", "Higher-end gallery reference; likely not low-friction.", "high"),
    opp("TAV Gallery", "TAV Gallery", "gallery", "Tokyo", "https://tavgallery.com/", "Contemporary gallery; check artist fit.", "medium"),
    opp("The Container", "The Container", "gallery", "Tokyo", "https://www.the-container.com/", "Small contemporary exhibition space.", "medium"),
    opp("Gallery Conceal Shibuya", "Gallery Conceal Shibuya", "gallery", "Tokyo", "https://galleryconceal.wixsite.com/gconceal", "Rental/exhibition space; verify model.", "medium"),
    opp("DESIGN FESTA GALLERY", "Design Festa Gallery", "gallery", "Tokyo", "https://designfestagallery.com/", "Low-friction rental/gallery wall ecosystem.", "low"),
    opp("Gallery IRO", "Gallery IRO", "gallery", "Tokyo", "https://1-6.jp/iro/", "Kichijoji gallery space; check submission/rental model.", "medium"),
    opp("Gallery HANA Shimokitazawa", "Gallery HANA Shimokitazawa", "gallery", "Tokyo", "https://www.g-hana.jp/", "Small gallery space; check exhibition terms.", "medium"),
    opp("Picaresque Gallery", "Picaresque Gallery", "gallery", "Tokyo", "https://picaresquejpn.com/", "Gallery/shop with approachable art goods ecosystem.", "medium"),
    opp("Cafe Gallery HATTIFNATT", "HATTIFNATT", "cafe_gallery", "Koenji", "https://www.hattifnatt.jp/", "Koenji cafe/gallery atmosphere; verify exhibition options."),
    opp("Cafe Cross Point", "Cafe Cross Point", "cafe_gallery", "Koenji", "https://cafecrosspoint.jp/", "Koenji cafe/gallery candidate; verify wall/display opportunities."),
    opp("MADO Café", "MADO Café", "cafe_gallery", "Koenji", "https://www.instagram.com/madocafe/", "Instagram-first local cafe candidate; verify current activity."),
    opp("Yonchome Cafe", "Yonchome Cafe", "cafe_gallery", "Koenji", "https://www.yonchome.com/", "Koenji cafe candidate; verify art wall/open events."),
    opp("Cafe Mame-Hico", "Cafe Mame-Hico", "cafe_gallery", "Tokyo", "https://www.mamehico.com/", "Cafe ecosystem; check events/exhibitions."),
    opp("B&B Shimokitazawa", "Bookstore B&B", "bookstore_event", "Tokyo", "https://bookandbeer.com/", "Bookstore/event ecosystem; potential talks/zines."),
    opp("BONUS TRACK", "BONUS TRACK", "market_event", "Shimokitazawa", "https://bonus-track.net/", "Market/community/event ecosystem."),
    opp("reload Shimokitazawa", "reload", "market_event", "Shimokitazawa", "https://reload-shimokita.com/", "Commercial/community space; check popups."),
    opp("VACANT", "VACANT", "event_space", "Tokyo", "https://www.vacant.vc/", "Event/gallery/pop-up ecosystem."),
    opp("Spiral", "Spiral", "gallery_event", "Tokyo", "https://www.spiral.co.jp/", "Art/design exhibitions and market events.", "medium"),
    opp("BankART1929", "BankART1929", "artist_space", "Yokohama", "https://bankart1929.com/", "Artist programs/exhibitions near Tokyo.", "medium"),
    opp("Creative Space Hayashi", "Creative Space Hayashi", "gallery", "Yokohama", "https://csh.yokohama/", "Yokohama exhibition space; verify fit."),
    opp("Koganecho Area Management Center", "Koganecho", "artist_space", "Yokohama", "https://koganecho.net/", "Artist-in-residence and local art programs.", "medium"),
    opp("Zushi Art Gallery", "Zushi Art Gallery", "gallery", "Kanagawa", "https://zushi-art.com/", "Regional gallery candidate."),
    opp("Tokyo Wonder Site / TOKAS Residency", "Tokyo Arts and Space", "residency", "Tokyo", "https://www.tokyoartsandspace.jp/en/archive/residence/", "Residency reference; verify current calls.", "high"),
    opp("AIR 3331", "3331 Arts Chiyoda", "residency", "Tokyo", "https://residence.3331.jp/", "Artist residency archive/reference; verify current status.", "medium"),
]

save_json("memory/opportunities_master.json", opportunities)
save_json("memory/opportunities.json", opportunities)

print(f"Seeded {len(opportunities)} Tokyo-first sourced opportunities.")