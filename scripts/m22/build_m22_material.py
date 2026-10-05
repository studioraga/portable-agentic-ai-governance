#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.enterprise_security.common import M21_1_BASELINE_COMMIT,M21_1_BASELINE_TAG,M22_VERSION,sha256_file,write_json
from portable_ai_governance.enterprise_security.evaluation import evaluate_catalog
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

SOURCE_FILES=[
 'governance/enterprise/m22/cissp-domain-catalog.json',
 'governance/enterprise/m22/enterprise-security-requirements.json',
 'governance/enterprise/m22/enterprise-control-mapping.json',
 'governance/enterprise/m22/gap-register.json',
 'governance/enterprise/m22/evidence-policy.json',
 'src/portable_ai_governance/enterprise_security/common.py',
 'src/portable_ai_governance/enterprise_security/catalog.py',
 'src/portable_ai_governance/enterprise_security/evaluation.py',
 'src/portable_ai_governance/enterprise_security/runtime.py',
 'scripts/m22/build_m22_material.py',
 'scripts/m22/validate_m22_node.py',
 'scripts/m22/validate_m22_local.sh',
 'scripts/m22/validate_m22_regression.sh',
 'scripts/m22/verify_node1.sh',
 'scripts/m22/verify_node2.sh',
 'scripts/m22/ci_validate.sh',
 'deploy/m22/deploy_node.sh',
 'deploy/m22/one_shot_node1.sh',
 'deploy/m22/one_shot_node2.sh',
 'deploy/m22/package_verifier_material.sh',
 'schemas/m22/enterprise-requirements.schema.json',
 'schemas/m22/control-mapping.schema.json',
 'schemas/m22/gap-register.schema.json',
 'schemas/m22/evidence-record.schema.json',
 'tests/enterprise_security/test_m22_enterprise_security.py',
 '.github/workflows/m22-enterprise-security.yml',
 'docs/M22-CISSP-Enterprise-Security-Control-Foundation.md',
 'docs/Prerequisites-M22.md',
 'docs/Deployment-M22.md',
 'docs/Validation-M22.md',
 'governance/mappings/framework-mapping.json',
 'pyproject.toml',
 '.gitignore',
]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
 copies={
 'governance/enterprise/m22/cissp-domain-catalog.json':'cissp-domain-catalog.json',
 'governance/enterprise/m22/enterprise-security-requirements.json':'enterprise-security-requirements.json',
 'governance/enterprise/m22/enterprise-control-mapping.json':'enterprise-control-mapping.json',
 'governance/enterprise/m22/gap-register.json':'gap-register.json',
 'governance/enterprise/m22/evidence-policy.json':'evidence-policy.json'}
 for src,name in copies.items(): shutil.copy2(ROOT/src,out/name);(out/name).chmod(0o600)
 domains=json.loads((out/'cissp-domain-catalog.json').read_text());req=json.loads((out/'enterprise-security-requirements.json').read_text());mapping=json.loads((out/'enterprise-control-mapping.json').read_text());gaps=json.loads((out/'gap-register.json').read_text());controls=json.loads((ROOT/'governance/controls/control-catalog.json').read_text())
 summary=evaluate_catalog(domains,req,mapping,gaps,controls);write_json(out/'m22-evaluation-summary.json',summary)
 source_manifest={'version':M22_VERSION,'parent_baseline_commit':M21_1_BASELINE_COMMIT,'parent_baseline_tag':M21_1_BASELINE_TAG,'source_binding':'content_digest_allows_precommit_validation_without_claiming_uncommitted_tree_is_a_release','files':{p:sha256_file(ROOT/p) for p in SOURCE_FILES}}
 write_json(out/'m22-source-manifest.json',source_manifest)
 private=out/'signing-private.pem';public=out/'signing-public.pem';generate_ed25519_keypair(private,public)
 protected=['cissp-domain-catalog.json','enterprise-security-requirements.json','enterprise-control-mapping.json','gap-register.json','evidence-policy.json','m22-evaluation-summary.json','m22-source-manifest.json','signing-public.pem']
 head=subprocess.run(['git','-c',f'safe.directory={ROOT}','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
 manifest={'version':M22_VERSION,'milestone':'M22','title':'CISSP / Enterprise Security Control Foundation','m21_1_baseline_commit':M21_1_BASELINE_COMMIT,'m21_1_baseline_tag':M21_1_BASELINE_TAG,'repository_head_at_generation':head,'source_binding':'m22-source-manifest.json content digests','artifacts':{n:sha256_file(out/n) for n in protected},'boundaries':{'historical_m0_m21_immutable':True,'node2_verifier_only':True,'no_runtime_enterprise_control_claim':True},'claim_boundaries':{'cissp_certification_claim':False,'iso_iec_27001_certification_claim':False,'iso_iec_42001_certification_claim':False,'cra_conformity_claim':False},'evaluation':{'ok':summary['ok'],'requirement_count':summary['requirement_count'],'open_gap_count':summary['open_gap_count'],'state_counts':summary['state_counts']}}
 write_json(out/'m22-enterprise-manifest.json',manifest);sign_blob(out/'m22-enterprise-manifest.json',private,out/'m22-enterprise-manifest.json.sig')
 print(json.dumps({'ok':summary['ok'],'out':str(out),'open_gaps':summary['open_gap_count']},indent=2))
if __name__=='__main__': main()
