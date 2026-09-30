#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_incident_clock.engine import evaluate_fixture_set
from portable_ai_governance.cra_incident_clock.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--validation-now',default='2026-10-03T12:00:00Z');a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
 policy,assess,cases,states,journal=evaluate_fixture_set(ROOT,a.validation_now)
 shutil.copy2(ROOT/'governance/cra/m13/incident-classification-policy.json',out/'incident-classification-policy.json');shutil.copy2(ROOT/'governance/cra/m13/m13-control-mapping.json',out/'m13-control-mapping.json')
 for n in ('incident-classification-policy.json','m13-control-mapping.json'):os.chmod(out/n,0o600)
 write_json(out/'incident-assessments.json',assess);write_json(out/'cra-cases.json',cases);write_json(out/'deadline-states.json',states);write_json(out/'awareness-journal.json',journal)
 generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
 names=['incident-classification-policy.json','m13-control-mapping.json','incident-assessments.json','cra-cases.json','deadline-states.json','awareness-journal.json','signing-public.pem']
 manifest={'version':'0.13.0','milestone':'M13','purpose':'CRA Incident Classification & Statutory Clock','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'validation_now':a.validation_now,'boundaries':{'classification_and_clock_only':True,'enisa_submission':False,'report_generation':False,'cra_conformity_claim':False,'node2_verifier_only':True}}
 write_json(out/'m13-clock-manifest.json',manifest);sign_blob(out/'m13-clock-manifest.json',out/'signing-private.pem',out/'m13-clock-manifest.json.sig');secure_tree(out);print(f'PASS: M13 incident/clock material generated at {out}');print('PASS: severe/not-severe/incomplete classifications and AEV/SI clocks exercised')
if __name__=='__main__':main()
