# Milestone 4 Prerequisites

## Required on release-authority Node1

- Linux with Bash
- Python >= 3.10
- Python standard library (`json`, `hashlib`, `pathlib`, `tomllib` where dependency preflight is used)
- OpenSSL with Ed25519 support
- `sha256sum`, `install`, `tar`, `gzip`
- validated M3 material containing `artifact-locks.json`
- M2/M3 production configuration for the combined production gate

Run before M4 validation:

```bash
./scripts/m4/preflight_dependencies.sh
```

M4 declares zero third-party Python runtime dependencies. If `pyproject.toml` gains runtime dependencies later, the dependency preflight intentionally fails until those dependencies are reviewed and pinned.

## Node2 verifier

Node2 requires Python >= 3.10, OpenSSL, the same M4 source, the M3 artifact lock, and verifier-only M4 material. It does not require the M4 private signing key or an LLM/embedding runtime.

## Python 3.10 TOML compatibility

M4 supports Python 3.10 and later. The dependency preflight does not directly import
`tomllib`; it uses the repository's Python-3.10-safe deterministic dependency inventory.
No `tomli` runtime dependency is required on verifier nodes.
