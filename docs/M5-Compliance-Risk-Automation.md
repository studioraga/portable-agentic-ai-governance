# Milestone 5 — Compliance and Risk Automation

M5 adds deterministic governance automation on top of the frozen M4 AI-security substrate. It does not add autonomous LLM behavior.

## Trust model

M5 may calculate, validate, monitor and report. It may not accept risk, self-approve exceptions, certify compliance or issue legal conclusions. Accountable human owners remain the decision boundary.

## Control domains

1. **Impact assessment** — purpose, stakeholders, impact domains, inherent/residual risk, controls, accountable decision and review date.
2. **Privacy** — purpose, categories, legal basis, retention, rights, transfer safeguards, sensitive-data justification and DPIA gate.
3. **Exceptions** — default deny, independent approver, compensating controls, explicit expiry and closed/rejected lifecycle.
4. **Third parties** — owner, service, criticality, data access/residency, security assessment, processing terms, contract state, review and exit plan.
5. **Continuous controls** — status, last-check timestamp, maximum evidence age, evidence SHA-256 and blocking failure behavior.
6. **Compliance reports** — evidence-backed control summaries with explicit non-certification disclaimer.

## Integrity

`compliance-risk-manifest.json` SHA-256-binds every M5 artifact and the M4 AI-security manifest. The manifest is signed with Ed25519. Only the public verification key is distributed to verifier-only nodes.

## Production gate

`PAG_COMPLIANCE_RISK_REQUIRED=1` activates M5 inside the production security profile. M2, M3, M4 and M5 must all verify simultaneously.

## M12 integration

M12 contributes evidence to CRA risk/compliance automation through deterministic vulnerability-to-product and exploitation correlation. It does not promote any M11 requirement to `met` or make a compliance/conformity decision by itself.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
