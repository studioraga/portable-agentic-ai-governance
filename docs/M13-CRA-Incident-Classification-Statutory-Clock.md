# M13 — CRA Incident Classification & Statutory Clock

M13 consumes the frozen M11 CRA baseline, M12 AEV candidate evidence and M9 incident/security facts. It deterministically classifies CRA Article 14(5) severe incidents, records immutable manufacturer-awareness time, derives statutory deadline evidence, signs the resulting material on Node1, and lets Node2 independently verify the same evidence.

## Scope

- Article 14(5)(a): availability, authenticity, integrity or confidentiality impact affecting sensitive/important data or functions.
- Article 14(5)(b): malicious-code introduction/execution in the product or the user's network/information systems.
- AEV: 24-hour early warning and 72-hour notification from manufacturer awareness; final-report deadline 14 days after corrective/mitigating measure availability.
- Severe incident: 24-hour early warning and 72-hour incident notification from manufacturer awareness; final report one calendar month after the incident notification.
- Immutable awareness T0 represented by a hash-chained journal.
- Deadline states: PENDING, DUE, BREACHED, SATISFIED, NOT_APPLICABLE.

## Explicit boundaries

M13 does not perform ENISA/SRP submission, does not generate the M14 reporting package, and makes no CRA conformity claim.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
