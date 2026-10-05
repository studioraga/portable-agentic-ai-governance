#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.operational_security.runtime import evaluate_m26_material
p=argparse.ArgumentParser();p.add_argument('--material',required=True);p.add_argument('--repo-root',default=str(ROOT));a=p.parse_args();r=evaluate_m26_material(a.material,a.repo_root);print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 2)
