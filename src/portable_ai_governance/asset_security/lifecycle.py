from __future__ import annotations
from dataclasses import dataclass
class DataLifecycleError(RuntimeError): pass
@dataclass(frozen=True)
class RetentionDecision:
    action:str;reason:str

def validate_lifecycle_policy(policy:dict)->None:
    profiles=policy.get('retention_profiles',{})
    if not profiles: raise DataLifecycleError('retention profiles required')
    for name,p in profiles.items():
        days=int(p.get('retention_days',0))
        if days<=0 or days>36500: raise DataLifecycleError(f'invalid retention period: {name}')
    if policy.get('legal_hold',{}).get('overrides_disposal') is not True: raise DataLifecycleError('legal hold must override disposal')
    allowed=set(policy.get('sanitization',{}).get('approved_methods',[]))
    if not {'crypto-erase','secure-delete','physical-destruction'}<=allowed: raise DataLifecycleError('required sanitization methods absent')

def retention_decision(record:dict,policy:dict,now:int)->RetentionDecision:
    validate_lifecycle_policy(policy)
    profile=policy['retention_profiles'].get(record.get('retention_profile'))
    if not profile: raise DataLifecycleError('unknown retention profile')
    if record.get('legal_hold') is True:return RetentionDecision('retain','legal hold active')
    created=int(record.get('created_at',0)); due=created+int(profile['retention_days'])*86400
    return RetentionDecision('retain','retention period active') if now<due else RetentionDecision('sanitize','retention period expired')

def validate_sanitization_record(record:dict,policy:dict)->None:
    validate_lifecycle_policy(policy)
    method=record.get('method')
    if method not in policy['sanitization']['approved_methods']: raise DataLifecycleError('unapproved sanitization method')
    for k in ('record_id','asset_id','performed_at','performed_by','method','evidence_sha256'):
        if record.get(k) in (None,''): raise DataLifecycleError(f'missing sanitization field: {k}')
    digest=str(record['evidence_sha256']).lower()
    if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest): raise DataLifecycleError('invalid sanitization evidence digest')
    if record.get('classification')=='restricted' and not record.get('approved_by'): raise DataLifecycleError('restricted sanitization requires approval')
