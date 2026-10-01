# Milestone 6 — First bounded agent: Evidence Analyst

M6 introduces the first production agent only after M2 security, M3 supply-chain, M4 AI-system security and M5 compliance/risk controls exist. The Evidence Analyst is deliberately read-only. It is not the security boundary, approval authority, risk-acceptance authority, compliance authority, or policy engine.

## Capabilities

Allowed tools are limited to `evidence.list`, `evidence.metadata`, `evidence.read`, `evidence.verify`, and `evidence.summarize`. Evidence is selected by a signed, deny-by-default catalog and copied into an owner-private evidence snapshot. Every artifact is SHA-256 bound. M6 is cryptographically bound to the exact M5 compliance/risk manifest.

## Prohibited capabilities

The agent cannot write, append, delete, execute shell commands, use network tools, modify policy, accept risk, approve exceptions, certify compliance, delegate to another agent, or invoke side-effecting tools. These are deny-list invariants validated at startup.

## Initial evidence scope

The portable initial catalog contains non-secret M3, M4 and M5 evidence. M2 continues to be enforced independently by the combined M2+M3+M4+M5+M6 production gate. M2 secret stores, tokens and production environment files are never copied into the agent evidence snapshot. A future public/signed M2 evidence adapter may be added without widening agent authority.

## No LLM dependency

The first implementation uses deterministic read-only operations and does not require an LLM runtime or external model API. A later reasoning adapter may consume these tools, but the signed capability policy and deterministic control plane remain authoritative.

## M12 integration

The bounded Evidence Analyst may read M12 signed assessments and provenance, but M12 classification is deterministic and must not be overridden by free-form model reasoning. Any explanation must remain grounded in recorded source/evidence IDs.

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
