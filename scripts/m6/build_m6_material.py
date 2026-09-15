#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.evidence_analyst.common import write_private_json,secure_tree,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def copy_evidence(srcroot:Path,outroot:Path,milestone:str,files:list[str],entries:list[dict]):
    for name in files:
        src=srcroot/name
        if not src.is_file(): raise SystemExit(f'FAIL: required {milestone} evidence missing: {src}')
        dst=outroot/milestone.lower()/name; dst.parent.mkdir(parents=True,exist_ok=True,mode=0o700); shutil.copy2(src,dst); os.chmod(dst,0o600)
        entries.append({'evidence_id':f'{milestone.lower()}:{name}','milestone':milestone,'kind':'governance-evidence','path':str(dst.relative_to(outroot)),'artifact_path':str(dst.relative_to(outroot.parent)),'sha256':sha256_file(dst),'access':'read-only'})

def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser(); ap.add_argument('--m3-material',required=True); ap.add_argument('--m4-material',required=True); ap.add_argument('--m5-material',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    m3,m4,m5=map(lambda x:Path(x).resolve(),(a.m3_material,a.m4_material,a.m5_material)); out=Path(a.out).resolve(); evroot=out/'evidence'; out.mkdir(parents=True,exist_ok=True,mode=0o700); evroot.mkdir(exist_ok=True,mode=0o700)
    entries=[]
    copy_evidence(m3,evroot,'M3',['artifact-locks.json','software.cdx.json','ai-ml.cdx.json','provenance.intoto.json','vulnerability-report.json','vulnerability-policy.json'],entries)
    copy_evidence(m4,evroot,'M4',['ai-security-manifest.json','model-governance.json','data-provenance.json','retrieval-policy.json','embedding-policy.json','evaluation-results.json','threat-model.json'],entries)
    copy_evidence(m5,evroot,'M5',['compliance-risk-manifest.json','impact-assessment.json','privacy-assessment.json','exception-register.json','third-parties.json','continuous-controls.json','compliance-report.json'],entries)
    policy={'version':'0.6.0','agent_id':'EVIDENCE-ANALYST-001','purpose':'Read-only analysis of allowlisted governance/security evidence','mode':'read-only','permissions':{'tools':['evidence.list','evidence.metadata','evidence.read','evidence.verify','evidence.summarize'],'deny':['write','append','delete','execute','shell','network','policy.modify','risk.accept','exception.approve','compliance.certify','tool.side_effect','agent.delegate']},'budget':{'max_steps':6,'max_tool_calls':6,'max_output_chars':12000},'limits':{'max_read_bytes':65536},'decision_boundaries':{'security_boundary':'deterministic-control-plane','approval_boundary':'deterministic-control-plane','risk_acceptance_boundary':'deterministic-control-plane','compliance_boundary':'deterministic-control-plane'},'llm_required':False,'side_effecting_tools':False}
    write_private_json(out/'agent-policy.json',policy)
    write_private_json(out/'evidence-catalog.json',{'version':'0.6.0','default_access':'deny','entries':entries})
    artifacts=['agent-policy.json','evidence-catalog.json',*[e['artifact_path'] for e in entries]]
    manifest={'version':'0.6.0','agent_id':'EVIDENCE-ANALYST-001','m5_manifest_sha256':sha256_file(m5/'compliance-risk-manifest.json'),'artifacts':{n:sha256_file(out/n) for n in artifacts},'boundary':{'read_only':True,'side_effecting_tools':False,'security_decisions':False,'approval_decisions':False,'risk_acceptance':False,'compliance_certification':False,'delegation':False}}
    write_private_json(out/'evidence-analyst-manifest.json',manifest)
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem'); sign_blob(out/'evidence-analyst-manifest.json',out/'signing-private.pem',out/'evidence-analyst-manifest.json.sig')
    secure_tree(out)
    print(f'PASS: M6 Evidence Analyst material generated at {out}')
    print(f'PASS: cataloged {len(entries)} read-only evidence artifacts from M3-M5')
    print('IMPORTANT: Evidence Analyst has no side-effecting tools and is not an authorization/approval/risk/compliance boundary.')
if __name__=='__main__': main()
