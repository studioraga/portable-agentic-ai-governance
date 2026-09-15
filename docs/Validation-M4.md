# Milestone 4 Validation

Run dependencies first:

```bash
./scripts/m4/preflight_dependencies.sh
```

Local positive/negative gate:

```bash
./scripts/m4/validate_m4_local.sh
```

The negative suite proves cross-tenant retrieval rejection, failed-evaluation rejection, autonomy rejection, and model-digest-drift rejection.

Node verifier:

```bash
./scripts/m4/preflight_m4.sh ~/.config/portable-ai-governance/m4/m4.env
python3 scripts/m4/validate_m4_node.py ~/.config/portable-ai-governance/m4/m4.env
```

Combined production gate:

```bash
./scripts/m4/validate_combined_node.sh \
  ~/.config/portable-ai-governance/m2/production.env \
  ~/.config/portable-ai-governance/m3/m3.env \
  ~/.config/portable-ai-governance/m4/m4.env
```
