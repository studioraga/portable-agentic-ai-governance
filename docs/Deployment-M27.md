# M27 Deployment

## Node1

1. Confirm the exact M26 parent.
2. Apply M27 with `git apply` to keep the working tree uncommitted.
3. Create `.venv`, install `-e '.[dev]'`, export `PYTHONPATH`.
4. Run `tests/application_security` and the framework-mapping acceptance test.
5. Run `./scripts/m27/validate_m27_local.sh`.
6. Generate persistent material with `./deploy/m27/one_shot_node1.sh`.
7. Inspect `var/m27-material/` and the verifier archive.
8. Confirm no private key is present in `var/m27-verifier.tar.gz`.

## Node2

1. Start from the same M26 parent and apply the same M27 source uncommitted.
2. Install the same Python development environment.
3. Transfer only `m27-verifier.tar.gz` and its checksum.
4. Verify the checksum and extract the archive.
5. Run `./scripts/m27/verify_node2.sh <material-dir>`.
6. Perform the documented tamper test.

## Production scanner integration

Production pipelines should transform native scanner output into the normalized M27 report contract and retain the original scanner artifacts separately. M27 does not require one vendor; it requires complete categories, severity normalization, source binding, deterministic gate semantics, and verifiable evidence.
