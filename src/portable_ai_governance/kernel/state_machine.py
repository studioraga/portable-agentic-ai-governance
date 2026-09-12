from __future__ import annotations
from dataclasses import dataclass

ALLOWED = {
    "START": {"VALIDATE_REQUEST"},
    "VALIDATE_REQUEST": {"AUTHORIZE", "FAILED"},
    "AUTHORIZE": {"LOAD_TRUSTED_CONTEXT", "DENIED"},
    "LOAD_TRUSTED_CONTEXT": {"PLAN", "FAILED"},
    "PLAN": {"POLICY_VALIDATE_PLAN", "FAILED"},
    "POLICY_VALIDATE_PLAN": {"EXECUTE_BOUNDED_TOOLS", "DENIED", "APPROVAL_REQUIRED"},
    "APPROVAL_REQUIRED": {"EXECUTE_BOUNDED_TOOLS", "APPROVAL_REJECTED"},
    "EXECUTE_BOUNDED_TOOLS": {"VERIFY_OUTPUT", "FAILED", "BUDGET_EXCEEDED"},
    "VERIFY_OUTPUT": {"RECORD_EVIDENCE", "FAILED"},
    "RECORD_EVIDENCE": {"COMPLETE", "FAILED"},
    "COMPLETE": set(), "DENIED": set(), "FAILED": set(), "CANCELLED": set(),
    "BUDGET_EXCEEDED": set(), "APPROVAL_REJECTED": set(),
}

@dataclass
class WorkflowState:
    state: str = "START"

    def transition(self, new_state: str) -> None:
        if new_state not in ALLOWED.get(self.state, set()):
            raise ValueError(f"illegal transition {self.state} -> {new_state}")
        self.state = new_state
