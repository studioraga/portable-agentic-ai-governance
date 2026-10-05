from __future__ import annotations
class IncidentResponseError(RuntimeError): pass
ALLOWED={'detected':'triaged','triaged':'contained','contained':'eradicated','eradicated':'recovered','recovered':'closed'}
def run_playbook(incident,policy,steps):
 state=incident['status'];journal=[]
 required=policy['required_steps']
 for target in steps:
  if ALLOWED.get(state)!=target: raise IncidentResponseError(f'illegal transition {state}->{target}')
  journal.append({'from':state,'to':target,'incident_id':incident['incident_id']});state=target
 if state=='closed' and steps!=required: raise IncidentResponseError('closure requires full approved playbook sequence')
 return {'incident_id':incident['incident_id'],'initial_status':incident['status'],'final_status':state,'journal':journal,'notification_required':incident['severity'] in policy['notify_severities']}
def validate_incident_policy(p):
 if p.get('required_steps')!=['triaged','contained','eradicated','recovered','closed']: raise IncidentResponseError('required IR sequence invalid')
 if p.get('evidence_retention_days',0)<365: raise IncidentResponseError('incident evidence retention too short')
 return True
