from __future__ import annotations

from portable_ai_governance.kernel.security_profile import (
    evaluate_security_profile,
    signing_keys_are_independent,
)


def test_signing_key_separation_primitive():
    assert signing_keys_are_independent([b'a'*32,b'b'*32,b'c'*32,b'd'*32], expected=4)
    assert not signing_keys_are_independent([b'a'*32,b'a'*32,b'c'*32,b'd'*32], expected=4)


def test_m2_production_rejects_legacy_environment_only_profile():
    env={
        'PAG_SECURITY_PROFILE':'production',
        'PAG_FAIL_CLOSED':'1',
        'PAG_MTLS_REQUIRED':'1',
        'PAG_NODE_ID':'node1',
        'PAG_EVIDENCE_SIGNING_KEY':'a'*64,
        'PAG_REQUEST_SIGNING_KEY':'b'*64,
        'PAG_APPROVAL_SIGNING_KEY':'c'*64,
    }
    report=evaluate_security_profile(env)
    assert not report.ok
    assert any(c.name=='runtime_dependencies' and not c.ok for c in report.checks)
