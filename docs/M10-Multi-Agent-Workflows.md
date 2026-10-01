# Milestone 10 — Multi-Agent Workflows

## Purpose

M10 is the first milestone that permits multiple cooperating reasoning agents. It does **not** move authorization, side effects, security operations, risk acceptance, compliance certification, or approval authority into those agents.

```text
                GOVERNANCE-SUPERVISOR-001
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 RISK-AGENT-001   THREAT-AGENT-001  PRIVACY-AGENT-001
        |                |                |
        +----------------+----------------+
                         v
                 CONTROL-AGENT-001
                         |
                         v
                ASSURANCE-AGENT-001
                         |
                         v
              independent human decision
```

The specialist stages are logically parallel but executed deterministically by the reference implementation. This avoids nondeterministic shared-state races while preserving independent specialist outputs.

## Trust boundaries

- Supervisor owns orchestration order, case identity, budgets and handoff sequencing only.
- Specialists only generate bounded findings from their typed input domains.
- Control Agent only maps findings to deterministic governance controls.
- Assurance Agent checks evidence and control coverage and may block approval.
- Human reviewer signs the final governance disposition with a dedicated Ed25519 key.
- Approved M10 workflow output has `side_effect_authority=false`.
- M8 remains mandatory for side-effect execution.
- M9 remains authoritative for containment and recovery.
- Direct specialist-to-specialist calls are prohibited.
- Agent delegation outside the signed topology is prohibited.

## Typed handoffs

Every agent handoff uses `pag-m10-agent-handoff-v1` and carries:

- agent id and role,
- case id,
- SHA-256 of exact upstream input,
- typed output,
- SHA-256 of exact output.

The supervisor verifies the specialist input digest, Control input digest, Assurance input digest, and output digests before continuing.

## Budgets

The signed policy constrains:

- fixed agent invocation capacity,
- total case signals,
- findings per specialist,
- serialized workflow-result size.

Budget failure is fail-closed.

## Human decision

The final workflow result remains `pending-human-approval` until an independently signed decision is supplied. The signature binds:

- workflow id,
- proposal digest,
- assurance digest,
- reviewer,
- decision (`approve` or `reject`),
- issue/expiry time,
- one-use limit.

Decision replay is persistently rejected.

## Reference reasoning backend

The v0.10.0 reference backend is deterministic and offline. It normalizes risk/threat/privacy signals, maps them to existing governance controls, and performs deterministic assurance coverage checks. This proves the multi-agent control architecture without making a model runtime part of the security boundary. A future LLM/model adapter must remain behind the same typed contracts, budgets, evidence requirements, evaluations and human approval gate.

## M12 integration

M10 agents may consume M12 signed AEV candidate evidence, but no agent may change the deterministic candidate classification, start the statutory clock, submit to ENISA, or claim CRA conformity.

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
