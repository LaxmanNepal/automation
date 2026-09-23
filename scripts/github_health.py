#!/usr/bin/env python3
"""Scan configured repositories using the GitHub REST API."""
from pathlib import Path
from datetime import datetime, timezone
import json, os, urllib.request, urllib.error
ROOT = Path(__file__).resolve().parents[1]
config = ROOT / "config" / "projects.yml"
out = ROOT / "data" / "github" / "health.json"
out.parent.mkdir(parents=True, exist_ok=True)
repos = []
for line in config.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line.startswith("repository:"):
        repo = line.split(":", 1)[1].strip().strip('"')
        if repo and repo not in repos: repos.append(repo)
token = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
results = []
for repo in repos:
    item = {"repository": repo}
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", **({"Authorization": f"Bearer {token}"} if token else {})})
    try:
        with urllib.request.urlopen(request, timeout=20) as response: data = json.load(response)
        item.update({"accessible": True, "default_branch": data.get("default_branch"), "archived": data.get("archived"), "open_issues": data.get("open_issues_count"), "updated_at": data.get("updated_at"), "visibility": data.get("visibility")})
    except urllib.error.HTTPError as exc: item.update({"accessible": False, "error": f"HTTP {exc.code}"})
    except Exception as exc: item.update({"accessible": False, "error": str(exc)})
    results.append(item)
payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "repositories": results}
out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2))
