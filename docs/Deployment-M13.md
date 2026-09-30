# M13 Deployment

Node1:

```bash
./deploy/m13/one_shot_node1.sh "$PWD/var/m13-material"
./scripts/m13/verify_node1.sh "$PWD/var/m13-material"
./deploy/m13/package_verifier_material.sh "$PWD/var/m13-material" "$PWD/var/m13-verifier.tar.gz"
```

Node2:

```bash
./deploy/m13/one_shot_node2.sh /tmp/m13-verifier/m13-material
./scripts/m13/verify_node2.sh "$HOME/.config/portable-ai-governance/m13"
```
