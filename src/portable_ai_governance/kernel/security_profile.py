from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from ..security.policy_adapter import LocalPolicyAdapter
from ..security.runtime import SecurityDependencyError, build_runtime_dependencies
from ..security.tls_transport import validate_tls_material


@dataclass(frozen=True)
class SecurityCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class SecurityReport:
    profile: str
    checks: tuple[SecurityCheck, ...]

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks)


def signing_keys_are_independent(values: list[bytes] | tuple[bytes, ...], expected: int | None = None) -> bool:
    count = len(values) if expected is None else expected
    return len(values) == count and len(set(values)) == count

def evaluate_security_profile(environ: dict[str, str] | None = None) -> SecurityReport:
    env = dict(os.environ if environ is None else environ)
    profile = env.get("PAG_SECURITY_PROFILE", "lab").strip().lower()
    checks: list[SecurityCheck] = []

    if profile not in {"lab", "production"}:
        return SecurityReport(profile, (SecurityCheck("profile", False, "must be lab or production"),))
    checks.append(SecurityCheck("profile", True, profile))

    if profile == "lab":
        checks.append(SecurityCheck("fail_closed", True, "lab profile"))
        return SecurityReport(profile, tuple(checks))

    checks.append(SecurityCheck("fail_closed", env.get("PAG_FAIL_CLOSED", "") == "1", "must be enabled"))
    checks.append(SecurityCheck("mtls_required", env.get("PAG_MTLS_REQUIRED", "") == "1", "must be enabled"))
    node_id = env.get("PAG_NODE_ID", "").strip()
    checks.append(SecurityCheck("node_id", bool(node_id), node_id or "PAG_NODE_ID required"))

    try:
        deps = build_runtime_dependencies(env)
    except Exception as exc:
        checks.append(SecurityCheck("runtime_dependencies", False, str(exc)))
        return SecurityReport(profile, tuple(checks))

    ok, detail = deps.identity.health()
    checks.append(SecurityCheck("identity_provider", ok, detail))

    ok, detail = deps.secrets.health()
    checks.append(SecurityCheck("secret_provider", ok, detail))

    secrets: list[bytes] = []
    for name in ("evidence_signing", "request_signing", "approval_signing", "audit_signing"):
        try:
            value = deps.secrets.get(name, minimum_bytes=32)
            secrets.append(value)
            checks.append(SecurityCheck(f"secret:{name}", True, "configured"))
        except Exception as exc:
            checks.append(SecurityCheck(f"secret:{name}", False, str(exc)))
    separated = signing_keys_are_independent(secrets, expected=4)
    checks.append(SecurityCheck("signing_key_separation", separated, "independent" if separated else "all signing domains must use independent keys"))

    try:
        policy = LocalPolicyAdapter(deps.policy_catalog)
        ok, detail = policy.health()
    except Exception as exc:
        ok, detail = False, str(exc)
    checks.append(SecurityCheck("policy_provider", ok, detail))

    if deps.tls is None:
        checks.append(SecurityCheck("mtls_material", False, "mTLS material missing"))
    else:
        ok, detail = validate_tls_material(deps.tls)
        checks.append(SecurityCheck("mtls_material", ok, detail))

    audit_parent = deps.audit_log.parent
    try:
        audit_parent.mkdir(parents=True, exist_ok=True)
        mode = audit_parent.stat().st_mode & 0o777
        audit_ok = (mode & 0o077) == 0
        checks.append(SecurityCheck("audit_path", audit_ok, f"mode {oct(mode)}"))
    except OSError as exc:
        checks.append(SecurityCheck("audit_path", False, str(exc)))

    try:
        limit = int(env.get("PAG_RATE_LIMIT", "60"))
        window = int(env.get("PAG_RATE_WINDOW_SEC", "60"))
        rate_ok = limit > 0 and window > 0
    except ValueError:
        rate_ok = False
    checks.append(SecurityCheck("rate_limit", rate_ok, "configured" if rate_ok else "positive integer limit/window required"))

    if env.get("PAG_SUPPLY_CHAIN_REQUIRED", "0") == "1":
        try:
            from ..supply_chain.runtime import evaluate_supply_chain
            supply = evaluate_supply_chain(env)
            checks.append(SecurityCheck("supply_chain", supply.ok, "verified" if supply.ok else "; ".join(f"{n}:{d}" for n,o,d in supply.checks if not o)))
        except Exception as exc:
            checks.append(SecurityCheck("supply_chain", False, str(exc)))

    if env.get("PAG_AI_SECURITY_REQUIRED", "0") == "1":
        try:
            from ..ai_security.runtime import evaluate_ai_security
            ai = evaluate_ai_security(env)
            checks.append(SecurityCheck("ai_security", ai.ok, "verified" if ai.ok else "; ".join(f"{n}:{d}" for n,o,d in ai.checks if not o)))
        except Exception as exc:
            checks.append(SecurityCheck("ai_security", False, str(exc)))

    if env.get("PAG_COMPLIANCE_RISK_REQUIRED", "0") == "1":
        try:
            from ..compliance_risk.runtime import evaluate_compliance_risk
            cr = evaluate_compliance_risk(env)
            checks.append(SecurityCheck("compliance_risk", cr.ok, "verified" if cr.ok else "; ".join(f"{n}:{d}" for n,o,d in cr.checks if not o)))
        except Exception as exc:
            checks.append(SecurityCheck("compliance_risk", False, str(exc)))

    if env.get("PAG_EVIDENCE_ANALYST_REQUIRED", "0") == "1":
        try:
            from ..evidence_analyst.runtime import evaluate_evidence_analyst
            ea = evaluate_evidence_analyst(env)
            checks.append(SecurityCheck("evidence_analyst", ea.ok, "verified-read-only" if ea.ok else "; ".join(f"{n}:{d}" for n,o,d in ea.checks if not o)))
        except Exception as exc:
            checks.append(SecurityCheck("evidence_analyst", False, str(exc)))

    return SecurityReport(profile, tuple(checks))


def require_security_profile(environ: dict[str, str] | None = None) -> SecurityReport:
    report = evaluate_security_profile(environ)
    if not report.ok:
        failed = "; ".join(f"{c.name}: {c.detail}" for c in report.checks if not c.ok)
        raise RuntimeError(f"security profile rejected: {failed}")
    return report
