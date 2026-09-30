# Milestone 5 prerequisites

Required on Node1 and verifier nodes:

- Python 3.10 or newer.
- Bash.
- OpenSSL with Ed25519 support.
- `sha256sum`, `install`, `tar`, `gzip`.
- Valid M4 material and `ai-security-manifest.json`.
- Owner-private writable configuration storage.

Current Python runtime dependency count: **0 third-party packages**.

Run:

```bash
./scripts/m5/preflight_dependencies.sh
```

Do not begin node validation unless it prints `M5 DEPENDENCY PREFLIGHT: PASS`.

Production privacy/legal mappings are jurisdiction-specific and require accountable organizational review. The reference implementation does not claim legal certification.

## Python 3.10 TOML compatibility

M5 supports Python 3.10 and later. Python 3.10 does not include the standard-library
`tomllib` module (added in Python 3.11). M5 dependency preflight therefore reuses the
repository's Python-3.10-safe deterministic dependency inventory and does not require
`tomli` or another third-party TOML parser. Installing `tomli` is neither required nor
used by the production preflight.

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.
