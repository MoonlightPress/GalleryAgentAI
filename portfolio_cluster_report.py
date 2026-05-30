
import json
import os
from pathlib import Path

CATALOG = "memory/image_catalog.json"
CLUSTERS = "portfolio_cluster_template.json"
OUT = "reports/portfolio_cluster_report.md"

def load(path, fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():

    catalog = load(CATALOG,[])
    clusters = load(CLUSTERS,{})

    lines = [
        "# Portfolio Cluster Report",
        "",
        f"Images Cataloged: {len(catalog)}",
        ""
    ]

    for cluster in clusters.get("clusters",[]):
        lines.append(f"## {cluster['name']}")
        lines.append("")
        lines.append(f"Assigned Images: {len(cluster.get('images',[]))}")
        lines.append(cluster.get("notes",""))
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines),encoding="utf-8")

    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
