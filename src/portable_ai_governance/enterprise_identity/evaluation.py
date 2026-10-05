from __future__ import annotations

def evaluate_m23_policy(policy:dict,controls:dict)->dict:
    checks=[]
    req={'ENT-IAM-001','ENT-IAM-002','ENT-IAM-003','ENT-IAM-004','ENT-IAM-005','ENT-PAM-001','ENT-PAM-002','ENT-PAM-003','ENT-PAM-004','ENT-SOD-001'}
    ids={c.get('control_id') for c in controls.get('controls',[])}
    checks.append(('m23-controls-present',req<=ids))
    checks.append(('oidc-required',policy.get('federation',{}).get('protocol')=='OIDC'))
    checks.append(('privileged-phishing-resistant',policy.get('mfa',{}).get('privileged_phishing_resistant_required') is True))
    checks.append(('webauthn-accepted', 'webauthn' in policy.get('mfa',{}).get('phishing_resistant_methods',[])))
    checks.append(('jit-max-ttl',0<int(policy.get('pam',{}).get('jit_max_ttl_sec',0))<=3600))
    checks.append(('break-glass-dual-approval',policy.get('pam',{}).get('break_glass',{}).get('minimum_independent_approvers',0)>=2))
    checks.append(('break-glass-post-review',policy.get('pam',{}).get('break_glass',{}).get('post_review_required') is True))
    checks.append(('replay-protection',policy.get('pam',{}).get('single_use_grants') is True))
    checks.append(('entitlement-review',int(policy.get('entitlements',{}).get('review_interval_days',0))>0))
    boundaries=policy.get('claim_boundaries',{})
    for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'):
        checks.append((f'claim-boundary:{k}',boundaries.get(k) is False))
    return {'ok':all(v for _,v in checks),'checks':checks,'control_count':len(req)}
