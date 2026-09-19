#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.tool_agent.common import load_json
from portable_ai_governance.tool_agent.runtime import require_tool_agent
from portable_ai_governance.tool_agent.registry import ToolRegistry
from portable_ai_governance.tool_agent.authorization import build_tool_authorization
from portable_ai_governance.tool_agent.executors import evidence_handlers
from portable_ai_governance.tool_agent.broker import ToolBroker,ToolCall,ToolCallDenied
from portable_ai_governance.kernel.budgets import RunBudget
from portable_ai_governance.kernel.types import Principal
from portable_ai_governance.security.policy_adapter import LocalPolicyAdapter
from portable_ai_governance.security.secrets import FileSecretProvider
from portable_ai_governance.security.audit import SecurityAuditLog

def envfile(path):
    e={}
    for line in Path(path).read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            k,v=line.split('=',1); e[k]=v
    return e

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--m2-env',required=True); ap.add_argument('--m6-env',required=True); ap.add_argument('--m7-env',required=True); ap.add_argument('--tool',required=True,choices=['evidence.metadata','evidence.verify','evidence.summarize']); ap.add_argument('--evidence-id',required=True); ap.add_argument('--run-id',default='m7-smoke'); ap.add_argument('--call-id',default='call-1'); a=ap.parse_args()
    m2,m6,m7=envfile(a.m2_env),envfile(a.m6_env),envfile(a.m7_env); require_tool_agent(m7)
    policy=load_json(m7['PAG_M7_AGENT_POLICY']); pr=policy['principal']; principal=Principal(pr['principal_id'],tuple(pr['roles']),dict(pr.get('attributes',{})))
    registry=ToolRegistry(m7['PAG_M7_TOOL_REGISTRY']); auth=build_tool_authorization(m7['PAG_M7_AUTHORIZATION_RULES']); pad=LocalPolicyAdapter(Path(m2['PAG_POLICY_CATALOG']))
    budget=RunBudget(max_steps=int(policy['budget']['max_steps']),max_tool_calls=int(policy['budget']['max_tool_calls']))
    secret=FileSecretProvider(m2['PAG_SECRETS_DIR']).get('audit_signing')
    audit_path=Path(m2['PAG_SECURITY_AUDIT_LOG']).parent/'m7-tool-audit.jsonl'; audit_path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    audit=SecurityAuditLog(audit_path,secret,key_id='m7-tool-audit-v1')
    handlers=evidence_handlers(m6['PAG_M6_EVIDENCE_CATALOG'],m6['PAG_M6_EVIDENCE_ROOT'])
    broker=ToolBroker(registry=registry,principal=principal,authorization=auth,policy_adapter=pad,budget=budget,audit=audit,handlers=handlers)
    try:
        r=broker.invoke(ToolCall(a.run_id,a.call_id,a.tool,{'evidence_id':a.evidence_id}))
        print(json.dumps({'ok':r.ok,'tool_name':r.tool_name,'output':r.output,'audit_refs':r.audit_refs,'budget':{'steps':r.budget_steps,'tool_calls':r.budget_tool_calls}},indent=2))
    except ToolCallDenied as ex:
        print(json.dumps({'ok':False,'stage':ex.stage,'reason':ex.reason,'audit_ref':ex.audit_ref},indent=2)); raise SystemExit(2)
if __name__=='__main__': main()
