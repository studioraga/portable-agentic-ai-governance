from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .types import PolicyDecision, Principal

class PolicyError(RuntimeError):
    pass

class PolicyEngine:
    """Deterministic policy evaluator. Agents may explain decisions but cannot override them."""
    def __init__(self, controls_path: str | Path):
        payload = json.loads(Path(controls_path).read_text(encoding="utf-8"))
        self.controls = {c["control_id"]: c for c in payload["controls"]}

    def evaluate(self, control_id: str, *, principal: Principal, context: dict[str, Any]) -> PolicyDecision:
        if control_id not in self.controls:
            return PolicyDecision(False, control_id, "unknown mandatory control")
        control = self.controls[control_id]
        if not control.get("enabled", True):
            return PolicyDecision(False, control_id, "control disabled")
        required_roles = tuple(control.get("required_roles", []))
        if required_roles and not any(r in principal.roles for r in required_roles):
            return PolicyDecision(False, control_id, "required role missing")
        predicates = control.get("predicates", {})
        for key, expected in predicates.items():
            if context.get(key) != expected:
                return PolicyDecision(False, control_id, f"predicate failed: {key}")
        return PolicyDecision(True, control_id, "policy satisfied", bool(control.get("approval_required", False)))
