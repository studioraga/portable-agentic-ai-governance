# Milestone 9 — Security operations

M9 adds deterministic security operations on top of the validated M8 approval-controlled action boundary.

The reference pipeline is:

`SIEM ingest -> incident creation -> evidence preservation -> signed-runbook local containment -> recovery verification`

High and critical security events can create incidents. Only critical events matching the signed M9 runbook can trigger automatic containment, and reference containment is deliberately limited to reversible local security state (`model.quarantine.local` or `workload.isolate.local`). M9 does not gain arbitrary shell, network, firewall, ticketing or model-service authority; external effects remain behind M8 approvals or enterprise-specific adapters.

SIEM records are append-only and hash-chained. Incident state transitions are deterministic. Evidence is copied into owner-private incident directories and SHA-256 verified before recovery. Recovery is never automatic: the incident must already be contained, an operator identity is required, every declared recovery check must pass, and preserved evidence must still verify.

M9 has no LLM decision authority.

Recovery authorization uses a dedicated M9 Ed25519 authority. Node1 retains `recovery-signing-private.pem`; verifier nodes receive only `recovery-signing-public.pem`. Recovery grants are incident/containment/check-digest bound, short-lived and single-use.

Verified normalized SIEM events can be exported as owner-private NDJSON with `scripts/m9/export_siem.py` for a deployment-specific forwarder. The core framework does not store third-party SIEM credentials or make outbound network calls.

## M12 integration

M12 can ingest approved internal incident evidence as exploitation intelligence, but it does not replace M9 incident lifecycle/containment. M9 remains the security-operations boundary; M12 only preserves and evaluates exploitation evidence for product vulnerability correlation.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
