# Prerequisites — M19

- M18 release is the Git base on both Node1 and Node2.
- The same uncommitted M19 source is present on both nodes before live-profile capture.
- Node1 is Ubuntu 24.04 x86_64 and acts as release-validation/signing authority.
- Node2 is Ubuntu 22.04 aarch64 and acts as independent product verifier.
- SSH/SCP is available for exchanging the unsigned Node2 profile and verifier-only archive.
- The full repository regression environment is available on both nodes.
- No Node1 private signing key may be copied to Node2.
