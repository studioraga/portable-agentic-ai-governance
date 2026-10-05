# Prerequisites — M26

- Clean M25 release `138b56eacc8415de489581b15432c26dc1f1add8` / `m25-zero-trust-network-microsegmentation-v0.25.0`.
- Python 3.10+ and project development dependencies.
- Node1 is the evidence producer and holds the M26 validation signing private key.
- Node2 receives verifier-only material and the same uncommitted M26 source for source-digest verification.
- For production deployment, select an approved centralized SIEM/telemetry stack and immutable/offsite backup platform; M26 core validation remains vendor-neutral.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.
