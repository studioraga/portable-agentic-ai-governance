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
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.
