# Milestone 5 validation

## Dependency gate

```bash
./scripts/m5/preflight_dependencies.sh
```

## Local acceptance

```bash
./scripts/m5/validate_m5_local.sh
```

The suite must reject:

- expired approved exceptions;
- privacy assessments requiring DPIA when DPIA is not approved;
- stale continuous-control evidence;
- automated compliance certification claims.

## Node verification

```bash
./scripts/m5/preflight_m5.sh ~/.config/portable-ai-governance/m5/m5.env
python3 scripts/m5/validate_m5_node.py ~/.config/portable-ai-governance/m5/m5.env
```

## Combined production gate

```bash
./scripts/m5/validate_combined_node.sh \
  ~/.config/portable-ai-governance/m2/production.env \
  ~/.config/portable-ai-governance/m3/m3.env \
  ~/.config/portable-ai-governance/m4/m4.env \
  ~/.config/portable-ai-governance/m5/m5.env
```

Production acceptance requires all four milestone control planes to verify.

## Continuous-control operations gate

Validate that the refresh command succeeds only while the Node1 release-authority private key is present. Confirm the verifier bundle excludes that key. If refreshed evidence is not redistributed before `max_age_hours` expires, Node2/production verification must fail closed as stale.

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.
