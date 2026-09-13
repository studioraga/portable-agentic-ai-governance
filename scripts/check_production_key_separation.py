#!/usr/bin/env python3

from __future__ import annotations

from portable_ai_governance.kernel.security_profile import (
    evaluate_security_profile,
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


def require(
    name: str,
    condition: bool,
) -> None:
    if not condition:
        raise SystemExit(
            f"FAIL {name}"
        )

    print(
        f"PASS {name}"
    )


independent = evaluate_security_profile(
    production_env(
        "a" * 64,
        "b" * 64,
        "c" * 64,
    )
)

require(
    "production-independent-signing-keys",
    independent.ok,
)


cases = (
    (
        "production-all-key-reuse-rejected",
        (
            "a" * 64,
            "a" * 64,
            "a" * 64,
        ),
    ),
    (
        "production-evidence-request-reuse-rejected",
        (
            "a" * 64,
            "a" * 64,
            "b" * 64,
        ),
    ),
    (
        "production-evidence-approval-reuse-rejected",
        (
            "a" * 64,
            "b" * 64,
            "a" * 64,
        ),
    ),
    (
        "production-request-approval-reuse-rejected",
        (
            "a" * 64,
            "b" * 64,
            "b" * 64,
        ),
    ),
)


for name, values in cases:
    report = evaluate_security_profile(
        production_env(*values)
    )

    require(
        name,
        not report.ok,
    )


print(
    "KEY-SEPARATION TESTS PASS: 5/5"
)
