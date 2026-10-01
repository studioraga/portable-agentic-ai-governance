# M14 — CRA Reporting and ENISA SRP Evidence Pack

M14 converts M13 CRA cases and statutory deadlines into deterministic, signed reporting evidence packs for the three Article 14 stages: Early Warning, 72-hour Notification, and Final Report. It does **not** submit to ENISA or a CSIRT and makes no CRA conformity claim.

## Operational boundary

As of the M14 guidance snapshot, the CRA Single Reporting Platform is operational and mandatory manufacturer reporting applies from 11 September 2026. ENISA states that no API is provided in the initial SRP release, so M14 automates internal preparation and verification while an authorised Assigned Representative performs the portal submission.

## Inputs

- frozen M11 CRA requirements matrix;
- M12 vulnerability/exploitation intelligence controls;
- M13 AEV/severe-incident cases and statutory clocks;
- manufacturer, product, Assigned Representative and reporting-enrichment evidence.

## Outputs

- `reporting-packs.json` — per-case, per-stage field payloads;
- `submission-readiness.json` — deterministic completeness/readiness state;
- `srp-field-checklist.json` — field checklist suitable for portal handoff;
- signed `m14-reporting-manifest.json` binding the pack to M11/M12/M13 baselines.

## Report stages

### Actively exploited vulnerability

- 24h early warning;
- 72h vulnerability notification;
- final report no later than 14 days after a corrective/mitigating measure becomes available.

### Severe incident

- 24h early warning;
- 72h incident notification;
- final report within one month after the 72h notification.

## Particularly Exceptional Circumstances

M14 models the PEC flag only for the AEV 72-hour stage. The system never activates PEC automatically; it records evidence for Assigned Representative judgment and later M14/M15 governance decisions.

## Security properties

Node1 holds the M14 signing key and builds the authoritative pack. Node2 receives verifier-only material. All submission flags remain false; any private key in a Node2 package causes fail-closed rejection.

## Official references

- Regulation (EU) 2024/2847, Article 14 and Article 16: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847
- European Commission CRA reporting obligations: https://digital-strategy.ec.europa.eu/en/policies/cra-reporting
- ENISA CRA Single Reporting Platform: https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp
- ENISA SRP FAQ: https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp/frequently-asked-questions
- ENISA SRP Glossary: https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.
