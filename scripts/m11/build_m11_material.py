#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_foundation.catalog import load_requirement_matrix,validate_requirement_matrix,coverage_summary
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.multi_agent.common import write_json,sha256_file
from portable_ai_governance.action_agent.common import secure_tree

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
 matrix_src=ROOT/'governance/cra/cra-requirements.json';roles_src=ROOT/'governance/cra/node-role-profile.json';matrix=load_requirement_matrix(matrix_src);errors=validate_requirement_matrix(matrix,ROOT)
 if errors: raise SystemExit('FAIL: invalid CRA matrix: '+'; '.join(errors))
 for src,name in [(matrix_src,'cra-requirements.json'),(roles_src,'node-role-profile.json')]: (out/name).write_bytes(src.read_bytes());os.chmod(out/name,0o600)
 report=coverage_summary(matrix);report['generated_by']='M11 deterministic CRA foundation';report['legal_baseline']=matrix['regulation'];write_json(out/'cra-coverage-report.json',report)
 generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
 manifest={'version':'0.11.0','milestone':'M11','purpose':'CRA Product Security Foundation','authoritative_requirement_count':len(matrix['requirements']),'artifacts':{n:sha256_file(out/n) for n in ['cra-requirements.json','node-role-profile.json','cra-coverage-report.json','signing-public.pem']},'boundaries':{'cra_conformity_claim':False,'enisa_submission':False,'network_reporting':False,'node2_verifier_only':True}}
 write_json(out/'m11-cra-manifest.json',manifest);sign_blob(out/'m11-cra-manifest.json',out/'signing-private.pem',out/'m11-cra-manifest.json.sig');secure_tree(out)
 print(f'PASS: M11 CRA foundation material generated at {out}');print(f'PASS: {len(matrix["requirements"])} CRA requirement rows validated; no CRA conformity claim made')
if __name__=='__main__':main()
