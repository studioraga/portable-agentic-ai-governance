from __future__ import annotations
from dataclasses import dataclass
from .common import load_json
class RetrievalAuthorizationError(RuntimeError): pass
RANK={'public':0,'internal':1,'confidential':2,'restricted':3,'secret':4}
@dataclass(frozen=True)
class RetrievalPrincipal:
    principal_id:str; tenant:str; clearance:str; roles:tuple[str,...]=()

def authorize_record(principal:RetrievalPrincipal, record:dict, policy:dict)->tuple[bool,str]:
    if policy.get('deny_cross_tenant',True) and record.get('tenant')!=principal.tenant: return False,'cross-tenant denied'
    if RANK.get(record.get('classification'),99)>RANK.get(principal.clearance,-1): return False,'classification exceeds clearance'
    allowed=policy.get('allowed_roles',[])
    if allowed and not any(r in allowed for r in principal.roles): return False,'role not allowed'
    return True,'authorized'
def filter_authorized(principal, records, policy): return [r for r in records if authorize_record(principal,r,policy)[0]]
def require_retrieval_policy(path):
    p=load_json(path)
    if p.get('pre_retrieval_authorization') is not True: raise RetrievalAuthorizationError('authorization must occur before retrieval')
    if p.get('deny_cross_tenant') is not True: raise RetrievalAuthorizationError('cross-tenant retrieval must be denied')
    if p.get('default_decision')!='deny': raise RetrievalAuthorizationError('retrieval must default deny')
    return 'pre-retrieval tenant/classification authorization enabled'
