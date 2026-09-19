# instruction.md

## Purpose
Build and operate a portable Agentic AI security and governance control plane. Agents may reason, classify, correlate, recommend, and orchestrate bounded workflows. Deterministic identity, authorization, policy, cryptography, approvals, budgets, schema validation, evidence recording, and typed executors remain authoritative.

## Required operator reading order
1. `README.md`
2. `docs/Prerequisites.md`
3. `docs/Architecture.md`
4. `docs/Deployment.md`
5. `docs/Validation.md`
6. `docs/M2-Security-Control-Plane.md`
7. `docs/Deployment-M2.md`
8. `docs/Validation-M2.md`
9. `docs/Milestones.md`

Do not claim a milestone passed from architecture or documentation alone; execute the corresponding validation gate.

## Non-negotiable design rules
1. Fail closed for mandatory production controls.
2. Never let an LLM or agent authorize itself, accept risk, approve privileged actions, verify cryptography, or bypass policy.
3. Every privileged action is typed, schema-bound, authorized, policy-checked, budgeted, and audited.
4. Unknown controls, tools, identities, mappings, or artifacts are not trusted.
5. Original evidence is immutable; derived outputs create new evidence objects.
6. Every production model, prompt, agent manifest, tool registry, and policy bundle must be versioned and digest-bound before Milestone 6+.
7. Framework mappings are versioned data, not enforcement code.
8. Human approval is required for risk acceptance, policy changes, sensitive exports, evidence deletion, model promotion, permission expansion, and other high-impact side effects.
9. Agent cycles are bounded by monotonic budgets and terminal conditions.
10. Production claims require executable validation evidence, not documentation alone.
11. A clean source release must exclude `.git`, `.venv`, caches, bytecode, and runtime evidence/state.
12. Because this is a Python `src/` layout, every direct source execution path must install the package or set `PYTHONPATH`; scripts must not depend on an operator remembering this manually.
13. Full M0-M1 acceptance requires the extended pytest suite to execute; a skipped suite must be reported as skipped rather than PASS.
14. Secrets must be purpose-separated, never committed, and eventually replaced by managed secret/KMS/HSM implementations.

## Current status
Milestones 0 and 1 are frozen at tag `m0-m1-v0.1.2`. Milestone 2 is implemented as the v0.2.0 security-control-plane candidate and must pass its local/distributed and node-specific validation gates before tagging. Milestones 0-6 are frozen/validated baselines; Milestone 7 is the current implementation candidate. Milestones 8-10 remain planned.

## Milestone 3 supply-chain rule

Software, models, containers, prompts, and tools are untrusted until deterministic digest locks, signed BOM/provenance, and vulnerability policy pass. Private release signing keys never deploy to verifier-only workload nodes.


## Milestone 4 boundary
Milestone 4 adds deterministic AI-system-security controls for model governance, data provenance, pre-retrieval authorization, embedding policy, AI evaluation, and AI threat modeling. It introduces no autonomous LLM agent and no LLM-directed tool execution. See `docs/M4-AI-System-Security.md`.


## Milestone 5 operating rule

Compliance/risk automation may calculate, validate, monitor and report. It may not accept risk, self-approve exceptions, certify compliance, provide legal conclusions, or become an authorization boundary. Exception approval and compliance/accountability decisions remain explicit human responsibilities.

## Milestone 6 operating rule

The Evidence Analyst is read-only. It may list, inspect, verify and summarize allowlisted evidence. It must never write/delete evidence, execute shell/network actions, modify policy, accept risk, approve exceptions, certify compliance, delegate to another agent, or replace deterministic authorization. Any future LLM reasoning adapter remains subordinate to this signed capability boundary.


## Milestone 7 operating rule

A model or agent never calls an executor directly. Every M7 tool call must use the signed registry and pass input schema validation, deterministic RBAC/ABAC authorization, deterministic policy, monotonic budget, and a signed pre-execution audit before the executor can run. Tool output is schema checked and result-audited. M7 side effects are prohibited; approval-controlled side effects begin only at M8.


## Milestone 8 — Approval-controlled actions
M8 adds exactly four typed side effects behind independently issued signed single-use approvals. See `docs/M8-Approval-Controlled-Actions.md`.
