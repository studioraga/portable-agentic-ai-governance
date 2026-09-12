from __future__ import annotations
from pathlib import Path
from ...kernel.evidence import EvidenceLedger
from ...kernel.types import AgentRequest, AgentResult

class GovernanceEvidenceAgent:
    agent_id = "GOV-10"
    def __init__(self, ledger: EvidenceLedger):
        self.ledger = ledger

    def record(self, request: AgentRequest, *, event_type: str, payload: dict) -> AgentResult:
        envelope = self.ledger.append(event_type, {"run_id": request.run_id, "principal": request.principal.principal_id, **payload})
        return AgentResult(request.run_id, self.agent_id, "ok", ({"envelope_sha256": envelope["envelope_sha256"]},), evidence_refs=(envelope["envelope_sha256"],), next_state="COMPLETE")

    def verify(self, request: AgentRequest) -> AgentResult:
        ok, detail = self.ledger.verify()
        return AgentResult(request.run_id, self.agent_id, "ok" if ok else "failed", ({"verified": ok, "detail": detail},), next_state="COMPLETE" if ok else "FAILED")
