# Milestone 8 — Approval-controlled actions

M8 introduces exactly four bounded side effects: `incident.create`, `rerun.request`, `ticket.create`, and `model.quarantine`. Every call passes `schema -> authorization -> policy -> budget -> approval -> audit` before executor access.

Approvals are independently issued by an operator/human authority and signed with the dedicated M8 Ed25519 approval key. The approval private key remains on the release/approval-authority node; verifier/executor nodes receive only `approval-signing-public.pem`. Every approval is bound to the exact tool, canonical resource, requester, run/call identity, canonical arguments SHA-256, request SHA-256, issuance/expiry times, and `max_uses=1`. The signed M8 policy controls the default/max TTL and allowed clock skew. The agent cannot issue or self-approve approvals, accept risk, certify compliance, approve exceptions, delegate, or gain arbitrary shell/network/filesystem capability.

Replay state and action-effect journals are owner-private durable local state under the M8 runtime action root and are preserved across M8 redeployment. An approval is claimed before the pre-execution allow audit; if that audit is unavailable, the approval remains consumed and no side effect runs. If a side effect commits but the result audit cannot be persisted, the CLI reports `effect_committed=true` and writes an owner-private reconciliation record so operators do not mistake the outcome for an unexecuted action.

Reference side effects are owner-private durable local records; external incident/ticket/model-registry adapters are deployment-specific extensions behind the same boundary.
