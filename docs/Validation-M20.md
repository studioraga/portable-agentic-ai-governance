# M20 Validation

Run `scripts/m20/validate_m20_regression.sh` on both nodes before commit/tag. Node1 must additionally pass `verify_node1.sh`; Node2 must pass `verify_node2.sh`, tamper rejection, and private-key rejection. The secure-agentic demo is validated via `scripts/m20/run_secure_agentic_demo.py` in Node1 producer and Node2 verifier modes.
