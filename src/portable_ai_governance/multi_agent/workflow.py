from __future__ import annotations
import time,uuid
from .agents import SpecialistAgent,ControlAgent,AssuranceAgent
from .contracts import validate_case,validate_envelope
from .common import sha256_obj,canonical_json_bytes
from .approval import DecisionVerifier,DecisionUseStore,from_dict,WorkflowDecisionError
from .store import WorkflowJournal
class WorkflowError(RuntimeError):pass
class GovernanceSupervisor:
 def __init__(self,policy,topology,runtime_root,decision_public_key):
  self.policy=policy;self.topology=topology;self.root=runtime_root;self.journal=WorkflowJournal(runtime_root/'workflows.jsonl');self.verifier=DecisionVerifier(decision_public_key,policy['human_decision']['ttl_max_seconds'],policy['human_decision']['clock_skew_seconds']);self.uses=DecisionUseStore(runtime_root/'workflow-decision-uses.jsonl')
  if topology['direct_peer_calls'] is not False or topology['fixed_topology'] is not True:raise WorkflowError('unsafe topology')
 def analyze(self,case):
  validate_case(case);wid=str(uuid.uuid4());b=self.policy['budgets'];total=sum(len(case[k]) for k in ('risk_signals','threat_signals','privacy_signals'))
  if total>b['max_total_signals']:raise WorkflowError('workflow signal budget exceeded')
  if int(b['max_agent_invocations'])<6:raise WorkflowError('workflow agent-invocation budget too small for fixed topology')
  for key in ('risk_signals','threat_signals','privacy_signals'):
   if len(case[key])>b['max_findings_per_specialist']:raise WorkflowError('specialist finding budget exceeded')
  case_sha=sha256_obj(case);self.journal.append(wid,'started',{'case_id':case['case_id'],'case_sha256':case_sha})
  specialists=[]
  for cat in ('risk','threat','privacy'):
   e=SpecialistAgent(cat).analyze(case)
   if e['input_sha256']!=case_sha:raise WorkflowError('specialist handoff input digest mismatch')
   specialists.append(e);self.journal.append(wid,'specialist_complete',{'agent_id':e['agent_id'],'output_sha256':e['output_sha256']})
  control=ControlAgent().synthesize(case['case_id'],specialists)
  expected_control_input=sha256_obj({'specialist_output_sha256':[e['output_sha256'] for e in specialists]})
  if control['input_sha256']!=expected_control_input:raise WorkflowError('control handoff input digest mismatch')
  self.journal.append(wid,'control_complete',{'output_sha256':control['output_sha256']})
  assurance=AssuranceAgent().assess(case['case_id'],specialists,control)
  expected_assurance_input=sha256_obj({'specialist_output_sha256':[e['output_sha256'] for e in specialists],'control_output_sha256':control['output_sha256']})
  if assurance['input_sha256']!=expected_assurance_input:raise WorkflowError('assurance handoff input digest mismatch')
  self.journal.append(wid,'assurance_complete',{'output_sha256':assurance['output_sha256'],'ready':assurance['output']['ready_for_human_approval']})
  proposal={'workflow_id':wid,'case_id':case['case_id'],'system_id':case['system_id'],'specialists':specialists,'control':control,'assurance':assurance,'side_effect_authority':False,'m8_required_for_side_effects':True,'m9_authority_unchanged':True}
  proposal_sha=sha256_obj(proposal);result={'schema':'pag-m10-workflow-result-v1','workflow_id':wid,'proposal':proposal,'proposal_sha256':proposal_sha,'assurance_sha256':assurance['output_sha256'],'status':'pending-human-approval' if assurance['output']['ready_for_human_approval'] else 'blocked'}
  if len(canonical_json_bytes(result))>b['max_workflow_output_bytes']:raise WorkflowError('workflow output budget exceeded')
  self.journal.append(wid,'pending_human_approval',{'proposal_sha256':proposal_sha,'assurance_sha256':assurance['output_sha256']})
  return result
 def finalize(self,result,decision_doc):
  if result.get('schema')!='pag-m10-workflow-result-v1':raise WorkflowError('workflow result schema invalid')
  if result.get('proposal_sha256')!=sha256_obj(result.get('proposal')):raise WorkflowError('workflow proposal digest mismatch')
  ass=result['proposal']['assurance'];validate_envelope(ass,agent_id='ASSURANCE-AGENT-001',role='assurance',case_id=result['proposal']['case_id'])
  if result.get('assurance_sha256')!=ass['output_sha256']:raise WorkflowError('workflow assurance digest mismatch')
  g,sig=from_dict(decision_doc);self.verifier.verify(g,sig)
  if g.workflow_id!=result['workflow_id'] or g.proposal_sha256!=result['proposal_sha256'] or g.assurance_sha256!=result['assurance_sha256']:raise WorkflowDecisionError('workflow decision binding mismatch')
  if g.reviewer not in self.policy['human_decision']['reviewers']:raise WorkflowDecisionError('reviewer not authorized')
  if g.decision=='approve' and not ass['output']['ready_for_human_approval']:raise WorkflowDecisionError('assurance blocks approval')
  self.uses.claim(g.decision_id,g.workflow_id)
  final='approved' if g.decision=='approve' else 'rejected';self.journal.append(g.workflow_id,final,{'decision_id':g.decision_id,'reviewer':g.reviewer,'proposal_sha256':g.proposal_sha256})
  return {'ok':True,'workflow_id':g.workflow_id,'status':final,'reviewer':g.reviewer,'decision_id':g.decision_id,'side_effect_authority':False}
