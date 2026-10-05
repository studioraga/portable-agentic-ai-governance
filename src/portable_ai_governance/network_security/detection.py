from __future__ import annotations
class DetectionPolicyError(ValueError): pass

def validate_detection_policy(p):
    required={'denied_flow','identity_mismatch','unauthorized_egress','port_scan'}
    kinds={r.get('event_type') for r in p.get('rules',[])}
    if not required<=kinds: raise DetectionPolicyError('required detection rules missing')
    if not p.get('telemetry_sources'): raise DetectionPolicyError('telemetry sources required')
    return True

def detect(events,policy):
    validate_detection_policy(policy);configured={r['event_type']:r for r in policy['rules']};alerts=[]
    for e in events:
        if e.get('event_type') in configured:
            alerts.append({'event_id':e.get('event_id'),'event_type':e['event_type'],'severity':configured[e['event_type']].get('severity','medium'),'decision':'alert'})
    return alerts
