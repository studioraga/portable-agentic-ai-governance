import json
from pathlib import Path
import pytest
from portable_ai_governance.operational_security.soc import normalize_event,correlate,SOCPolicyError
from portable_ai_governance.operational_security.vulnerability import assess_finding
from portable_ai_governance.operational_security.incident import run_playbook,IncidentResponseError
from portable_ai_governance.operational_security.backup import validate_backup_policy,make_backup_record,verify_restore,BackupPolicyError
from portable_ai_governance.operational_security.evaluation import evaluate_m26_policy
ROOT=Path(__file__).resolve().parents[2]
def J(p): return json.loads((ROOT/p).read_text())
def test_soc_normalize_and_correlate():
 p=J('governance/enterprise/m26/soc-policy.json');ev=[{'event_id':'1','event_type':'denied_flow','severity':'high','source':'m25-network','subject':'node2','timestamp':1},{'event_id':'2','event_type':'unauthorized_egress','severity':'critical','source':'m25-network','subject':'node1','timestamp':2}];assert len(correlate([normalize_event(x,p) for x in ev],p))==1
def test_unapproved_soc_source_rejected():
 p=J('governance/enterprise/m26/soc-policy.json')
 with pytest.raises(SOCPolicyError): normalize_event({'event_id':'1','event_type':'x','severity':'high','source':'evil','subject':'x','timestamp':1},p)
def test_critical_vulnerability_due():
 p=J('governance/enterprise/m26/vulnerability-operations-policy.json');r=assess_finding({'finding_id':'V1','severity':'critical','detected_at':0,'known_exploited':False,'owner':'sec','status':'open'},p,90000);assert r['remediation_due']
def test_known_exploited_is_emergency():
 p=J('governance/enterprise/m26/vulnerability-operations-policy.json');r=assess_finding({'finding_id':'V2','severity':'medium','detected_at':100,'known_exploited':True,'owner':'sec','status':'open'},p,200);assert r['priority']=='emergency' and r['remediation_due']
def test_ir_full_sequence_closes():
 p=J('governance/enterprise/m26/incident-response-policy.json');r=run_playbook({'incident_id':'I1','status':'detected','severity':'critical'},p,p['required_steps']);assert r['final_status']=='closed' and r['notification_required']
def test_ir_out_of_order_rejected():
 p=J('governance/enterprise/m26/incident-response-policy.json')
 with pytest.raises(IncidentResponseError): run_playbook({'incident_id':'I1','status':'detected','severity':'high'},p,['contained'])
def test_backup_policy_rejects_nonimmutable():
 p=J('governance/enterprise/m26/backup-dr-policy.json');p['immutable_copies_required']=0
 with pytest.raises(BackupPolicyError): validate_backup_policy(p)
def test_restore_integrity_and_objectives():
 p=J('governance/enterprise/m26/backup-dr-policy.json');d=b'critical dataset';b=make_backup_record('control-db',d,p,1000);r=verify_restore(b,d,2000,5600,p,1000);assert r['ok'] and r['digest_match'] and r['rpo_met'] and r['rto_met']
def test_restore_tamper_rejected():
 p=J('governance/enterprise/m26/backup-dr-policy.json');b=make_backup_record('control-db',b'good',p,1000);r=verify_restore(b,b'bad',2000,2100,p,1000);assert not r['ok'] and not r['digest_match']
def test_m26_control_set():
 ev=evaluate_m26_policy(J('governance/enterprise/m26/soc-policy.json'),J('governance/enterprise/m26/vulnerability-operations-policy.json'),J('governance/enterprise/m26/incident-response-policy.json'),J('governance/enterprise/m26/backup-dr-policy.json'),J('governance/controls/control-catalog.json'));assert ev['ok'] and ev['control_count']==10
