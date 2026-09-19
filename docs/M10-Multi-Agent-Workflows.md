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
