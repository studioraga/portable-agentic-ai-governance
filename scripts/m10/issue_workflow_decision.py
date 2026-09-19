#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.multi_agent.common import load_json,write_json
from portable_ai_governance.multi_agent.approval import WorkflowDecisionGrant,DecisionIssuer,to_dict

def envfile(p):
 d={}
 for l in Path(p).read_text().splitlines():
  if l and not l.startswith('#') and '=' in l:k,v=l.split('=',1);d[k]=v
 return d
ap=argparse.ArgumentParser();ap.add_argument('--env',required=True);ap.add_argument('--private-key',required=True);ap.add_argument('--workflow-result',required=True);ap.add_argument('--reviewer',required=True);ap.add_argument('--decision',choices=['approve','reject'],required=True);ap.add_argument('--ttl-seconds',type=int);ap.add_argument('--out',required=True);a=ap.parse_args();e=envfile(a.env);policy=load_json(e['PAG_M10_POLICY']);hp=policy['human_decision']
if a.reviewer not in hp['reviewers']:raise SystemExit('FAIL: reviewer not authorized by signed M10 policy')
ttl=hp['ttl_default_seconds'] if a.ttl_seconds is None else a.ttl_seconds
if not 60<=ttl<=hp['ttl_max_seconds']:raise SystemExit('FAIL: decision TTL outside signed M10 policy')
r=load_json(a.workflow_result)
if a.decision=='approve' and r.get('status')!='pending-human-approval':raise SystemExit('FAIL: Assurance has not cleared workflow for approval')
n=int(time.time());g=WorkflowDecisionGrant(str(uuid.uuid4()),r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],a.reviewer,a.decision,n,n+ttl,1);sig=DecisionIssuer(a.private_key).sign(g);write_json(a.out,to_dict(g,sig));print(json.dumps({'ok':True,'decision_id':g.decision_id,'workflow_id':g.workflow_id,'decision':g.decision,'reviewer':g.reviewer,'ttl_seconds':ttl,'expires_at':g.expires_at,'out':a.out},indent=2))
