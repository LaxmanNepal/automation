#!/usr/bin/env python3
"""Dependency-light validation for Laxman OS configuration."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
required = [ROOT / "config" / "priorities.yml", ROOT / "config" / "channels.yml", ROOT / "config" / "projects.yml"]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    print("Missing configuration files:")
    for item in missing: print(f" - {item}")
    sys.exit(1)
for path in required:
    if not path.read_text(encoding="utf-8").strip():
        print(f"Empty configuration: {path.relative_to(ROOT)}")
        sys.exit(1)
print("Configuration files present and non-empty.")
