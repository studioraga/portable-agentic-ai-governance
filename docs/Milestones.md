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
