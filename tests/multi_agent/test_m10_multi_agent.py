import json,time
from pathlib import Path
import pytest
from portable_ai_governance.multi_agent.contracts import validate_case,ContractError,validate_envelope
from portable_ai_governance.multi_agent.agents import SpecialistAgent,ControlAgent,AssuranceAgent
from portable_ai_governance.multi_agent.workflow import GovernanceSupervisor,WorkflowError
from portable_ai_governance.multi_agent.approval import WorkflowDecisionGrant,DecisionIssuer,DecisionVerifier,to_dict,DecisionUseStore,WorkflowDecisionError
from portable_ai_governance.multi_agent.common import sha256_obj,write_json
from portable_ai_governance.multi_agent.store import WorkflowJournal
from portable_ai_governance.multi_agent.runtime import evaluate_multi_agent
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def case(evidence=True):
 ev=['evidence:a'] if evidence else []
 return {'case_id':'case-001','system_id':'sys-001','risk_signals':[{'id':'r1','severity':'high','summary':'risk','evidence_refs':ev}], 'threat_signals':[{'id':'t1','severity':'critical','summary':'threat','evidence_refs':['evidence:t']}], 'privacy_signals':[{'id':'p1','severity':'medium','summary':'privacy','evidence_refs':['evidence:p']}]}
def policy():return {'version':'0.10.0','side_effect_authority':False,'direct_agent_delegation':False,'m8_side_effect_boundary':True,'m9_secops_boundary':True,'budgets':{'max_agent_invocations':6,'max_total_signals':48,'max_findings_per_specialist':16,'max_workflow_output_bytes':262144},'human_decision':{'required':True,'reviewers':['HUMAN-GOVERNANCE-REVIEWER-001'],'ttl_default_seconds':1800,'ttl_max_seconds':1800,'clock_skew_seconds':60}}
def topology():return {'fixed_topology':True,'direct_peer_calls':False,'agents':{'GOVERNANCE-SUPERVISOR-001':{},'RISK-AGENT-001':{},'THREAT-AGENT-001':{},'PRIVACY-AGENT-001':{},'CONTROL-AGENT-001':{},'ASSURANCE-AGENT-001':{}}}
def keys(tmp_path):
 priv=tmp_path/'priv.pem';pub=tmp_path/'pub.pem';generate_ed25519_keypair(priv,pub);return priv,pub
def sup(tmp_path):
 priv,pub=keys(tmp_path);return GovernanceSupervisor(policy(),topology(),tmp_path/'runtime',pub),priv,pub

def test_case_contract_valid():assert validate_case(case())['case_id']=='case-001'
def test_case_contract_rejects_duplicate_signal():
 c=case();c['risk_signals'].append(dict(c['risk_signals'][0]))
 with pytest.raises(ContractError):validate_case(c)
def test_specialists_emit_typed_handoffs():
 for cat,aid in [('risk','RISK-AGENT-001'),('threat','THREAT-AGENT-001'),('privacy','PRIVACY-AGENT-001')]:
  e=SpecialistAgent(cat).analyze(case());assert e['agent_id']==aid;validate_envelope(e,case_id='case-001')
def test_handoff_tamper_detected():
 e=SpecialistAgent('risk').analyze(case());e['output']['findings'][0]['summary']='tamper'
 with pytest.raises(ContractError):validate_envelope(e)
def test_control_agent_maps_controls_and_no_side_effect():
 s=[SpecialistAgent(x).analyze(case()) for x in ('risk','threat','privacy')];e=ControlAgent().synthesize('case-001',s);assert all(not r['side_effect_requested'] for r in e['output']['recommendations']);assert 'AIS-ACTION-APPROVAL-001' in e['output']['recommendations'][1]['control_ids']
def test_assurance_ready_with_evidence():
 s=[SpecialistAgent(x).analyze(case()) for x in ('risk','threat','privacy')];c=ControlAgent().synthesize('case-001',s);a=AssuranceAgent().assess('case-001',s,c);assert a['output']['ready_for_human_approval'] is True
