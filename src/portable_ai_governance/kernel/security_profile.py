from __future__ import annotations
import os
from dataclasses import dataclass

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


def evaluate_security_profile(environ: dict[str, str] | None = None) -> SecurityReport:
    env = dict(os.environ if environ is None else environ)
    profile = env.get("PAG_SECURITY_PROFILE", "lab").strip().lower()
    checks: list[SecurityCheck] = []
    if profile not in {"lab", "production"}:
        return SecurityReport(profile, (SecurityCheck("profile", False, "must be lab or production"),))
    checks.append(SecurityCheck("profile", True, profile))
    if profile == "production":
        for var in ("PAG_EVIDENCE_SIGNING_KEY", "PAG_REQUEST_SIGNING_KEY", "PAG_APPROVAL_SIGNING_KEY"):
            value = env.get(var, "")
            checks.append(SecurityCheck(var, len(value) >= 32 and "change" not in value.lower(), "configured" if len(value) >= 32 else "missing/too short"))
        checks.append(SecurityCheck("fail_closed", env.get("PAG_FAIL_CLOSED", "1") == "1", "must be enabled"))
    return SecurityReport(profile, tuple(checks))


def require_security_profile(environ: dict[str, str] | None = None) -> SecurityReport:
    report = evaluate_security_profile(environ)
    if not report.ok:
        failed = "; ".join(f"{c.name}: {c.detail}" for c in report.checks if not c.ok)
        raise RuntimeError(f"security profile rejected: {failed}")
    return report
