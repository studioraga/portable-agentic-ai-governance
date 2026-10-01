#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_technical_file.catalog import build_technical_file_index,summarize,gaps
from portable_ai_governance.cra_technical_file.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
    os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
    copies=[
      ('governance/cra/m18/technical-file-policy.json','technical-file-policy.json'),
      ('governance/cra/m18/m18-control-mapping.json','m18-control-mapping.json'),
      ('governance/cra/m18/annex-vii-map.json','annex-vii-map.json'),
      ('tests/fixtures/m18/product-technical-profile.json','product-technical-profile.json')]
    for rel,name in copies: shutil.copy2(ROOT/rel,out/name);os.chmod(out/name,0o600)
    idx=build_technical_file_index(ROOT);write_json(out/'annex-vii-technical-file-index.json',idx);write_json(out/'annex-vii-readiness-summary.json',summarize(idx));write_json(out/'annex-vii-gap-register.json',gaps(idx))
    profile=json.loads((out/'product-technical-profile.json').read_text());summary=summarize(idx)
    cover={'version':'0.18.0','milestone':'M18','title':'CRA Annex-VII Technical Documentation / Technical File','product_id':profile['product_id'],'product_name':profile['product_name'],'technical_file_status':'DRAFT_EVIDENCE_FILE','annex_vii_sections':summary['total_sections'],'readiness_states':summary['states'],'cra_conformity_claim':False,'eu_declaration_of_conformity_included':False,'m19_production_validation_required':True}
    write_json(out/'technical-file-cover.json',cover)
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
    names=['technical-file-policy.json','m18-control-mapping.json','annex-vii-map.json','product-technical-profile.json','annex-vii-technical-file-index.json','annex-vii-readiness-summary.json','annex-vii-gap-register.json','technical-file-cover.json','signing-public.pem']
    policy=json.loads((out/'technical-file-policy.json').read_text())
    man={'version':'0.18.0','milestone':'M18','purpose':'CRA Annex-VII Technical Documentation / Technical File','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'m12_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m12/m12-control-mapping.json'),'m13_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m13/m13-control-mapping.json'),'m14_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m14/m14-control-mapping.json'),'m15_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m15/m15-control-mapping.json'),'m16_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m16/m16-control-mapping.json'),'m17_control_mapping_sha256':sha256_file(ROOT/'governance/cra/m17/m17-control-mapping.json'),'artifacts':{n:sha256_file(out/n) for n in names},'boundaries':policy['boundaries']}
    write_json(out/'m18-technical-file-manifest.json',man);sign_blob(out/'m18-technical-file-manifest.json',out/'signing-private.pem',out/'m18-technical-file-manifest.json.sig');secure_tree(out)
    s=summarize(idx);print(f'PASS: M18 Annex-VII technical-file material generated at {out}');print(f"PASS: {s['total_sections']} Annex-VII sections indexed; states={s['states']}; no CRA conformity claim made")
if __name__=='__main__':main()
