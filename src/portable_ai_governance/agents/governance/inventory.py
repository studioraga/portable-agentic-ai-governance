from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
from ...kernel.types import AgentRequest, AgentResult, ProposedAction

@dataclass(frozen=True)
class AISystemRecord:
    system_id: str
    name: str
    system_types: tuple[str, ...]
    business_owner: str
    technical_owner: str
    environments: tuple[str, ...]
    data_classes: tuple[str, ...]
    models: tuple[str, ...]
    external_providers: tuple[str, ...]
    autonomy_level: int
    human_oversight: str
    criticality: str

    def validate(self) -> None:
        if not self.system_id or not self.name:
            raise ValueError("system_id and name are required")
        if self.autonomy_level not in range(0, 6):
            raise ValueError("autonomy_level must be 0..5")
        if self.criticality not in {"low", "moderate", "high", "critical"}:
            raise ValueError("invalid criticality")

class AISystemInventoryAgent:
    agent_id = "GOV-01"
    def analyze(self, request: AgentRequest, record: AISystemRecord) -> AgentResult:
        record.validate()
        findings: list[dict[str, Any]] = [{"inventory_record": asdict(record)}]
        if record.criticality in {"high", "critical"} and record.human_oversight == "none":
            findings.append({"warning": "high/critical AI system lacks human oversight"})
        return AgentResult(request.run_id, self.agent_id, "ok", tuple(findings),
            (ProposedAction("inventory.register", record.system_id),), next_state="COMPLETE")
