#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_annex_evidence.catalog import build_evidence_index,summarize,gaps
from portable_ai_governance.cra_annex_evidence.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
    os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
    for rel,name in [('governance/cra/m17/annex-i-evidence-policy.json','annex-i-evidence-policy.json'),('governance/cra/m17/m17-control-mapping.json','m17-control-mapping.json'),('governance/cra/m17/annex-i-evidence-map.json','annex-i-evidence-map.json')]:shutil.copy2(ROOT/rel,out/name);os.chmod(out/name,0o600)
    idx=build_evidence_index(ROOT);write_json(out/'annex-i-evidence-index.json',idx);write_json(out/'annex-i-coverage-summary.json',summarize(idx));write_json(out/'annex-i-evidence-gaps.json',gaps(idx))
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
    names=['annex-i-evidence-policy.json','m17-control-mapping.json','annex-i-evidence-map.json','annex-i-evidence-index.json','annex-i-coverage-summary.json','annex-i-evidence-gaps.json','signing-public.pem']
    policy=json.loads((out/'annex-i-evidence-policy.json').read_text())
    man={'version':'0.17.0','milestone':'M17','purpose':'CRA Annex-I Compliance Evidence','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'m13_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m13/m13-control-mapping.json'),'m14_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m14/m14-control-mapping.json'),'m15_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m15/m15-control-mapping.json'),'m16_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m16/m16-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'boundaries':policy['boundaries']}
    write_json(out/'m17-annex-i-manifest.json',man);sign_blob(out/'m17-annex-i-manifest.json',out/'signing-private.pem',out/'m17-annex-i-manifest.json.sig');secure_tree(out)
    s=summarize(idx);print(f'PASS: M17 Annex-I evidence material generated at {out}');print(f"PASS: {s['total']} Annex-I rows indexed; states={s['states']}; no CRA conformity claim made")
if __name__=='__main__':main()
