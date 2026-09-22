#!/usr/bin/env python3
"""Build a deterministic action queue from configured projects and health data."""
from pathlib import Path
from datetime import datetime, timezone
import json

ROOT = Path(__file__).resolve().parents[1]
health_path = ROOT / "data" / "github" / "health.json"
out_dir = ROOT / "reports" / "actions"
out_dir.mkdir(parents=True, exist_ok=True)

health = json.loads(health_path.read_text(encoding="utf-8")) if health_path.exists() else {"repositories": []}
actions = []

for item in health.get("repositories", []):
    repo = item["repository"]
    if not item.get("accessible"):
        actions.append({
            "priority": 10,
            "category": "github",
            "repository": repo,
            "action": f"Restore GitHub API access for {repo}",
            "reason": item.get("error", "unknown error"),
        })
    elif item.get("archived"):
        actions.append({
            "priority": 8,
            "category": "github",
            "repository": repo,
            "action": f"Review archived status of {repo}",
            "reason": "Repository is archived.",
        })
    elif (item.get("open_issues") or 0) > 0:
        actions.append({
            "priority": 6,
            "category": "github",
            "repository": repo,
            "action": f"Review open issues in {repo}",
            "reason": f"{item.get('open_issues')} open issue(s).",
        })

actions.extend([
    {
        "priority": 10,
        "category": "money",
        "repository": None,
        "action": "Research one monetizable problem for a small tool, template, or guide",
        "reason": "Revenue is the top configured priority.",
    },
    {
        "priority": 9,
        "category": "youtube",
        "repository": None,
        "action": "Research one high-intent topic for @laxmannepalofficial",
        "reason": "YouTube is the second configured priority.",
    },
])

actions.sort(key=lambda x: (-x["priority"], x["category"], x["action"]))
date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

lines = [f"# Laxman OS — Action Queue ({date})", "", "| Priority | Category | Action | Reason |", "|---:|---|---|---|"]
for action in actions:
    lines.append(f"| {action['priority']} | {action['category']} | {action['action']} | {action['reason']} |")
lines += ["", "## Rule", "Pick one action for execution. Research and prioritization do not automatically authorize publishing, spending, trading, merging, or destructive changes."]

content = "\n".join(lines) + "\n"
(out_dir / f"{date}.md").write_text(content, encoding="utf-8")
(out_dir / "latest.md").write_text(content, encoding="utf-8")
print(content)
