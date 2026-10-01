# M15 Deployment

Node1 is the PSIRT/CVD evidence authority and retains the M15 private signing key. Node2 is verifier-only.

```bash
./deploy/m15/one_shot_node1.sh "$PWD/var/m15-material"
./deploy/m15/package_verifier_material.sh "$PWD/var/m15-material" "$PWD/var/m15-verifier.tar.gz"
./deploy/m15/one_shot_node2.sh /tmp/m15-verifier/m15-material
```

No deployment action performs vulnerability publication, user notification, component-maintainer contact, or ENISA submission.
