#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_annex_evidence.runtime import evaluate_m17_material
ap=argparse.ArgumentParser();ap.add_argument('--material',required=True);ap.add_argument('--repo-root');a=ap.parse_args();r=evaluate_m17_material(a.material,a.repo_root);print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r['ok'] else 2)
