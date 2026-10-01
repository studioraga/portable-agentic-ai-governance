# M11 — CRA Product Security Foundation

M11 creates the authoritative engineering specification for future CRA work. It does **not** claim CRA conformity and does not implement ENISA reporting side effects.

## Authority split

- **Node1 — CRA release authority:** owns the authoritative requirement matrix, produces deterministic coverage reports, and signs the M11 manifest. The M11 private signing key remains on Node1.
- **Node2 — CRA independent verifier:** receives only verifier material, verifies signature/digests and runs read-only M11 checks. Node2 must not receive M11 private signing material.

## Authoritative inputs

`governance/cra/cra-requirements.json` maps manufacturer/product-security obligations to current M0-M10 implementation, current coverage (`met`, `partial`, `gap`), a future `CRA-*` control, and the target milestone M11-M20.

The matrix covers the M11 engineering baseline for Article 13, Article 14, Article 31, Annex I Parts I-II, Annex II, and Annex VII. Obligation text is paraphrased for engineering use; the exact `legal_reference` controls and must be checked against the current EUR-Lex text.

## M11 non-goals

M11 does not implement active-exploitation intelligence, statutory deadline clocks, SRP submission, PSIRT/CVD intake, user notification, secure update distribution, technical-file generation, conformity assessment, or CE/DoC issuance. Those are explicitly assigned to M12-M20.

## Local validation

```bash
./scripts/m11/validate_m11_local.sh
```

## Node1

```bash
./deploy/m11/one_shot_node1.sh ./var/m11-material
./deploy/m11/package_verifier_material.sh ./var/m11-material ./var/m11-verifier.tar.gz
```

Transfer only the verifier package/material to Node2. Never transfer `signing-private.pem`.

## Node2

After extracting the verifier package:

```bash
./deploy/m11/one_shot_node2.sh /path/to/m11-material
```

A passing M11 validation proves integrity and traceability of the CRA engineering baseline; it does not prove CRA legal conformity.

## M12 implementation hand-off

M12 implements the vulnerability/exploitation-intelligence precursor for selected M11 requirements while leaving the M11 matrix immutable. In particular, M12 advances engineering evidence for `CRA-REQ-005`, `CRA-REQ-023`, `CRA-REQ-028`, and `CRA-REQ-058`; Article 14 reporting submission remains deferred to M14 and the statutory clock remains deferred to M13.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
