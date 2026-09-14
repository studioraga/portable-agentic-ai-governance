from __future__ import annotations

import hashlib, json, os
from portable_ai_governance.kernel.identity import FileIdentityProvider, IdentityError
from portable_ai_governance.kernel.authorization import AuthorizationEngine, AuthorizationRule
from portable_ai_governance.kernel.types import Principal


def test_file_identity_and_abac(tmp_path):
    token = "secret-token"
    p = tmp_path / "identities.json"
    p.write_text(json.dumps({"identities":[{"name":"alice","token_sha256":hashlib.sha256(token.encode()).hexdigest(),"roles":["operator"],"attributes":{"environment":"production","department":"security"}}]}))
    os.chmod(p,0o600)
    principal = FileIdentityProvider(p).authenticate(token)
    engine = AuthorizationEngine((AuthorizationRule("read",("operator",),"asset/",principal_attributes={"department":("security",)},resource_attributes={"environment":("production",)}),))
    assert engine.authorize(principal,action="read",resource="asset/1",resource_attributes={"environment":"production"})[0]
    assert not engine.authorize(principal,action="read",resource="asset/1",resource_attributes={"environment":"dev"})[0]


def test_identity_file_permissions_fail_closed(tmp_path):
    p = tmp_path / "identities.json"; p.write_text('{"identities":[]}'); os.chmod(p,0o644)
    try:
        FileIdentityProvider(p)
    except IdentityError:
        return
    raise AssertionError("open identity file accepted")
