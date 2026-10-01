#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_psirt.engine import build_fixture_material
from portable_ai_governance.cra_psirt.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
 policy,cases,coords,advs,notifs,contract=build_fixture_material(ROOT)
 shutil.copy2(ROOT/'governance/cra/m15/psirt-cvd-policy.json',out/'psirt-cvd-policy.json');shutil.copy2(ROOT/'governance/cra/m15/m15-control-mapping.json',out/'m15-control-mapping.json')
 for n in ('psirt-cvd-policy.json','m15-control-mapping.json'): os.chmod(out/n,0o600)
 write_json(out/'psirt-cases.json',cases);write_json(out/'maintainer-coordination.json',coords);write_json(out/'vulnerability-advisories.json',advs);write_json(out/'user-notifications.json',notifs);write_json(out/'public-contact-cvd-contract.json',contract)
 generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
 names=['psirt-cvd-policy.json','m15-control-mapping.json','psirt-cases.json','maintainer-coordination.json','vulnerability-advisories.json','user-notifications.json','public-contact-cvd-contract.json','signing-public.pem']
 manifest={'version':'0.15.0','milestone':'M15','purpose':'CRA PSIRT / Coordinated Vulnerability Disclosure / User Notification','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'m13_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m13/m13-control-mapping.json'),'m14_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m14/m14-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'boundaries':policy['boundaries']}
 write_json(out/'m15-psirt-manifest.json',manifest);sign_blob(out/'m15-psirt-manifest.json',out/'signing-private.pem',out/'m15-psirt-manifest.json.sig');secure_tree(out)
 print(f'PASS: M15 PSIRT/CVD/user-notification material generated at {out}');print('PASS: PSIRT intake, maintainer coordination, fixed advisory, and AEV/severe-incident user-notification evidence exercised')
if __name__=='__main__': main()
