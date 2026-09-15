from __future__ import annotations
class AgentPolicyError(RuntimeError): pass
ALLOWED_TOOLS={"evidence.list","evidence.metadata","evidence.read","evidence.verify","evidence.summarize"}
FORBIDDEN_CAPABILITIES={"write","append","delete","execute","shell","network","policy.modify","risk.accept","exception.approve","compliance.certify","tool.side_effect","agent.delegate"}

def require_agent_policy(doc):
    if doc.get('agent_id')!='EVIDENCE-ANALYST-001': raise AgentPolicyError('unexpected agent_id')
    if doc.get('mode')!='read-only': raise AgentPolicyError('agent mode must be read-only')
    perms=doc.get('permissions',{})
    tools=set(perms.get('tools',[])); deny=set(perms.get('deny',[]))
    if not tools or not tools <= ALLOWED_TOOLS: raise AgentPolicyError('tool allowlist contains non-read-only capability')
    missing=FORBIDDEN_CAPABILITIES-deny
    if missing: raise AgentPolicyError('deny list missing: '+','.join(sorted(missing)))
    b=doc.get('budget',{})
    if not (1 <= int(b.get('max_steps',0)) <= 12): raise AgentPolicyError('max_steps outside bounded range')
    if not (1 <= int(b.get('max_tool_calls',0)) <= 12): raise AgentPolicyError('max_tool_calls outside bounded range')
    if int(b.get('max_output_chars',0)) < 256: raise AgentPolicyError('max_output_chars too small')
    boundaries=doc.get('decision_boundaries',{})
    for k in ('security_boundary','approval_boundary','risk_acceptance_boundary','compliance_boundary'):
        if boundaries.get(k)!='deterministic-control-plane': raise AgentPolicyError(f'{k} must remain deterministic-control-plane')
    return 'bounded read-only Evidence Analyst policy valid'
