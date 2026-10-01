# M9 validation

Required gates:

1. M9 dependency preflight.
2. Full pytest and trust-kernel regression.
3. All governance controls mapped.
4. M8 -> M9 digest binding.
5. Static M9 manifest/signature/policy validation.
6. SIEM hash-chain positive and tamper-negative tests.
7. High/critical incident creation.
8. Critical signed-runbook local containment.
9. Evidence copy/digest verification and tamper rejection.
10. Illegal incident transition rejection.
11. Recovery rejection before containment.
12. Recovery rejection if any health/integrity check fails.
13. Recovery success only with contained state, operator, passing checks and verified evidence.
14. Node1 and Node2 M0-M9 full one-shot validation.
15. Node2 contains no M9 private signing key.
16. Physical Node2 -> Node1 M2 mTLS regression.
17. Clean v0.9.0 release extraction and source-manifest verification.

Recovery authorization uses a dedicated M9 Ed25519 authority. Node1 retains `recovery-signing-private.pem`; verifier nodes receive only `recovery-signing-public.pem`. Recovery grants are incident/containment/check-digest bound, short-lived and single-use.

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
