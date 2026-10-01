# M15 Deployment

Node1 is the PSIRT/CVD evidence authority and retains the M15 private signing key. Node2 is verifier-only.

```bash
./deploy/m15/one_shot_node1.sh "$PWD/var/m15-material"
./deploy/m15/package_verifier_material.sh "$PWD/var/m15-material" "$PWD/var/m15-verifier.tar.gz"
./deploy/m15/one_shot_node2.sh /tmp/m15-verifier/m15-material
```

No deployment action performs vulnerability publication, user notification, component-maintainer contact, or ENISA submission.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.
