from __future__ import annotations
import time
from dataclasses import dataclass
from pathlib import Path
from .common import EnterpriseIdentityError, verify_compact

PHISHING_RESISTANT_AMR={'webauthn','fido2','hwk','piv','smartcard'}

@dataclass(frozen=True)
class FederatedPrincipal:
    subject:str; issuer:str; roles:tuple[str,...]; groups:tuple[str,...]; attributes:dict[str,str]
    amr:tuple[str,...]; acr:str; auth_time:int; expires_at:int; phishing_resistant:bool

@dataclass(frozen=True)
class FederationPolicy:
    issuer:str; audience:str; required_acr:str; max_auth_age_sec:int=43200; clock_skew_sec:int=60
    privileged_requires_phishing_resistant:bool=True

def verify_oidc_assertion(token:str, public_key:str|Path, policy:FederationPolicy, *, now:int|None=None, privileged:bool=False)->FederatedPrincipal:
    _,c=verify_compact(token,public_key); now=int(time.time() if now is None else now)
    if c.get('iss')!=policy.issuer: raise EnterpriseIdentityError('issuer not trusted')
    aud=c.get('aud',[]); aud=[aud] if isinstance(aud,str) else aud
    if policy.audience not in aud: raise EnterpriseIdentityError('audience mismatch')
    if not c.get('sub'): raise EnterpriseIdentityError('subject missing')
    exp=int(c.get('exp',0)); iat=int(c.get('iat',0)); auth_time=int(c.get('auth_time',0))
    if exp <= now-policy.clock_skew_sec: raise EnterpriseIdentityError('assertion expired')
    if iat > now+policy.clock_skew_sec: raise EnterpriseIdentityError('assertion issued in future')
    if auth_time <= 0 or now-auth_time > policy.max_auth_age_sec: raise EnterpriseIdentityError('authentication too old')
    amr=tuple(str(x).lower() for x in c.get('amr',[])); acr=str(c.get('acr',''))
    if policy.required_acr and acr!=policy.required_acr: raise EnterpriseIdentityError('required authentication context not satisfied')
    phishing=bool(PHISHING_RESISTANT_AMR.intersection(amr))
    if privileged and policy.privileged_requires_phishing_resistant and not phishing: raise EnterpriseIdentityError('privileged access requires phishing-resistant MFA')
    roles=tuple(sorted({str(x) for x in c.get('roles',[])})); groups=tuple(sorted({str(x) for x in c.get('groups',[])}))
    attrs={str(k):str(v) for k,v in c.get('attributes',{}).items()}
    return FederatedPrincipal(str(c['sub']),str(c['iss']),roles,groups,attrs,amr,acr,auth_time,exp,phishing)


class OIDCIdentityProvider:
    """Enterprise OIDC adapter for the existing deterministic Principal contract.

    The adapter validates a signed OIDC-shaped assertion against configured trust
    material; production deployments supply the enterprise IdP public key/JWKS-
    derived key material out of band.
    """
    def __init__(self, *, public_key: str|Path, policy: FederationPolicy):
        self.public_key=Path(public_key); self.policy=policy

    def health(self)->tuple[bool,str]:
        if not self.public_key.is_file(): return False,'OIDC verification key missing'
        return True,'OIDC federated identity verifier available'

    def authenticate(self, credential:str):
        from portable_ai_governance.kernel.types import Principal
        p=verify_oidc_assertion(credential,self.public_key,self.policy,privileged=False)
        attrs=dict(p.attributes);attrs.update({'issuer':p.issuer,'acr':p.acr,'mfa':'true','phishing_resistant':'true' if p.phishing_resistant else 'false'})
        return Principal(p.subject,p.roles,attrs)
