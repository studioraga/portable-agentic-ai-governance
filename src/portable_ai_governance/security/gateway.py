from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Mapping

from ..kernel.authorization import AuthorizationEngine
from ..kernel.replay_cache import PersistentNonceCache, ReplayDetected
from ..kernel.request_signing import SignedRequest, verify_request
from ..kernel.types import Principal
from .audit import SecurityAuditLog, SecurityEvent
from .rate_limit import FixedWindowRateLimiter


@dataclass(frozen=True)
class SecurityRequest:
    principal: Principal
    method: str
    path: str
    body: bytes
    signed: SignedRequest
    action: str
    resource: str
    resource_attributes: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SecurityDecision:
    allowed: bool
    reason: str
    audit_ref: str = ""
    retry_after: int = 0


class SecurityGateway:
    """Fail-closed deterministic request security pipeline."""

    def __init__(
        self,
        *,
        request_signing_key: bytes,
        replay_cache: PersistentNonceCache,
        authorization: AuthorizationEngine,
        rate_limiter: FixedWindowRateLimiter,
        audit: SecurityAuditLog,
        max_skew_sec: int = 300,
    ):
        if len(request_signing_key) < 32:
            raise ValueError("request signing key must be at least 32 bytes")
        self.key = request_signing_key
        self.replay = replay_cache
        self.authorization = authorization
        self.rate = rate_limiter
        self.audit = audit
        self.max_skew_sec = max_skew_sec

    def _record(self, req: SecurityRequest, decision: str, reason: str, **attrs) -> str:
        return self.audit.record(SecurityEvent(
            event_type="security.request.decision",
            decision=decision,
            principal_id=req.principal.principal_id,
            action=req.action,
            resource=req.resource,
            reason=reason,
            attributes=dict(attrs),
        ))

    def authorize(self, req: SecurityRequest, *, now: int | None = None) -> SecurityDecision:
        current = int(time.time()) if now is None else int(now)
        if not verify_request(
            self.key,
            req.signed,
            method=req.method,
            path=req.path,
            body=req.body,
            max_skew_sec=self.max_skew_sec,
            now=current,
        ):
            ref = self._record(req, "deny", "request signature invalid or stale")
            return SecurityDecision(False, "request signature invalid or stale", ref)
        try:
            self.replay.consume(req.signed.nonce, now=current)
        except ReplayDetected:
            ref = self._record(req, "deny", "nonce replay detected")
            return SecurityDecision(False, "nonce replay detected", ref)
        except Exception as exc:
            ref = self._record(req, "deny", "replay store unavailable", error=type(exc).__name__)
            return SecurityDecision(False, "replay store unavailable", ref)

        allowed, reason = self.authorization.authorize(
            req.principal,
            action=req.action,
            resource=req.resource,
            resource_attributes=req.resource_attributes,
        )
        if not allowed:
            ref = self._record(req, "deny", reason)
            return SecurityDecision(False, reason, ref)

        rate_ok, retry_after = self.rate.allow(req.principal.principal_id, now=current)
        if not rate_ok:
            ref = self._record(req, "deny", "rate limit exceeded", retry_after=retry_after)
            return SecurityDecision(False, "rate limit exceeded", ref, retry_after)

        ref = self._record(req, "allow", reason)
        return SecurityDecision(True, reason, ref)
