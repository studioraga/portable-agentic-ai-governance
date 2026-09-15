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
