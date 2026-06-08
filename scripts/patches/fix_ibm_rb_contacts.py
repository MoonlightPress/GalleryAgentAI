"""
fix_ibm_rb_contacts.py

One-shot fixes for IBM + RB entries after verification pass:
1. Gallery Rocket Harajuku — website is dead (DNS failure confirmed June 2026).
   Clears URL fields, updates contact to Instagram-only, updates quick_action.
2. 水性繪畫展覽 — contact field is [None, None, None] bug. Fixed to None.
3. Northwest Watercolor Society — official_website was empty. Set to nwws.org.

SSL false-negatives (UTRECHT etc.) are handled by targeted_verification_agent.py
after the ssl fallback fix was applied to that script — no need to hardcode here.

Idempotent — safe to run again.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT     = Path(__file__).parent.parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"


def main():
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    changed = 0

    for opp in opps:
        name  = opp.get("name") or opp.get("title") or ""
        short = name[:60]

        # 1. Gallery Rocket — dead domain, Instagram DM only
        if "Gallery Rocket" in name and "Harajuku" in name:
            opp["official_website"]        = ""
            opp["submission_page"]         = ""
            opp["url_verification_status"] = "no_url"
            opp["url_status_code"]         = None
            opp["site_http_code"]          = None
            opp["contact"] = "@galleryrocket (Instagram DM — website offline as of 2026-06)"
            opp["quick_action"] = (
                "DM @galleryrocket on Instagram, or visit the gallery in person "
                "(Harajuku). Website is currently offline — Instagram is the only "
                "confirmed contact channel."
            )
            print(f"  FIXED Gallery Rocket: cleared dead URL, updated contact")
            changed += 1

        # 2. Null contact list bug
        if isinstance(opp.get("contact"), list):
            opp["contact"] = None
            print(f"  FIXED null contact list: {short}")
            changed += 1

        # 3. Northwest Watercolor Society — add official website
        if name == "Northwest Watercolor Society" and not opp.get("official_website"):
            opp["official_website"] = "https://www.nwws.org/"
            opp["contact"] = "nwws.org contact form"
            print(f"  FIXED NWWS: added official website + contact")
            changed += 1

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. {changed} entries fixed.")


if __name__ == "__main__":
    main()
