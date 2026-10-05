# Deployment — M25 Zero-Trust Network & Micro-segmentation

## First-time Node1 procedure

1. Verify the M24 baseline.
2. Apply the M25 mailbox patch with `git apply` so the tree remains uncommitted.
3. Create/activate `.venv` and install `.[dev]`.
4. Run `python -m pytest -q tests/network_security`.
5. Run `./scripts/m25/validate_m25_local.sh`.
6. Run `./deploy/m25/one_shot_node1.sh`.
7. Verify `var/m25-material` with `./scripts/m25/verify_node1.sh var/m25-material`.
8. Transfer only `var/m25-verifier.tar.gz` and its SHA-256 file to Node2.

## First-time Node2 procedure

1. Start from the same M24 release and apply the same M25 patch uncommitted.
2. Create/activate `.venv` and install `.[dev]`.
3. Verify the transferred tar checksum.
4. Extract the verifier archive into a temporary directory.
5. Run `./scripts/m25/verify_node2.sh <extracted>/m25-material`.
6. Perform the tamper test from `docs/Validation-M25.md`.

## Production enforcement

The validation package contains `generated-nftables.conf`. Review it against the actual network architecture before any application. M25 deliberately does not auto-apply the file, because changing host firewall policy remotely can sever administrative access or disrupt unrelated services.
