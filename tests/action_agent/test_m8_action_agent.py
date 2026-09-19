from __future__ import annotations
import json,time,subprocess,sys,hashlib
from pathlib import Path
import pytest
from portable_ai_governance.action_agent.approval import *
from portable_ai_governance.action_agent.registry import ActionRegistry
from portable_ai_governance.action_agent.authorization import build_action_authorization
from portable_ai_governance.action_agent.broker import ActionBroker,ActionCall,ActionDenied
from portable_ai_governance.action_agent.store import ActionStore,action_handlers
from portable_ai_governance.action_agent.common import canonical_json_bytes,sha256_bytes
from portable_ai_governance.kernel.budgets import RunBudget
from portable_ai_governance.kernel.types import Principal
from portable_ai_governance.security.policy_adapter import LocalPolicyAdapter
from portable_ai_governance.security.audit import SecurityAuditLog
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair
ROOT=Path(__file__).resolve().parents[2]
def wr(p,x):p.write_text(json.dumps(x));return p
def fixtures(t):
 generic={'type':'object','properties':{},'additionalProperties':True};incident={'type':'object','properties':{'title':{'type':'string','minLength':1},'severity':{'type':'string','enum':['low','medium','high','critical']}},'required':['title','severity'],'additionalProperties':False};out={'type':'object','additionalProperties':True};names=['incident.create','rerun.request','ticket.create','model.quarantine'];tools=[{'name':n,'version':'1','action':'action.execute','resource':f'action://{n}','policy_control_id':'AIS-ACTION-POLICY-001','side_effecting':True,'approval_required':True,'input_schema':incident if n=='incident.create' else generic,'output_schema':out} for n in names];reg=wr(t/'reg.json',{'version':'0.8.0','default':'deny','tools':tools});auth=wr(t/'auth.json',{'version':'0.8.0','default':'deny','rules':[{'action':'action.execute','roles':['action_agent'],'resource_prefix':f'action://{n}','effect':'allow','principal_attributes':{'agent_class':['approval-controlled-action-agent']},'resource_attributes':{'side_effecting':['true'],'approval_required':['true']}} for n in names]});ctrl=wr(t/'ctrl.json',{'catalog_version':'0.8.0','controls':[{'control_id':'AIS-ACTION-POLICY-001','title':'x','enabled':True,'required_roles':['action_agent'],'predicates':{'tool_gateway':True,'side_effecting':True,'approval_required':True},'approval_required':True,'failure_action':'block'}]});return reg,auth,ctrl
def make(t):
 reg,auth,ctrl=fixtures(t);priv=t/'approval-private.pem';pub=t/'approval-public.pem';generate_ed25519_keypair(priv,pub);holder={'id':''};store=ActionStore(t/'effects');b=ActionBroker(registry=ActionRegistry(reg),principal=Principal('ACTION-AGENT-001',('action_agent',),{'agent_class':'approval-controlled-action-agent'}),authorization=build_action_authorization(auth),policy_adapter=LocalPolicyAdapter(ctrl),budget=RunBudget(max_steps=4,max_tool_calls=4),audit=SecurityAuditLog(t/'audit.jsonl',b'a'*32,'m8-test'),approval_authority=ApprovalVerifier(pub),approval_store=ApprovalUseStore(t/'uses.jsonl'),handlers=action_handlers(store,lambda:holder['id']),reconciliation=store.record_reconciliation);return b,priv,holder
def grant(priv,c,approver='human-1',requester='ACTION-AGENT-001',ttl=300,aid='appr-1'):
 ah=sha256_bytes(canonical_json_bytes(c.arguments));req=ApprovalRequest(f'{c.run_id}:{c.call_id}',c.run_id,c.call_id,c.tool_name,f'action://{c.tool_name}',requester,ah);now=int(time.time());g=ApprovalGrant(aid,request_sha256(req),c.tool_name,f'action://{c.tool_name}',requester,approver,ah,now,now+ttl,1);return SignedApproval(g,ApprovalIssuer(priv).sign(g))
def test_approved_incident_side_effect_and_audit(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'GPU fault','severity':'high'});x=grant(k,c);h['id']=x.grant.approval_id;r=b.invoke(c,x);assert r.ok and len(r.audit_refs)==2 and r.output['status']=='open'
def test_self_approval_rejected(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c,approver='ACTION-AGENT-001');h['id']=x.grant.approval_id
 with pytest.raises(ActionDenied) as e:b.invoke(c,x)
 assert e.value.stage=='approval'
def test_argument_tamper_rejected(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c);h['id']=x.grant.approval_id
 with pytest.raises(ActionDenied) as e:b.invoke(ActionCall('r','c','incident.create',{'title':'changed','severity':'low'}),x)
 assert e.value.stage=='approval'
