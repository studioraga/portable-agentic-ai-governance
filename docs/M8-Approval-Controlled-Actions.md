# Milestone 8 — Approval-controlled actions

M8 introduces exactly four bounded side effects: `incident.create`, `rerun.request`, `ticket.create`, and `model.quarantine`. Every call passes `schema -> authorization -> policy -> budget -> approval -> audit` before executor access.

Approvals are independently issued by an operator/human authority and signed with the dedicated M8 Ed25519 approval key. The approval private key remains on the release/approval-authority node; verifier/executor nodes receive only `approval-signing-public.pem`. Every approval is bound to the exact tool, canonical resource, requester, run/call identity, canonical arguments SHA-256, request SHA-256, issuance/expiry times, and `max_uses=1`. The signed M8 policy controls the default/max TTL and allowed clock skew. The agent cannot issue or self-approve approvals, accept risk, certify compliance, approve exceptions, delegate, or gain arbitrary shell/network/filesystem capability.

Replay state and action-effect journals are owner-private durable local state under the M8 runtime action root and are preserved across M8 redeployment. An approval is claimed before the pre-execution allow audit; if that audit is unavailable, the approval remains consumed and no side effect runs. If a side effect commits but the result audit cannot be persisted, the CLI reports `effect_committed=true` and writes an owner-private reconciliation record so operators do not mistake the outcome for an unexecuted action.

Reference side effects are owner-private durable local records; external incident/ticket/model-registry adapters are deployment-specific extensions behind the same boundary.

## M12 integration

M12 has no regulatory submission side effect. If later milestones introduce external reporting or notification actions, they must remain behind M8 approval controls rather than being granted directly to the M12 intelligence engine.

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
