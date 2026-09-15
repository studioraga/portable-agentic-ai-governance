# Milestone 5 validation

## Dependency gate

```bash
./scripts/m5/preflight_dependencies.sh
```

## Local acceptance

```bash
./scripts/m5/validate_m5_local.sh
```

The suite must reject:

- expired approved exceptions;
- privacy assessments requiring DPIA when DPIA is not approved;
- stale continuous-control evidence;
- automated compliance certification claims.

## Node verification

```bash
./scripts/m5/preflight_m5.sh ~/.config/portable-ai-governance/m5/m5.env
python3 scripts/m5/validate_m5_node.py ~/.config/portable-ai-governance/m5/m5.env
```

## Combined production gate

```bash
./scripts/m5/validate_combined_node.sh \
  ~/.config/portable-ai-governance/m2/production.env \
  ~/.config/portable-ai-governance/m3/m3.env \
  ~/.config/portable-ai-governance/m4/m4.env \
  ~/.config/portable-ai-governance/m5/m5.env
```

Production acceptance requires all four milestone control planes to verify.

## Continuous-control operations gate

Validate that the refresh command succeeds only while the Node1 release-authority private key is present. Confirm the verifier bundle excludes that key. If refreshed evidence is not redistributed before `max_age_hours` expires, Node2/production verification must fail closed as stale.
