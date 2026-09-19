from __future__ import annotations
from .contracts import envelope,validate_case,validate_envelope

AGENTS={
 'risk':('RISK-AGENT-001','risk'),
 'threat':('THREAT-AGENT-001','threat'),
 'privacy':('PRIVACY-AGENT-001','privacy'),
}
CONTROL_MAP={
 'risk':['AIS-RISK-001','AIS-IMPACT-001'],
 'threat':['AIS-THREAT-001','AIS-AUTH-001'],
 'privacy':['AIS-PRIVACY-001','AIS-DATA-001'],
}

class SpecialistAgent:
 def __init__(self,category):
  if category not in AGENTS:raise ValueError(category)
  self.category=category;self.agent_id,self.role=AGENTS[category]
 def analyze(self,case):
  validate_case(case);key=f'{self.category}_signals';findings=[]
  for s in case[key]:
   findings.append({'finding_id':f"{self.category}:{s['id']}",'category':self.category,'severity':s['severity'],'summary':s['summary'],'evidence_refs':list(s['evidence_refs']),'source_signal_id':s['id']})
  return envelope(self.agent_id,self.role,case['case_id'],case,{'findings':findings})

class ControlAgent:
 agent_id='CONTROL-AGENT-001';role='control'
 def synthesize(self,case_id,specialists):
  findings=[]
  for e in specialists:
   validate_envelope(e,case_id=case_id);findings.extend(e['output']['findings'])
  recs=[]
  for f in findings:
   controls=list(CONTROL_MAP[f['category']])
   if f['severity'] in {'high','critical'}:controls.append('AIS-EVID-001')
   if f['severity']=='critical':controls.append('AIS-ACTION-APPROVAL-001')
   recs.append({'finding_id':f['finding_id'],'control_ids':sorted(set(controls)),'requires_human_review':f['severity'] in {'high','critical'},'side_effect_requested':False})
  inp={'specialist_output_sha256':[e['output_sha256'] for e in specialists]}
  return envelope(self.agent_id,self.role,case_id,inp,{'recommendations':recs})

class AssuranceAgent:
 agent_id='ASSURANCE-AGENT-001';role='assurance'
 def assess(self,case_id,specialists,control):
  validate_envelope(control,agent_id='CONTROL-AGENT-001',role='control',case_id=case_id)
  findings=[]
  for e in specialists:
   validate_envelope(e,case_id=case_id);findings.extend(e['output']['findings'])
  rec={x['finding_id']:x for x in control['output']['recommendations']}
  gaps=[]
  for f in findings:
   if not f['evidence_refs']:gaps.append({'finding_id':f['finding_id'],'gap':'missing_evidence'})
   if f['finding_id'] not in rec or not rec[f['finding_id']]['control_ids']:gaps.append({'finding_id':f['finding_id'],'gap':'missing_control'})
  ready=not gaps
  inp={'specialist_output_sha256':[e['output_sha256'] for e in specialists],'control_output_sha256':control['output_sha256']}
  return envelope(self.agent_id,self.role,case_id,inp,{'ready_for_human_approval':ready,'gaps':gaps,'finding_count':len(findings),'recommendation_count':len(rec)})
