from __future__ import annotations

import os
from portable_ai_governance.kernel.authorization import AuthorizationEngine, AuthorizationRule
from portable_ai_governance.kernel.replay_cache import PersistentNonceCache
from portable_ai_governance.kernel.request_signing import sign_request
from portable_ai_governance.kernel.types import Principal
from portable_ai_governance.security.audit import SecurityAuditLog
from portable_ai_governance.security.gateway import SecurityGateway, SecurityRequest
from portable_ai_governance.security.rate_limit import FixedWindowRateLimiter
from portable_ai_governance.security.secrets import FileSecretProvider, SecretError


def test_file_secret_provider_permissions(tmp_path):
    root=tmp_path/'secrets'; root.mkdir(); os.chmod(root,0o700)
    f=root/'request_signing.key'; f.write_bytes(b'x'*32); os.chmod(f,0o600)
    assert FileSecretProvider(root).get('request_signing') == b'x'*32
    os.chmod(f,0o644)
    try: FileSecretProvider(root).get('request_signing')
    except SecretError: return
    raise AssertionError('open secret accepted')


def test_gateway_signature_replay_abac_rate_and_audit(tmp_path):
    key=b'r'*32; audit_key=b'a'*32
    auth=AuthorizationEngine((AuthorizationRule('security.ping',('node_client',),'node/node1/',principal_attributes={'environment':('production',)},resource_attributes={'environment':('production',)}),))
    gateway=SecurityGateway(request_signing_key=key,replay_cache=PersistentNonceCache(tmp_path/'nonces.json'),authorization=auth,rate_limiter=FixedWindowRateLimiter(1,60),audit=SecurityAuditLog(tmp_path/'audit.jsonl',audit_key),max_skew_sec=300)
    principal=Principal('node2',('node_client',),{'environment':'production'})
    body=b'{}'
    s1=sign_request(key,method='POST',path='/secure-ping',body=body,timestamp=1000,nonce='n1')
    req=SecurityRequest(principal,'POST','/secure-ping',body,s1,'security.ping','node/node1/security-probe',{'environment':'production'})
    assert gateway.authorize(req,now=1000).allowed
    assert not gateway.authorize(req,now=1000).allowed
    s2=sign_request(key,method='POST',path='/secure-ping',body=body,timestamp=1000,nonce='n2')
    req2=SecurityRequest(principal,'POST','/secure-ping',body,s2,'security.ping','node/node1/security-probe',{'environment':'production'})
    d=gateway.authorize(req2,now=1000); assert not d.allowed and d.reason=='rate limit exceeded'
    assert gateway.audit.verify()[0]
