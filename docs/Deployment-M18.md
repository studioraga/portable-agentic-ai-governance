# M18 Deployment

## Node1

```bash
./deploy/m18/one_shot_node1.sh "$PWD/var/m18-material"
./scripts/m18/verify_node1.sh "$PWD/var/m18-material"
./deploy/m18/package_verifier_material.sh "$PWD/var/m18-material" "$PWD/var/m18-verifier.tar.gz"
```

## Node2

Verify/extract the verifier archive, then:

```bash
./deploy/m18/one_shot_node2.sh /tmp/m18-verifier/m18-material
./scripts/m18/verify_node2.sh "$HOME/.config/portable-ai-governance/m18"
```

Node2 must never receive `signing-private.pem`.
