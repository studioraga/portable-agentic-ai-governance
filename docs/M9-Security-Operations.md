# Milestone 9 — Security operations

M9 adds deterministic security operations on top of the validated M8 approval-controlled action boundary.

The reference pipeline is:

`SIEM ingest -> incident creation -> evidence preservation -> signed-runbook local containment -> recovery verification`

High and critical security events can create incidents. Only critical events matching the signed M9 runbook can trigger automatic containment, and reference containment is deliberately limited to reversible local security state (`model.quarantine.local` or `workload.isolate.local`). M9 does not gain arbitrary shell, network, firewall, ticketing or model-service authority; external effects remain behind M8 approvals or enterprise-specific adapters.

SIEM records are append-only and hash-chained. Incident state transitions are deterministic. Evidence is copied into owner-private incident directories and SHA-256 verified before recovery. Recovery is never automatic: the incident must already be contained, an operator identity is required, every declared recovery check must pass, and preserved evidence must still verify.

M9 has no LLM decision authority.

Recovery authorization uses a dedicated M9 Ed25519 authority. Node1 retains `recovery-signing-private.pem`; verifier nodes receive only `recovery-signing-public.pem`. Recovery grants are incident/containment/check-digest bound, short-lived and single-use.

Verified normalized SIEM events can be exported as owner-private NDJSON with `scripts/m9/export_siem.py` for a deployment-specific forwarder. The core framework does not store third-party SIEM credentials or make outbound network calls.
