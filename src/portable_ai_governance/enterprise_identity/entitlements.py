from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Entitlement:
    subject:str; role:str; resource_prefix:str; owner:str; expires_at:int; approved:bool=True

def evaluate_entitlement(entitlement:Entitlement, *, subject:str, role:str, resource:str, now:int)->tuple[bool,str]:
    if not entitlement.approved: return False,'entitlement not approved'
    if entitlement.subject!=subject: return False,'subject mismatch'
    if entitlement.role!=role: return False,'role mismatch'
    if not resource.startswith(entitlement.resource_prefix): return False,'resource outside entitlement scope'
    if entitlement.expires_at<=now: return False,'entitlement expired'
    return True,'entitlement allowed'

def review_entitlements(records:list[Entitlement], *, now:int)->dict:
    expired=[r.subject+':'+r.role for r in records if r.expires_at<=now]
    missing_owner=[r.subject+':'+r.role for r in records if not r.owner]
    return {'ok':not expired and not missing_owner,'count':len(records),'expired':expired,'missing_owner':missing_owner}
