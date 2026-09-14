from __future__ import annotations

from portable_ai_governance.kernel.security_profile import evaluate_security_profile


def test_production_fails_closed_without_m2_dependencies():
    report=evaluate_security_profile({'PAG_SECURITY_PROFILE':'production','PAG_FAIL_CLOSED':'1','PAG_MTLS_REQUIRED':'1','PAG_NODE_ID':'node1'})
    assert not report.ok
    assert any(c.name=='runtime_dependencies' and not c.ok for c in report.checks)