def test_assurance_blocks_missing_evidence():
 s=[SpecialistAgent(x).analyze(case(False)) for x in ('risk','threat','privacy')];c=ControlAgent().synthesize('case-001',s);a=AssuranceAgent().assess('case-001',s,c);assert a['output']['ready_for_human_approval'] is False;assert a['output']['gaps']
def test_supervisor_full_analysis(tmp_path):
 s,_,_=sup(tmp_path);r=s.analyze(case());assert r['status']=='pending-human-approval';assert r['proposal']['side_effect_authority'] is False;assert s.journal.verify()
def test_supervisor_signal_budget(tmp_path):
 s,_,_=sup(tmp_path);c=case();sig={'id':'x','severity':'low','summary':'x','evidence_refs':['e']};c['risk_signals']=[dict(sig,id=f'r{i}') for i in range(49)]
 with pytest.raises(WorkflowError):s.analyze(c)
def test_topology_rejects_peer_calls(tmp_path):
 priv,pub=keys(tmp_path);t=topology();t['direct_peer_calls']=True
 with pytest.raises(WorkflowError):GovernanceSupervisor(policy(),t,tmp_path/'r',pub)
def test_human_approve_finalize(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());n=int(time.time());g=WorkflowDecisionGrant('d1',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1);doc=to_dict(g,DecisionIssuer(priv).sign(g));out=s.finalize(r,doc);assert out['status']=='approved';assert out['side_effect_authority'] is False
def test_human_reject_finalize(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());n=int(time.time());g=WorkflowDecisionGrant('d2',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','reject',n,n+600,1);out=s.finalize(r,to_dict(g,DecisionIssuer(priv).sign(g)));assert out['status']=='rejected'
def test_decision_replay_rejected(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());n=int(time.time());g=WorkflowDecisionGrant('d3',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1);doc=to_dict(g,DecisionIssuer(priv).sign(g));s.finalize(r,doc)
 with pytest.raises(WorkflowDecisionError):s.finalize(r,doc)
def test_unauthorized_reviewer_rejected(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());n=int(time.time());g=WorkflowDecisionGrant('d4',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'OTHER','approve',n,n+600,1)
 with pytest.raises(WorkflowDecisionError):s.finalize(r,to_dict(g,DecisionIssuer(priv).sign(g)))
def test_decision_binding_mismatch(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());n=int(time.time());g=WorkflowDecisionGrant('d5',r['workflow_id'],'0'*64,r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1)
 with pytest.raises(WorkflowDecisionError):s.finalize(r,to_dict(g,DecisionIssuer(priv).sign(g)))
def test_approval_blocked_when_assurance_not_ready(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case(False));assert r['status']=='blocked';n=int(time.time());g=WorkflowDecisionGrant('d6',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1)
 with pytest.raises(WorkflowDecisionError):s.finalize(r,to_dict(g,DecisionIssuer(priv).sign(g)))
def test_workflow_result_tamper_rejected(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());r['proposal']['system_id']='tampered';n=int(time.time());g=WorkflowDecisionGrant('d7',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1)
 with pytest.raises(WorkflowError):s.finalize(r,to_dict(g,DecisionIssuer(priv).sign(g)))
def test_journal_tamper_detected(tmp_path):
 j=WorkflowJournal(tmp_path/'j.jsonl');j.append('w','a',{});assert j.verify();p=tmp_path/'j.jsonl';d=json.loads(p.read_text());d['event']='x';p.write_text(json.dumps(d)+'\n');assert not j.verify()
def test_decision_expiry_and_future(tmp_path):
 priv,pub=keys(tmp_path);v=DecisionVerifier(pub,1800,60);n=int(time.time());g=WorkflowDecisionGrant('d','w','0'*64,'1'*64,'HUMAN-GOVERNANCE-REVIEWER-001','approve',n-1000,n-1,1);sig=DecisionIssuer(priv).sign(g)
 with pytest.raises(WorkflowDecisionError):v.verify(g,sig,now=n)
 g2=WorkflowDecisionGrant('d2','w','0'*64,'1'*64,'HUMAN-GOVERNANCE-REVIEWER-001','approve',n+1000,n+1100,1);sig2=DecisionIssuer(priv).sign(g2)
 with pytest.raises(WorkflowDecisionError):v.verify(g2,sig2,now=n)
def test_runtime_valid_and_m9_drift(tmp_path):
 m9=tmp_path/'m9.json';m9.write_text('{}');pol=tmp_path/'multi-agent-policy.json';top=tmp_path/'multi-agent-topology.json';decpriv=tmp_path/'dpriv.pem';decpub=tmp_path/'workflow-decision-public.pem';generate_ed25519_keypair(decpriv,decpub);write_json(pol,policy());write_json(top,{**topology(),'version':'0.10.0','flow':[],'handoff_schema':'pag-m10-agent-handoff-v1'});sp=tmp_path/'spriv.pem';pub=tmp_path/'signing-public.pem';generate_ed25519_keypair(sp,pub);from portable_ai_governance.multi_agent.common import sha256_file
 man=tmp_path/'multi-agent-manifest.json';write_json(man,{'version':'0.10.0','m9_manifest_sha256':sha256_file(m9),'artifacts':{'multi-agent-policy.json':sha256_file(pol),'multi-agent-topology.json':sha256_file(top),'workflow-decision-public.pem':sha256_file(decpub)}});sig=tmp_path/'multi-agent-manifest.json.sig';sign_blob(man,sp,sig)
 env={'PAG_M10_ROOT':str(tmp_path),'PAG_M10_MANIFEST':str(man),'PAG_M10_MANIFEST_SIG':str(sig),'PAG_M10_PUBLIC_KEY':str(pub),'PAG_M10_POLICY':str(pol),'PAG_M10_TOPOLOGY':str(top),'PAG_M10_DECISION_PUBLIC_KEY':str(decpub),'PAG_M9_MANIFEST':str(m9),'PAG_M10_RUNTIME_ROOT':str(tmp_path/'runtime')};assert evaluate_multi_agent(env).ok;m9.write_text('{"drift":1}');assert not evaluate_multi_agent(env).ok

def test_specialist_finding_budget(tmp_path):
 s,_,_=sup(tmp_path);c=case();sig={'id':'x','severity':'low','summary':'x','evidence_refs':['e']};c['risk_signals']=[dict(sig,id=f'r{i}') for i in range(17)]
 with pytest.raises(WorkflowError,match='specialist finding budget'):s.analyze(c)

def test_assurance_digest_field_tamper_rejected(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());r['assurance_sha256']='0'*64;n=int(time.time());g=WorkflowDecisionGrant('d8',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1)
 with pytest.raises(WorkflowError,match='assurance digest'):s.finalize(r,to_dict(g,DecisionIssuer(priv).sign(g)))

def test_agent_invocation_budget_must_fit_fixed_topology(tmp_path):
 p=policy();p['budgets']['max_agent_invocations']=5;priv,pub=keys(tmp_path);s=GovernanceSupervisor(p,topology(),tmp_path/'r',pub)
 with pytest.raises(WorkflowError,match='agent-invocation budget'):s.analyze(case())

def test_workflow_cannot_be_finalized_twice_with_different_decisions(tmp_path):
 s,priv,_=sup(tmp_path);r=s.analyze(case());n=int(time.time())
 g1=WorkflowDecisionGrant('unique-1',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1)
 s.finalize(r,to_dict(g1,DecisionIssuer(priv).sign(g1)))
 g2=WorkflowDecisionGrant('unique-2',r['workflow_id'],r['proposal_sha256'],r['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','reject',n,n+600,1)
 with pytest.raises(WorkflowDecisionError,match='workflow already finalized'):s.finalize(r,to_dict(g2,DecisionIssuer(priv).sign(g2)))

def test_output_budget_enforced(tmp_path):
 p=policy();p['budgets']['max_workflow_output_bytes']=100;priv,pub=keys(tmp_path);s=GovernanceSupervisor(p,topology(),tmp_path/'r',pub)
 with pytest.raises(WorkflowError,match='workflow output budget'):s.analyze(case())
