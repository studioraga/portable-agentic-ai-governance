# M8 deployment

Build M8 from the exact accepted M7 material. Node1 retains M8 release-signing and dedicated Ed25519 approval-signing private material; Node2 receives verifier-only material and `approval-signing-public.pem` only. Approval issuance is an operator workflow and is not an `ACTION-AGENT-001` tool.

Runtime action state is owner-private under `~/.config/portable-ai-governance/m8/runtime/actions` and is deliberately preserved across M8 redeployment. This includes the single-use approval ledger, effect journals, and reconciliation records. Deployment overwrites signed configuration/verifier material but never resets runtime replay state. Do not manually delete the runtime action directory to make a replay test pass.

The signed M8 policy sets approval TTL defaults/maxima and clock-skew tolerance. For manual physical acceptance testing, issue a fresh approval immediately before execution; do not reuse an expired approval merely to test replay semantics.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
