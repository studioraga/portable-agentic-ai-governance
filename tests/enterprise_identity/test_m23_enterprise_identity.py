import json,sys,tempfile
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair
from portable_ai_governance.enterprise_identity.common import sign_compact,EnterpriseIdentityError,M22_BASELINE_COMMIT
from portable_ai_governance.enterprise_identity.federation import FederationPolicy,verify_oidc_assertion
from portable_ai_governance.enterprise_identity.entitlements import Entitlement,evaluate_entitlement,review_entitlements
from portable_ai_governance.enterprise_identity.pam import ReplayLedger,issue_jit_grant,authorize_jit
from portable_ai_governance.enterprise_identity.evaluation import evaluate_m23_policy

def keys(td):
    priv=Path(td)/'p.pem';pub=Path(td)/'u.pem';generate_ed25519_keypair(priv,pub);return priv,pub

def claims(now=1700000000,amr=('pwd','webauthn')):
    return {'iss':'https://id.example.invalid/realms/enterprise','aud':['portable-ai-governance'],'sub':'alice','iat':now-10,'exp':now+600,'auth_time':now-30,'amr':list(amr),'acr':'urn:studioraga:aal2','roles':['security-admin'],'groups':['security'],'attributes':{'department':'security'}}

def policy(): return FederationPolicy('https://id.example.invalid/realms/enterprise','portable-ai-governance','urn:studioraga:aal2')

def test_m22_parent_is_frozen(): assert M22_BASELINE_COMMIT=='f020822162591f7d279f7004dea628efb7989525'

def test_privileged_oidc_webauthn_passes():
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td);tok=sign_compact({'alg':'EdDSA','typ':'JWT'},claims(),priv);p=verify_oidc_assertion(tok,pub,policy(),now=1700000000,privileged=True);assert p.subject=='alice' and p.phishing_resistant

def test_privileged_otp_only_is_rejected():
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td);tok=sign_compact({'alg':'EdDSA','typ':'JWT'},claims(amr=('pwd','otp')),priv)
        with pytest.raises(EnterpriseIdentityError,match='phishing-resistant'): verify_oidc_assertion(tok,pub,policy(),now=1700000000,privileged=True)

def test_wrong_issuer_expired_and_wrong_audience_are_rejected():
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td)
        for patch in ({'iss':'https://evil.invalid'},{'exp':1699999000},{'aud':['other-service']}):
            c=claims();c.update(patch);tok=sign_compact({'alg':'EdDSA','typ':'JWT'},c,priv)
            with pytest.raises(EnterpriseIdentityError): verify_oidc_assertion(tok,pub,policy(),now=1700000000,privileged=False)

def test_entitlements_are_scoped_and_reviewed():
    e=Entitlement('alice','security-admin','prod/','sec-owner',1700001000)
    assert evaluate_entitlement(e,subject='alice',role='security-admin',resource='prod/service',now=1700000000)[0]
    assert not evaluate_entitlement(e,subject='alice',role='security-admin',resource='dev/service',now=1700000000)[0]
    assert review_entitlements([e],now=1700000000)['ok']

def test_jit_requires_independent_approver_and_is_single_use():
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td);ledger=ReplayLedger();tok=issue_jit_grant(subject='alice',approver='bob',action='service.restart',resource_prefix='prod/',reason='approved maintenance',private_key=priv,now=1700000000,ttl_sec=600)
        g=authorize_jit(tok,pub,ledger,subject='alice',action='service.restart',resource='prod/api',now=1700000010);assert not g.emergency
        with pytest.raises(EnterpriseIdentityError,match='replay'): authorize_jit(tok,pub,ledger,subject='alice',action='service.restart',resource='prod/api',now=1700000020)
        with pytest.raises(EnterpriseIdentityError,match='independent'): issue_jit_grant(subject='alice',approver='alice',action='x',resource_prefix='prod/',reason='approved maintenance',private_key=priv,now=1700000000)

def test_break_glass_requires_second_approver_and_post_review():
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td)
        with pytest.raises(EnterpriseIdentityError,match='second independent'): issue_jit_grant(subject='alice',approver='bob',action='emergency.shell',resource_prefix='prod/',reason='service outage emergency',private_key=priv,now=1700000000,emergency=True)
        tok=issue_jit_grant(subject='alice',approver='bob',second_approver='carol',action='emergency.shell',resource_prefix='prod/',reason='service outage emergency',private_key=priv,now=1700000000,ttl_sec=3600,emergency=True)
        g=authorize_jit(tok,pub,ReplayLedger(),subject='alice',action='emergency.shell',resource='prod/node1',now=1700000010);assert g.emergency and g.expires_at-g.issued_at<=900 and g.post_review_required

def test_policy_has_all_m23_controls_and_false_claims():
    p=json.loads((ROOT/'governance/enterprise/m23/enterprise-identity-policy.json').read_text()); c=json.loads((ROOT/'governance/controls/control-catalog.json').read_text());r=evaluate_m23_policy(p,c);assert r['ok'],r
    assert all(v is False for v in p['claim_boundaries'].values())

def test_oidc_provider_is_supported_by_production_runtime():
    from portable_ai_governance.security.runtime import build_runtime_dependencies,SecurityDependencyError
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td)
        env={'PAG_SECURITY_PROFILE':'production','PAG_IDENTITY_PROVIDER':'oidc','PAG_OIDC_ISSUER':'https://id.example.invalid/realms/enterprise','PAG_OIDC_AUDIENCE':'portable-ai-governance','PAG_OIDC_PUBLIC_KEY':str(pub),'PAG_OIDC_REQUIRED_ACR':'urn:studioraga:aal2','PAG_SECRET_PROVIDER':'bad'}
        with pytest.raises(SecurityDependencyError,match='protected secret provider'):
            build_runtime_dependencies(env)

def test_jit_out_of_scope_resource_is_rejected():
    with tempfile.TemporaryDirectory() as td:
        priv,pub=keys(td);tok=issue_jit_grant(subject='alice',approver='bob',action='service.restart',resource_prefix='prod/',reason='approved maintenance',private_key=priv,now=1700000000,ttl_sec=600)
        with pytest.raises(EnterpriseIdentityError,match='out of scope'):
            authorize_jit(tok,pub,ReplayLedger(),subject='alice',action='service.restart',resource='dev/api',now=1700000010)
