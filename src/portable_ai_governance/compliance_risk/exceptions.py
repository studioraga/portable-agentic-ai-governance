from __future__ import annotations
from datetime import datetime,timezone
from .common import load_json
class ExceptionRegisterError(RuntimeError): pass

def _ts(v): return datetime.fromisoformat(v.replace('Z','+00:00'))
def require_exception_register(path, now=None):
    d=load_json(path); now=now or datetime.now(timezone.utc)
    if d.get('default_policy')!='deny-unapproved': raise ExceptionRegisterError('default exception policy must deny unapproved')
    seen=set()
    for x in d.get('exceptions',[]):
        for k in ('exception_id','control_id','owner','approver','reason','compensating_controls','created_at','expires_at','status'):
            if not x.get(k): raise ExceptionRegisterError(f"exception missing {k}")
        if x['exception_id'] in seen: raise ExceptionRegisterError('duplicate exception id')
        seen.add(x['exception_id'])
        if x['owner']==x['approver']: raise ExceptionRegisterError('exception owner cannot self-approve')
        if x['status']=='approved' and _ts(x['expires_at']) <= now: raise ExceptionRegisterError(f"approved exception expired: {x['exception_id']}")
        if x['status'] not in {'approved','rejected','closed'}: raise ExceptionRegisterError('invalid exception status')
    return 'exception register valid'
