#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_psirt.runtime import evaluate_m15_material
a=argparse.ArgumentParser();a.add_argument('--material',required=True);a.add_argument('--repo-root');ns=a.parse_args();r=evaluate_m15_material(ns.material,ns.repo_root);print(json.dumps(r,indent=2,sort_keys=True));sys.exit(0 if r['ok'] else 2)
