#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.enterprise_validation.common import *
from portable_ai_governance.enterprise_validation.coverage import build_requirement_matrix
from portable_ai_governance.enterprise_validation.aggregation import verify_inputs
from portable_ai_governance.enterprise_validation.readiness import assess_production_readiness
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
SOURCE_FILES=['governance/enterprise/m29/cross-domain-validation-policy.json','governance/enterprise/m29/m29-control-mapping.json','governance/enterprise/m29/m29-reconciliation.json','governance/controls/control-catalog.json','governance/mappings/framework-mapping.json']
SOURCE_FILES += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'src/portable_ai_governance/enterprise_validation').glob('*.py'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'schemas/m29').glob('*')) if p.is_file()]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'scripts/m29').glob('*')) if p.is_file()]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'deploy/m29').glob('*')) if p.is_file()]+['tests/enterprise_validation/test_m29_enterprise_validation.py','.github/workflows/m29-enterprise-validation.yml','pyproject.toml','.gitignore','README.md','instruction.md']+sorted(str(p.relative_to(ROOT)) for p in (ROOT/'docs').glob('*.md'));SOURCE_FILES=list(dict.fromkeys(SOURCE_FILES))
def J(p):return json.loads((ROOT/p).read_text())
def copy_public(src,dst):
 shutil.rmtree(dst,ignore_errors=True);dst.mkdir(parents=True)
 for p in src.iterdir():
  if p.is_file() and 'private' not in p.name.lower():shutil.copy2(p,dst/p.name)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--evidence-root',default=str(ROOT/'var'));a=ap.parse_args();out=Path(a.out);er=Path(a.evidence_root);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True);(out/'inputs').mkdir()
 names=['cross-domain-validation-policy.json','m29-control-mapping.json','m29-reconciliation.json']
 for n in names:shutil.copy2(ROOT/'governance/enterprise/m29'/n,out/n)
 for m in range(21,29):
  src=er/f'm{m}-material'
  if not src.is_dir():raise SystemExit(f'missing prerequisite material: {src}; run scripts/m29/prepare_m29_inputs.sh')
  copy_public(src,out/'inputs'/f'm{m}')
 nested=verify_inputs(out/'inputs',ROOT)
 if not all(x.get('ok') for x in nested.values()):raise SystemExit('one or more nested M21-M28 evidence sets failed verification')
 req=J('governance/enterprise/m22/enterprise-security-requirements.json');closures={}
 for m in range(23,29): closures[f'M{m}']=J(f'governance/enterprise/m{m}/m{m}-gap-closure.json')
 matrix=build_requirement_matrix(req['requirements'],closures,J('governance/enterprise/m29/m29-reconciliation.json'));write_json(out/'m29-requirement-matrix.json',matrix)
 m21=json.loads((out/'inputs/m21/platform-validation-summary.json').read_text());m27=json.loads((out/'inputs/m27/m27-validation-summary.json').read_text());m28=json.loads((out/'inputs/m28/m28-validation-summary.json').read_text())
 readiness=assess_production_readiness(matrix,m21,m27,m28,node2_verified=False,no_private_keys=True)
 summary={'ok':True,'nested_milestones_verified':sorted(nested),'requirement_state_counts':matrix['state_counts'],'domain_verdicts':matrix['domains'],'open_requirements':matrix['open_requirements'],'production_ready':readiness['production_ready'],'production_gates':readiness['gates'],'blocking_gates':readiness['blocking_gates'],'validation_mode':'PREPRODUCTION_CROSS_DOMAIN_AGGREGATION'};write_json(out/'m29-cross-domain-summary.json',summary)
 idx={}
 for m in range(21,29): idx[f'm{m}']={p.name:sha256_file(p) for p in sorted((out/'inputs'/f'm{m}').iterdir()) if p.is_file()}
 write_json(out/'m29-input-index.json',idx)
 write_json(out/'m29-source-manifest.json',{'version':M29_VERSION,'parent_baseline_commit':M28_BASELINE_COMMIT,'parent_baseline_tag':M28_BASELINE_TAG,'source_binding':'content_digest_allows_precommit_validation_without claiming uncommitted tree is a release'.replace(' ','_'),'files':{p:sha256_file(ROOT/p) for p in SOURCE_FILES}})
 priv=out/'signing-private.pem';pub=out/'signing-public.pem';generate_ed25519_keypair(priv,pub)
 protected=names+['m29-requirement-matrix.json','m29-cross-domain-summary.json','m29-input-index.json','m29-source-manifest.json','signing-public.pem'];head=subprocess.run(['git','-c',f'safe.directory={ROOT}','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip();pol=J('governance/enterprise/m29/cross-domain-validation-policy.json')
 manifest={'version':M29_VERSION,'milestone':'M29','title':'Enterprise Cross-Domain Node1/Node2 Validation','m28_baseline_commit':M28_BASELINE_COMMIT,'m28_baseline_tag':M28_BASELINE_TAG,'repository_head_at_generation':head,'artifacts':{n:sha256_file(out/n) for n in protected},'input_index_sha256':sha256_file(out/'m29-input-index.json'),'boundaries':{'historical_m0_m28_immutable':True,'node1_evidence_authority':True,'node2_verifier_only':True,'nested_inputs_exclude_private_keys':True,'integrity_pass_does_not_equal_production_ready':True},'claim_boundaries':pol['claim_boundaries'],'cross_domain_summary':summary};write_json(out/'m29-enterprise-validation-manifest.json',manifest);sign_blob(out/'m29-enterprise-validation-manifest.json',priv,out/'m29-enterprise-validation-manifest.json.sig');print(json.dumps({'ok':True,'production_ready':summary['production_ready'],'blocking_gates':summary['blocking_gates'],'out':str(out)},indent=2))
if __name__=='__main__':main()
