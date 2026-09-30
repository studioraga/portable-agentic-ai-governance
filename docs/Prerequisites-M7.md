# M7 prerequisites

Required on every node: Python >=3.10, Bash, OpenSSL Ed25519, sha256sum, install, tar, gzip, owner-private storage, validated M2 runtime material and validated M6 material. M7 has zero third-party Python runtime dependencies. A real invocation additionally requires M2 `PAG_POLICY_CATALOG`, the owner-private M2 secret provider containing `audit_signing.key`, and M6 evidence catalog/root.

Run:

```bash
./scripts/m7/preflight_dependencies.sh
```

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.
