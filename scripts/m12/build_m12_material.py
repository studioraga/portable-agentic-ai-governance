#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys,json,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_vulnerability_intel.engine import evaluate_fixture_set
from portable_ai_governance.cra_vulnerability_intel.common import write_json,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree

def main():
    os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--validation-now',default='2026-09-30T13:00:00Z');a=ap.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700);now=datetime.fromisoformat(a.validation_now.replace('Z','+00:00'))
    policy,inventory,result=evaluate_fixture_set(ROOT,now)
    expected=json.loads((ROOT/'tests/fixtures/m12/expected/assessments.json').read_text());actual={x['vulnerability_id']:x['decision'] for x in result['aev_assessments']}
    if actual!=expected:raise SystemExit(f'FAIL: deterministic M12 fixture decisions differ: {actual!r}')
    shutil.copy2(ROOT/'governance/cra/m12/intelligence-source-policy.json',out/'intelligence-source-policy.json');os.chmod(out/'intelligence-source-policy.json',0o600)
    shutil.copy2(ROOT/'governance/cra/m12/m12-control-mapping.json',out/'m12-control-mapping.json');os.chmod(out/'m12-control-mapping.json',0o600)
    write_json(out/'product-inventory.json',inventory);write_json(out/'normalized-vulnerabilities.json',result['normalized_vulnerabilities']);write_json(out/'exploitation-evidence.json',result['exploitation_evidence']);write_json(out/'aev-assessments.json',result['aev_assessments'])
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
    names=['intelligence-source-policy.json','m12-control-mapping.json','product-inventory.json','normalized-vulnerabilities.json','exploitation-evidence.json','aev-assessments.json','signing-public.pem']
    manifest={'version':'0.12.0','milestone':'M12','purpose':'CRA Vulnerability & Exploitation Intelligence','m11_requirement_matrix_sha256':sha256_file(ROOT/'governance/cra/cra-requirements.json'),'artifacts':{n:sha256_file(out/n) for n in names},'fixture_validation_now':a.validation_now,'boundaries':{'aev_candidate_only':True,'starts_statutory_clock':False,'enisa_submission':False,'cra_conformity_claim':False,'network_ingestion':False,'node2_verifier_only':True}}
    write_json(out/'m12-intel-manifest.json',manifest);sign_blob(out/'m12-intel-manifest.json',out/'signing-private.pem',out/'m12-intel-manifest.json.sig');secure_tree(out)
    print(f'PASS: M12 CRA vulnerability/exploitation material generated at {out}');print('PASS: deterministic decisions NOT_AEV / AEV_CANDIDATE / NOT_AFFECTED / INCOMPLETE exercised')
if __name__=='__main__':main()
