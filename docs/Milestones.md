# Milestones

### Milestone 11

- Authoritative CRA engineering matrix with Article/Annex subparagraph locators.
- Existing M0-M10 control/source mapping and explicit `met`/`partial`/`gap` status.
- A proposed `CRA-*` control ID for every partial/gap row and target milestone M11-M20.
- Deterministic coverage report that explicitly forbids a CRA conformity claim.
- Node1 signing authority and Node2 verifier-only separation.
- Signed digest-bound M11 manifest and positive/negative acceptance tests.

# Milestone Matrix

| Milestone | Status | Primary deliverable | Release gate |
|---|---|---|---|
| 0 Schemas/Trust Kernel | Implemented | deterministic enforcement primitives | kernel positive/negative tests |
| 1 Governance foundation | Implemented | GOV-01/03/06/10 + onboarding | signed end-to-end evidence |
| 2 Security control plane | Implemented/validated | identity/RBAC+ABAC/mTLS/signing/replay/secrets/crypto/audit | M2 local+distributed positive/negative security suite |
| 3 Supply chain | Implemented/validated | SBOM/AI BOM/model-container-prompt-tool locks/provenance/signing/vulnerability policy | signed fail-closed supply-chain gate |
| 4 AI security | Implemented/validated | model governance/data provenance/RAG authorization/embedding controls/evals/threat model | signed deterministic AI-security/eval gate |
| 5 Risk/compliance automation | Implemented/validated | impact/privacy/exceptions/third parties/continuous controls/compliance reports | signed compliance/risk + continuous-control gate |
| 6 First bounded agent | Implemented/validated | read-only analyst | grounded/citation/eval gate |
| 7 Tool-using agent | Implemented/validated | typed mediated tools | schema+authorization+policy+budget+audit gate |
| 8 Approval actions | Implemented/validated | four approval-controlled typed side effects | signed independent approval + replay/audit gate |
| 9 SecOps | Implemented/validated | SIEM/IR/recovery | respond/recover gate |
| 10 Multi-agent | Implementation candidate | supervisor + Risk/Threat/Privacy + Control + Assurance + human decision | typed handoff + assurance + human-decision gate |

## Milestone 6 — First bounded agent

Status: implementation candidate. Implements Evidence Analyst only, with read-only allowlisted evidence tools, deterministic budgets, signed capability/evidence manifests, no side-effecting tools, no delegation, and no security/approval/risk/compliance authority.


## Milestone 7 — Tool-using agent

Status: implementation candidate. Adds `TOOL-ANALYST-001`, a signed typed-tool registry, signed agent/authorization policy, and a deterministic tool broker. Executors are unreachable until schema, authorization, policy and budget gates pass and the signed pre-execution audit is persisted. Side-effecting tools, direct executor access, delegation, approval, risk acceptance and compliance certification remain prohibited.


## Milestone 8 — Approval-controlled actions
M8 adds exactly four typed side effects behind independently issued signed single-use approvals. See `docs/M8-Approval-Controlled-Actions.md`.


## Milestone 9 — Security operations
M9 adds deterministic SIEM ingestion, incident response, bounded local containment, recovery verification and incident evidence preservation. See `docs/M9-Security-Operations.md`.


## Milestone 10 — Multi-agent workflows
M10 adds the first cooperating reasoning-agent workflow only after M2-M9 controls exist. The signed fixed topology is Governance Supervisor -> Risk/Threat/Privacy specialists -> Control Agent -> Assurance Agent -> independent human workflow decision. Handoffs are typed and digest-bound, workflow state is hash-chain journaled, budgets are deterministic, and M10 has no direct side-effect or SecOps authority. See `docs/M10-Multi-Agent-Workflows.md`.

### Milestone 12

- Approved vulnerability/exploitation intelligence source registry and provenance.
- OSV/vendor normalization with CVE/GHSA/other alias de-duplication.
- Product/component correlation using inventory/PURL metadata.
- Deterministic `AEV_CANDIDATE`, `NOT_AEV`, `NOT_AFFECTED`, and `INCOMPLETE` decisions.
- Fail-closed stale/conflicting/unapproved-source handling.
- Signed Node1 intelligence material and Node2 verifier-only validation.
- No M13 clock, M14 ENISA submission, or CRA conformity claim.

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
