#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import json
import os
import ssl
import threading
import secrets
from pathlib import Path

from portable_ai_governance.kernel.request_signing import sign_request
from portable_ai_governance.kernel.security_profile import evaluate_security_profile
from portable_ai_governance.security.runtime import build_runtime_dependencies
from portable_ai_governance.security.tls_transport import build_client_context
from portable_ai_governance.services.security_probe import build_server


def load_env(path: Path) -> dict[str,str]:
    out={}
    for raw in path.read_text().splitlines():
        raw=raw.strip()
        if not raw or raw.startswith('#'): continue
        k,v=raw.split('=',1); out[k]=v
    return out


def apply(env: dict[str,str]):
    for k in list(os.environ):
        if k.startswith('PAG_'): os.environ.pop(k)
    os.environ.update(env)


def send(host,port,ctx,key,nonce,*,tamper=False):
    body=b'{"ping":"m2"}'
    s=sign_request(key,method='POST',path='/secure-ping',body=body,nonce=nonce)
    sig='0'*len(s.signature) if tamper else s.signature
    headers={'Content-Type':'application/json','Content-Length':str(len(body)),'X-PAG-Timestamp':str(s.timestamp),'X-PAG-Nonce':s.nonce,'X-PAG-Body-SHA256':s.body_sha256,'X-PAG-Signature':sig}
    c=http.client.HTTPSConnection(host,port,context=ctx,timeout=3)
    c.request('POST','/secure-ping',body=body,headers=headers)
    r=c.getresponse(); data=json.loads(r.read().decode()); c.close(); return r.status,data


def main():
    p=argparse.ArgumentParser(); p.add_argument('--node1-env',required=True); p.add_argument('--node2-env',required=True); a=p.parse_args()
    n1=load_env(Path(a.node1_env)); n2=load_env(Path(a.node2_env))
    apply(n1); r=evaluate_security_profile(); assert r.ok, r
    server=build_server('127.0.0.1',0); port=server.server_port
    t=threading.Thread(target=server.serve_forever,daemon=True); t.start()
    try:
        apply(n2); r=evaluate_security_profile(); assert r.ok, r
        d2=build_runtime_dependencies(); assert d2.tls
        key=d2.secrets.get('request_signing')
        ctx=build_client_context(d2.tls,check_hostname=True)
        prefix=secrets.token_hex(8)
        status,_=send('127.0.0.1',port,ctx,key,f'{prefix}-positive'); assert status==200, status
        print('PASS mtls-signed-authorized-request')
        status,_=send('127.0.0.1',port,ctx,key,f'{prefix}-badsig',tamper=True); assert status==403, status
        print('PASS bad-signature-rejected')
        replay_nonce=f'{prefix}-replay'
        status,_=send('127.0.0.1',port,ctx,key,replay_nonce); assert status==200, status
        status,_=send('127.0.0.1',port,ctx,key,replay_nonce); assert status==403, status
        print('PASS replay-rejected')

        # Node1 cert is valid under the CA but is not authorized in Node1's workload registry as a client.
        n1deps_env=n1.copy(); apply(n1deps_env); n1deps=build_runtime_dependencies(); assert n1deps.tls
        wrong_ctx=build_client_context(n1deps.tls,check_hostname=True)
        apply(n2)
        status,_=send('127.0.0.1',port,wrong_ctx,key,f'{prefix}-wrong-workload'); assert status==403, status
        print('PASS unauthorized-workload-rejected')

        # No client certificate: TLS handshake must fail before HTTP authorization.
        no_client=ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile=n2['PAG_TLS_CA_FILE'])
        no_client.minimum_version=ssl.TLSVersion.TLSv1_3
        failed=False
        try:
            send('127.0.0.1',port,no_client,key,'m2-no-client-cert')
        except (ssl.SSLError,OSError,http.client.HTTPException):
            failed=True
        assert failed
        print('PASS missing-client-certificate-rejected')

        apply(n1)
        deps=build_runtime_dependencies(); from portable_ai_governance.security.audit import SecurityAuditLog
        ok,detail=SecurityAuditLog(deps.audit_log,deps.secrets.get('audit_signing')).verify(); assert ok,detail
        print('PASS security-audit-chain-verified')
    finally:
        server.shutdown(); server.server_close(); t.join(timeout=2)
    print('M2 TRANSPORT VALIDATION PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
