# M6 prerequisites

Required: Python 3.10+, Bash, OpenSSL with Ed25519 support, `sha256sum`, `install`, `tar`, `gzip`, validated M3/M4/M5 material, and owner-private local storage. Runtime Python dependencies remain zero. No LLM SDK, model server, vector database, network API, shell-execution plugin, or side-effecting tool is required or permitted for the initial Evidence Analyst.

Run `scripts/m6/preflight_dependencies.sh` on every node before M6 validation.

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.
