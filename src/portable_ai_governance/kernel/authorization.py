from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .types import Principal


@dataclass(frozen=True)
class AuthorizationRule:
    action: str
    roles: tuple[str, ...]
    resource_prefix: str = ""
    principal_attributes: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    resource_attributes: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    effect: str = "allow"


class AuthorizationEngine:
    """Deterministic RBAC + ABAC engine with deny-overrides semantics."""

    def __init__(self, rules: tuple[AuthorizationRule, ...]):
        self.rules = rules

    @staticmethod
    def _attrs_match(actual: Mapping[str, str], required: Mapping[str, tuple[str, ...]]) -> bool:
        for key, allowed in required.items():
            if actual.get(key) not in allowed:
                return False
        return True

    def authorize(
        self,
        principal: Principal,
        *,
        action: str,
        resource: str,
        resource_attributes: Mapping[str, str] | None = None,
    ) -> tuple[bool, str]:
        rattrs = dict(resource_attributes or {})
        matching = [
            rule for rule in self.rules
            if rule.action == action and resource.startswith(rule.resource_prefix)
        ]
        if not matching:
            return False, "no authorization rule"

        eligible = []
        for rule in matching:
            role_ok = any(role in principal.roles for role in rule.roles)
            if not role_ok:
                continue
            if not self._attrs_match(principal.attributes, rule.principal_attributes):
                continue
            if not self._attrs_match(rattrs, rule.resource_attributes):
                continue
            eligible.append(rule)

        if any(rule.effect == "deny" for rule in eligible):
            return False, "explicit deny rule"
        if any(rule.effect == "allow" for rule in eligible):
            return True, "RBAC/ABAC rule allowed"
        return False, "principal/resource attributes did not satisfy policy"
