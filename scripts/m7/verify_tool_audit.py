#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.security.secrets import FileSecretProvider
from portable_ai_governance.security.audit import SecurityAuditLog

def envfile(path):
    e={}
    for line in Path(path).read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            k,v=line.split('=',1); e[k]=v
    return e
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--m2-env',required=True); a=ap.parse_args(); e=envfile(a.m2_env)
    key=FileSecretProvider(e['PAG_SECRETS_DIR']).get('audit_signing'); path=Path(e['PAG_SECURITY_AUDIT_LOG']).parent/'m7-tool-audit.jsonl'
    audit=SecurityAuditLog(path,key,key_id='m7-tool-audit-v1'); ok,detail=audit.verify(); print(json.dumps({'ok':ok,'audit_path':str(path),'detail':detail},indent=2)); raise SystemExit(0 if ok else 2)
