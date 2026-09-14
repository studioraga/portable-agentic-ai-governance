#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import json
import os
from pathlib import Path

from portable_ai_governance.kernel.request_signing import sign_request
from portable_ai_governance.security.runtime import build_runtime_dependencies
from portable_ai_governance.security.tls_transport import build_client_context


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", required=True)
    p.add_argument("--port", type=int, default=9443)
    p.add_argument("--nonce")
    p.add_argument("--timestamp", type=int)
    p.add_argument("--tamper-signature", action="store_true")
    args = p.parse_args()

    deps = build_runtime_dependencies()
    if deps.tls is None:
        raise SystemExit("mTLS material required")
    body = json.dumps({"ping": "m2", "node": os.environ.get("PAG_NODE_ID", "unknown")}, sort_keys=True).encode()
    key = deps.secrets.get("request_signing")
    signed = sign_request(key, method="POST", path="/secure-ping", body=body, timestamp=args.timestamp, nonce=args.nonce)
    signature = ("0" * len(signed.signature)) if args.tamper_signature else signed.signature
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
        "X-PAG-Timestamp": str(signed.timestamp),
        "X-PAG-Nonce": signed.nonce,
        "X-PAG-Body-SHA256": signed.body_sha256,
        "X-PAG-Signature": signature,
    }
    conn = http.client.HTTPSConnection(args.host, args.port, context=build_client_context(deps.tls, check_hostname=True), timeout=5)
    conn.request("POST", "/secure-ping", body=body, headers=headers)
    response = conn.getresponse()
    payload = response.read().decode()
    print(json.dumps({"status": response.status, "body": json.loads(payload)}, indent=2))
    return 0 if response.status == 200 else 2


if __name__ == "__main__":
    raise SystemExit(main())
