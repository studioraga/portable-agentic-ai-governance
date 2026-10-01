# Prerequisites — M19

- M18 release is the Git base on both Node1 and Node2.
- The same uncommitted M19 source is present on both nodes before live-profile capture.
- Node1 is Ubuntu 24.04 x86_64 and acts as release-validation/signing authority.
- Node2 is Ubuntu 22.04 aarch64 and acts as independent product verifier.
- SSH/SCP is available for exchanging the unsigned Node2 profile and verifier-only archive.
- The full repository regression environment is available on both nodes.
- No Node1 private signing key may be copied to Node2.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.
