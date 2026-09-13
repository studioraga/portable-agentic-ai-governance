from __future__ import annotations

import pytest

from portable_ai_governance.kernel.security_profile import (
    evaluate_security_profile,
    require_security_profile,
)


def production_env(
    evidence_key: str,
    request_key: str,
    approval_key: str,
) -> dict[str, str]:
    return {
        "PAG_SECURITY_PROFILE": "production",
        "PAG_FAIL_CLOSED": "1",
        "PAG_EVIDENCE_SIGNING_KEY": evidence_key,
        "PAG_REQUEST_SIGNING_KEY": request_key,
        "PAG_APPROVAL_SIGNING_KEY": approval_key,
    }


def test_production_accepts_independent_signing_keys():
    env = production_env(
        "a" * 64,
        "b" * 64,
        "c" * 64,
    )

    report = require_security_profile(env)

    assert report.ok is True

    checks = {
        check.name: check
        for check in report.checks
    }

    assert checks[
        "signing_key_separation"
    ].ok is True


def test_production_rejects_all_signing_keys_reused():
    shared = "a" * 64

    env = production_env(
        shared,
        shared,
        shared,
    )

    report = evaluate_security_profile(env)

    assert report.ok is False

    checks = {
        check.name: check
        for check in report.checks
    }

    assert checks[
        "signing_key_separation"
    ].ok is False

    with pytest.raises(RuntimeError):
        require_security_profile(env)


@pytest.mark.parametrize(
    ("evidence_key", "request_key", "approval_key"),
    [
        ("a" * 64, "a" * 64, "b" * 64),
        ("a" * 64, "b" * 64, "a" * 64),
        ("a" * 64, "b" * 64, "b" * 64),
    ],
)
def test_production_rejects_partial_signing_key_reuse(
    evidence_key,
    request_key,
    approval_key,
):
    env = production_env(
        evidence_key,
        request_key,
        approval_key,
    )

    report = evaluate_security_profile(env)

    assert report.ok is False

    checks = {
        check.name: check
        for check in report.checks
    }

    assert checks[
        "signing_key_separation"
    ].ok is False

    with pytest.raises(RuntimeError):
        require_security_profile(env)
