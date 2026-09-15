from pathlib import Path
import json, stat
import pytest
from portable_ai_governance.ai_security.model_governance import require_model_governance,ModelGovernanceError
from portable_ai_governance.ai_security.provenance import require_data_provenance,DataProvenanceError
from portable_ai_governance.ai_security.retrieval import RetrievalPrincipal,authorize_record
from portable_ai_governance.ai_security.embeddings import require_embedding_policy,EmbeddingControlError
from portable_ai_governance.ai_security.evaluation import require_evaluation,EvaluationError
from portable_ai_governance.ai_security.threat_model import require_threat_model,ThreatModelError

def dump(p,d): p.write_text(json.dumps(d)); return p

def test_model_governance_requires_m3_digest(tmp_path):
    lock=dump(tmp_path/'lock.json',{'artifacts':[{'type':'model','name':'m','sha256':'a'*64}]})
    gov=dump(tmp_path/'g.json',{'models':[{'name':'m','sha256':'a'*64,'status':'approved','owner':'o','intended_use':'x','risk_tier':'high','autonomy':0}]})
    assert 'digest-bound' in require_model_governance(gov,lock)
    d=json.loads(gov.read_text()); d['models'][0]['sha256']='b'*64; dump(gov,d)
    with pytest.raises(ModelGovernanceError): require_model_governance(gov,lock)

def test_data_provenance_requires_consent(tmp_path):
    p=dump(tmp_path/'p.json',{'records':[{'record_id':'1','source':'s','sha256':'a'*64,'owner':'o','classification':'public','tenant':'t','license_or_consent':'owned','collected_at':'x'}]})
    assert require_data_provenance(p)
    d=json.loads(p.read_text()); d['records'][0]['license_or_consent']=''; dump(p,d)
    with pytest.raises(DataProvenanceError): require_data_provenance(p)

def test_retrieval_authorization_denies_cross_tenant_and_overclearance():
    p=RetrievalPrincipal('u','a','internal',('ai_user',)); policy={'deny_cross_tenant':True,'allowed_roles':['ai_user']}
    assert authorize_record(p,{'tenant':'b','classification':'public'},policy)[0] is False
    assert authorize_record(p,{'tenant':'a','classification':'confidential'},policy)[0] is False
    assert authorize_record(p,{'tenant':'a','classification':'internal'},policy)[0] is True

def test_embedding_controls_block_restricted(tmp_path):
    prov=dump(tmp_path/'prov.json',{'records':[{'record_id':'x','classification':'restricted'}]})
    pol=dump(tmp_path/'e.json',{'tenant_partitioning':True,'store_raw_source_text':False,'max_dimensions':1024,'blocked_classifications':['restricted'],'approved_entries':[{'source_record_id':'x','chunk_sha256':'a'*64,'embedding_model_sha256':'b'*64,'dimensions':10}]})
    with pytest.raises(EmbeddingControlError): require_embedding_policy(pol,prov)

def test_evaluation_gate_fail_closed(tmp_path):
    req=['retrieval_cross_tenant_denied','retrieval_clearance_enforced','provenance_complete','embedding_policy_enforced','model_lock_binding','no_agent_autonomy']
    s=dump(tmp_path/'s.json',{'minimum_score':1.0,'required_evaluations':req}); r=dump(tmp_path/'r.json',{'score':.8,'results':[{'name':x,'passed':x!='no_agent_autonomy'} for x in req]})
    with pytest.raises(EvaluationError): require_evaluation(s,r)

def test_threat_model_forbids_autonomy(tmp_path):
    ids=['prompt-injection','sensitive-information-disclosure','data-model-poisoning','vector-embedding-weakness','model-theft','retrieval-authorization-bypass','excessive-agency']
    doc={'llm_agent_autonomy':True,'llm_tool_execution':False,'threats':[{'threat_id':i,'mitigations':['m'],'verification':['v']} for i in ids]}
    p=dump(tmp_path/'t.json',doc)
    with pytest.raises(ThreatModelError): require_threat_model(p)
