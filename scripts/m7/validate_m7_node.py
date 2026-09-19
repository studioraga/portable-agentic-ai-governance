#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.tool_agent.runtime import evaluate_tool_agent

def load_env(path):
    e={}
    for line in Path(path).read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            k,v=line.split('=',1); e[k]=v
    return e
if __name__=='__main__':
    e=load_env(sys.argv[1]); r=evaluate_tool_agent(e); print(json.dumps({'ok':r.ok,'checks':[{'name':n,'ok':o,'detail':d} for n,o,d in r.checks]},indent=2)); raise SystemExit(0 if r.ok else 2)
