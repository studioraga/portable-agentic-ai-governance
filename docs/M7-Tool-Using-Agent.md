# Milestone 7 — Tool-using agent

## Security objective

M7 introduces a typed-tool agent without introducing uncontrolled agency. `TOOL-ANALYST-001` can request only tools declared in a signed registry. The registry, tool-agent policy and authorization rules are SHA-256 bound in the signed M7 manifest, which is bound to the exact M6 Evidence Analyst manifest.

## Mandatory call path

```text
agent request
   |
   v
input schema
   |
   v
RBAC + ABAC authorization
   |
   v
deterministic governance policy
   |
   v
monotonic step/tool-call budget
   |
   v
signed pre-execution audit
   |
   v
non-side-effecting executor
   |
   v
output schema
   |
   v
signed result audit
```

A failed schema, authorization, policy or budget gate is denied and signed into the audit log. If the pre-execution audit cannot be persisted, the executor is not invoked.

## M7 boundary

M7 tools are non-side-effecting. Shell/network execution, writes, deletion, policy changes, approvals, risk acceptance, compliance certification and delegated execution are not permitted. M8 introduces signed approval-controlled side effects.

## Attestation-generation lifecycle

M7 is bound to the exact M6 manifest, M6 is bound to the exact M5 manifest, and M5 is bound to the exact M4 manifest. Continuous-control refreshes that change M5 are therefore new attestation generations. Once M6/M7 exist, the bound M5 release snapshot is immutable. Refreshing continuous controls requires rebuilding/re-signing M6 and M7 and redistributing the verifier chain.

## M12 integration

Any future live-feed M12 connector must remain behind M7 typed-tool mediation and approved-source policy. The M12 acceptance path intentionally uses offline fixtures and performs no network ingestion.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.
