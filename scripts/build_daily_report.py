#!/usr/bin/env python3
"""Build a concise daily command report."""
from pathlib import Path
from datetime import datetime, timezone
import json
ROOT = Path(__file__).resolve().parents[1]
health_path = ROOT / "data" / "github" / "health.json"
report_dir = ROOT / "reports" / "daily"
report_dir.mkdir(parents=True, exist_ok=True)
date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
health = json.loads(health_path.read_text(encoding="utf-8")) if health_path.exists() else {"repositories": []}
lines = [f"# Laxman OS — Daily Command ({date})", "", "## Today's focus", "1. Find one revenue opportunity.", "2. Pick one YouTube action with measurable upside.", "3. Fix one high-value GitHub or website problem.", "", "## GitHub health"]
for item in health.get("repositories", []):
    if item.get("accessible"):
        lines.append(f"- **{item['repository']}** — branch `{item.get('default_branch')}`, open issues: {item.get('open_issues')}, archived: {item.get('archived')}.")
    else:
        lines.append(f"- **{item['repository']}** — inaccessible: {item.get('error', 'unknown error')}.")
lines += ["", "## Human review", "- Choose the single highest-value action before starting work.", "- Do not auto-merge, auto-publish, auto-spend, or auto-trade."]
content = "\n".join(lines) + "\n"
(report_dir / f"{date}.md").write_text(content, encoding="utf-8")
(report_dir / "latest.md").write_text(content, encoding="utf-8")
print(content)
