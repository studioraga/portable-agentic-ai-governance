#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.evidence_analyst.runtime import require_evidence_analyst
from portable_ai_governance.evidence_analyst.agent import EvidenceAnalyst,AgentRequest

def load_env(path):
    e=dict(os.environ)
    for line in Path(path).read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            k,v=line.split('=',1); e[k]=v
    return e
ap=argparse.ArgumentParser(); ap.add_argument('--env',required=True); ap.add_argument('--operation',required=True,choices=['evidence.list','evidence.metadata','evidence.read','evidence.verify','evidence.summarize']); ap.add_argument('--evidence-id'); a=ap.parse_args()
e=load_env(a.env); require_evidence_analyst(e); ag=EvidenceAnalyst(e['PAG_M6_AGENT_POLICY'],e['PAG_M6_EVIDENCE_CATALOG'],e['PAG_M6_EVIDENCE_ROOT']); r=ag.run(AgentRequest(a.operation,a.evidence_id)); out=json.dumps({'ok':r.ok,'operation':r.operation,'tool_calls':r.tool_calls,'result':r.result},indent=2); maxchars=int(json.load(open(e['PAG_M6_AGENT_POLICY']))['budget']['max_output_chars']); print(out[:maxchars])
