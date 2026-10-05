import json
from pathlib import Path
import pytest
from portable_ai_governance.application_security.sast import scan_python
from portable_ai_governance.application_security.secrets import scan_text
from portable_ai_governance.application_security.iac_container import scan_container_text,scan_iac_text
from portable_ai_governance.application_security.api_security import evaluate_api_probes
from portable_ai_governance.application_security.fuzzing import evaluate_fuzz_result
from portable_ai_governance.application_security.pentest import validate_pentest_evidence,PenTestEvidenceError
from portable_ai_governance.application_security.reports import normalize_report,gate_reports
from portable_ai_governance.application_security.evaluation import evaluate_m27_policy
ROOT=Path(__file__).resolve().parents[2]
def J(p):return json.loads((ROOT/p).read_text())
def policy():return J('governance/enterprise/m27/appsec-policy.json')
def test_sast_detects_eval():assert scan_python('x=eval("1+1")','x.py')[0]['severity']=='high'
def test_sast_safe_code():assert scan_python('x=1+1','x.py')==[]
def test_secret_detects_private_key():assert scan_text('-----BEGIN PRIVATE KEY-----','x.txt')
def test_container_latest_rejected():assert scan_container_text('FROM ubuntu:latest\n','Dockerfile')[0]['rule']=='unpinned-latest'
def test_iac_world_open_admin_rejected():assert scan_iac_text('cidr=0.0.0.0/0 port=22','x.tf')
def test_api_negative_probes():
 probes=[{'probe':x,'accepted':False} for x in ['unauthenticated_access','invalid_method','oversized_payload','injection_string']];assert evaluate_api_probes(probes)['ok']
def test_api_accepted_injection_fails():
 probes=[{'probe':x,'accepted':x=='injection_string'} for x in ['unauthenticated_access','invalid_method','oversized_payload','injection_string']];assert not evaluate_api_probes(probes)['ok']
def test_fuzz_requires_zero_crash_and_hang():assert evaluate_fuzz_result({'executions':100,'crashes':0,'hangs':0})['ok'] and not evaluate_fuzz_result({'executions':100,'crashes':1,'hangs':0})['ok']
def test_release_gate_blocks_high():
 reps=[normalize_report(c,'t',[]) for c in policy()['required_security_tests']];reps[0]['findings']=[{'finding_id':'F1','severity':'high','status':'open'}];assert not gate_reports(reps,policy())['ok']
def test_release_gate_requires_all_categories():assert not gate_reports([normalize_report('sast','t',[])],policy())['ok']
def test_pentest_independence_enforced():
 e={'engagement_id':'1','scope':['app'],'tester':'same','implementation_owner':'same','started_at':'a','completed_at':'b','findings':[],'retest_status':'not_required','authorization_reference':'A','evidence_type':'SIMULATED_SCHEMA_VALIDATION_ONLY'}
 with pytest.raises(PenTestEvidenceError):validate_pentest_evidence(e)
def test_production_pentest_rejects_simulation():
 e={'engagement_id':'1','scope':['app'],'tester':'red','implementation_owner':'blue','started_at':'a','completed_at':'b','findings':[],'retest_status':'not_required','authorization_reference':'A','evidence_type':'SIMULATED_SCHEMA_VALIDATION_ONLY'}
 with pytest.raises(PenTestEvidenceError):validate_pentest_evidence(e,production=True)
def test_m27_control_set():
 e=evaluate_m27_policy(policy(),J('governance/controls/control-catalog.json'),J('governance/mappings/framework-mapping.json'),J('governance/enterprise/m27/m27-gap-closure.json'));assert e['ok'] and e['control_count']==9
