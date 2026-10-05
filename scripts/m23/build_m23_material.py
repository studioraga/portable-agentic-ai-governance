#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
import sys;sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.enterprise_identity.common import M22_BASELINE_COMMIT,M22_BASELINE_TAG,M23_VERSION,sha256_file,write_json,sign_compact
from portable_ai_governance.enterprise_identity.federation import FederationPolicy,verify_oidc_assertion
from portable_ai_governance.enterprise_identity.pam import ReplayLedger,issue_jit_grant,authorize_jit
from portable_ai_governance.enterprise_identity.evaluation import evaluate_m23_policy

SOURCE_FILES=[
'governance/enterprise/m23/enterprise-identity-policy.json','governance/enterprise/m23/m23-control-mapping.json','governance/enterprise/m23/m23-gap-closure.json',
'governance/controls/control-catalog.json','governance/mappings/framework-mapping.json',
'src/portable_ai_governance/enterprise_identity/__init__.py','src/portable_ai_governance/enterprise_identity/common.py','src/portable_ai_governance/enterprise_identity/federation.py','src/portable_ai_governance/enterprise_identity/entitlements.py','src/portable_ai_governance/enterprise_identity/pam.py','src/portable_ai_governance/enterprise_identity/evaluation.py','src/portable_ai_governance/enterprise_identity/runtime.py','src/portable_ai_governance/security/runtime.py',
'scripts/m23/build_m23_material.py','scripts/m23/validate_m23_node.py','scripts/m23/validate_m23_local.sh','scripts/m23/validate_m23_regression.sh','scripts/m23/verify_node1.sh','scripts/m23/verify_node2.sh','scripts/m23/ci_validate.sh',
'deploy/m23/deploy_node.sh','deploy/m23/one_shot_node1.sh','deploy/m23/one_shot_node2.sh','deploy/m23/package_verifier_material.sh',
'schemas/m23/enterprise-identity-policy.schema.json','schemas/m23/m23-control-mapping.schema.json','schemas/m23/m23-gap-closure.schema.json','schemas/m23/m23-evidence-record.schema.json',
'tests/enterprise_identity/test_m23_enterprise_identity.py','.github/workflows/m23-enterprise-identity.yml','docs/M23-Enterprise-Identity-MFA-PAM.md','docs/Prerequisites-M23.md','docs/Deployment-M23.md','docs/Validation-M23.md','pyproject.toml','.gitignore']
SOURCE_FILES += ['README.md','instruction.md'] + sorted(str(p.relative_to(ROOT)) for p in (ROOT/'docs').glob('*.md'))
SOURCE_FILES = list(dict.fromkeys(SOURCE_FILES))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
    for src,name in {
      'governance/enterprise/m23/enterprise-identity-policy.json':'enterprise-identity-policy.json','governance/enterprise/m23/m23-control-mapping.json':'m23-control-mapping.json','governance/enterprise/m23/m23-gap-closure.json':'m23-gap-closure.json'}.items(): shutil.copy2(ROOT/src,out/name);(out/name).chmod(0o600)
    federation_private=out/'federation-private.pem';federation_public=out/'federation-public.pem';generate_ed25519_keypair(federation_private,federation_public)
    pam_private=out/'pam-private.pem';pam_public=out/'pam-public.pem';generate_ed25519_keypair(pam_private,pam_public)
    signing_private=out/'signing-private.pem';signing_public=out/'signing-public.pem';generate_ed25519_keypair(signing_private,signing_public)
    now=1700000000
    claims={'iss':'https://id.example.invalid/realms/enterprise','aud':['portable-ai-governance'],'sub':'m23-validation-admin','iat':now-10,'exp':now+600,'auth_time':now-30,'amr':['pwd','webauthn'],'acr':'urn:studioraga:aal2','roles':['security-admin'],'groups':['security'],'attributes':{'environment':'validation'}}
    assertion=sign_compact({'alg':'EdDSA','typ':'JWT'},claims,federation_private);(out/'positive-federated-assertion.jwt').write_text(assertion+'\n')
    fp=FederationPolicy(claims['iss'],'portable-ai-governance','urn:studioraga:aal2');principal=verify_oidc_assertion(assertion,federation_public,fp,now=now,privileged=True)
    jit=issue_jit_grant(subject=principal.subject,approver='m23-approver',action='service.restart',resource_prefix='prod/',reason='validated maintenance window',private_key=pam_private,now=now,ttl_sec=600);(out/'positive-jit-grant.jwt').write_text(jit+'\n')
    grant=authorize_jit(jit,pam_public,ReplayLedger(),subject=principal.subject,action='service.restart',resource='prod/api',now=now+10)
    emergency=issue_jit_grant(subject=principal.subject,approver='m23-approver',second_approver='m23-security-officer',action='emergency.shell',resource_prefix='prod/',reason='validated emergency recovery',private_key=pam_private,now=now,ttl_sec=3600,emergency=True);(out/'positive-break-glass-grant.jwt').write_text(emergency+'\n')
    bg=authorize_jit(emergency,pam_public,ReplayLedger(),subject=principal.subject,action='emergency.shell',resource='prod/node1',now=now+10)
    policy=json.loads((out/'enterprise-identity-policy.json').read_text());controls=json.loads((ROOT/'governance/controls/control-catalog.json').read_text());pol=evaluate_m23_policy(policy,controls)
    summary={'ok':pol['ok'] and principal.phishing_resistant and bg.post_review_required,'validation_time':now,'policy':pol,'positive_tests':{'federated_identity':True,'phishing_resistant_mfa':principal.phishing_resistant,'jit':grant.grant_id!='','break_glass':bg.emergency and bg.post_review_required},'negative_tests_required':['otp-only privileged assertion rejected','wrong issuer rejected','expired assertion rejected','wrong audience rejected','self-approved JIT rejected','JIT replay rejected','out-of-scope resource rejected','break-glass without second approver rejected']}
    write_json(out/'m23-validation-summary.json',summary)
    write_json(out/'m23-source-manifest.json',{'version':M23_VERSION,'parent_baseline_commit':M22_BASELINE_COMMIT,'parent_baseline_tag':M22_BASELINE_TAG,'source_binding':'content_digest_allows_precommit_validation_without_claiming_uncommitted_tree_is_a_release','files':{p:sha256_file(ROOT/p) for p in SOURCE_FILES}})
    protected=['enterprise-identity-policy.json','m23-control-mapping.json','m23-gap-closure.json','m23-validation-summary.json','m23-source-manifest.json','federation-public.pem','pam-public.pem','signing-public.pem','positive-federated-assertion.jwt','positive-jit-grant.jwt','positive-break-glass-grant.jwt']
    head=subprocess.run(['git','-c',f'safe.directory={ROOT}','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
    manifest={'version':M23_VERSION,'milestone':'M23','title':'Enterprise Identity, MFA & PAM','m22_baseline_commit':M22_BASELINE_COMMIT,'m22_baseline_tag':M22_BASELINE_TAG,'repository_head_at_generation':head,'source_binding':'m23-source-manifest.json content digests','artifacts':{n:sha256_file(out/n) for n in protected},'boundaries':{'historical_m0_m22_immutable':True,'node1_identity_and_pam_authority':True,'node2_verifier_only':True,'validation_private_keys_are_non_production':True},'claim_boundaries':policy['claim_boundaries'],'evaluation':summary}
    write_json(out/'m23-identity-manifest.json',manifest);sign_blob(out/'m23-identity-manifest.json',signing_private,out/'m23-identity-manifest.json.sig')
    print(json.dumps({'ok':summary['ok'],'out':str(out),'m22_baseline':M22_BASELINE_COMMIT},indent=2))
if __name__=='__main__':main()
