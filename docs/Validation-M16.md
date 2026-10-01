# M16 Validation

Run `scripts/m16/validate_m16_local.sh` for focused acceptance and `scripts/m16/validate_m16_regression.sh` for the full M0-M16 regression plus M11-M16 acceptance chain.

Required negative tests on Node2: tampered `security-update.bin` must fail verification, tampered `security-update.json` must fail signature validation, rollback/non-monotonic version must be rejected in unit tests, and any verifier bundle containing `signing-private.pem` must be rejected.
