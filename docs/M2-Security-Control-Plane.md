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
