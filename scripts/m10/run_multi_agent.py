#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.multi_agent.common import load_json
from portable_ai_governance.multi_agent.runtime import require_multi_agent
from portable_ai_governance.multi_agent.workflow import GovernanceSupervisor

def envfile(p):
 d={}
 for l in Path(p).read_text().splitlines():
  if l and not l.startswith('#') and '=' in l:k,v=l.split('=',1);d[k]=v
 return d
ap=argparse.ArgumentParser();ap.add_argument('--env',required=True);sub=ap.add_subparsers(dest='cmd',required=True)
a=sub.add_parser('analyze');a.add_argument('--case-json');a.add_argument('--case-file');a.add_argument('--out')
f=sub.add_parser('finalize');f.add_argument('--workflow-result',required=True);f.add_argument('--decision',required=True)
v=sub.add_parser('verify');v.add_argument('--workflow-id')
args=ap.parse_args();e=envfile(args.env);require_multi_agent(e);policy=load_json(e['PAG_M10_POLICY']);top=load_json(e['PAG_M10_TOPOLOGY']);sup=GovernanceSupervisor(policy,top,Path(e['PAG_M10_RUNTIME_ROOT']),e['PAG_M10_DECISION_PUBLIC_KEY'])
try:
 if args.cmd=='analyze':
  if bool(args.case_json)==bool(args.case_file):raise RuntimeError('provide exactly one of --case-json or --case-file')
  case=json.loads(args.case_json) if args.case_json else load_json(args.case_file);r=sup.analyze(case)
  if args.out:Path(args.out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 elif args.cmd=='finalize':r=sup.finalize(load_json(args.workflow_result),load_json(args.decision))
 else:r={'ok':sup.journal.verify(),'workflow_id':args.workflow_id,'events':sup.journal.events(args.workflow_id) if args.workflow_id else []}
 print(json.dumps({'ok':True,'result':r},indent=2));raise SystemExit(0)
except Exception as ex:
 print(json.dumps({'ok':False,'reason':str(ex)},indent=2));raise SystemExit(2)
