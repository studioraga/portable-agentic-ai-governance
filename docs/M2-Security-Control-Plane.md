# Milestone 2 — Security Control Plane

Milestone 2 turns the M0-M1 trust kernel into a portable distributed security plane.

## Control boundary

Agents and application code may request actions. They cannot authenticate themselves, grant roles, bypass policy, disable mTLS, consume a nonce twice, select signing keys, or suppress audit events. The deterministic security plane remains authoritative.

Request path:

```text
TLS 1.3 mutual authentication
        |
        v
workload URI SAN -> workload registry -> Principal
        |
        v
body-bound HMAC signature + timestamp
        |
        v
persistent nonce cache
        |
        v
RBAC + ABAC deny-by-default authorization
        |
        v
rate limiter
        |
        v
signed/chained security audit
        |
        v
application handler
```

## Implemented components

- `IdentityProvider` protocol plus local/bootstrap and protected file identity adapters.
- Hashed-token identity file with roles and principal attributes.
- RBAC + ABAC authorization with resource attributes and deny-overrides semantics.
- TLS 1.3 server/client contexts requiring mutual certificates.
- Workload identity extracted from a SPIFFE-style URI SAN.
- Protected workload registry mapping certificate identities to principals/roles/attributes.
- Existing timestamped/body-bound HMAC request signing retained from M0-M1.
- Existing persistent fail-closed nonce cache integrated into the network security gateway.
- `SecretProvider` protocol with lab environment provider and owner-only file provider.
- Independent evidence/request/approval/audit signing domains.
- `CryptoService` for provider-backed HMAC and SHA-256 operations.
- Signed/chained security decision audit ledger.
- Deterministic fixed-window rate limiter.
- Local deterministic policy adapter and production dependency health gate.
- Fail-closed M2 production security profile.
- Minimal TLS security-probe service for distributed acceptance testing.

## Production profile dependencies

Production startup is denied unless all mandatory dependencies pass:

```text
PAG_SECURITY_PROFILE=production
PAG_FAIL_CLOSED=1
PAG_NODE_ID=<node identity>
PAG_IDENTITY_PROVIDER=file
PAG_IDENTITY_FILE=<0600 file>
PAG_SECRET_PROVIDER=file
PAG_SECRETS_DIR=<0700 directory>
PAG_POLICY_CATALOG=<readable catalog>
PAG_MTLS_REQUIRED=1
PAG_TLS_CA_FILE=<CA>
PAG_TLS_CERT_FILE=<node certificate>
PAG_TLS_KEY_FILE=<0600 private key>
PAG_WORKLOAD_REGISTRY=<0600 registry>
PAG_SECURITY_AUDIT_LOG=<protected audit path>
PAG_REPLAY_CACHE=<protected persistent nonce path>
PAG_RATE_LIMIT=<positive integer>
PAG_RATE_WINDOW_SEC=<positive integer>
```

Four production signing keys are mandatory and independent:

```text
evidence_signing.key
request_signing.key
approval_signing.key
audit_signing.key
```

## Network trust

The bootstrap PKI script creates a local private CA only for controlled deployment/bootstrap. The CA private key is kept under `ca-private/` and MUST NOT be copied to Node1 or Node2. Node certificates include:

- serverAuth and clientAuth EKUs;
- DNS/IP SANs;
- `spiffe://<trust-domain>/<node>` URI SAN.

The security probe requires TLS 1.3 and client certificates. A certificate that chains to the CA but is absent from the workload registry is still denied.

## Identity scope

The built-in file identity adapter is the sovereign/offline reference implementation. The `IdentityProvider` interface is deliberately portable so enterprise OIDC/SAML-backed adapters can be added without changing authorization or agent code. For Internet-facing enterprise production, federation/MFA lifecycle controls remain an organizational integration requirement; do not mistake a static file identity registry for workforce SSO.

## Runtime portability

M2 requires Python 3.10+ and OpenSSL/TLS 1.3. This keeps the control plane compatible with Ubuntu 24.04 Node1 and Ubuntu 22.04-class edge nodes while retaining the same deterministic controls.

## M2 release acceptance

M2 is accepted only when:

- M0-M1 regression suite passes;
- M2 unit/security suite passes;
- production profile passes with complete dependencies;
- production profile fails when a mandatory identity/secret/policy/TLS dependency is removed;
- mTLS positive request passes;
- missing client certificate fails;
- unauthorized workload certificate fails;
- bad request signature fails;
- replayed nonce fails;
- RBAC/ABAC negative cases fail;
- rate limiting fails closed when exhausted;
- signed security audit verifies;
- runtime secrets/private keys are owner-only;
- clean release packaging excludes `.git`, `.venv`, caches and runtime state.

## M12 integration

M12 adds a CRA vulnerability/exploitation-intelligence layer without changing this milestone's authority boundary. M12 consumes existing evidence where relevant, emits signed AEV candidate assessments, and performs no statutory-clock, ENISA-submission, or CRA-conformity side effect.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.

## M18 integration

M18 assembles the CRA Article 31 / Annex VII technical-documentation evidence file from the evidence produced by M3-M17. This document remains an input/reference to that assembly; M18 does not retroactively change this milestone's scope. The M18 technical file is explicitly a draft evidence package: it makes no CRA conformity claim, does not perform a conformity assessment, does not authorize CE marking, and does not fabricate the EU Declaration of Conformity. Product-specific production/security test evidence that remains incomplete is carried forward to M19 as an explicit readiness gap.

## M19 integration — CRA Node1/Node2 Production Validation

M19 consumes this milestone's evidence as part of the heterogeneous Node1/Node2 production-validation chain. The M19 signed validation bundle binds the frozen CRA baselines, checks source/version/platform parity and verifier-key isolation, and supplies a production-evidence candidate for Annex I Part II(3) regular product-security testing. M19 does not rewrite this milestone's historical claims, perform conformity assessment, or make a CRA conformity claim.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

This historical milestone document remains authoritative for its original scope. M23 does not rewrite it; M23 consumes the existing identity/authorization/evidence lineage and adds enterprise federation, strong/phishing-resistant MFA policy, entitlement review, PAM/JIT, break-glass, segregation-of-duties, and Node1/Node2 verifier evidence. See `docs/M23-Enterprise-Identity-MFA-PAM.md`.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.
