
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPORT = Path("reports/git_backup_report.md")

def run(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True, shell=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    Path("reports").mkdir(exist_ok=True)

    lines = [
        "# Git Backup Report",
        "",
        f"Created: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]

    commands = [
        "git status --short",
        "git add .",
        'git commit -m "backup verified watercolor opportunity pipeline"',
        "git status --short",
    ]

    for cmd in commands:
        code, out, err = run(cmd)
        lines.append(f"## {cmd}")
        lines.append("")
        lines.append(f"Exit code: {code}")
        if out:
            lines.append("")
            lines.append("```")
            lines.append(out)
            lines.append("```")
        if err:
            lines.append("")
            lines.append("```")
            lines.append(err)
            lines.append("```")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")
    print("If commit succeeded, run: git push")
    print("If commit says nothing to commit, the repo was already clean.")

if __name__ == "__main__":
    main()
