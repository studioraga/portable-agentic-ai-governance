from __future__ import annotations
from dataclasses import dataclass, asdict
from ...kernel.types import AgentRequest, AgentResult, ProposedAction

@dataclass(frozen=True)
class RiskRecord:
    risk_id: str
    system_id: str
    statement: str
    likelihood: int
    impact: int
    controls: tuple[str, ...]
    owner: str
    treatment: str = "mitigate"

    @property
    def inherent_risk(self) -> int:
        return self.likelihood * self.impact

    def validate(self) -> None:
        if not (1 <= self.likelihood <= 5 and 1 <= self.impact <= 5):
            raise ValueError("likelihood and impact must be 1..5")
        if self.treatment not in {"mitigate", "avoid", "transfer", "accept"}:
            raise ValueError("invalid risk treatment")
        if self.treatment == "accept":
            raise ValueError("risk acceptance requires human approval workflow; agent cannot accept")

class AIRiskAgent:
    agent_id = "GOV-03"
    def analyze(self, request: AgentRequest, risk: RiskRecord) -> AgentResult:
        risk.validate()
        severity = "critical" if risk.inherent_risk >= 20 else "high" if risk.inherent_risk >= 12 else "moderate" if risk.inherent_risk >= 6 else "low"
        findings = ({"risk": asdict(risk), "inherent_risk": risk.inherent_risk, "severity": severity},)
        action = ProposedAction("risk.register", risk.risk_id, {"requires_owner": True})
        return AgentResult(request.run_id, self.agent_id, "ok", findings, (action,), next_state="COMPLETE")
