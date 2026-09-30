# Milestone 4 Validation

Run dependencies first:

```bash
./scripts/m4/preflight_dependencies.sh
```

Local positive/negative gate:

```bash
./scripts/m4/validate_m4_local.sh
```

The negative suite proves cross-tenant retrieval rejection, failed-evaluation rejection, autonomy rejection, and model-digest-drift rejection.

Node verifier:

```bash
./scripts/m4/preflight_m4.sh ~/.config/portable-ai-governance/m4/m4.env
python3 scripts/m4/validate_m4_node.py ~/.config/portable-ai-governance/m4/m4.env
```

Combined production gate:

```bash
./scripts/m4/validate_combined_node.sh \
  ~/.config/portable-ai-governance/m2/production.env \
  ~/.config/portable-ai-governance/m3/m3.env \
  ~/.config/portable-ai-governance/m4/m4.env
```

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.
