#!/usr/bin/env python3
"""Generate implementation-ready GitHub issue specs from revenue assets."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, os, urllib.parse, urllib.request

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/assets/latest.json"
OUT=ROOT/"data/assets/issue_specs.json"
REPORT=ROOT/"reports/assets"
REPO=os.environ.get("GITHUB_REPOSITORY","LaxmanNepal/automation")

def md_list(items):
    return "\n".join(f"- {x}" for x in items) if items else "- None specified"

def issue_for(a):
    aid=a.get("id","asset-unknown")
    title=a.get("asset","Revenue asset")
    body=f"""<!-- laxman-os-asset-id: {aid} -->
## Objective
Build and validate the proposed revenue asset as a small, useful MVP.

## Problem
{a.get("problem","")}

## Target audience
{a.get("audience","")}

## Proposed asset
**{title}**

## Monetization
{a.get("monetization","")}

## MVP implementation
{md_list(a.get("mvp",[]))}

## SEO requirements
{md_list(a.get("seo",[]))}

## Analytics
Track core feature usage, primary CTA/conversion interaction, relevant outbound clicks, and basic errors.

## Acceptance criteria
{md_list(a.get("definition_of_done",[]))}

## Research signal
{a.get("research_signal",0)}

Source opportunity: `{a.get("source_opportunity","")}`

## Execution checklist
- [ ] Confirm the opportunity and current user need
- [ ] Confirm scope and monetization approach
- [ ] Implement the MVP
- [ ] Test mobile and desktop
- [ ] Check accessibility
- [ ] Check SEO title, description, canonical, and indexability
- [ ] Verify analytics events
- [ ] Human review before launch

## Safety gate
This is an implementation plan, not proof of demand or revenue. Do not spend money, publish, deploy, or make commercial commitments without human approval.
"""
    return {"id":aid,"title":f"build: {title}","body":body,"source_opportunity":a.get("source_opportunity"),"status":"draft"}

def create_issue(spec,token):
    q=urllib.parse.urlencode({"q":f'repo:{REPO} in:body "laxman-os-asset-id: {spec["id"]}" is:issue'})
    req=urllib.request.Request("https://api.github.com/search/issues?"+q,headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","User-Agent":"laxman-os"})
    with urllib.request.urlopen(req,timeout=20) as r:
        found=json.load(r).get("items",[])
    if found:
        spec.update(status="deduplicated",issue_number=found[0].get("number"),issue_url=found[0].get("html_url"))
        return spec
    payload=json.dumps({"title":spec["title"],"body":spec["body"]}).encode()
    req=urllib.request.Request(f"https://api.github.com/repos/{REPO}/issues",data=payload,method="POST",headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","Content-Type":"application/json","User-Agent":"laxman-os"})
    with urllib.request.urlopen(req,timeout=20) as r:
        created=json.load(r)
    spec.update(status="created",issue_number=created.get("number"),issue_url=created.get("html_url"))
    return spec

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--create-issues",action="store_true")
    args=ap.parse_args()
    data=json.loads(SOURCE.read_text(encoding="utf-8")) if SOURCE.exists() else {"assets":[]}
    specs=[issue_for(a) for a in data.get("assets",[])]
    if args.create_issues:
        token=os.environ.get("GITHUB_TOKEN")
        if not token: raise SystemExit("GITHUB_TOKEN is required when --create-issues is used")
        specs=[create_issue(s,token) for s in specs]
    payload={"generated_at":datetime.now(timezone.utc).isoformat(),"repository":REPO,"count":len(specs),"specs":specs}
    OUT.parent.mkdir(parents=True,exist_ok=True); REPORT.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines=[f"# Laxman OS — Build Issue Specs ({date})","","| Asset ID | Issue | Status |","|---|---|---|"]
    for s in specs:
        issue=f"[#{s['issue_number']}]({s['issue_url']})" if s.get("issue_url") else s["title"]
        lines.append(f"| {s['id']} | {issue} | {s['status']} |")
    lines += ["","## Gate","Issue specs are generated from revenue-asset specifications. Human validation is required before implementation or launch."]
    content="\n".join(lines)+"\n"
    (REPORT/f"{date}-issues.md").write_text(content,encoding="utf-8")
    (REPORT/"issues-latest.md").write_text(content,encoding="utf-8")
    print(content)

if __name__=="__main__":
    main()
