
import json
import os
import py_compile

REQUIRED_FILES = [
    "app.py",
    "deploy_data/compact_opportunities.json",
    "static/assets/headers/mochi_hero.png",
]

OPTIONAL_IMPORT_FILES = [
    "opportunity_report_engine.py",
    "mochi_dashboard_components.py",
    "mochi_action_components.py",
]

def fail(message):
    print("FAIL:", message)
    raise SystemExit(1)

def ok(message):
    print("OK:", message)

def main():
    print("\\nSAFE DEPLOY CHECK")
    print("=" * 70)

    for path in REQUIRED_FILES:
        if not os.path.exists(path):
            fail(f"Missing required file: {path}")
        ok(f"Found {path}")

    for path in OPTIONAL_IMPORT_FILES:
        if os.path.exists(path):
            ok(f"Found {path}")
        else:
            print(f"WARNING: optional/import file missing: {path}")

    try:
        py_compile.compile("app.py", doraise=True)
        ok("app.py compiles")
    except Exception as e:
        fail(f"app.py does not compile: {e}")

    try:
        with open("deploy_data/compact_opportunities.json", "r", encoding="utf-8") as f:
            opps = json.load(f)
    except Exception as e:
        fail(f"Could not read opportunities JSON: {e}")

    if not isinstance(opps, list):
        fail("compact_opportunities.json is not a list")
    if not opps:
        fail("No opportunities found")

    ok(f"Loaded {len(opps)} opportunities")

    print("\\nDEPLOY CHECK PASSED")

if __name__ == "__main__":
    main()
