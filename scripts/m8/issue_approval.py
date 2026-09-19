#!/usr/bin/env python3
import argparse, json, time, uuid, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.action_agent.approval import ApprovalIssuer,ApprovalGrant,ApprovalRequest,SignedApproval,request_sha256,signed_approval_to_dict
from portable_ai_governance.action_agent.common import canonical_json_bytes,sha256_bytes,write_private_json,load_json
from portable_ai_governance.action_agent.runtime import require_action_agent
from portable_ai_governance.security.secrets import FileSecretProvider
from portable_ai_governance.security.audit import SecurityAuditLog,SecurityEvent

def envfile(p):
    e={}
    for line in Path(p).read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            k,v=line.split('=',1); e[k]=v
    return e

if __name__=='__main__':
    ap=argparse.ArgumentParser(description='Operator approval issuer; never exposed to ACTION-AGENT-001')
    ap.add_argument('--m2-env',required=True); ap.add_argument('--m8-env',required=True); ap.add_argument('--approval-private-key',required=True)
    ap.add_argument('--tool',required=True,choices=['incident.create','rerun.request','ticket.create','model.quarantine'])
    ap.add_argument('--arguments-json',required=True); ap.add_argument('--run-id',required=True); ap.add_argument('--call-id',required=True)
    ap.add_argument('--requester',default='ACTION-AGENT-001'); ap.add_argument('--approver',required=True); ap.add_argument('--ttl-seconds',type=int,default=None); ap.add_argument('--out',required=True)
    a=ap.parse_args(); m2,m8=envfile(a.m2_env),envfile(a.m8_env); require_action_agent(m8)
    if a.requester==a.approver: raise SystemExit('FAIL: self-approval prohibited')
    policy=load_json(m8['PAG_M8_AGENT_POLICY']); ttl_max=int(policy['approval_ttl_max_seconds']); ttl_default=int(policy.get('approval_ttl_default_seconds',ttl_max)); ttl=ttl_default if a.ttl_seconds is None else int(a.ttl_seconds)
    if not 60<=ttl<=ttl_max: raise SystemExit(f'FAIL: ttl must be 60..{ttl_max} seconds per signed M8 policy')
    authorities=load_json(m8['PAG_M8_APPROVAL_AUTHORITIES']); allowed={x['principal_id'] for x in authorities.get('approvers',[]) if 'human_approver' in x.get('roles',[])}
    if a.approver not in allowed: raise SystemExit('FAIL: approver is not in signed M8 approval authorities')
    args=json.loads(a.arguments_json); argsha=sha256_bytes(canonical_json_bytes(args)); resource=f'action://{a.tool}'; req=ApprovalRequest(f'{a.run_id}:{a.call_id}',a.run_id,a.call_id,a.tool,resource,a.requester,argsha); now=int(time.time())
    g=ApprovalGrant(str(uuid.uuid4()),request_sha256(req),a.tool,resource,a.requester,a.approver,argsha,now,now+ttl,1)
    sec=FileSecretProvider(m2['PAG_SECRETS_DIR']); issuer=ApprovalIssuer(a.approval_private_key); signed=SignedApproval(g,issuer.sign(g)); write_private_json(a.out,signed_approval_to_dict(signed))
    audit=SecurityAuditLog(Path(m2['PAG_SECURITY_AUDIT_LOG']).parent/'m8-action-audit.jsonl',sec.get('audit_signing'),key_id='m8-action-audit-v1')
    ref=audit.record(SecurityEvent(event_type='agent.action.approval',decision='allow',principal_id=a.approver,action='approval.issue',resource=resource,reason='independent approval issued',run_id=a.run_id,attributes={'approval_id':g.approval_id,'call_id':a.call_id,'requester':a.requester,'request_sha256':g.request_sha256,'arguments_sha256':g.arguments_sha256,'expires_at':g.expires_at}))
    print(json.dumps({'ok':True,'approval_id':g.approval_id,'approver':g.approver,'expires_at':g.expires_at,'ttl_seconds':ttl,'audit_ref':ref,'out':str(Path(a.out))},indent=2))
