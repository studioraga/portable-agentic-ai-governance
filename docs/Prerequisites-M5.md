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
