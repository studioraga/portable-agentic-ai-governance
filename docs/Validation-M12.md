# Validation — M12

M12 acceptance is deterministic and offline.

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q
./scripts/m12/validate_m12_local.sh
```

The fixtures must exercise:

1. affected CVE with no exploitation evidence -> `NOT_AEV`;
2. affected high-severity CVE with authoritative exploitation evidence -> `AEV_CANDIDATE`;
3. exploited vulnerability absent from product -> `NOT_AFFECTED`;
4. conflicting authoritative exploitation evidence -> `INCOMPLETE`;
5. stale intelligence -> fail closed;
6. unapproved source -> reject;
7. alias de-duplication;
8. malicious-actor information preserved without inference;
9. tampered signed material -> reject;
10. Node2 package/private-key isolation -> reject any private-key-bearing material.

M12 must also prove `starts_statutory_clock=false`, `enisa_submission=false`, and `cra_conformity_claim=false`.

## Node-specific verifier scripts

```bash
# Node1 after material generation
./scripts/m12/verify_node1.sh "$PWD/var/m12-material"

# Node2 after verifier-only deployment
./scripts/m12/verify_node2.sh "$HOME/.config/portable-ai-governance/m12"

# Full M0-M12 regression on a qualified node
./scripts/m12/validate_m12_regression.sh
```

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
