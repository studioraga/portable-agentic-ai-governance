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
