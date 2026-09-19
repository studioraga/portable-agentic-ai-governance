#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.security_ops.common import load_json
from portable_ai_governance.security_ops.engine import SecurityOperations
from portable_ai_governance.security_ops.recovery import RecoveryVerifier,RecoveryUseStore,from_dict

def envfile(p):
 d={}
 for l in Path(p).read_text().splitlines():
  if l and not l.startswith('#') and '=' in l:
   k,v=l.split('=',1);d[k]=v
 return d
ap=argparse.ArgumentParser();ap.add_argument('--env',required=True);sp=ap.add_subparsers(dest='cmd',required=True)
i=sp.add_parser('ingest');i.add_argument('--event-json',required=True);i.add_argument('--evidence',action='append',default=[])
r=sp.add_parser('recover');r.add_argument('--incident-id',required=True);r.add_argument('--containment-id',required=True);r.add_argument('--checks-json',required=True);r.add_argument('--authorization',required=True)
v=sp.add_parser('verify');v.add_argument('--incident-id')
a=ap.parse_args()
try:
 e=envfile(a.env);policy=load_json(e['PAG_M9_POLICY']);rv=RecoveryVerifier(e['PAG_M9_RECOVERY_PUBLIC_KEY'],max_ttl=policy['recovery']['authorization_ttl_max_seconds']);ru=RecoveryUseStore(Path(e['PAG_M9_RUNTIME_ROOT'])/'recovery/recovery-uses.jsonl');ops=SecurityOperations(e['PAG_M9_RUNTIME_ROOT'],policy,rv,ru)
 if a.cmd=='ingest':out=ops.ingest(json.loads(a.event_json),a.evidence)
 elif a.cmd=='recover':out=ops.recover(a.incident_id,a.containment_id,json.loads(a.checks_json),from_dict(json.load(open(a.authorization))))
 else:
  ok,detail=ops.siem.verify();io,idet=ops.incidents.verify();co,cdet=ops.containment.verify();out={'siem_ok':ok,'siem_detail':detail,'incident_journal_ok':io,'incident_journal_detail':idet,'containment_journal_ok':co,'containment_journal_detail':cdet}
  if a.incident_id:
   eok,ed=ops.evidence.verify(a.incident_id);out.update({'evidence_ok':eok,'evidence_detail':ed})
 print(json.dumps({'ok':True,'result':out},indent=2))
except Exception as exc:
 print(json.dumps({'ok':False,'stage':a.cmd,'reason':str(exc)},indent=2));raise SystemExit(2)
