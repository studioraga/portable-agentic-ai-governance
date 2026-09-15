from __future__ import annotations
from datetime import datetime,timezone,timedelta
from .common import load_json
class ContinuousControlError(RuntimeError): pass

def _ts(v): return datetime.fromisoformat(v.replace('Z','+00:00'))
def require_continuous_controls(path, now=None):
    d=load_json(path); now=now or datetime.now(timezone.utc); seen=set()
    if d.get('default_failure_action')!='block': raise ContinuousControlError('continuous controls must default to block')
    for c in d.get('controls',[]):
        for k in ('control_id','owner','status','last_checked','max_age_hours','evidence_sha256','failure_action'):
            if c.get(k) in (None,''): raise ContinuousControlError(f'continuous control missing {k}')
        if c['control_id'] in seen: raise ContinuousControlError('duplicate continuous control')
        seen.add(c['control_id'])
        if c['status']!='pass': raise ContinuousControlError(f"continuous control failed: {c['control_id']}")
        if c['failure_action']!='block': raise ContinuousControlError('mandatory control must block on failure')
        if now-_ts(c['last_checked']) > timedelta(hours=int(c['max_age_hours'])): raise ContinuousControlError(f"continuous control stale: {c['control_id']}")
        if len(c['evidence_sha256'])!=64: raise ContinuousControlError('invalid evidence digest')
    if not d.get('controls'): raise ContinuousControlError('continuous controls required')
    return 'continuous controls current'
