from __future__ import annotations
from dataclasses import dataclass
from .types import Principal

@dataclass(frozen=True)
class AuthorizationRule:
    action: str
    roles: tuple[str, ...]
    resource_prefix: str = ""

class AuthorizationEngine:
    def __init__(self, rules: tuple[AuthorizationRule, ...]):
        self.rules = rules

    def authorize(self, principal: Principal, *, action: str, resource: str) -> tuple[bool, str]:
        matching = [r for r in self.rules if r.action == action and resource.startswith(r.resource_prefix)]
        if not matching:
            return False, "no authorization rule"
        for rule in matching:
            if any(role in principal.roles for role in rule.roles):
                return True, "role allowed"
        return False, "principal lacks required role"
