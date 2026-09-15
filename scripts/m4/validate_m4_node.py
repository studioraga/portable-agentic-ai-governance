#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.ai_security.runtime import evaluate_ai_security

def load_env(p):
    env={}
    for line in Path(p).read_text().splitlines():
        if line and not line.lstrip().startswith('#') and '=' in line:
            k,v=line.split('=',1); env[k]=v
    return env
def main():
    if len(sys.argv)!=2: raise SystemExit('usage: validate_m4_node.py <m4.env>')
    r=evaluate_ai_security(load_env(sys.argv[1])); print(json.dumps({'ok':r.ok,'checks':[{'name':n,'ok':o,'detail':d} for n,o,d in r.checks]},indent=2)); raise SystemExit(0 if r.ok else 2)
if __name__=='__main__': main()
