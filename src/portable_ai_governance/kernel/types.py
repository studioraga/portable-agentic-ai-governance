from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

TERMINAL_STATES = {"COMPLETE", "DENIED", "FAILED", "CANCELLED", "BUDGET_EXCEEDED", "APPROVAL_REJECTED"}

@dataclass(frozen=True)
class Principal:
    principal_id: str
    roles: tuple[str, ...]
    attributes: dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class AgentRequest:
    run_id: str
    principal: Principal
    objective: str
    context_refs: tuple[str, ...] = ()
    policy_context: str = "production"
    budget_id: str = "default"

@dataclass(frozen=True)
class ProposedAction:
    action: str
    resource: str
    attributes: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class AgentResult:
    run_id: str
    agent_id: str
    status: str
    findings: tuple[dict[str, Any], ...] = ()
    proposed_actions: tuple[ProposedAction, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    policy_decisions: tuple[str, ...] = ()
    next_state: str = "COMPLETE"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    control_id: str
    reason: str
    approval_required: bool = False
