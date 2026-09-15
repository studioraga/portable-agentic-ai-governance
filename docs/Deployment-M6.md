# M6 deployment

Node1 is the M6 release authority. Generate M6 material from validated M3/M4/M5 material and deploy with `deploy/m6/one_shot_node1.sh`. Package verifier-only material with `deploy/m6/package_verifier_material.sh`; `signing-private.pem` must never be transferred to Node2.

Node2 deploys only the verifier bundle with `deploy/m6/one_shot_node2.sh`. Full-stack deployment is available through `deploy/m6/one_shot_node1_full.sh` and `deploy/m6/one_shot_node2_full.sh`.

All M6 directories are owner-only (`0700`) and all material files are owner-only (`0600`).
