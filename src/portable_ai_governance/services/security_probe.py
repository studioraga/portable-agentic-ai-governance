from __future__ import annotations

import argparse
import json
import os
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ..kernel.authorization import AuthorizationEngine, AuthorizationRule
from ..kernel.replay_cache import PersistentNonceCache
from ..kernel.request_signing import SignedRequest
from ..kernel.security_profile import require_security_profile
from ..security.audit import SecurityAuditLog
from ..security.gateway import SecurityGateway, SecurityRequest
from ..security.rate_limit import FixedWindowRateLimiter
from ..security.runtime import build_runtime_dependencies
from ..security.tls_transport import build_server_context
from ..security.workload_identity import FileWorkloadRegistry, extract_workload_identity


class ProbeHandler(BaseHTTPRequestHandler):
    server_version = "PAGSecurityProbe/0.2"

    def log_message(self, fmt, *args):
        return

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"ok": True, "service": "pag-security-probe"})
        else:
            self._json(404, {"ok": False})

    def do_POST(self):
        if self.path != "/secure-ping":
            self._json(404, {"ok": False})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 0 or size > 65536:
                self._json(413, {"ok": False, "reason": "body too large"})
                return
            body = self.rfile.read(size)
            peer_cert = self.connection.getpeercert()
            wid = extract_workload_identity(peer_cert, trust_domain=self.server.trust_domain)
            principal = self.server.workloads.resolve(wid)
            signed = SignedRequest(
                int(self.headers["X-PAG-Timestamp"]),
                self.headers["X-PAG-Nonce"],
                self.headers["X-PAG-Body-SHA256"],
                self.headers["X-PAG-Signature"],
            )
            req = SecurityRequest(
                principal=principal,
                method="POST",
                path="/secure-ping",
                body=body,
                signed=signed,
                action="security.ping",
                resource="node/node1/security-probe",
                resource_attributes={"environment": "production"},
            )
            decision = self.server.gateway.authorize(req)
            if not decision.allowed:
                status = 429 if decision.reason == "rate limit exceeded" else 403
                self._json(status, {"ok": False, "reason": decision.reason, "audit_ref": decision.audit_ref})
                return
            self._json(200, {"ok": True, "principal": principal.principal_id, "workload": wid.uri, "audit_ref": decision.audit_ref})
        except Exception as exc:
            self._json(403, {"ok": False, "reason": type(exc).__name__})


class ProbeServer(ThreadingHTTPServer):
    def __init__(self, address, handler, *, gateway, workloads, trust_domain):
        super().__init__(address, handler)
        self.gateway = gateway
        self.workloads = workloads
        self.trust_domain = trust_domain


def build_server(host: str, port: int) -> ProbeServer:
    require_security_profile()
    deps = build_runtime_dependencies()
    assert deps.tls is not None
    request_key = deps.secrets.get("request_signing")
    audit_key = deps.secrets.get("audit_signing")
    workload_registry = os.environ.get("PAG_WORKLOAD_REGISTRY", "")
    if not workload_registry:
        raise RuntimeError("PAG_WORKLOAD_REGISTRY required")
    workloads = FileWorkloadRegistry(workload_registry)
    replay = PersistentNonceCache(Path(os.environ.get("PAG_REPLAY_CACHE", "var/state/security-probe-nonces.json")))
    authz = AuthorizationEngine((
        AuthorizationRule(
            "security.ping",
            ("node_client",),
            "node/node1/",
            principal_attributes={"environment": ("production",)},
            resource_attributes={"environment": ("production",)},
        ),
    ))
    rate = FixedWindowRateLimiter(
        int(os.environ.get("PAG_RATE_LIMIT", "60")),
        int(os.environ.get("PAG_RATE_WINDOW_SEC", "60")),
    )
    audit = SecurityAuditLog(deps.audit_log, audit_key)
    gateway = SecurityGateway(
        request_signing_key=request_key,
        replay_cache=replay,
        authorization=authz,
        rate_limiter=rate,
        audit=audit,
    )
    server = ProbeServer((host, port), ProbeHandler, gateway=gateway, workloads=workloads, trust_domain=os.environ.get("PAG_TRUST_DOMAIN", "pag.local"))
    server.socket = build_server_context(deps.tls).wrap_socket(server.socket, server_side=True)
    return server


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("PAG_BIND_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PAG_BIND_PORT", "9443")))
    args = parser.parse_args(argv)
    server = build_server(args.host, args.port)
    print(f"PAG security probe listening on {args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
