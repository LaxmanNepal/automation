#!/usr/bin/env python3
"""Build a digest from module findings. Delivery is intentionally gated."""
import json, pathlib
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
alerts=[]
for module,rel in [("github","data/problems/latest.json"),("seo","data/seo/latest.json"),("website","data/website/latest.json")]:
    try: obj=json.loads((ROOT/rel).read_text())
    except Exception: continue
    for item in obj.get("findings",[]):
        alerts.append({"module":module,"severity":"warning","detail":item})
now=datetime.now(timezone.utc).isoformat()
payload={"version":1,"generated_at":now,"status":"warning" if alerts else "healthy","alerts":alerts[:50],"human_validation_required":True,"delivery":"digest-only"}
p=ROOT/"data/alerts";p.mkdir(parents=True,exist_ok=True);(p/"latest.json").write_text(json.dumps(payload,indent=2)+"\n")
r=ROOT/"reports/alerts";r.mkdir(parents=True,exist_ok=True);(r/"latest.md").write_text("# Alert Digest\n\n"+("\n".join(f"- **{a['module']}**: {a['detail']}" for a in alerts) if alerts else "No current alerts.")+"\n\nAutomatic external notification delivery is disabled.\n")
