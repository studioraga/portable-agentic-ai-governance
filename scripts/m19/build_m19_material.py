#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_production_validation.common import write_json,sha256_file
from portable_ai_governance.cra_production_validation.evaluation import evaluate_profiles
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--node1-profile',required=True);ap.add_argument('--node2-profile',required=True);a=ap.parse_args();os.umask(0o077);out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
for rel,name in [('governance/cra/m19/production-validation-policy.json','production-validation-policy.json'),('governance/cra/m19/m19-control-mapping.json','m19-control-mapping.json'),('governance/cra/m19/production-validation-plan.json','production-validation-plan.json')]:
    shutil.copy2(ROOT/rel,out/name);os.chmod(out/name,0o600)
for src,name in [(a.node1_profile,'node1-runtime-profile.json'),(a.node2_profile,'node2-runtime-profile.json')]:
    shutil.copy2(src,out/name);os.chmod(out/name,0o600)
n1=json.loads((out/'node1-runtime-profile.json').read_text());n2=json.loads((out/'node2-runtime-profile.json').read_text());pol=json.loads((out/'production-validation-policy.json').read_text());cross,summary=evaluate_profiles(n1,n2,pol);write_json(out/'cross-node-validation.json',cross);write_json(out/'production-validation-summary.json',summary)
generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
names=['production-validation-policy.json','m19-control-mapping.json','production-validation-plan.json','node1-runtime-profile.json','node2-runtime-profile.json','cross-node-validation.json','production-validation-summary.json','signing-public.pem']
man={'version':'0.19.0','milestone':'M19','purpose':'CRA Node1/Node2 Production Validation','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'m13_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m13/m13-control-mapping.json'),'m14_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m14/m14-control-mapping.json'),'m15_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m15/m15-control-mapping.json'),'m16_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m16/m16-control-mapping.json'),'m17_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m17/m17-control-mapping.json'),'m18_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m18/m18-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'boundaries':pol['boundaries']}
write_json(out/'m19-validation-manifest.json',man);sign_blob(out/'m19-validation-manifest.json',out/'signing-private.pem',out/'m19-validation-manifest.json.sig');secure_tree(out)
print(f'PASS: M19 Node1/Node2 validation material generated at {out}');print(f"PASS: mode={summary['validation_mode']} checks={summary['passed']}/{summary['total_checks']} production_complete={summary['production_validation_complete']} no CRA conformity claim made")
