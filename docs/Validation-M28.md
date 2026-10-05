# Validation — M28

Run `python3 -m pytest -q tests/organizational_security`, then `./scripts/m28/validate_m28_local.sh`. Node1 generates persistent evidence with `./deploy/m28/one_shot_node1.sh` and verifies it using `./scripts/m28/verify_node1.sh var/m28-material`. Node2 extracts the verifier tar and runs `./scripts/m28/verify_node2.sh <material-dir>`. Tampering with any manifest-bound artifact must produce a non-zero verifier exit. Production validation must reject simulated evidence and require authorized real-world records.
