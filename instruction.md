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
Milestones 0 and 1 are frozen at tag `m0-m1-v0.1.2`. Milestone 2 is implemented as the v0.2.0 security-control-plane candidate and must pass its local/distributed and node-specific validation gates before tagging. Milestones 3-10 remain planned.
