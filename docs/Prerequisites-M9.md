# M9 prerequisites

- Validated M2 through M8 production configuration.
- Exact M8 action-agent manifest used to build the M9 material.
- Python >= 3.10.
- Bash, OpenSSL with Ed25519, sha256sum, install, tar and gzip.
- Python stdlib `fcntl` for locked append-only local journals.
- Owner-private writable M9 runtime root.
- Fresh M3 vulnerability evidence before full production validation.
- M5 continuous-control timer quiesced while generating a downstream-bound release generation.

M9 adds no third-party Python runtime dependency.

Recovery authorization uses a dedicated M9 Ed25519 authority. Node1 retains `recovery-signing-private.pem`; verifier nodes receive only `recovery-signing-public.pem`. Recovery grants are incident/containment/check-digest bound, short-lived and single-use.

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.
