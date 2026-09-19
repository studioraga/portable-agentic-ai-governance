from __future__ import annotations
import json,subprocess,sys,time
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.security_ops.siem import SIEMStore,SIEMError
from portable_ai_governance.security_ops.incidents import IncidentStore,IncidentError
from portable_ai_governance.security_ops.evidence import EvidenceVault
from portable_ai_governance.security_ops.engine import SecurityOperations,SecOpsError
from portable_ai_governance.security_ops.runtime import evaluate_security_ops
from portable_ai_governance.security_ops.recovery import RecoveryIssuer,RecoveryVerifier,RecoveryUseStore
POL={'version':'0.9.0','incident_severities':['high','critical'],'containment_rules':[{'rule_id':'r1','event_types':['model.integrity.failure'],'severities':['critical'],'action':'model.quarantine.local'}],'recovery':{'operators':['HUMAN-RESPONDER-001'],'authorization_ttl_max_seconds':900},'evidence_max_bytes':100000,'llm_decision_authority':False}
def ev(sev='critical',eid='e1',etype='model.integrity.failure'):return {'event_id':eid,'event_type':etype,'severity':sev,'source':'node1','timestamp':int(time.time()),'subject':'model:test'}
def test_siem_hash_chain_and_duplicate(tmp_path):
 s=SIEMStore(tmp_path/'events.jsonl');s.ingest(ev());assert s.verify()[0]
 with pytest.raises(SIEMError):s.ingest(ev())
def test_siem_tamper_detected(tmp_path):
 s=SIEMStore(tmp_path/'events.jsonl');s.ingest(ev());p=tmp_path/'events.jsonl';d=json.loads(p.read_text());d['event']['severity']='low';p.write_text(json.dumps(d)+'\n');assert not s.verify()[0]
def test_siem_export_only_after_chain_verification(tmp_path):
 s=SIEMStore(tmp_path/'events.jsonl');s.ingest(ev());out=tmp_path/'export/events.ndjson';assert s.export_events(out)==1;assert json.loads(out.read_text())['event_id']=='e1'
def test_low_event_no_incident(tmp_path):
 o=SecurityOperations(tmp_path/'r',POL);r=o.ingest(ev('low'));assert r['incident'] is None
def test_critical_creates_incident_and_containment(tmp_path):
 o=SecurityOperations(tmp_path/'r',POL);r=o.ingest(ev());assert r['incident']['status']=='open';assert r['containment']['action']=='model.quarantine.local';assert o.incidents.current(r['incident']['incident_id'])['status']=='contained'
def test_evidence_preserve_and_tamper(tmp_path):
 p=tmp_path/'x.txt';p.write_text('evidence');v=EvidenceVault(tmp_path/'v');v.preserve('i1',[p]);assert v.verify('i1')[0];q=next((tmp_path/'v/i1').glob('000-*'));q.write_text('tamper');assert not v.verify('i1')[0]
def recovery_ops(tmp_path):
 from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair
 priv,pub=tmp_path/'rpriv.pem',tmp_path/'rpub.pem';generate_ed25519_keypair(priv,pub);rv=RecoveryVerifier(pub,max_ttl=900);ru=RecoveryUseStore(tmp_path/'uses.jsonl');return SecurityOperations(tmp_path/'r',POL,rv,ru),RecoveryIssuer(priv)
def test_recovery_requires_containment(tmp_path):
 o,issuer=recovery_ops(tmp_path);r=o.ingest(ev('high',etype='other'));auth=issuer.issue(r['incident']['incident_id'],'nope','HUMAN-RESPONDER-001',{'health':True})
 with pytest.raises(SecOpsError):o.recover(r['incident']['incident_id'],'nope',{'health':True},auth)
def test_recovery_requires_all_checks_and_evidence(tmp_path):
 p=tmp_path/'e.txt';p.write_text('ok');o,issuer=recovery_ops(tmp_path);r=o.ingest(ev(),[p]);iid=r['incident']['incident_id'];cid=r['containment']['containment_id']
 bad=issuer.issue(iid,cid,'HUMAN-RESPONDER-001',{'health':False})
 with pytest.raises(SecOpsError):o.recover(iid,cid,{'health':False},bad)
 checks={'health':True,'integrity':True};auth=issuer.issue(iid,cid,'HUMAN-RESPONDER-001',checks);out=o.recover(iid,cid,checks,auth);assert out['incident']['status']=='recovered'
