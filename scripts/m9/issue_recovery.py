#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.security_ops.recovery import RecoveryIssuer,to_dict
ap=argparse.ArgumentParser();ap.add_argument('--private-key',required=True);ap.add_argument('--incident-id',required=True);ap.add_argument('--containment-id',required=True);ap.add_argument('--operator',required=True);ap.add_argument('--checks-json',required=True);ap.add_argument('--ttl-seconds',type=int,default=900);ap.add_argument('--out',required=True);a=ap.parse_args();checks=json.loads(a.checks_json);x=RecoveryIssuer(a.private_key).issue(a.incident_id,a.containment_id,a.operator,checks,a.ttl_seconds);Path(a.out).write_text(json.dumps(to_dict(x),indent=2,sort_keys=True)+'\n');Path(a.out).chmod(0o600);print(json.dumps({'ok':True,'authorization_id':x.grant.authorization_id,'out':a.out},indent=2))
