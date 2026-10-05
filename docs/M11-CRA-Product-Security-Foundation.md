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

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.

## M18 integration

M18 assembles the CRA Article 31 / Annex VII technical-documentation evidence file from the evidence produced by M3-M17. This document remains an input/reference to that assembly; M18 does not retroactively change this milestone's scope. The M18 technical file is explicitly a draft evidence package: it makes no CRA conformity claim, does not perform a conformity assessment, does not authorize CE marking, and does not fabricate the EU Declaration of Conformity. Product-specific production/security test evidence that remains incomplete is carried forward to M19 as an explicit readiness gap.

## M19 integration — CRA Node1/Node2 Production Validation

M19 consumes this milestone's evidence as part of the heterogeneous Node1/Node2 production-validation chain. The M19 signed validation bundle binds the frozen CRA baselines, checks source/version/platform parity and verifier-key isolation, and supplies a production-evidence candidate for Annex I Part II(3) regular product-security testing. M19 does not rewrite this milestone's historical claims, perform conformity assessment, or make a CRA conformity claim.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.
