#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_reporting.engine import build_fixture_packs
from portable_ai_governance.cra_reporting.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--validation-now',default='2026-10-03T12:00:00Z');a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
 policy,packs,readiness=build_fixture_packs(ROOT,a.validation_now)
 shutil.copy2(ROOT/'governance/cra/m14/reporting-policy.json',out/'reporting-policy.json');shutil.copy2(ROOT/'governance/cra/m14/m14-control-mapping.json',out/'m14-control-mapping.json')
 for n in ('reporting-policy.json','m14-control-mapping.json'):os.chmod(out/n,0o600)
 write_json(out/'reporting-packs.json',packs);write_json(out/'submission-readiness.json',readiness)
 checklist=[]
 for p in packs:
  for s in p['stages']:
   checklist.append({'pack_id':p['pack_id'],'case_type':p['case_type'],'stage':s['stage'],'deadline_at':s['deadline_at'],'readiness':s['readiness'],'field_names':sorted(s['fields']),'missing_required_fields':s['missing_required_fields'],'human_submission_required':True})
 write_json(out/'srp-field-checklist.json',checklist)
 generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
 names=['reporting-policy.json','m14-control-mapping.json','reporting-packs.json','submission-readiness.json','srp-field-checklist.json','signing-public.pem']
 manifest={'version':'0.14.0','milestone':'M14','purpose':'CRA Reporting and ENISA SRP Evidence Pack','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'m13_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m13/m13-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'validation_now':a.validation_now,'srp_glossary_version':policy['srp']['srp_glossary_version'],'srp_api_available':False,'boundaries':policy['boundaries']}
 write_json(out/'m14-reporting-manifest.json',manifest);sign_blob(out/'m14-reporting-manifest.json',out/'signing-private.pem',out/'m14-reporting-manifest.json.sig');secure_tree(out)
 print(f'PASS: M14 reporting/SRP evidence material generated at {out}');print('PASS: AEV and severe-incident Early Warning / 72h / Final Report evidence packs exercised')
if __name__=='__main__':main()
