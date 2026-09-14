# Milestone 3 Validation

## Local deterministic acceptance

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q
./scripts/m2/validate_m2_local.sh
./scripts/m3/validate_m3_local.sh
python scripts/check_control_mapping.py
```

Expected M3 negative controls include:

- modified prompt rejected by digest lock;
- mutable/non-digest-pinned container reference rejected;
- modified signed SBOM rejected;
- high/critical vulnerability rejected;
- stale/unknown vulnerability data rejected by policy;
- private release signing key rejected from Node2 verifier deployment.

## Node validation

```bash
./scripts/m3/preflight_m3.sh ~/.config/portable-ai-governance/m3/m3.env
python scripts/m3/validate_m3_node.py ~/.config/portable-ai-governance/m3/m3.env
./scripts/m3/validate_combined_node.sh \
  ~/.config/portable-ai-governance/m2/production.env \
  ~/.config/portable-ai-governance/m3/m3.env
```

Production acceptance requires `PAG_SUPPLY_CHAIN_REQUIRED=1` and a non-fixture vulnerability report unless an operator explicitly opts into fixture mode for testing.
