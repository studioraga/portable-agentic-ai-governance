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
Permit only narrowly bounded side effects such as create incident, request rerun, create ticket, or quarantine candidate model. High-impact actions require signed human approval.

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
