#!/usr/bin/env python3
"""Check configured websites. Network failures are reported, not diagnosed."""
import json,pathlib,re,urllib.request,urllib.error
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=(ROOT/"config/websites.yml").read_text(encoding="utf-8")
sites=re.findall(r'- id: ([^\n]+)\n    name: "([^"]+)"\n    url: "([^"]+)"\n    enabled: (true|false)',s)
out=[]
for sid,name,url,enabled in sites:
    item={"id":sid,"name":name,"url":url,"status":"disabled" if enabled!="true" else "unavailable"}
    if enabled=="true":
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Laxman-OS-Health/1.0"})
            with urllib.request.urlopen(req,timeout=15) as r: item.update(status="healthy" if r.status<400 else "warning",http_status=r.status)
        except urllib.error.HTTPError as e: item.update(status="warning",http_status=e.code)
        except Exception as e: item.update(error_type=type(e).__name__)
    out.append(item)
now=datetime.now(timezone.utc).isoformat()
payload={"version":1,"generated_at":now,"status":"healthy" if out and all(x["status"]=="healthy" for x in out) else "warning","sites":out,"findings":[],"human_validation_required":True}
(ROOT/"data/website").mkdir(parents=True,exist_ok=True);(ROOT/"data/website/latest.json").write_text(json.dumps(payload,indent=2)+"\n")
(ROOT/"reports/website").mkdir(parents=True,exist_ok=True)
(ROOT/"reports/website/latest.md").write_text("# Website Health\n\n"+"\n".join(f"- {x['name']}: {x['status']} — {x['url']}" for x in out)+"\n")
