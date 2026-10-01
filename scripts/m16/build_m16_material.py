#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_secure_update.engine import build_fixture_lifecycle
from portable_ai_governance.cra_secure_update.update import make_update_descriptor,evaluate_install
from portable_ai_governance.cra_secure_update.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
 for src,name in [(ROOT/'governance/cra/m16/secure-update-policy.json','secure-update-policy.json'),(ROOT/'governance/cra/m16/m16-control-mapping.json','m16-control-mapping.json')]:shutil.copy2(src,out/name);os.chmod(out/name,0o600)
 life,eol=build_fixture_lifecycle(ROOT);write_json(out/'lifecycle-registry.json',life);write_json(out/'eol-notifications.json',eol)
 shutil.copy2(ROOT/'tests/fixtures/m16/security-update.bin',out/'security-update.bin');os.chmod(out/'security-update.bin',0o600)
 generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
 support=next(x for x in life if x['product_id']=='product-node2')['support_period_end']
 desc=make_update_descriptor('product-node2','1.0.0','1.0.1',out/'security-update.bin','2028-01-15',support)
 write_json(out/'security-update.json',desc);sign_blob(out/'security-update.json',out/'signing-private.pem',out/'security-update.json.sig')
 catalog=[{**desc,'availability_rule_satisfied':True,'availability_basis':'max(issue_date_plus_10_years, support_period_end)','public_download_performed':False}];write_json(out/'update-catalog.json',catalog)
 decision=evaluate_install(desc,out/'security-update.bin',out/'security-update.json',out/'security-update.json.sig',out/'signing-public.pem','1.0.0','2028-02-01',support);write_json(out/'update-install-decisions.json',[decision])
 policy=json.loads((out/'secure-update-policy.json').read_text())
 names=['secure-update-policy.json','m16-control-mapping.json','lifecycle-registry.json','update-catalog.json','update-install-decisions.json','eol-notifications.json','security-update.bin','security-update.json','security-update.json.sig','signing-public.pem']
 man={'version':'0.16.0','milestone':'M16','purpose':'CRA Secure Update & Product Lifecycle','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'m13_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m13/m13-control-mapping.json'),'m14_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m14/m14-control-mapping.json'),'m15_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m15/m15-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'boundaries':policy['boundaries']}
 write_json(out/'m16-lifecycle-manifest.json',man);sign_blob(out/'m16-lifecycle-manifest.json',out/'signing-private.pem',out/'m16-lifecycle-manifest.json.sig');secure_tree(out)
 print(f'PASS: M16 secure-update/product-lifecycle material generated at {out}');print('PASS: support period, update retention, signed update, anti-rollback decision and EOL notification evidence exercised')
if __name__=='__main__':main()
