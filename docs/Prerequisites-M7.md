# M7 prerequisites

Required on every node: Python >=3.10, Bash, OpenSSL Ed25519, sha256sum, install, tar, gzip, owner-private storage, validated M2 runtime material and validated M6 material. M7 has zero third-party Python runtime dependencies. A real invocation additionally requires M2 `PAG_POLICY_CATALOG`, the owner-private M2 secret provider containing `audit_signing.key`, and M6 evidence catalog/root.

Run:

```bash
./scripts/m7/preflight_dependencies.sh
```

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.
