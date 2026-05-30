
import json
import os
from pathlib import Path

REPORT = Path("reports/deployment_readiness_audit.md")

IMPORTANT_FILES = [
    "app.py",
    "requirements.txt",
    "deploy_data/compact_opportunities.json",
    "memory/verified_opportunities.json",
    "memory/typed_opportunities.json",
    "reports/application_action_report.md",
]

OPTIONAL_BUT_USEFUL = [
    ".streamlit/config.toml",
    ".streamlit/config.toml.txt",
    "packages.txt",
    "README.md",
]

def exists(path):
    return Path(path).exists()

def json_count(path):
    try:
        data = json.load(open(path, encoding="utf-8"))
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict):
            return len(data.keys())
    except Exception as e:
        return f"error: {e}"
    return "unknown"

def main():
    Path("reports").mkdir(exist_ok=True)

    lines = [
        "# Deployment Readiness Audit",
        "",
        "This checks whether the project has the basic files needed to run as a dashboard online.",
        "",
        "## Required / Important Files",
        "",
    ]

    for f in IMPORTANT_FILES:
        status = "OK" if exists(f) else "MISSING"
        extra = ""
        if f.endswith(".json") and exists(f):
            extra = f" — records: {json_count(f)}"
        lines.append(f"- {status}: `{f}`{extra}")

    lines += ["", "## Optional Useful Files", ""]
    for f in OPTIONAL_BUT_USEFUL:
        status = "OK" if exists(f) else "MISSING"
        lines.append(f"- {status}: `{f}`")

    lines += [
        "",
        "## Online Notes",
        "",
        "- The Streamlit dashboard should be deployable if `app.py` and dependencies are present.",
        "- Web crawling may be unreliable online because remote hosts can block automated requests.",
        "- Do not rely on live crawling for the public app until you add caching, rate limits, and retry handling.",
        "- Best online model: display saved JSON/report outputs; run crawlers locally or as controlled admin-only tasks.",
        "",
        "## Recommended Commit",
        "",
        '```powershell',
        'python project_backup_git_helper.py',
        'git push',
        '```',
    ]

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")

if __name__ == "__main__":
    main()
