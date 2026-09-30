# Validation — M12

M12 acceptance is deterministic and offline.

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q
./scripts/m12/validate_m12_local.sh
```

The fixtures must exercise:

1. affected CVE with no exploitation evidence -> `NOT_AEV`;
2. affected high-severity CVE with authoritative exploitation evidence -> `AEV_CANDIDATE`;
3. exploited vulnerability absent from product -> `NOT_AFFECTED`;
4. conflicting authoritative exploitation evidence -> `INCOMPLETE`;
5. stale intelligence -> fail closed;
6. unapproved source -> reject;
7. alias de-duplication;
8. malicious-actor information preserved without inference;
9. tampered signed material -> reject;
10. Node2 package/private-key isolation -> reject any private-key-bearing material.

M12 must also prove `starts_statutory_clock=false`, `enisa_submission=false`, and `cra_conformity_claim=false`.

## Node-specific verifier scripts

```bash
# Node1 after material generation
./scripts/m12/verify_node1.sh "$PWD/var/m12-material"

# Node2 after verifier-only deployment
./scripts/m12/verify_node2.sh "$HOME/.config/portable-ai-governance/m12"

# Full M0-M12 regression on a qualified node
./scripts/m12/validate_m12_regression.sh
```