def test_expired_rejected(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c,ttl=-1);h['id']=x.grant.approval_id
 with pytest.raises(ActionDenied) as e:b.invoke(c,x)
 assert e.value.stage=='approval'
def test_replay_rejected(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c);h['id']=x.grant.approval_id;b.invoke(c,x)
 with pytest.raises(ActionDenied) as e:b.invoke(c,x)
 assert e.value.stage=='approval'
def test_bad_signature_rejected(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c);x=SignedApproval(x.grant,'0'*64);h['id']=x.grant.approval_id
 with pytest.raises(ActionDenied) as e:b.invoke(c,x)
 assert e.value.stage=='approval'
def test_audit_failure_prevents_effect(tmp_path):
 b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c);h['id']=x.grant.approval_id
 class Bad:
  def record(self,e):raise OSError('down')
 b.audit=Bad()
 with pytest.raises(ActionDenied) as e:b.invoke(c,x)
 assert e.value.stage=='audit' and not list((tmp_path/'effects').glob('*.jsonl'))
def test_builder_binds_m7(tmp_path):
 m7=tmp_path/'m7';m7.mkdir();(m7/'tool-agent-manifest.json').write_text('{}');out=tmp_path/'m8';subprocess.run([sys.executable,str(ROOT/'scripts/m8/build_m8_material.py'),'--m7-material',str(m7),'--out',str(out)],check=True,cwd=ROOT);assert json.loads((out/'action-agent-manifest.json').read_text())['m7_manifest_sha256']==hashlib.sha256((m7/'tool-agent-manifest.json').read_bytes()).hexdigest()
def test_registry_exact_four(tmp_path):
 reg,_,_=fixtures(tmp_path);r=ActionRegistry(reg);assert len(r.tools)==4 and all(x.approval_required for x in r.tools.values())

def test_signed_approval_envelope_schema_rejected(tmp_path):
    b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c)
    d=signed_approval_to_dict(x);d['schema']='wrong'
    with pytest.raises(ApprovalError): signed_approval_from_dict(d)

def test_future_dated_approval_rejected(tmp_path):
    _,priv,_=make(tmp_path);pub=tmp_path/'approval-public.pem'
    # make() generated the keypair at these paths
    now=int(time.time());g=ApprovalGrant('future','0'*64,'incident.create','action://incident.create','ACTION-AGENT-001','human-1','1'*64,now+120,now+300,1)
    s=SignedApproval(g,ApprovalIssuer(priv).sign(g))
    with pytest.raises(ApprovalError,match='future'):
        ApprovalVerifier(pub,clock_skew_seconds=30).verify(s,now=now)

def test_approval_ttl_policy_enforced(tmp_path):
    _,priv,_=make(tmp_path);pub=tmp_path/'approval-public.pem';now=int(time.time())
    g=ApprovalGrant('ttl','0'*64,'incident.create','action://incident.create','ACTION-AGENT-001','human-1','1'*64,now,now+301,1)
    s=SignedApproval(g,ApprovalIssuer(priv).sign(g))
    with pytest.raises(ApprovalError,match='TTL'):
        ApprovalVerifier(pub,max_ttl_seconds=300).verify(s,now=now)



def test_result_audit_failure_records_reconciliation(tmp_path):
    b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c);h['id']=x.grant.approval_id
    delegate=b.audit
    class FailSecond:
        def __init__(self): self.n=0
        def record(self,e):
            self.n+=1
            if self.n==2: raise OSError('result-audit-down')
            return delegate.record(e)
    b.audit=FailSecond()
    with pytest.raises(ActionDenied) as e: b.invoke(c,x)
    assert e.value.stage=='audit' and e.value.effect_committed and e.value.action_id==x.grant.approval_id
    assert (tmp_path/'effects'/'incidents.jsonl').is_file()
    rec=tmp_path/'effects'/'reconciliation.jsonl'
    assert rec.is_file() and x.grant.approval_id in rec.read_text()

def test_preexecution_audit_failure_consumes_approval_without_effect(tmp_path):
    b,k,h=make(tmp_path);c=ActionCall('r','c','incident.create',{'title':'x','severity':'low'});x=grant(k,c);h['id']=x.grant.approval_id
    class Bad:
        def record(self,e): raise OSError('down')
    b.audit=Bad()
    with pytest.raises(ActionDenied) as e: b.invoke(c,x)
    assert e.value.stage=='audit' and not e.value.effect_committed
    assert x.grant.approval_id in (tmp_path/'uses.jsonl').read_text()
    assert not list((tmp_path/'effects').glob('incidents.jsonl'))
