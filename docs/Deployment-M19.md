# Deployment — M19

## 1. Node2 live profile

```bash
mkdir -p var/m19-validation/node2
python3 scripts/m19/collect_node_profile.py --role node2 --out var/m19-validation/node2/node2-runtime-profile.json
```

Transfer only this unsigned profile to Node1.

## 2. Node1 signed production-validation material

```bash
./deploy/m19/one_shot_node1.sh /path/to/node2-runtime-profile.json "$PWD/var/m19-material"
./scripts/m19/verify_node1.sh "$PWD/var/m19-material"
./deploy/m19/package_verifier_material.sh "$PWD/var/m19-material" "$PWD/var/m19-verifier.tar.gz"
```

## 3. Node2 independent verification

After extracting the verifier archive:

```bash
./deploy/m19/one_shot_node2.sh /tmp/m19-verifier/m19-material
./scripts/m19/verify_node2.sh "$HOME/.config/portable-ai-governance/m19"
```

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.
