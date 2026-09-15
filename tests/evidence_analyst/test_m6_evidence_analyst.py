import json,os,subprocess,sys
from pathlib import Path
import pytest
from portable_ai_governance.evidence_analyst.policy import require_agent_policy,AgentPolicyError
from portable_ai_governance.evidence_analyst.agent import EvidenceAnalyst,AgentRequest,AgentExecutionError
from portable_ai_governance.evidence_analyst.catalog import require_catalog,EvidenceCatalogError

def policy():
 return {'agent_id':'EVIDENCE-ANALYST-001','mode':'read-only','permissions':{'tools':['evidence.list','evidence.read','evidence.verify'],'deny':['write','append','delete','execute','shell','network','policy.modify','risk.accept','exception.approve','compliance.certify','tool.side_effect','agent.delegate']},'budget':{'max_steps':4,'max_tool_calls':3,'max_output_chars':1024},'limits':{'max_read_bytes':4096},'decision_boundaries':{k:'deterministic-control-plane' for k in ['security_boundary','approval_boundary','risk_acceptance_boundary','compliance_boundary']}}
def test_policy_read_only(): assert 'read-only' in require_agent_policy(policy())
def test_policy_rejects_side_effect_tool():
 p=policy(); p['permissions']['tools'].append('shell')
 with pytest.raises(AgentPolicyError): require_agent_policy(p)
def test_policy_rejects_missing_risk_deny():
 p=policy(); p['permissions']['deny'].remove('risk.accept')
 with pytest.raises(AgentPolicyError): require_agent_policy(p)
def test_agent_rejects_write(tmp_path):
 ev=tmp_path/'evidence'; ev.mkdir(); f=ev/'x.json'; f.write_text('{}')
 import hashlib
 dig=hashlib.sha256(f.read_bytes()).hexdigest(); cat=tmp_path/'cat.json'; cat.write_text(json.dumps({'entries':[{'evidence_id':'x','path':'x.json','sha256':dig,'access':'read-only'}]})); pol=tmp_path/'pol.json'; pol.write_text(json.dumps(policy()))
 a=EvidenceAnalyst(pol,cat,ev)
 with pytest.raises(AgentExecutionError): a.run(AgentRequest('write','x'))
def test_catalog_rejects_escape(tmp_path):
 ev=tmp_path/'evidence'; ev.mkdir(); cat=tmp_path/'cat.json'; cat.write_text(json.dumps({'entries':[{'evidence_id':'x','path':'../x','sha256':'0'*64,'access':'read-only'}]}))
 with pytest.raises(EvidenceCatalogError): require_catalog(cat,ev)
def test_dependency_preflight():
 root=Path(__file__).resolve().parents[2]; env=dict(os.environ); env.pop('PYTHONPATH',None)
 r=subprocess.run(['bash',str(root/'scripts/m6/preflight_dependencies.sh')],cwd=root,env=env,text=True,capture_output=True)
 assert r.returncode==0,r.stdout+r.stderr
 assert 'M6 DEPENDENCY PREFLIGHT: PASS' in r.stdout
