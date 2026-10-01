# M16 Deployment

Node1 builds signed M16 lifecycle/update material with `deploy/m16/one_shot_node1.sh`, validates it, and creates a private-key-free verifier archive using `deploy/m16/package_verifier_material.sh`.

Node2 verifies the archive checksum, confirms that no private key is present, then runs `deploy/m16/one_shot_node2.sh <m16-material>` and `scripts/m16/verify_node2.sh`.

M16 deployment does not update the operating system or flash device firmware; its update payload is a synthetic acceptance artifact used to prove signing, digest, policy and anti-rollback controls.
