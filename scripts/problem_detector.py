#!/usr/bin/env python3
"""Detect actionable GitHub problems across configured repositories."""
from pathlib import Path
from datetime import datetime, timezone
import json, os, re, urllib.request, urllib.error, urllib.parse

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"config"/"projects.yml"
OUT=ROOT/"data"/"problems"/"latest.json"
OUT.parent.mkdir(parents=True,exist_ok=True)

def repos():
    out=[]
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if line.startswith("repository:"):
            r=line.split(":",1)[1].strip().strip('"')
            if r and r not in out: out.append(r)
    return out

TOKEN=os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
HEADERS={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"laxman-os-problem-detector/1"}
if TOKEN: HEADERS["Authorization"]=f"Bearer {TOKEN}"

def api(path):
    req=urllib.request.Request("https://api.github.com"+path,headers=HEADERS)
    try:
        with urllib.request.urlopen(req,timeout=25) as r: return json.load(r),None
    except urllib.error.HTTPError as e: return None,f"HTTP {e.code}"
    except Exception as e: return None,str(e)

def age_days(value):
    if not value: return 0
    try: return (datetime.now(timezone.utc)-datetime.fromisoformat(value.replace("Z","+00:00"))).days
    except Exception: return 0

def add(items,repo,kind,title,detail,priority,fingerprint):
    items.append({"repository":repo,"kind":kind,"title":title,"detail":detail,"priority":priority,"fingerprint":fingerprint})

def scan(repo):
    p=[]; base=f"/repos/{repo}"
    runs,err=api(base+"/actions/runs?per_page=20")
    if runs is not None:
        for x in runs.get("workflow_runs",[]):
            if x.get("conclusion") in {"failure","timed_out","startup_failure","action_required"} and age_days(x.get("updated_at"))<=30:
                add(p,repo,"workflow_failure",f"Workflow failing: {x.get('name') or 'workflow'}",f"Conclusion={x.get('conclusion')}; commit={(x.get('head_sha') or '')[:8]}; updated={x.get('updated_at')}",100,f"workflow:{x.get('id')}:{x.get('conclusion')}")
    else: p.append({"repository":repo,"kind":"scan_warning","title":"Actions scan unavailable","detail":err,"priority":0})

    issues,err=api(base+"/issues?state=open&per_page=100&sort=updated&direction=asc")
    if issues is not None:
        for x in issues:
            if x.get("pull_request"): continue
            a=age_days(x.get("updated_at"))
            if a>=30: add(p,repo,"stale_issue",f"Stale issue: #{x.get('number')} {x.get('title')}",f"Unchanged for about {a} days: {x.get('html_url')}",55,f"issue:{x.get('number')}")
    else: p.append({"repository":repo,"kind":"scan_warning","title":"Issues scan unavailable","detail":err,"priority":0})

    prs,err=api(base+"/pulls?state=open&per_page=100&sort=updated&direction=asc")
    if prs is not None:
        for x in prs:
            a=age_days(x.get("updated_at"))
            if a>=14: add(p,repo,"stale_pr",f"Stale PR: #{x.get('number')} {x.get('title')}",f"Open and unchanged for about {a} days: {x.get('html_url')}",70,f"pr:{x.get('number')}")
    else: p.append({"repository":repo,"kind":"scan_warning","title":"PR scan unavailable","detail":err,"priority":0})

    data,err=api(base)
    if data is not None:
        if data.get("archived"): add(p,repo,"archived","Repository is archived","Archived repositories cannot receive normal active development.",20,f"archived:{repo}")
        if data.get("has_issues") and data.get("open_issues_count",0)>25: add(p,repo,"issue_backlog","Large open-issue backlog",f"{data.get('open_issues_count')} open issues.",45,f"backlog:{repo}")
    else: p.append({"repository":repo,"kind":"scan_warning","title":"Repository scan unavailable","detail":err,"priority":0})

    for endpoint,kind,label,default_priority,prefix in [
        ("/dependabot/alerts?state=open&per_page=100","dependabot","Open dependency security alert",70,"dependabot"),
        ("/secret-scanning/alerts?state=open&per_page=100","secret_scanning","Open secret-scanning alert",100,"secret"),
        ("/code-scanning/alerts?state=open&per_page=100","code_scanning","Open code-scanning alert",75,"code")]:
        arr,err=api(base+endpoint)
        if arr is not None:
            for x in arr:
                if kind=="dependabot":
                    sev=((x.get("security_advisory") or {}).get("severity") or "unknown").lower()
                    dep=((x.get("dependency") or {}).get("package") or {}).get("name") or "dependency"
                    pr={"critical":98,"high":90,"moderate":70,"low":45}.get(sev,60)
                    add(p,repo,kind,f"Open dependency security alert: {dep}",f"Severity={sev}; alert #{x.get('number')}.",pr,f"{prefix}:{x.get('number')}")
                elif kind=="secret_scanning":
                    add(p,repo,kind,label,f"Alert #{x.get('number')} is open; review it in GitHub.",100,f"{prefix}:{x.get('number')}")
                else:
                    sev=((x.get("rule") or {}).get("security_severity_level") or "unknown").lower()
                    pr={"critical":98,"high":90,"medium":75,"low":50}.get(sev,65)
                    desc=((x.get("rule") or {}).get("description") or "security finding")
                    add(p,repo,kind,f"Open code-scanning alert: {desc}",f"Security severity={sev}; alert #{x.get('number')}.",pr,f"{prefix}:{x.get('number')}")
        elif err not in {"HTTP 403","HTTP 404"}:
            p.append({"repository":repo,"kind":"scan_warning","title":f"{kind} scan unavailable","detail":err,"priority":0})
    return p

allp=[]
for r in repos(): allp.extend(scan(r))
allp.sort(key=lambda x:(-x.get("priority",0),x.get("repository",""),x.get("kind","")))
payload={"generated_at":datetime.now(timezone.utc).isoformat(),"repositories":repos(),"problem_count":len([x for x in allp if x.get("kind")!="scan_warning"]),"problems":allp}
OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
print(json.dumps(payload,indent=2))

if os.getenv("CREATE_GITHUB_ISSUES","false").lower()=="true":
    for p in allp:
        if p.get("kind")=="scan_warning" or p.get("priority",0)<70: continue
        fp=p["fingerprint"]
        q=urllib.parse.quote(f"repo:{p['repository']} in:body {fp}")
        existing,_=api(f"/search/issues?q={q}&state=open&per_page=1")
        if existing and existing.get("total_count",0): continue
        body=f"""<!-- laxman-os:fingerprint={fp} -->
## Detected by Laxman OS

**Repository:** \`{p['repository']}\`
**Type:** {p['kind']}
**Priority:** {p['priority']}

{p['detail']}

### Next step
Review the finding, confirm it is actionable, then fix or close this issue.

> Created automatically by the Problem Detector. No production change or merge is performed automatically.
"""
        data=json.dumps({"title":p["title"],"body":body}).encode()
        req=urllib.request.Request("https://api.github.com/repos/"+p["repository"]+"/issues",data=data,headers={**HEADERS,"Content-Type":"application/json"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=25) as r: created=json.load(r)
            print(f"Created issue #{created.get('number')} for {p['repository']}")
        except Exception as e: print(f"Could not create issue for {p['repository']}: {e}")
