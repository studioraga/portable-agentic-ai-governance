# Milestone 2 Validation

## Local two-node simulation on Node1

This is the fastest complete M2 acceptance run and does not need the physical Node2:

```bash
./scripts/m2/validate_m2_local.sh
```

The script:

1. generates disposable CA/node certificates;
2. generates independent protected signing keys;
3. deploys Node1 and Node2 configurations into a protected temporary tree;
4. validates both production profiles;
5. starts an mTLS Node1 security probe on loopback;
6. performs a valid Node2 signed request;
7. rejects a bad signature;
8. rejects a replay;
9. rejects an unauthorized workload certificate;
10. rejects a client with no certificate;
11. verifies the signed security audit chain;
12. removes an identity dependency and proves production fails closed.

Expected terminal line:

```text
PASS: Milestone 2 local/distributed security validation complete
```

## Node-specific validation

```bash
./scripts/m2/preflight_m2.sh ~/.config/portable-ai-governance/m2/production.env
./scripts/m2/validate_m2_node.sh ~/.config/portable-ai-governance/m2/production.env
```

## Full regression suite

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q
python scripts/run_self_tests.py
python scripts/check_control_mapping.py
python scripts/check_production_key_separation.py
python scripts/check_runtime_permissions.py
```

## Mandatory negative production tests

At minimum demonstrate failure for:

- local/bootstrap identity selected in production;
- missing identity file;
- identity file with group/world permissions;
- missing secret provider;
- missing secret file;
- secret file with group/world permissions;
- reused signing key domains;
- missing policy catalog;
- mTLS disabled;
- missing CA/cert/key;
- private TLS key with permissive mode;
- mismatched certificate/private key;
- no client certificate;
- unregistered workload URI SAN;
- modified signed body/signature;
- stale signature timestamp;
- nonce replay;
- RBAC denial;
- ABAC denial;
- rate limit exhaustion;
- replay-cache corruption/unavailability.

`UNKNOWN` or skipped mandatory security tests do not count as PASS.

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
