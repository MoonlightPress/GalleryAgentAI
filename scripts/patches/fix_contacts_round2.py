"""
fix_contacts_round2.py

Post-verification-pass fixes — run after targeted_verification_agent.py completes,
since verification loads a snapshot and writes the full file back.

Fixes:
1. アートオリンピア2026 — wrong official_website (x.com/artkoubo → real page)
2. 第九屆水主題國際評審藝術比賽 — add contact_verified + contact
3. FACE Exhibition 2026 — fix official_website + add contact
4. 2026春季二科展 NIKA+nika — revert incorrect Art Olympia URL/contact
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
        name = opp.get("name") or opp.get("title") or ""

        # 1. アートオリンピア2026 — fix website from x.com/artkoubo to real URL
        if "artkoubo" in str(opp.get("official_website", "")) and "artolympia" not in str(opp.get("official_website", "")).lower():
            # Only fix entries whose name contains artolympia/art olympia (JP name encoded)
            if "artkoubo" in str(opp.get("official_website", "")).lower() and opp.get("exclusive_primary_bucket") == "immediate_best_moves":
                # Check submission_page to see if it's Art Olympia specifically
                sub = str(opp.get("submission_page", ""))
                if "artolympia" in sub.lower():
                    opp["official_website"]  = "https://www.artkoubo.jp/artolympia/"
                    opp["contact"]           = "Online submission: compe.japandesign.ne.jp/artolympia-2026"
                    opp["contact_verified"]  = True
                    print(f"  FIXED Art Olympia website: {name[:50]}")
                    changed += 1

        # 2. 第九屆水主題 — bhuntr competition, add contact
        if "bhuntr.com/tw/competitions/208h5hxfrofrnv2jhx" in str(opp.get("submission_page", "")) and not opp.get("contact"):
            opp["contact"]          = "Online submission via bhuntr.com"
            opp["contact_verified"] = True
            print(f"  FIXED 9th Water Competition contact: {name[:50]}")
            changed += 1

        # 3. FACE Exhibition 2026 — fix to official Sompo Foundation URL
        if name == "FACE Exhibition 2026":
            opp["official_website"] = "https://www.smaf.jp/face/"
            opp["contact"]          = "Online application: smaf.jp/face"
            opp["contact_verified"] = True
            print(f"  FIXED FACE Exhibition: {name[:50]}")
            changed += 1

        # 4. NIKA+nika — revert if it got the wrong artolympia URL
        if ("NIKA+nika" in name or "NIKA nika" in name) and "artolympia" in str(opp.get("official_website", "")).lower():
            opp["official_website"]  = "https://compe.japandesign.ne.jp/"
            opp["contact"]           = None
            opp["contact_verified"]  = False
            print(f"  REVERTED NIKA+nika wrong URL: {name[:50]}")
            changed += 1

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. {changed} entries fixed.")


if __name__ == "__main__":
    main()
