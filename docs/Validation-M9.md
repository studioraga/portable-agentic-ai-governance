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
