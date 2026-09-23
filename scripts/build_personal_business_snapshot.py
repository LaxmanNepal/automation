#!/usr/bin/env python3
import json,pathlib,re
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1];s=(ROOT/"config/business.yml").read_text()
goals=re.findall(r'- id: ([^\n]+)\n    name: "([^"]+)"\n    target: "([^"]+)"\n    status: ([^\n]+)',s)
projects=re.findall(r'- id: ([^\n]+)\n    name: "([^"]+)"\n    repository: "([^"]+)"\n    status: ([^\n]+)',s)
payload={"version":1,"generated_at":datetime.now(timezone.utc).isoformat(),"status":"healthy","goals":[dict(zip(["id","name","target","status"],x)) for x in goals],"projects":[dict(zip(["id","name","repository","status"],x)) for x in projects],"assets":[],"human_validation_required":True}
(ROOT/"data/business/latest.json").write_text(json.dumps(payload,indent=2)+"\n")
