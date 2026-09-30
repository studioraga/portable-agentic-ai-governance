# M8 prerequisites
Validated M2 and frozen M7; Python >=3.10; Bash/OpenSSL/sha256sum/install/tar/gzip; stdlib fcntl; zero third-party Python runtime dependencies. Run `./scripts/m8/preflight_dependencies.sh` on every node before validation.

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.
