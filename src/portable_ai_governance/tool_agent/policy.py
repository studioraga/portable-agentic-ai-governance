from __future__ import annotations
from .common import load_json
class ToolAgentPolicyError(RuntimeError): pass
REQUIRED_STAGES=("schema","authorization","policy","budget","audit")
def require_tool_agent_policy(doc):
    if doc.get("version")!="0.7.0": raise ToolAgentPolicyError("unexpected policy version")
    if doc.get("agent_id")!="TOOL-ANALYST-001": raise ToolAgentPolicyError("unexpected agent_id")
    principal=doc.get("principal",{})
    if principal.get("principal_id")!="TOOL-ANALYST-001": raise ToolAgentPolicyError("agent principal mismatch")
    roles=tuple(principal.get("roles",[]))
    if "tool_agent" not in roles: raise ToolAgentPolicyError("tool_agent role required")
    if tuple(doc.get("required_pipeline",[]))!=REQUIRED_STAGES: raise ToolAgentPolicyError("mandatory tool pipeline order changed")
    if doc.get("side_effecting_tools") is not False: raise ToolAgentPolicyError("M7 side effects prohibited")
    if doc.get("direct_executor_access") is not False: raise ToolAgentPolicyError("direct executor access prohibited")
    budget=doc.get("budget",{})
    if not 1<=int(budget.get("max_steps",0))<=20: raise ToolAgentPolicyError("max_steps outside bounded range")
    if not 1<=int(budget.get("max_tool_calls",0))<=20: raise ToolAgentPolicyError("max_tool_calls outside bounded range")
    allowed=doc.get("allowed_tools",[])
    if not isinstance(allowed,list) or not allowed: raise ToolAgentPolicyError("allowed_tools required")
    if len(set(allowed))!=len(allowed): raise ToolAgentPolicyError("duplicate allowed tool")
    return "typed-tool policy valid; mandatory mediation enforced"
