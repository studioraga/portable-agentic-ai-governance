# M29 Prerequisites

1. Clean M28 release `2c9dfd7fa964faa5f639f44937a2b3e76fdec343` / `m28-personnel-physical-bcp-organizational-v0.28.0`.
2. Python 3 virtual environment and `pip install -e '.[dev]'`.
3. OpenSSL and Git available.
4. Existing signed M21 material in `var/m21-material`.
5. M22–M28 builders available; `scripts/m29/prepare_m29_inputs.sh` regenerates their evidence against the current M29 working tree.
6. Node1 retains signing authority. Node2 receives verifier-only material.
7. Production-readiness expectations must remain fail-closed until M21, M27 and M28 real-evidence prerequisites are satisfied.
