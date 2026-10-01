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

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
