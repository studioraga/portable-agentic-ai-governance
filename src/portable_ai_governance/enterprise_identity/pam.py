from __future__ import annotations
import time, uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from .common import EnterpriseIdentityError, sign_compact, verify_compact

@dataclass(frozen=True)
class JITGrant:
    grant_id:str; subject:str; approver:str; action:str; resource_prefix:str; issued_at:int; expires_at:int; reason:str; emergency:bool=False; second_approver:str=''; post_review_required:bool=False

class ReplayLedger:
    def __init__(self): self._used:set[str]=set()
    def consume(self,grant_id:str)->None:
        if grant_id in self._used: raise EnterpriseIdentityError('JIT grant replay detected')
        self._used.add(grant_id)

def issue_jit_grant(*,subject:str,approver:str,action:str,resource_prefix:str,reason:str,private_key:str|Path,now:int|None=None,ttl_sec:int=900,emergency:bool=False,second_approver:str='')->str:
    now=int(time.time() if now is None else now)
    if not subject or not approver or subject==approver: raise EnterpriseIdentityError('independent approver required')
    if ttl_sec<=0 or ttl_sec>3600: raise EnterpriseIdentityError('JIT TTL must be 1..3600 seconds')
    if not action or not resource_prefix or len(reason.strip())<8: raise EnterpriseIdentityError('bounded action/resource and meaningful reason required')
    if emergency:
        if not second_approver or second_approver in {subject,approver}: raise EnterpriseIdentityError('break-glass requires a second independent approver')
        ttl_sec=min(ttl_sec,900)
    g=JITGrant(str(uuid.uuid4()),subject,approver,action,resource_prefix,now,now+ttl_sec,reason,emergency,second_approver,emergency)
    return sign_compact({'alg':'EdDSA','typ':'PAG-JIT'},asdict(g),private_key)

def authorize_jit(token:str,public_key:str|Path,ledger:ReplayLedger,*,subject:str,action:str,resource:str,now:int|None=None)->JITGrant:
    now=int(time.time() if now is None else now); h,p=verify_compact(token,public_key)
    if h.get('typ')!='PAG-JIT': raise EnterpriseIdentityError('wrong token type')
    g=JITGrant(**p)
    if g.subject!=subject: raise EnterpriseIdentityError('JIT subject mismatch')
    if g.action!=action: raise EnterpriseIdentityError('JIT action mismatch')
    if not resource.startswith(g.resource_prefix): raise EnterpriseIdentityError('JIT resource out of scope')
    if now<g.issued_at-60 or now>=g.expires_at: raise EnterpriseIdentityError('JIT grant expired or not yet valid')
    if g.emergency and (not g.second_approver or not g.post_review_required): raise EnterpriseIdentityError('invalid break-glass grant')
    ledger.consume(g.grant_id); return g
