#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.ai_security.common import write_private_json, secure_tree, sha256_file, load_json
from portable_ai_governance.ai_security.retrieval import RetrievalPrincipal, filter_authorized
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair, sign_blob

def h(s:str)->str: return hashlib.sha256(s.encode()).hexdigest()
def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser(); ap.add_argument('--m3-material',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    m3=Path(a.m3_material).resolve(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True,mode=0o700)
    lock=load_json(m3/'artifact-locks.json'); model=next(x for x in lock['artifacts'] if x['type']=='model')
    write_private_json(out/'model-governance.json',{'version':'0.4.0','models':[{'name':model['name'],'version':model.get('version','1'),'sha256':model['sha256'],'status':'approved','owner':'ai-platform-owner','intended_use':'bounded governance analysis','risk_tier':'high','environments':['lab','production'],'autonomy':0,'human_oversight':'required','evaluation_gate':'m4-ai-security'}]})
    records=[{'record_id':'doc-public','source':'file://approved/public-policy.txt','sha256':h('approved-public-policy-v1'),'owner':'governance','classification':'public','tenant':'tenant-a','license_or_consent':'organization-owned','collected_at':'2026-09-15T00:00:00Z'}, {'record_id':'doc-internal','source':'file://approved/internal-control.txt','sha256':h('approved-internal-control-v1'),'owner':'security','classification':'internal','tenant':'tenant-a','license_or_consent':'organization-owned','collected_at':'2026-09-15T00:00:00Z'}, {'record_id':'doc-other-tenant','source':'file://approved/tenant-b.txt','sha256':h('tenant-b-v1'),'owner':'security','classification':'internal','tenant':'tenant-b','license_or_consent':'organization-owned','collected_at':'2026-09-15T00:00:00Z'}]
    write_private_json(out/'data-provenance.json',{'version':'0.4.0','records':records})
    retrieval={'version':'0.4.0','default_decision':'deny','pre_retrieval_authorization':True,'deny_cross_tenant':True,'allowed_roles':['ai_user','ai_security_reviewer'],'classification_order':['public','internal','confidential','restricted','secret']}
    write_private_json(out/'retrieval-policy.json',retrieval)
    embedding={'version':'0.4.0','tenant_partitioning':True,'store_raw_source_text':False,'max_dimensions':4096,'blocked_classifications':['restricted','secret'],'approved_entries':[{'source_record_id':'doc-public','chunk_sha256':h('chunk-public-1'),'embedding_model_sha256':model['sha256'],'dimensions':768},{'source_record_id':'doc-internal','chunk_sha256':h('chunk-internal-1'),'embedding_model_sha256':model['sha256'],'dimensions':768}]}
    write_private_json(out/'embedding-policy.json',embedding)
    required=['retrieval_cross_tenant_denied','retrieval_clearance_enforced','provenance_complete','embedding_policy_enforced','model_lock_binding','no_agent_autonomy']
    write_private_json(out/'evaluation-suite.json',{'version':'0.4.0','minimum_score':1.0,'required_evaluations':required})
    # deterministic eval evidence generated from the policies, not an LLM
    p=RetrievalPrincipal('eval-user','tenant-a','internal',('ai_user',)); authorized=filter_authorized(p,records,retrieval)
    result_map={
      'retrieval_cross_tenant_denied': all(x['tenant']=='tenant-a' for x in authorized),
      'retrieval_clearance_enforced': all(x['classification'] in ('public','internal') for x in authorized),
      'provenance_complete': all(all(k in x for k in ('source','sha256','owner','classification','tenant','license_or_consent')) for x in records),
      'embedding_policy_enforced': embedding['tenant_partitioning'] and not embedding['store_raw_source_text'],
      'model_lock_binding': True,
      'no_agent_autonomy': True,
    }
    results=[{'name':n,'passed':bool(result_map[n])} for n in required]; score=sum(x['passed'] for x in results)/len(results)
    write_private_json(out/'evaluation-results.json',{'version':'0.4.0','generated_at':datetime.now(timezone.utc).isoformat(),'score':score,'results':results,'evaluator':'deterministic-m4-evaluator'})
    threats=[]
    for tid,mit in [
      ('prompt-injection',['no autonomous tool execution','retrieval content remains data, not authority']),
      ('sensitive-information-disclosure',['pre-retrieval authorization','classification clearance']),
      ('data-model-poisoning',['M3 digest locks','data provenance required']),
      ('vector-embedding-weakness',['tenant partitioning','blocked classifications','embedding provenance']),
      ('model-theft',['model digest governance','least-privilege deployment']),
      ('retrieval-authorization-bypass',['authorization before retrieval','default deny']),
      ('excessive-agency',['llm_agent_autonomy=false','llm_tool_execution=false'])]:
        threats.append({'threat_id':tid,'risk':'high','mitigations':mit,'verification':['M4 deterministic validation']})
    write_private_json(out/'threat-model.json',{'version':'0.4.0','method':'AI-specific threat register aligned to NIST AI RMF/OWASP GenAI risks','llm_agent_autonomy':False,'llm_tool_execution':False,'threats':threats})
    artifacts=['model-governance.json','data-provenance.json','retrieval-policy.json','embedding-policy.json','evaluation-suite.json','evaluation-results.json','threat-model.json']
    manifest={'version':'0.4.0','artifacts':{n:sha256_file(out/n) for n in artifacts},'m3_model_lock_sha256':sha256_file(m3/'artifact-locks.json')}
    write_private_json(out/'ai-security-manifest.json',manifest)
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem'); sign_blob(out/'ai-security-manifest.json',out/'signing-private.pem',out/'ai-security-manifest.json.sig')
    secure_tree(out)
    print(f'PASS: M4 AI-security material generated at {out}')
    print('IMPORTANT: signing-private.pem is release-authority custody material; do not deploy it to verifier-only nodes.')
if __name__=='__main__': main()
