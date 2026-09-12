from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from ..agents.governance import AISystemInventoryAgent, AIRiskAgent, ControlMappingAgent, GovernanceEvidenceAgent, AISystemRecord, RiskRecord
from ..kernel.authorization import AuthorizationEngine
from ..kernel.budgets import RunBudget
from ..kernel.policy import PolicyEngine
from ..kernel.state_machine import WorkflowState
from ..kernel.types import AgentRequest

class OnboardingWorkflow:
    """Golden workflow for Milestones 0-1: inventory -> risk -> control mapping -> signed governance evidence."""
    def __init__(self, *, authz: AuthorizationEngine, policy: PolicyEngine, mapper: ControlMappingAgent, evidence: GovernanceEvidenceAgent):
        self.authz, self.policy, self.mapper, self.evidence = authz, policy, mapper, evidence
        self.inventory_agent = AISystemInventoryAgent()
        self.risk_agent = AIRiskAgent()

    def run(self, request: AgentRequest, system: AISystemRecord, risks: tuple[RiskRecord, ...], control_ids: tuple[str, ...], budget: RunBudget | None = None) -> dict:
        budget = budget or RunBudget()
        state = WorkflowState()
        trace: list[str] = [state.state]
        def go(s: str):
            budget.consume_step(); state.transition(s); trace.append(state.state)
        go("VALIDATE_REQUEST")
        if not request.objective.strip():
            go("FAILED"); return {"status":"FAILED", "trace":trace}
        go("AUTHORIZE")
        allowed, reason = self.authz.authorize(request.principal, action="ai_system.onboard", resource=f"ai-system/{system.system_id}")
        if not allowed:
            go("DENIED"); return {"status":"DENIED", "reason":reason, "trace":trace}
        go("LOAD_TRUSTED_CONTEXT"); go("PLAN"); go("POLICY_VALIDATE_PLAN")
        decision = self.policy.evaluate("AIS-GOV-001", principal=request.principal, context={"workflow":"ai_system_onboarding"})
        if not decision.allowed:
            go("DENIED"); return {"status":"DENIED", "reason":decision.reason, "trace":trace}
        go("EXECUTE_BOUNDED_TOOLS")
        inv = self.inventory_agent.analyze(request, system)
        risk_results = [self.risk_agent.analyze(request, r) for r in risks]
        mappings = self.mapper.analyze(request, control_ids)
        go("VERIFY_OUTPUT")
        if mappings.status != "ok":
            go("FAILED")
            return {"status":"FAILED", "reason":"unmapped controls", "trace":trace, "mapping":mappings.as_dict()}
        go("RECORD_EVIDENCE")
        ev = self.evidence.record(request, event_type="ai_system_onboarded", payload={
            "system": asdict(system), "risks": [rr.findings[0] for rr in risk_results], "controls": list(control_ids), "mapping": mappings.findings[0]
        })
        go("COMPLETE")
        return {"status":"COMPLETE", "trace":trace, "inventory":inv.as_dict(), "risks":[r.as_dict() for r in risk_results], "mapping":mappings.as_dict(), "evidence":ev.as_dict()}
