# M6 validation

Run dependency preflight first, then `scripts/m6/validate_m6_local.sh`. The suite proves the positive read-only path and rejects side-effecting tool requests, catalog path traversal, evidence digest tampering and M5 binding drift. Production acceptance requires `scripts/m6/validate_combined_node.sh` to verify M2+M3+M4+M5+M6 simultaneously.

Manual agent smoke tests use `scripts/m6/run_evidence_analyst.py` with one of the five allowlisted read-only operations.

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.
