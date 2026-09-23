#!/usr/bin/env python3
"""Basic static SEO checks for local HTML files."""
import json,pathlib,re
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1];findings=[]
for p in ROOT.rglob("*.html"):
    if ".git" in p.parts or "node_modules" in p.parts: continue
    s=p.read_text(encoding="utf-8",errors="ignore")
    checks=[("title",bool(re.search(r"<title>\s*[^<]+</title>",s,re.I))),("meta description",bool(re.search(r'<meta[^>]+name=["\']description["\'][^>]*>',s,re.I))),("viewport",bool(re.search(r'<meta[^>]+name=["\']viewport["\'][^>]*>',s,re.I)))]
    for name,ok in checks:
        if not ok: findings.append({"file":str(p.relative_to(ROOT)),"check":name,"status":"missing"})
now=datetime.now(timezone.utc).isoformat()
payload={"version":1,"generated_at":now,"status":"warning" if findings else "healthy","sites":[],"findings":findings,"human_validation_required":True}
out=ROOT/"data/seo";out.mkdir(parents=True,exist_ok=True);(out/"latest.json").write_text(json.dumps(payload,indent=2)+"\n")
rep=ROOT/"reports/seo";rep.mkdir(parents=True,exist_ok=True)
(rep/"latest.md").write_text("# SEO Static Checks\n\n"+("\n".join(f"- {x['file']}: missing {x['check']}" for x in findings) if findings else "No basic local HTML metadata findings.")+"\n")
