from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from ..kernel.policy import PolicyEngine
from ..kernel.types import PolicyDecision, Principal


class PolicyAdapter(Protocol):
    def health(self) -> tuple[bool, str]: ...
    def evaluate(self, control_id: str, *, principal: Principal, context: dict[str, Any]) -> PolicyDecision: ...


@dataclass
class LocalPolicyAdapter:
    catalog: Path

    def __post_init__(self) -> None:
        self.engine = PolicyEngine(self.catalog)

    def health(self) -> tuple[bool, str]:
        if not self.catalog.is_file():
            return False, "policy catalog missing"
        return True, "local policy catalog available"

    def evaluate(self, control_id: str, *, principal: Principal, context: dict[str, Any]) -> PolicyDecision:
        return self.engine.evaluate(control_id, principal=principal, context=context)
