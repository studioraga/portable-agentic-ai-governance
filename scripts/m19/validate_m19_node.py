#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_production_validation.runtime import evaluate_m19_material
ap=argparse.ArgumentParser();ap.add_argument('--material',required=True);ap.add_argument('--repo-root');ap.add_argument('--current-node2-profile');a=ap.parse_args();r=evaluate_m19_material(a.material,a.repo_root,a.current_node2_profile);print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r['ok'] else 2)
