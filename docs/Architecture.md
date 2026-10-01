# Architecture

## 1. Core principle

Agents reason; deterministic controls authorize. Agents propose; typed executors act. Agents never become the security boundary.

```text
Enterprise governance
        |
Governance/Security/Assurance/Operations agents
        |
        v
+--------------------------------------------------+
| Deterministic Trust Kernel                       |
| identity | RBAC/ABAC | policy | approvals        |
| budgets | schemas | crypto | evidence | tools    |
+--------------------------------------------------+
        |
        v
Application adapters: camera | RAG | GenAI | SOC
```

## 2. Development hierarchy — Milestones 0 through 10

### Milestone 0 — Schemas and Trust Kernel — IMPLEMENTED
- Agent/control/risk/system/evidence schemas.
- State graph with terminal states.
- RBAC interface.
- Policy engine.
- Signed approvals.
- Bounded budgets.
- Request signing.
- Persistent replay cache.
- Chained signed evidence.
- Artifact digest verification.
- Fail-closed production security profile.

Acceptance: illegal transitions, budget overflow, tampered requests, replay, unknown policy controls, weak production profiles and evidence tampering fail closed.

### Milestone 1 — Governance foundation — IMPLEMENTED
- GOV-01 AI System Inventory Agent.
- GOV-03 AI Risk Agent.
- GOV-06 Control Mapping Agent.
- GOV-10 Governance Evidence Agent.
- Golden onboarding workflow.

Acceptance: one AI system -> risk -> controls -> framework mappings -> signed evidence can be traced end to end. Unauthorized onboarding is denied. Agent risk acceptance is rejected.

### Milestone 2 — Security control plane — NEXT
Implement enterprise identity adapters, RBAC+ABAC, mTLS/workload identity, secrets abstraction, API security middleware, signed inter-service messages, rate limits, secure configuration drift, security event schema, and policy-as-code adapter.

Acceptance: production profile cannot start without required identity/crypto/policy dependencies; negative authentication/authorization/replay/TLS tests pass.

### Milestone 3 — Supply chain
Implement software SBOM, model/AI BOM, prompt/tool/agent locks, container/model signatures, SLSA-style provenance, vulnerability/VEX policy, secret scanning and release gates.

Acceptance: unapproved digest, unsigned critical artifact, exploitable critical vulnerability, stale exception, or missing provenance blocks promotion.

### Milestone 4 — AI system security
Implement model governance, dataset provenance, authorization-first RAG, digest-locked retrieval/reranking, AI evaluation, threat model and model/data integrity checks.

Acceptance: cross-tenant/resource retrieval, unknown model digest, index poisoning test fixture, or failed AI quality/security threshold blocks the operation.

### Milestone 5 — Compliance and risk automation
Implement AI impact assessment, privacy/data classification, retention/legal hold, exception lifecycle, third-party AI registry, regulatory obligations and continuous controls.

Acceptance: high/critical systems cannot reach production without owners, impact assessment, current risks, valid exceptions, and required privacy controls.

### Milestone 6 — First bounded agent
Add one read-only Evidence/Assurance Analyst with versioned model/prompt/tool identity, durable checkpoints, citation requirements, output validation and no side-effect tools.

### Milestone 7 — Tool-using agent
Add typed least-privilege tools. Every tool call passes schema -> principal authorization -> agent authorization -> policy -> budget -> audit.

### Milestone 8 — Approval-controlled actions
Permit exactly four bounded reference side effects: `incident.create`, `rerun.request`, `ticket.create`, and `model.quarantine`. Every call passes schema -> authorization -> policy -> budget -> approval -> audit. Approval is an independent Ed25519-signed, exact-arguments-bound, short-lived, single-use artifact; ACTION-AGENT-001 cannot sign or self-approve it. Node2 receives the approval public key only. Reference executors write owner-private durable local state; external systems remain deployment adapters behind the same boundary.

### Milestone 9 — Security operations
Add SIEM/OpenTelemetry security events, incident triage, evidence preservation, containment, credential/key incident response, recovery and postmortem control feedback.

