from __future__ import annotations
from .siem import SIEMStore
from .incidents import IncidentStore
from .containment import ContainmentStore
from .evidence import EvidenceVault
class SecOpsError(RuntimeError):pass
class SecurityOperations:
 def __init__(self,root,policy,recovery_verifier=None,recovery_use_store=None):
  from pathlib import Path
  r=Path(root);r.mkdir(parents=True,exist_ok=True,mode=0o700);self.policy=policy;self.recovery_verifier=recovery_verifier;self.recovery_use_store=recovery_use_store;self.siem=SIEMStore(r/'siem/events.jsonl');self.incidents=IncidentStore(r/'incidents/incidents.jsonl');self.containment=ContainmentStore(r/'containment/actions.jsonl');self.evidence=EvidenceVault(r/'evidence',int(policy.get('evidence_max_bytes',10485760)))
 def ingest(self,event,evidence_paths=()):
  import time
  now=int(time.time());ts=int(event.get('timestamp',-1));sp=self.policy.get('siem',{})
  if ts>now+int(sp.get('max_future_skew_seconds',60)):raise SecOpsError('SIEM event timestamp too far in future')
  if ts<now-int(sp.get('max_event_age_seconds',86400)):raise SecOpsError('SIEM event exceeds maximum age')
  sr=self.siem.ingest(event);sev=event['severity'];inc=None;cnt=None;evm=None;everr=''
  if sev in self.policy['incident_severities']:
   inc=self.incidents.create(event)
   rule=next((r for r in self.policy['containment_rules'] if event['event_type'] in r['event_types'] and sev in r['severities']),None)
   if rule:
    cnt=self.containment.apply(inc,event,rule['action']);self.incidents.transition(inc['incident_id'],'contained',f'automatic:{rule["action"]}')
   if evidence_paths:
    try:evm=self.evidence.preserve(inc['incident_id'],evidence_paths)
    except Exception as exc:everr=f'{type(exc).__name__}: {exc}'
  return {'siem':sr,'incident':inc,'containment':cnt,'evidence':evm,'evidence_error':everr}
 def recover(self,incident_id,containment_id,checks,authorization):
  if self.recovery_verifier is None or self.recovery_use_store is None:raise SecOpsError('signed recovery authorization required')
  g=authorization.grant
  if self.recovery_use_store.used(g.authorization_id):raise SecOpsError('recovery authorization already used')
  cur=self.incidents.current(incident_id)
  if cur['status']!='contained':raise SecOpsError('incident must be contained before recovery')
  if not checks or not all(checks.values()):raise SecOpsError('all recovery checks must pass')
  if g.incident_id!=incident_id or g.containment_id!=containment_id:raise SecOpsError('recovery authorization binding mismatch')
  operators=self.policy.get('recovery',{}).get('operators',[])
  self.recovery_verifier.verify(authorization,checks,operators)
  ok,detail=self.evidence.verify(incident_id)
  if not ok:raise SecOpsError(detail)
  self.recovery_use_store.claim(g.authorization_id)
  self.incidents.transition(incident_id,'recovering',f'operator:{g.operator}');rel=self.containment.release(containment_id,incident_id);rec=self.incidents.transition(incident_id,'recovered','authorized recovery checks passed and evidence verified');return {'incident':rec,'containment':rel,'evidence':detail,'operator':g.operator,'authorization_id':g.authorization_id}
