#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'src'
if str(SRC) not in sys.path:sys.path.insert(0,str(SRC))
from portable_ai_governance.action_agent.common import load_json
from portable_ai_governance.action_agent.runtime import require_action_agent
from portable_ai_governance.action_agent.registry import ActionRegistry
from portable_ai_governance.action_agent.authorization import build_action_authorization
from portable_ai_governance.action_agent.approval import ApprovalVerifier,ApprovalUseStore,signed_approval_from_dict,ApprovalError
from portable_ai_governance.action_agent.store import ActionStore,action_handlers
from portable_ai_governance.action_agent.broker import ActionBroker,ActionCall,ActionDenied
from portable_ai_governance.kernel.budgets import RunBudget
from portable_ai_governance.kernel.types import Principal
from portable_ai_governance.security.policy_adapter import LocalPolicyAdapter
from portable_ai_governance.security.secrets import FileSecretProvider
from portable_ai_governance.security.audit import SecurityAuditLog
def envfile(p):
 e={}
 for line in Path(p).read_text().splitlines():
  if line and not line.startswith('#') and '=' in line:k,v=line.split('=',1);e[k]=v
 return e
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--m2-env',required=True);ap.add_argument('--m8-env',required=True);ap.add_argument('--tool',required=True,choices=['incident.create','rerun.request','ticket.create','model.quarantine']);ap.add_argument('--arguments-json',required=True);ap.add_argument('--approval',required=True);ap.add_argument('--run-id',required=True);ap.add_argument('--call-id',required=True);a=ap.parse_args();m2,m8=envfile(a.m2_env),envfile(a.m8_env);require_action_agent(m8);policy=load_json(m8['PAG_M8_AGENT_POLICY']);pr=policy['principal'];principal=Principal(pr['principal_id'],tuple(pr['roles']),dict(pr.get('attributes',{})));reg=ActionRegistry(m8['PAG_M8_TOOL_REGISTRY']);auth=build_action_authorization(m8['PAG_M8_AUTHORIZATION_RULES']);pad=LocalPolicyAdapter(Path(m2['PAG_POLICY_CATALOG']));budget=RunBudget(max_steps=int(policy['budget']['max_steps']),max_tool_calls=int(policy['budget']['max_tool_calls']));sec=FileSecretProvider(m2['PAG_SECRETS_DIR']);audit=SecurityAuditLog(Path(m2['PAG_SECURITY_AUDIT_LOG']).parent/'m8-action-audit.jsonl',sec.get('audit_signing'),key_id='m8-action-audit-v1');authority=ApprovalVerifier(m8['PAG_M8_APPROVAL_PUBLIC_KEY'],max_ttl_seconds=int(policy['approval_ttl_max_seconds']),clock_skew_seconds=int(policy.get('approval_clock_skew_seconds',60)));root=Path(m8['PAG_M8_ACTION_ROOT']);uses=ApprovalUseStore(root/'approval-uses.jsonl');store=ActionStore(root/'effects');
 try:signed=signed_approval_from_dict(load_json(a.approval))
 except (ApprovalError,KeyError,TypeError,ValueError) as ex:
  print(json.dumps({'ok':False,'stage':'approval','reason':str(ex),'audit_ref':''},indent=2));raise SystemExit(2)
 handlers=action_handlers(store,lambda:signed.grant.approval_id);broker=ActionBroker(registry=reg,principal=principal,authorization=auth,policy_adapter=pad,budget=budget,audit=audit,approval_authority=authority,approval_store=uses,handlers=handlers,reconciliation=store.record_reconciliation)
 try:r=broker.invoke(ActionCall(a.run_id,a.call_id,a.tool,json.loads(a.arguments_json)),signed);print(json.dumps({'ok':r.ok,'tool_name':r.tool_name,'output':r.output,'approval_id':r.approval_id,'audit_refs':r.audit_refs,'budget':{'steps':r.budget_steps,'tool_calls':r.budget_tool_calls}},indent=2))
 except ActionDenied as ex:print(json.dumps({'ok':False,'stage':ex.stage,'reason':ex.reason,'audit_ref':ex.audit_ref,'effect_committed':ex.effect_committed,'action_id':ex.action_id},indent=2));raise SystemExit(2)
