# M16 Validation

Run `scripts/m16/validate_m16_local.sh` for focused acceptance and `scripts/m16/validate_m16_regression.sh` for the full M0-M16 regression plus M11-M16 acceptance chain.

Required negative tests on Node2: tampered `security-update.bin` must fail verification, tampered `security-update.json` must fail signature validation, rollback/non-monotonic version must be rejected in unit tests, and any verifier bundle containing `signing-private.pem` must be rejected.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.
