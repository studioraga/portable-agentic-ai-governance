from __future__ import annotations
class SOCPolicyError(RuntimeError): pass
REQ={'event_id','event_type','severity','source','subject','timestamp'}
SEV={'low','medium','high','critical'}
def normalize_event(event,policy):
 if not REQ<=set(event): raise SOCPolicyError('missing event fields')
 if event['severity'] not in SEV: raise SOCPolicyError('invalid severity')
 if event['source'] not in policy['approved_sources']: raise SOCPolicyError('unapproved telemetry source')
 return {k:event[k] for k in sorted(event)}
def correlate(events,policy):
 alerts=[]
 for rule in policy['correlation_rules']:
  hits=[e for e in events if e['event_type'] in rule['event_types'] and e['severity'] in rule['severities']]
  if len(hits)>=rule['threshold']:
   alerts.append({'rule_id':rule['rule_id'],'decision':'alert','event_ids':[x['event_id'] for x in hits],'severity':rule['alert_severity']})
 return alerts
def validate_soc_policy(p):
 if p.get('default_action')!='retain-and-evaluate': raise SOCPolicyError('SOC default action must retain-and-evaluate')
 if not p.get('approved_sources') or not p.get('correlation_rules'): raise SOCPolicyError('SOC sources/rules required')
 return True
