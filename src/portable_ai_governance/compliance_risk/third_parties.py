from __future__ import annotations
from .common import load_json
class ThirdPartyRiskError(RuntimeError): pass
REQ=('provider_id','name','owner','service','criticality','data_access','data_residency','security_assessment','contract_status','review_due','exit_plan')
def require_third_party_register(path):
    d=load_json(path); seen=set()
    if d.get('default_decision')!='deny-unassessed': raise ThirdPartyRiskError('default third-party decision must deny unassessed')
    for p in d.get('providers',[]):
        miss=[k for k in REQ if p.get(k) in (None,'',[])]
        if miss: raise ThirdPartyRiskError('provider missing fields: '+','.join(miss))
        if p['provider_id'] in seen: raise ThirdPartyRiskError('duplicate provider id')
        seen.add(p['provider_id'])
        if p['criticality'] in {'high','critical'} and p['security_assessment']!='approved': raise ThirdPartyRiskError('high/critical provider requires approved security assessment')
        if p['data_access']!='none' and not p.get('data_processing_terms'): raise ThirdPartyRiskError('data processing terms required')
        if p['contract_status']!='active': raise ThirdPartyRiskError('provider contract must be active')
    return 'third-party register valid'