### Milestone 10 — Multi-agent workflows
Add supervisor-directed specialist workflows only after measured need. Supervisor owns sequence/state/dependencies/budgets, not authorization, risk acceptance, policy override, or approvals.

## 3. Reusable workflow 88 — AI system onboarding

Implemented golden path:

```text
START
 -> VALIDATE_REQUEST
 -> AUTHORIZE
 -> LOAD_TRUSTED_CONTEXT
 -> PLAN
 -> POLICY_VALIDATE_PLAN
 -> EXECUTE_BOUNDED_TOOLS
      -> inventory
      -> risk
      -> control mapping
 -> VERIFY_OUTPUT
 -> RECORD_EVIDENCE
 -> COMPLETE
```

Future Milestone 5 expands this same workflow with data classification, provider assessment, impact assessment, threat model, privacy review, AI evaluation, supply-chain verification and human production approval.

## 4. Reusable workflow 89 — model promotion

Planned deterministic sequence:
`candidate -> immutable digest -> license/provider -> vulnerability/security scan -> AI evaluation -> red team -> risk delta -> model BOM/SBOM -> human approval -> signed lock -> production registry`.

## 5. Reusable workflow 90 — controlled AI inference

Planned generic sequence:
`request -> identity -> authorization -> policy -> approved model -> digest verification -> authorized evidence -> bounded execution -> output validation -> signed evidence`.

## 6. Reusable workflow 91 — secure RAG

Planned invariant: authorize before retrieval. The server constructs resource/tenant filters. Reranking may only process already-authorized candidates. Output is citation-checked and DLP-checked.

## 7. Reusable workflow 92 — tool execution

`agent proposes -> tool exists -> input schema -> user/workload authorized -> agent authorized -> policy -> approval if required -> budget -> executor -> signed audit result`.
Tool outputs return to an LLM as untrusted data, never as instruction authority.

## 8. Reusable workflow 93 — incident response

`detect -> triage -> preserve -> contain proposal -> policy/approval -> contain -> investigate -> recover -> validate -> postmortem -> risk/control update`.

## 9. What an LLM may and may not do — workflow 94

Allowed: summarize, classify, correlate, recommend, generate hypotheses, draft controls, explain policy decisions.
Forbidden authority: authentication, authorization, cryptographic verification, risk acceptance, privileged approval, deleting protected evidence, arbitrary shell execution, policy override.

## 10. Testing hierarchy — workflow 95

Every agent/control receives unit, schema, policy, permission, budget, negative, adversarial, integration, evidence and acceptance tests. An allowed-path test is never sufficient without denied-path tests.

## 11. Required fail-closed tests — workflow 96

Unknown model digest, expired approval, unknown tool, invalid schema, wrong tenant/resource, policy unavailable, missing mandatory evidence, expired identity, replay, exhausted budget and illegal transition must fail closed.

## 12. Golden acceptance — workflow 97

Specification -> reference implementation -> positive/negative tests -> runtime evidence -> score/decision. No production claim is based only on prose documentation.

## 13. Production scorecard — workflow 98

Mandatory gates: Security, Privacy, AI Evaluation, Supply Chain, Threat Assessment, Risk, Control Evidence, Exceptions, Human Approval, Observability, Incident Response and Recovery.

## 14. Decision rule — workflow 99

No weighted average may hide a mandatory control failure. A mandatory security/privacy/safety control failure yields `RELEASE_BLOCKED` regardless of high model accuracy.

## 15. M0-M1 production cryptographic-domain separation

The bootstrap production profile has three independent symmetric-key domains:

```text
PAG_EVIDENCE_SIGNING_KEY
    -> governance/evidence envelope integrity

PAG_REQUEST_SIGNING_KEY
    -> signed request authentication and body integrity

PAG_APPROVAL_SIGNING_KEY
    -> privileged approval artifact integrity
```

