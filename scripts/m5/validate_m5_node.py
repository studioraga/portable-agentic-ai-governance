#!/usr/bin/env python3
from __future__ import annotations
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.compliance_risk.runtime import evaluate_compliance_risk

def load_env(path):
    env=dict(os.environ)
    for raw in Path(path).read_text().splitlines():
        s=raw.strip()
        if not s or s.startswith('#') or '=' not in s: continue
        k,v=s.split('=',1); env[k]=v
    return env

def main():
    if len(sys.argv)!=2: raise SystemExit('usage: validate_m5_node.py <m5.env>')
    r=evaluate_compliance_risk(load_env(sys.argv[1])); print(json.dumps({'ok':r.ok,'checks':[{'name':n,'ok':o,'detail':d} for n,o,d in r.checks]},indent=2)); raise SystemExit(0 if r.ok else 2)
if __name__=='__main__': main()
