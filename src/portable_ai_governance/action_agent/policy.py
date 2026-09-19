from __future__ import annotations
class ActionPolicyError(RuntimeError): pass
REQUIRED_STAGES=('schema','authorization','policy','budget','approval','audit')
def require_action_policy(doc):
 if doc.get('version')!='0.8.0': raise ActionPolicyError('unexpected policy version')
 if doc.get('agent_id')!='ACTION-AGENT-001': raise ActionPolicyError('unexpected agent_id')
 principal=doc.get('principal',{})
 if principal.get('principal_id')!='ACTION-AGENT-001': raise ActionPolicyError('agent principal mismatch')
 if 'action_agent' not in tuple(principal.get('roles',[])): raise ActionPolicyError('action_agent role required')
 if tuple(doc.get('required_pipeline',[]))!=REQUIRED_STAGES: raise ActionPolicyError('mandatory M8 pipeline order changed')
 if doc.get('side_effecting_tools') is not True or doc.get('approval_required') is not True: raise ActionPolicyError('M8 approvals and side-effect boundary mandatory')
 for key in ('agent_can_approve','self_approval','direct_executor_access','risk_acceptance','compliance_certification','delegation'):
  if doc.get(key) is not False: raise ActionPolicyError(f'{key} must be false')
 budget=doc.get('budget',{})
 if not 1<=int(budget.get('max_steps',0))<=20 or not 1<=int(budget.get('max_tool_calls',0))<=20: raise ActionPolicyError('budget outside bounded range')
 ttl_max=int(doc.get('approval_ttl_max_seconds',0));ttl_default=int(doc.get('approval_ttl_default_seconds',0));skew=int(doc.get('approval_clock_skew_seconds',-1))
 if not 60<=ttl_max<=3600: raise ActionPolicyError('approval TTL outside bounded range')
 if not 60<=ttl_default<=ttl_max: raise ActionPolicyError('approval default TTL outside bounded range')
 if not 0<=skew<=300: raise ActionPolicyError('approval clock skew outside bounded range')
 allowed=doc.get('allowed_tools',[])
 if len(allowed)!=4 or len(set(allowed))!=4: raise ActionPolicyError('exactly four unique action tools required')
 return 'approval-controlled side-effect policy valid; self-approval prohibited'
