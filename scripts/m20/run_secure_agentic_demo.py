#!/usr/bin/env python3
import argparse,json,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_final_freeze.secure_agentic_demo import run_node1,verify_node2
ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['node1','node2'],required=True);ap.add_argument('--out');ap.add_argument('--case');ap.add_argument('--trace');ap.add_argument('--public-key');a=ap.parse_args()
if a.mode=='node1':
 case=json.loads(Path(a.case or ROOT/'examples/secure-agentic-node1-node2/case.json').read_text());t=run_node1(case,a.out);print(json.dumps({'ok':True,'workflow_id':t['proposal']['workflow_id'],'status':t['final']['status'],'side_effect_authority':False},indent=2))
else:
 r=verify_node2(a.trace,a.public_key);print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 2)
