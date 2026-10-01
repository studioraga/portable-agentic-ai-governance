# M19 — CRA Node1/Node2 Production Validation

M19 converts the repository's prior CRA evidence into a signed, heterogeneous-node production-validation record. Node1 is the validation/signing authority; Node2 is the independent verifier target. Local fixture acceptance is explicitly `SIMULATED` and cannot set `production_validation_complete=true`.

## CRA scope

The primary M11 row is `CRA-REQ-060` / Annex I Part II(3): effective and regular product-security tests and reviews. M19 also reports closure candidates for the M17 evidence gaps, but does not mutate M11 or M17. Product-specific secure-default/reset, other-device/network availability impact, and secure data-removal/transfer remain explicit gaps unless separately demonstrated.

## Live workflow

1. Apply the uncommitted M19 source to both nodes from the same M18 base.
2. Node2 captures and transfers an unsigned live runtime profile to Node1.
3. Node1 captures its own live profile, checks platform/source/version parity and signs the M19 validation bundle.
4. Node1 transfers only verifier material to Node2.
5. Node2 recollects its current live profile and independently verifies the signed bundle.

## Boundaries

M19 performs no destructive test, firmware flash, host update, external network side effect, conformity assessment, or CRA conformity claim.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.
## M21 integration — Embedded Linux & Platform Security

M21 extends the frozen M0–M20 governance/CRA baseline into demonstrable platform security for BIOS/UEFI, Jetson/embedded boot firmware, BMC/device firmware inventory, firmware signing and anti-rollback, debug restrictions, Linux least privilege and systemd isolation, AppArmor/SELinux capability evidence, TPM/DICE roots of trust, platform threat modeling and CI/CD gates. It is non-destructive: live acceptance observes platform state and uses synthetic firmware for signing/rollback demonstrations; it never burns fuses, enrolls UEFI keys or flashes firmware. See `docs/M21-Embedded-Linux-Platform-Security-Validation.md`.
