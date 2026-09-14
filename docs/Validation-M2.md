# Milestone 2 Validation

## Local two-node simulation on Node1

This is the fastest complete M2 acceptance run and does not need the physical Node2:

```bash
./scripts/m2/validate_m2_local.sh
```

The script:

1. generates disposable CA/node certificates;
2. generates independent protected signing keys;
3. deploys Node1 and Node2 configurations into a protected temporary tree;
4. validates both production profiles;
5. starts an mTLS Node1 security probe on loopback;
6. performs a valid Node2 signed request;
7. rejects a bad signature;
8. rejects a replay;
9. rejects an unauthorized workload certificate;
10. rejects a client with no certificate;
11. verifies the signed security audit chain;
12. removes an identity dependency and proves production fails closed.

Expected terminal line:

```text
PASS: Milestone 2 local/distributed security validation complete
```

## Node-specific validation

```bash
./scripts/m2/preflight_m2.sh ~/.config/portable-ai-governance/m2/production.env
./scripts/m2/validate_m2_node.sh ~/.config/portable-ai-governance/m2/production.env
```

## Full regression suite

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q
python scripts/run_self_tests.py
python scripts/check_control_mapping.py
python scripts/check_production_key_separation.py
python scripts/check_runtime_permissions.py
```

## Mandatory negative production tests

At minimum demonstrate failure for:

- local/bootstrap identity selected in production;
- missing identity file;
- identity file with group/world permissions;
- missing secret provider;
- missing secret file;
- secret file with group/world permissions;
- reused signing key domains;
- missing policy catalog;
- mTLS disabled;
- missing CA/cert/key;
- private TLS key with permissive mode;
- mismatched certificate/private key;
- no client certificate;
- unregistered workload URI SAN;
- modified signed body/signature;
- stale signature timestamp;
- nonce replay;
- RBAC denial;
- ABAC denial;
- rate limit exhaustion;
- replay-cache corruption/unavailability.

`UNKNOWN` or skipped mandatory security tests do not count as PASS.
