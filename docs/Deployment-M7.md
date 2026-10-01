# M7 deployment

Node1 release authority:

```bash
./deploy/m7/one_shot_node1.sh "$PWD/var/m6-material" "$PWD/var/m7-material"
./deploy/m7/package_verifier_material.sh "$PWD/var/m7-material" "$PWD/../m7-verifier-material.tar.gz"
```

Node2 verifier:

```bash
./deploy/m7/one_shot_node2.sh /path/to/m7-material /path/to/m6/evidence-analyst-manifest.json
```

Never transfer M7 `signing-private.pem`. M7 execution uses the node's existing M2 audit-signing secret and M6 read-only evidence material.

## Release-generation freeze and M5 continuous-control refresh

M6 and M7 cryptographically bind the exact M5 compliance-risk manifest. Therefore a background refresh of the same release-authority `var/m5-material` after M6/M7 are built invalidates the downstream chain. For an M7 release:

1. Disable `pag-m5-continuous-controls.timer` before generating the final M4-M7 release generation.
2. Run `deploy/m7/one_shot_node1_full.sh`; it verifies M4->M5->M6->M7 and writes `var/m5-material/.pag-downstream-bound.json`.
3. Do not refresh that frozen M5 directory in place. A new continuous-control attestation requires a new M5 generation followed by M6 and M7 rebuild/re-signing and verifier redistribution.
4. Package and distribute M4, M5, M6 and M7 verifier materials from the same frozen generation.

The M5 timer installer and refresh command fail closed when pointed at downstream-bound M5 release material.

For release distribution, prefer the chain packager over four independent commands:

```bash
./deploy/m7/package_verifier_chain.sh \
  "$PWD/var/m4-material" "$PWD/var/m5-material" \
  "$PWD/var/m6-material" "$PWD/var/m7-material" \
  "$PWD/../m7-verifier-chain-final"
```

It verifies M4->M5->M6->M7 first, creates verifier-only bundles for all four milestones, checks private signing keys are absent, and emits `release-chain.json` plus `verifier-chain.sha256`.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

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
