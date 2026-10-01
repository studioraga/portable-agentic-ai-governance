# Milestone 3 Validation

## Local deterministic acceptance

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q
./scripts/m2/validate_m2_local.sh
./scripts/m3/validate_m3_local.sh
python scripts/check_control_mapping.py
```

Expected M3 negative controls include:

- modified prompt rejected by digest lock;
- mutable/non-digest-pinned container reference rejected;
- modified signed SBOM rejected;
- high/critical vulnerability rejected;
- stale/unknown vulnerability data rejected by policy;
- private release signing key rejected from Node2 verifier deployment.

## Node validation

```bash
./scripts/m3/preflight_m3.sh ~/.config/portable-ai-governance/m3/m3.env
python scripts/m3/validate_m3_node.py ~/.config/portable-ai-governance/m3/m3.env
./scripts/m3/validate_combined_node.sh \
  ~/.config/portable-ai-governance/m2/production.env \
  ~/.config/portable-ai-governance/m3/m3.env
```

Production acceptance requires `PAG_SUPPLY_CHAIN_REQUIRED=1` and a non-fixture vulnerability report unless an operator explicitly opts into fixture mode for testing.

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
