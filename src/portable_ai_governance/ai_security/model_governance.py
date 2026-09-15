from __future__ import annotations
from .common import load_json
class ModelGovernanceError(RuntimeError): pass

def require_model_governance(path, m3_lock_path):
    doc=load_json(path); lock=load_json(m3_lock_path)
    models={x['name']:x for x in lock.get('artifacts',[]) if x.get('type')=='model'}
    records=doc.get('models',[])
    if not records: raise ModelGovernanceError('no governed models')
    for r in records:
        if r.get('status')!='approved': raise ModelGovernanceError(f"model {r.get('name')} not approved")
        if r.get('autonomy') not in (0,'0'): raise ModelGovernanceError('M4 requires model autonomy=0')
        if r.get('name') not in models: raise ModelGovernanceError('model missing from M3 lock')
        if r.get('sha256') != models[r['name']].get('sha256'): raise ModelGovernanceError('model digest does not match M3 lock')
        if not r.get('owner') or not r.get('intended_use') or not r.get('risk_tier'): raise ModelGovernanceError('model governance fields incomplete')
    return 'approved models are M3-digest-bound and autonomy=0'
