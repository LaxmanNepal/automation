#!/usr/bin/env python3
"""Inventory public repositories visible to the workflow token."""
import json,os,pathlib,urllib.request
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
token=os.getenv("GITHUB_TOKEN"); owner=os.getenv("GITHUB_OWNER","LaxmanNepal")
headers={"Accept":"application/vnd.github+json","User-Agent":"Laxman-OS"}
if token: headers["Authorization"]="Bearer "+token
items=[]
if token:
    url=f"https://api.github.com/users/{owner}/repos?per_page=100&type=all&sort=updated"
    try:
        req=urllib.request.Request(url,headers=headers)
        with urllib.request.urlopen(req,timeout=20) as r: raw=json.load(r)
        for x in raw:
            items.append({"name":x.get("name"),"full_name":x.get("full_name"),"archived":x.get("archived",False),"open_issues":x.get("open_issues_count",0),"updated_at":x.get("updated_at"),"html_url":x.get("html_url")})
    except Exception as e:
        items=[];error=type(e).__name__
else: error="missing GITHUB_TOKEN"
payload={"version":1,"generated_at":datetime.now(timezone.utc).isoformat(),"status":"healthy" if items else "waiting","repositories":items,"error":locals().get("error"),"human_validation_required":True}
(ROOT/"data/github").mkdir(parents=True,exist_ok=True);(ROOT/"data/github/inventory.json").write_text(json.dumps(payload,indent=2)+"\n")