def test_recovery_replay_rejected(tmp_path):
 p=tmp_path/'e.txt';p.write_text('ok');o,issuer=recovery_ops(tmp_path);r=o.ingest(ev(),[p]);iid=r['incident']['incident_id'];cid=r['containment']['containment_id'];checks={'health':True};auth=issuer.issue(iid,cid,'HUMAN-RESPONDER-001',checks);o.recover(iid,cid,checks,auth)
 with pytest.raises(Exception):o.recover(iid,cid,checks,auth)
def test_incident_and_containment_journals_verify(tmp_path):
 o,_=recovery_ops(tmp_path);o.ingest(ev());assert o.incidents.verify()[0];assert o.containment.verify()[0]
def test_recovery_use_store_rejects_duplicate_claim(tmp_path):
 s=RecoveryUseStore(tmp_path/'recovery-uses.jsonl');s.claim('a1')
 with pytest.raises(Exception):s.claim('a1')
def test_illegal_incident_transition(tmp_path):
 s=IncidentStore(tmp_path/'i.jsonl');i=s.create(ev())
 with pytest.raises(IncidentError):s.transition(i['incident_id'],'recovered','bad')

def test_critical_containment_survives_evidence_copy_failure(tmp_path):
 o,_=recovery_ops(tmp_path);r=o.ingest(ev(),[tmp_path/'missing.txt']);assert r['containment'] is not None;assert r['evidence'] is None;assert r['evidence_error']
def test_future_event_rejected(tmp_path):
 import time
 o=SecurityOperations(tmp_path/'r',POL);e=ev();e['timestamp']=int(time.time())+1000
 with pytest.raises(SecOpsError):o.ingest(e)
def test_private_key_evidence_rejected(tmp_path):
 p=tmp_path/'signing-private.pem';p.write_text('secret');v=EvidenceVault(tmp_path/'v')
 with pytest.raises(Exception):v.preserve('i1',[p])
def test_builder_binds_m8_and_runtime(tmp_path):
 m8=tmp_path/'m8';m8.mkdir();(m8/'action-agent-manifest.json').write_text('{}')
 out=tmp_path/'m9';subprocess.run([sys.executable,str(ROOT/'scripts/m9/build_m9_material.py'),'--m8-material',str(m8),'--out',str(out)],check=True,capture_output=True,text=True)
 env={'PAG_M9_ROOT':str(out),'PAG_M9_MANIFEST':str(out/'security-ops-manifest.json'),'PAG_M9_MANIFEST_SIG':str(out/'security-ops-manifest.json.sig'),'PAG_M9_PUBLIC_KEY':str(out/'signing-public.pem'),'PAG_M9_POLICY':str(out/'security-ops-policy.json'),'PAG_M9_RECOVERY_PUBLIC_KEY':str(out/'recovery-signing-public.pem'),'PAG_M8_MANIFEST':str(m8/'action-agent-manifest.json'),'PAG_M9_RUNTIME_ROOT':str(tmp_path/'runtime')};assert evaluate_security_ops(env).ok
def test_runtime_rejects_m8_drift(tmp_path):
 m8=tmp_path/'m8';m8.mkdir();p=m8/'action-agent-manifest.json';p.write_text('{}');out=tmp_path/'m9';subprocess.run([sys.executable,str(ROOT/'scripts/m9/build_m9_material.py'),'--m8-material',str(m8),'--out',str(out)],check=True,capture_output=True,text=True);p.write_text('{"drift":1}')
 env={'PAG_M9_ROOT':str(out),'PAG_M9_MANIFEST':str(out/'security-ops-manifest.json'),'PAG_M9_MANIFEST_SIG':str(out/'security-ops-manifest.json.sig'),'PAG_M9_PUBLIC_KEY':str(out/'signing-public.pem'),'PAG_M9_POLICY':str(out/'security-ops-policy.json'),'PAG_M9_RECOVERY_PUBLIC_KEY':str(out/'recovery-signing-public.pem'),'PAG_M8_MANIFEST':str(p),'PAG_M9_RUNTIME_ROOT':str(tmp_path/'runtime')};assert not evaluate_security_ops(env).ok
