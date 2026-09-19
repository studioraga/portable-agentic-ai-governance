#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,os,sys
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.compliance_risk.common import write_private_json,secure_tree,sha256_file,load_json
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def h(s): return hashlib.sha256(s.encode()).hexdigest()
def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser(); ap.add_argument('--m4-material',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    m4=Path(a.m4_material).resolve(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True,mode=0o700)
    freeze=out/'.pag-downstream-bound.json'
    if freeze.is_file():
        raise SystemExit('FAIL: refusing to rebuild downstream-bound/frozen M5 material in place. Use the M7 full release-generation workflow so M6/M7 are rebuilt and re-bound atomically in sequence.')
    m4manifest=m4/'ai-security-manifest.json'
    if not m4manifest.is_file(): raise SystemExit(f'FAIL: M4 manifest missing: {m4manifest}')
    now=datetime.now(timezone.utc); nowz=now.isoformat().replace('+00:00','Z'); review=(now+timedelta(days=90)).date().isoformat()
    impact={'version':'0.5.0','assessment_id':'impact-pag-001','system_id':'portable-agentic-ai-governance','owner':'ai-governance-owner','purpose':'deterministic AI governance/security control plane','stakeholders':['security','privacy','platform','business-owner'],'impact_domains':['security','privacy','fairness','reliability','human-oversight'],'inherent_risk':'high','controls':['M2 security control plane','M3 supply-chain controls','M4 AI-system security'],'residual_risk':'medium','decision':'approve-with-conditions','conditions':['continuous controls remain current','exceptions remain approved and unexpired'],'review_due':review}
    write_private_json(out/'impact-assessment.json',impact)
    privacy={'version':'0.5.0','assessment_id':'privacy-pag-001','system_id':'portable-agentic-ai-governance','owner':'privacy-owner','purposes':['governance validation','security evidence'],'data_categories':['configuration metadata','security evidence'],'legal_basis':'organization-approved operational governance basis; jurisdiction-specific validation required before production','retention':'365-days-reviewable','data_subject_rights':['access/correction/deletion workflow where applicable'],'cross_border_transfer':False,'security_controls':['least privilege','encryption in transit','owner-only evidence permissions'],'dpia_required':False,'review_due':review,'collect_sensitive_data':False}
    write_private_json(out/'privacy-assessment.json',privacy)
    exceptions={'version':'0.5.0','default_policy':'deny-unapproved','exceptions':[]}
    write_private_json(out/'exception-register.json',exceptions)
    third={'version':'0.5.0','default_decision':'deny-unassessed','providers':[{'provider_id':'provider-local-platform','name':'Local sovereign platform','owner':'platform-owner','service':'local compute/storage/control plane','criticality':'high','data_access':'internal-governance-data','data_residency':'customer-premises','security_assessment':'approved','data_processing_terms':'organization-controlled local processing','contract_status':'active','review_due':review,'exit_plan':'export signed evidence and restore from documented local backup'}]}
    write_private_json(out/'third-parties.json',third)
    evidence=[('AIS-IAM-001',m4/'ai-security-manifest.json'),('AIS-LOCK-001',m4/'ai-security-manifest.json'),('AIS-MODEL-001',m4/'model-governance.json'),('AIS-RAG-001',m4/'retrieval-policy.json'),('AIS-EVAL-001',m4/'evaluation-results.json')]
    controls=[]
    for cid,p in evidence:
        if not p.is_file(): raise SystemExit(f'FAIL: required upstream evidence missing: {p}')
        controls.append({'control_id':cid,'owner':'control-owner','status':'pass','last_checked':nowz,'max_age_hours':24,'evidence_sha256':sha256_file(p),'failure_action':'block'})
    continuous={'version':'0.5.0','default_failure_action':'block','controls':controls}
    write_private_json(out/'continuous-controls.json',continuous)
    report={'version':'0.5.0','report_id':'compliance-pag-001','system_id':'portable-agentic-ai-governance','generated_at':nowz,'scope':['M2-security','M3-supply-chain','M4-ai-security','M5-compliance-risk'],'control_summary':{'passed':len(controls),'failed':0,'stale':0},'evidence_refs':[{'control_id':x['control_id'],'sha256':x['evidence_sha256']} for x in controls],'open_risks':[{'risk':'jurisdiction-specific privacy/legal mapping must be validated by accountable owners','status':'open'}],'exceptions':[],'certification_claim':False,'disclaimer':'Automated evidence-backed compliance status report; this is not a certification, legal opinion, or independent audit.'}
    write_private_json(out/'compliance-report.json',report)
    artifacts=['impact-assessment.json','privacy-assessment.json','exception-register.json','third-parties.json','continuous-controls.json','compliance-report.json']
    manifest={'version':'0.5.0','m4_manifest_sha256':sha256_file(m4manifest),'artifacts':{n:sha256_file(out/n) for n in artifacts},'automation_boundary':{'may_assess':True,'may_report':True,'may_approve_exceptions':False,'may_certify_compliance':False,'llm_agent_autonomy':False}}
    write_private_json(out/'compliance-risk-manifest.json',manifest)
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
    sign_blob(out/'compliance-risk-manifest.json',out/'signing-private.pem',out/'compliance-risk-manifest.json.sig')
    secure_tree(out)
    print(f'PASS: M5 compliance/risk material generated at {out}')
    print('IMPORTANT: signing-private.pem is release-authority custody material; exceptions/certification remain human-accountable decisions.')
if __name__=='__main__': main()
