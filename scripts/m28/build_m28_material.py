#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.organizational_security.common import M27_BASELINE_COMMIT,M27_BASELINE_TAG,M28_VERSION,sha256_file,write_json
from portable_ai_governance.organizational_security.governance import validate_governance
from portable_ai_governance.organizational_security.personnel import validate_personnel
from portable_ai_governance.organizational_security.physical import validate_physical
from portable_ai_governance.organizational_security.bcp import validate_bcp
from portable_ai_governance.organizational_security.evaluation import evaluate_m28_policy
SOURCE_FILES=['governance/enterprise/m28/organizational-governance-policy.json','governance/enterprise/m28/personnel-security-policy.json','governance/enterprise/m28/physical-environmental-policy.json','governance/enterprise/m28/business-continuity-policy.json','governance/enterprise/m28/m28-control-mapping.json','governance/enterprise/m28/m28-gap-closure.json','governance/controls/control-catalog.json','governance/mappings/framework-mapping.json']
SOURCE_FILES += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'src/portable_ai_governance/organizational_security').glob('*.py'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'schemas/m28').glob('*'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'scripts/m28').glob('*'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'deploy/m28').glob('*'))]+['tests/organizational_security/test_m28_organizational_security.py','.github/workflows/m28-organizational-security.yml','pyproject.toml','.gitignore','README.md','instruction.md']+sorted(str(p.relative_to(ROOT)) for p in (ROOT/'docs').glob('*.md'));SOURCE_FILES=list(dict.fromkeys(SOURCE_FILES))
def J(p): return json.loads((ROOT/p).read_text())
def att(record_id,subject,authority,role,kind=None,control=None):
 d={'record_id':record_id,'subject':subject,'authority':authority,'authority_role':role,'observed_at':'2026-10-06T00:00:00Z','expires_at':'2027-10-06T00:00:00Z','evidence_type':'SIMULATED_SCHEMA_VALIDATION_ONLY','evidence_reference':'M28-LOCAL-VALIDATION','production_evidence':False,'requires_independence':True}
 if kind:d['kind']=kind
 if control:d['control']=control
 return d
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
 names=['organizational-governance-policy.json','personnel-security-policy.json','physical-environmental-policy.json','business-continuity-policy.json','m28-control-mapping.json','m28-gap-closure.json']
 for n in names: shutil.copy2(ROOT/'governance/enterprise/m28'/n,out/n)
 priv=out/'signing-private.pem';pub=out/'signing-public.pem';generate_ed25519_keypair(priv,pub)
 charter={'roles':{r:r+'-principal' for r in J('governance/enterprise/m28/organizational-governance-policy.json')['required_roles']},'raci':{'security_policy':['security_owner','executive_sponsor'],'bcp':['continuity_owner','executive_sponsor']},'policy_owners':{'security':'security_owner','personnel':'hr_owner','physical':'facilities_owner','continuity':'continuity_owner'}};write_json(out/'governance-charter.json',charter)
 ga=att('GOV-ATTEST-001','security-governance-program','executive-sponsor-principal','executive_sponsor');write_json(out/'governance-attestation.json',ga)
 kinds=J('governance/enterprise/m28/personnel-security-policy.json')['required_evidence'];prs=[att('PEOPLE-'+str(i), 'validation-worker','hr-principal' if 'training' not in k else 'training-principal','hr_owner' if 'training' not in k else 'training_owner',kind=k) for i,k in enumerate(kinds,1)];[r.update({'terminated':False,'revocation_hours':0}) for r in prs if r['kind']=='joiner_mover_leaver_review'];write_json(out/'personnel-evidence.json',prs)
 pp=J('governance/enterprise/m28/physical-environmental-policy.json');controls=[x for xs in pp['required_control_families'].values() for x in xs];ph=[att('PHYS-'+str(i),'node1-node2-facility','facilities-principal','facilities_owner',control=c) for i,c in enumerate(controls,1)];write_json(out/'physical-environmental-evidence.json',ph)
 plan={'bia_reference':'M26-BIA-EVIDENCE','continuity_plan_reference':'M28-BCP-PLAN','crisis_roles':['incident_commander','communications_lead','recovery_lead'],'communications_plan':'M28-COMMS-PLAN','dependency_register':['identity','network','backup','power','facility'],'inherits_m26_technical_dr':True};write_json(out/'bcp-plan.json',plan)
 ex=att('BCP-EX-001','enterprise-security-control-plane','continuity-principal','continuity_owner');ex['lessons_learned']=['validate alternate communications channel','review facility dependency evidence'];write_json(out/'bcp-exercise-evidence.json',ex)
 asof='2026-10-06T12:00:00Z';validate_governance(J('governance/enterprise/m28/organizational-governance-policy.json'),charter,ga,asof);validate_personnel(J('governance/enterprise/m28/personnel-security-policy.json'),prs,asof);validate_physical(pp,ph,asof);validate_bcp(J('governance/enterprise/m28/business-continuity-policy.json'),plan,ex,asof)
 ev=evaluate_m28_policy(J('governance/enterprise/m28/m28-control-mapping.json'),J('governance/controls/control-catalog.json'),J('governance/mappings/framework-mapping.json'),J('governance/enterprise/m28/m28-gap-closure.json'))
 summary={'ok':ev['ok'],'policy_evaluation':ev,'validation_mode':'SIMULATED_AUTHORITY_BOUND_EVIDENCE_SCHEMA_AND_SIGNATURE_VALIDATION','production_evidence_present':False,'inherited_m26_technical_dr_evidence':True};write_json(out/'m28-validation-summary.json',summary)
 write_json(out/'m28-source-manifest.json',{'version':M28_VERSION,'parent_baseline_commit':M27_BASELINE_COMMIT,'parent_baseline_tag':M27_BASELINE_TAG,'source_binding':'content_digest_allows_precommit_validation_without_claiming_uncommitted_tree_is_a_release','files':{p:sha256_file(ROOT/p) for p in SOURCE_FILES}})
 protected=names+['governance-charter.json','governance-attestation.json','personnel-evidence.json','physical-environmental-evidence.json','bcp-plan.json','bcp-exercise-evidence.json','m28-validation-summary.json','m28-source-manifest.json','signing-public.pem'];head=subprocess.run(['git','-c',f'safe.directory={ROOT}','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip();policy=J('governance/enterprise/m28/organizational-governance-policy.json')
 manifest={'version':M28_VERSION,'milestone':'M28','title':'Personnel, Physical, BCP & Organizational Controls','m27_baseline_commit':M27_BASELINE_COMMIT,'m27_baseline_tag':M27_BASELINE_TAG,'repository_head_at_generation':head,'source_binding':'m28-source-manifest.json content digests','artifacts':{n:sha256_file(out/n) for n in protected},'boundaries':{'historical_m0_m27_immutable':True,'node1_evidence_authority':True,'node2_verifier_only':True,'python_does_not_prove_real_world_control_operation':True,'simulated_records_are_not_production_evidence':True},'claim_boundaries':policy['claim_boundaries'],'evaluation':summary};write_json(out/'m28-organizational-manifest.json',manifest);sign_blob(out/'m28-organizational-manifest.json',priv,out/'m28-organizational-manifest.json.sig');print(json.dumps({'ok':summary['ok'],'out':str(out),'m27_baseline':M27_BASELINE_COMMIT},indent=2))
if __name__=='__main__': main()
