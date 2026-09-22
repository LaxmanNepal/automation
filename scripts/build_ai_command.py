#!/usr/bin/env python3
"""Evidence-based command synthesis. This is not a predictive model."""
import json,pathlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
try: snap=json.loads((ROOT/"data/os/latest.json").read_text())
except Exception: snap={}
actions=snap.get("actions",[])
now=datetime.now(timezone.utc).isoformat()
command={"version":1,"generated_at":now,"status":"ready" if actions else "waiting","top_actions":actions[:5],"reasoning":"Sorted from collected module evidence; no outcome prediction is made.","human_validation_required":True}
(ROOT/"data/os/command.json").write_text(json.dumps(command,indent=2)+"\n")
(ROOT/"reports/os/command.md").write_text("# Daily Command\n\nGenerated: "+now+"\n\n"+("\n".join(f"{i}. {a['action']} — {a['category']} / {a['priority']}" for i,a in enumerate(actions[:5],1)) if actions else "Waiting for evidence.")+"\n\nHuman approval is required.\n")
