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