The same secret MUST NOT be reused across any pair of these domains. Production preflight and the deterministic security-profile evaluator both enforce this rule and fail closed on full or partial reuse. This is an M0-M1 bootstrap control; M2 replaces direct environment-secret dependency with a provider abstraction and managed key lifecycle.

## 16. M0-M1 runtime privacy boundary

Runtime governance evidence and workflow state are private-by-default local security material. The required filesystem contract is:

```text
var/            0700
var/evidence/   0700
var/runs/       0700
var/state/      0700
runtime files   0600
```

Deployment and validation execute with `umask 077`. The evidence ledger also forces its file to `0600` after append and `fsync`, so its confidentiality does not depend solely on the invoking shell's umask. Runtime permission validation is part of the M0-M1 acceptance evidence.


## Milestone 4 boundary
Milestone 4 adds deterministic AI-system-security controls for model governance, data provenance, pre-retrieval authorization, embedding policy, AI evaluation, and AI threat modeling. It introduces no autonomous LLM agent and no LLM-directed tool execution. See `docs/M4-AI-System-Security.md`.


## Milestone 5 — Compliance and risk automation

M5 consumes the secured M4 AI-system substrate and adds deterministic governance automation: impact assessment, privacy assessment, exception lifecycle, third-party risk, continuous-control freshness and evidence-backed reporting. M5 artifacts are digest-bound and signed, and the M5 manifest is cryptographically bound to the M4 AI-security manifest. The production profile requires M2 security, M3 supply-chain, M4 AI security and M5 compliance/risk gates simultaneously.

Automation boundary: M5 can assess and report, but cannot accept risk, approve its own exceptions, certify compliance, render legal opinions, or introduce LLM agent autonomy.

## Milestone 6 — First bounded Evidence Analyst

M6 adds a read-only evidence-consumption layer above the deterministic M2–M5 control plane. A signed capability policy exposes only list/metadata/read/verify/summarize operations over a deny-by-default SHA-256 evidence catalog. No side-effecting tool exists. The M6 manifest is Ed25519 signed and bound to the exact M5 manifest. Initial portable evidence snapshots contain non-secret M3–M5 artifacts; M2 remains independently enforced by the combined production profile rather than exposing secret M2 runtime material to the agent.


## Milestone 7 — Mediated typed-tool agent

M7 places a deterministic `ToolBroker` between agent reasoning and executors. A registered call follows `input schema -> RBAC/ABAC authorization -> deterministic control policy -> RunBudget -> signed pre-execution audit -> executor -> output schema -> signed result audit`. Failure at any gate is denied and audited; failure to persist the pre-execution audit prevents executor invocation. The signed M7 manifest binds policy, registry and authorization rules to the exact M6 manifest. M7 allows only non-side-effecting evidence tools; M8 owns approval-controlled side effects.

### Signed-generation immutability

Signed cross-milestone manifests form a generation chain. Once a downstream milestone binds an upstream manifest, the bound upstream release directory is immutable. Operational refresh that changes a signed upstream manifest is a new attestation generation and requires downstream rebuild/re-signing; background mutation of a release-bound directory is fail-closed.

## M10 implemented architecture — supervised multi-agent workflow

M10 implements the planned supervisor-directed specialist workflow as a fixed signed topology. Risk, Threat and Privacy specialists emit typed digest-bound handoffs; Control maps findings to deterministic controls; Assurance checks evidence/control coverage; a separate human workflow decision key finalizes the governance disposition. Direct peer calls, agent delegation, side effects, M8 approval authority and M9 SecOps authority remain prohibited to M10 agents.

## M12 CRA vulnerability/exploitation intelligence layer

M12 sits between M3 supply-chain vulnerability evidence and the future M13 statutory-clock layer. It normalizes vulnerability identifiers/aliases, correlates affected components to the product inventory, evaluates approved exploitation evidence, and emits signed AEV candidate assessments. Node1 remains the authority; Node2 independently verifies evidence. The M12 boundary explicitly keeps `starts_statutory_clock=false`, `enisa_submission=false`, and `cra_conformity_claim=false`.

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
