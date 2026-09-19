#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.multi_agent.runtime import evaluate_multi_agent
def envfile(p):
 d={}
 for l in Path(p).read_text().splitlines():
  if l and not l.startswith('#') and '=' in l:k,v=l.split('=',1);d[k]=v
 return d
r=evaluate_multi_agent(envfile(sys.argv[1]));print(json.dumps({'ok':r.ok,'checks':[{'name':n,'ok':o,'detail':d} for n,o,d in r.checks]},indent=2));raise SystemExit(0 if r.ok else 2)
