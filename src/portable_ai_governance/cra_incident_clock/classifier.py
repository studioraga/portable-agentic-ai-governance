from __future__ import annotations
from .common import stable_id

PROPS=('availability','authenticity','integrity','confidentiality')

def classify_severe_incident(event,policy):
    impacts=event.get('security_property_impacts')
    sensitive=event.get('sensitive_or_important_data_or_function_affected')
    introduced=event.get('malicious_code_introduced')
    executed=event.get('malicious_code_executed')
    scope=event.get('malicious_code_scope')
    missing=impacts is None or sensitive is None or introduced is None or executed is None
    reasons=[]
    if missing:
        decision='INCOMPLETE';a=False;b=False;reasons.append('INSUFFICIENT_ARTICLE_14_5_FACTS')
    else:
        prop=any(bool(impacts.get(p)) for p in PROPS)
        a=bool(prop and sensitive)
        b=bool((introduced or executed) and scope in set(policy['malicious_code_scopes']))
        if a: reasons.append('ARTICLE_14_5_A_SECURITY_PROPERTY_IMPACT')
        if b: reasons.append('ARTICLE_14_5_B_MALICIOUS_CODE')
        decision='SEVERE_INCIDENT' if (a or b) else 'NOT_SEVERE'
        if decision=='NOT_SEVERE': reasons.append('ARTICLE_14_5_THRESHOLD_NOT_MET')
    return {
      'assessment_id':stable_id('SI',event.get('event_id'),decision,a,b),
      'event_id':event.get('event_id'),'product_id':event.get('product_id'),
      'decision':decision,'article_14_5_a':a,'article_14_5_b':b,
      'reason_codes':reasons,
      'availability_impact':None if impacts is None else bool(impacts.get('availability')),
      'authenticity_impact':None if impacts is None else bool(impacts.get('authenticity')),
      'integrity_impact':None if impacts is None else bool(impacts.get('integrity')),
      'confidentiality_impact':None if impacts is None else bool(impacts.get('confidentiality')),
      'sensitive_or_important_data_or_function_affected':sensitive,
      'malicious_code_introduced':introduced,'malicious_code_executed':executed,
      'malicious_code_scope':scope
    }
