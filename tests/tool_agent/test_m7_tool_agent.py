from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
import pytest
from portable_ai_governance.tool_agent.schema import validate_schema,ToolSchemaError
from portable_ai_governance.tool_agent.registry import ToolRegistry,ToolRegistryError
from portable_ai_governance.tool_agent.authorization import build_tool_authorization
from portable_ai_governance.tool_agent.broker import ToolBroker,ToolCall,ToolCallDenied
from portable_ai_governance.kernel.budgets import RunBudget
from portable_ai_governance.kernel.types import Principal
from portable_ai_governance.security.policy_adapter import LocalPolicyAdapter
from portable_ai_governance.security.audit import SecurityAuditLog

ROOT=Path(__file__).resolve().parents[2]

def write(p,v): p.write_text(json.dumps(v)); return p

def fixture_files(tmp_path, *, side_effecting=False, control_enabled=True):
    schema={'type':'object','properties':{'evidence_id':{'type':'string','minLength':1,'maxLength':256}},'required':['evidence_id'],'additionalProperties':False}
    out={'type':'object','properties':{'evidence_id':{'type':'string'},'ok':{'type':'boolean'}},'required':['evidence_id','ok'],'additionalProperties':False}
    reg={'version':'0.7.0','default':'deny','tools':[{'name':'evidence.verify','version':'1.0.0','action':'tool.invoke','resource':'tool://evidence.verify','policy_control_id':'AIS-TOOL-POLICY-001','side_effecting':side_effecting,'input_schema':schema,'output_schema':out}]}
    auth={'version':'0.7.0','default':'deny','rules':[{'action':'tool.invoke','roles':['tool_agent'],'resource_prefix':'tool://evidence.verify','effect':'allow','principal_attributes':{'agent_class':['bounded-tool-agent']},'resource_attributes':{'side_effecting':['false']}}]}
    controls={'catalog_version':'0.7.0','controls':[{'control_id':'AIS-TOOL-POLICY-001','title':'test','enabled':control_enabled,'required_roles':['tool_agent'],'predicates':{'tool_gateway':True,'side_effecting':False},'approval_required':False,'failure_action':'block'}]}
    return write(tmp_path/'registry.json',reg),write(tmp_path/'auth.json',auth),write(tmp_path/'controls.json',controls)

def broker(tmp_path, *, principal=None, budget=None, control_enabled=True, audit=None, handler=None):
    reg,auth,controls=fixture_files(tmp_path,control_enabled=control_enabled)
    principal=principal or Principal('TOOL-ANALYST-001',('tool_agent',),{'agent_class':'bounded-tool-agent'})
    audit=audit or SecurityAuditLog(tmp_path/'audit.jsonl',b'a'*32,'test')
    handler=handler or (lambda a:{'evidence_id':a['evidence_id'],'ok':True})
    return ToolBroker(registry=ToolRegistry(reg),principal=principal,authorization=build_tool_authorization(auth),policy_adapter=LocalPolicyAdapter(controls),budget=budget or RunBudget(max_steps=3,max_tool_calls=3),audit=audit,handlers={'evidence.verify':handler}),audit

def test_positive_pipeline_and_signed_audit(tmp_path):
    b,a=broker(tmp_path); r=b.invoke(ToolCall('run1','c1','evidence.verify',{'evidence_id':'m5:x'}))
    assert r.ok and r.budget_steps==1 and r.budget_tool_calls==1 and len(r.audit_refs)==2
    assert a.verify()[0]

def test_input_schema_rejects_extra_property_and_audits(tmp_path):
    b,a=broker(tmp_path)
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','evidence.verify',{'evidence_id':'x','write':True}))
    assert x.value.stage=='schema' and a.verify()[0]

def test_authorization_denies_wrong_role(tmp_path):
    p=Principal('bad',('viewer',),{'agent_class':'bounded-tool-agent'}); b,a=broker(tmp_path,principal=p)
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','evidence.verify',{'evidence_id':'x'}))
    assert x.value.stage=='authorization' and a.verify()[0]

def test_policy_denial(tmp_path):
    b,a=broker(tmp_path,control_enabled=False)
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','evidence.verify',{'evidence_id':'x'}))
    assert x.value.stage=='policy' and a.verify()[0]

def test_budget_denial(tmp_path):
    b,a=broker(tmp_path,budget=RunBudget(max_steps=1,max_tool_calls=0))
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','evidence.verify',{'evidence_id':'x'}))
    assert x.value.stage=='budget' and a.verify()[0]

def test_preexecution_audit_failure_prevents_executor(tmp_path):
    class BadAudit:
        def record(self,event): raise OSError('audit unavailable')
    calls=[]; b,_=broker(tmp_path,audit=BadAudit(),handler=lambda a:(calls.append(1) or {'evidence_id':'x','ok':True}))
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','evidence.verify',{'evidence_id':'x'}))
    assert x.value.stage=='audit' and calls==[]

def test_output_schema_is_mandatory(tmp_path):
    b,a=broker(tmp_path,handler=lambda a:{'evidence_id':a['evidence_id']})
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','evidence.verify',{'evidence_id':'x'}))
    assert x.value.stage=='output_schema' and a.verify()[0]

def test_unknown_tool_denied_and_audited(tmp_path):
    b,a=broker(tmp_path)
    with pytest.raises(ToolCallDenied) as x: b.invoke(ToolCall('run','c','missing.tool',{}))
    assert x.value.stage=='schema' and a.verify()[0]

def test_registry_rejects_side_effecting_tool(tmp_path):
    reg,_,_=fixture_files(tmp_path,side_effecting=True)
    with pytest.raises(ToolRegistryError): ToolRegistry(reg)

