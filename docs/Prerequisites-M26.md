# Prerequisites — M26

- Clean M25 release `138b56eacc8415de489581b15432c26dc1f1add8` / `m25-zero-trust-network-microsegmentation-v0.25.0`.
- Python 3.10+ and project development dependencies.
- Node1 is the evidence producer and holds the M26 validation signing private key.
- Node2 receives verifier-only material and the same uncommitted M26 source for source-digest verification.
- For production deployment, select an approved centralized SIEM/telemetry stack and immutable/offsite backup platform; M26 core validation remains vendor-neutral.
