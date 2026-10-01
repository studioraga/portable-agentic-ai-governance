# M17 Deployment

Node1 builds signed Annex-I evidence material with `deploy/m17/one_shot_node1.sh`, packages verifier-only material with `deploy/m17/package_verifier_material.sh`, and transfers only that package to Node2. Node2 deploys with `deploy/m17/one_shot_node2.sh`. No private signing key may reach Node2.