def test_schema_validator_limits_types():
    with pytest.raises(ToolSchemaError): validate_schema({'type':'object','properties':{'n':{'type':'integer'}},'required':['n'],'additionalProperties':False},{'n':'1'})

def test_m7_builder_and_static_validator(tmp_path):
    m6=tmp_path/'m6'; m6.mkdir(); (m6/'evidence-analyst-manifest.json').write_text('{}')
    out=tmp_path/'m7'
    subprocess.run([sys.executable,str(ROOT/'scripts/m7/build_m7_material.py'),'--m6-material',str(m6),'--out',str(out)],check=True,cwd=ROOT)
    env=tmp_path/'m7.env'
    env.write_text('\n'.join([f'PAG_M7_ROOT={out}',f'PAG_M7_MANIFEST={out}/tool-agent-manifest.json',f'PAG_M7_MANIFEST_SIG={out}/tool-agent-manifest.json.sig',f'PAG_M7_PUBLIC_KEY={out}/signing-public.pem',f'PAG_M7_AGENT_POLICY={out}/tool-agent-policy.json',f'PAG_M7_TOOL_REGISTRY={out}/typed-tool-registry.json',f'PAG_M7_AUTHORIZATION_RULES={out}/tool-authorization-rules.json',f'PAG_M6_MANIFEST={m6}/evidence-analyst-manifest.json']))
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m7/validate_m7_node.py'),str(env)],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==0 and '"ok": true' in r.stdout

def test_tool_using_agent_reuses_broker_budget(tmp_path):
    from portable_ai_governance.tool_agent.agent import ToolUsingAgent, ToolPlan
    b,_=broker(tmp_path,budget=RunBudget(max_steps=2,max_tool_calls=2))
    agent=ToolUsingAgent(b,max_plan_calls=2)
    plan=ToolPlan('run',(
        ToolCall('run','c1','evidence.verify',{'evidence_id':'x'}),
        ToolCall('run','c2','evidence.verify',{'evidence_id':'y'}),
    ))
    out=agent.run_plan(plan)
    assert len(out)==2 and out[-1].budget_tool_calls==2

def test_release_chain_verifier_and_freeze_marker(tmp_path):
    import hashlib
    m4=tmp_path/'m4'; m5=tmp_path/'m5'; m6=tmp_path/'m6'; m7=tmp_path/'m7'
    for d in (m4,m5,m6,m7): d.mkdir()
    p4=m4/'ai-security-manifest.json'; p4.write_text('{"m4":1}')
    h4=hashlib.sha256(p4.read_bytes()).hexdigest()
    p5=m5/'compliance-risk-manifest.json'; p5.write_text(json.dumps({'m4_manifest_sha256':h4}))
    h5=hashlib.sha256(p5.read_bytes()).hexdigest()
    p6=m6/'evidence-analyst-manifest.json'; p6.write_text(json.dumps({'m5_manifest_sha256':h5}))
    h6=hashlib.sha256(p6.read_bytes()).hexdigest()
    p7=m7/'tool-agent-manifest.json'; p7.write_text(json.dumps({'m6_manifest_sha256':h6}))
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m7/verify_release_chain.py'),'--m4-material',str(m4),'--m5-material',str(m5),'--m6-material',str(m6),'--m7-material',str(m7),'--freeze-m5'],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==0 and 'PASS: M4 -> M5 -> M6 -> M7 release chain coherent' in r.stdout
    assert (m5/'.pag-downstream-bound.json').is_file()


def test_release_chain_verifier_rejects_m5_m6_drift(tmp_path):
    import hashlib
    m4=tmp_path/'m4'; m5=tmp_path/'m5'; m6=tmp_path/'m6'; m7=tmp_path/'m7'
    for d in (m4,m5,m6,m7): d.mkdir()
    p4=m4/'ai-security-manifest.json'; p4.write_text('{"m4":1}')
    h4=hashlib.sha256(p4.read_bytes()).hexdigest()
    p5=m5/'compliance-risk-manifest.json'; p5.write_text(json.dumps({'m4_manifest_sha256':h4}))
    p6=m6/'evidence-analyst-manifest.json'; p6.write_text(json.dumps({'m5_manifest_sha256':'0'*64}))
    h6=hashlib.sha256(p6.read_bytes()).hexdigest()
    (m7/'tool-agent-manifest.json').write_text(json.dumps({'m6_manifest_sha256':h6}))
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m7/verify_release_chain.py'),'--m4-material',str(m4),'--m5-material',str(m5),'--m6-material',str(m6),'--m7-material',str(m7)],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode!=0 and 'release generation is not coherent' in (r.stdout+r.stderr)


def test_m5_refresh_refuses_downstream_bound_release(tmp_path):
    m4=tmp_path/'m4'; m5=tmp_path/'m5'; m4.mkdir(); m5.mkdir()
    (m5/'.pag-downstream-bound.json').write_text('{}')
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m5/refresh_continuous_controls.py'),'--m4-material',str(m4),'--m5-material',str(m5)],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode!=0 and 'downstream-bound/frozen' in (r.stdout+r.stderr)


def test_m5_builder_refuses_downstream_bound_release(tmp_path):
    m4=tmp_path/'m4'; m5=tmp_path/'m5'; m4.mkdir(); m5.mkdir()
    (m5/'.pag-downstream-bound.json').write_text('{}')
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m5/build_m5_material.py'),'--m4-material',str(m4),'--out',str(m5)],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode!=0 and 'downstream-bound/frozen' in (r.stdout+r.stderr)
