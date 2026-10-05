# M20 — Enterprise One-Shot Deployment / Final Production Freeze

M20 assembles a signed enterprise release/freeze evidence bundle from the frozen M11–M19 control chain. A deterministic local run is only a `RELEASE_CANDIDATE`; `FINAL_FREEZE_READY` requires M19 `LIVE` production validation with zero failed required checks. M20 does not perform CRA conformity assessment, CE marking, firmware flashing, host OS updates, or external deployment side effects.

## Secure GenAI / agentic demonstration

M20 also exposes a Node1/Node2 demonstration built directly on M10 commit `d4ce10a`: fixed supervisor topology, no peer delegation, typed/digest-bound handoffs, bounded signal/output budgets, assurance gating, a separately signed single-use human disposition, hash-linked workflow journal, and `side_effect_authority=false`. Node1 creates and signs the trace; Node2 independently verifies the proposal digest, assurance binding and human decision signature.
## M21 integration — Embedded Linux & Platform Security

M21 extends the frozen M0–M20 governance/CRA baseline into demonstrable platform security for BIOS/UEFI, Jetson/embedded boot firmware, BMC/device firmware inventory, firmware signing and anti-rollback, debug restrictions, Linux least privilege and systemd isolation, AppArmor/SELinux capability evidence, TPM/DICE roots of trust, platform threat modeling and CI/CD gates. It is non-destructive: live acceptance observes platform state and uses synthetic firmware for signing/rollback demonstrations; it never burns fuses, enrolls UEFI keys or flashes firmware. See `docs/M21-Embedded-Linux-Platform-Security-Validation.md`.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

This historical milestone document remains authoritative for its original scope. M23 does not rewrite it; M23 consumes the existing identity/authorization/evidence lineage and adds enterprise federation, strong/phishing-resistant MFA policy, entitlement review, PAM/JIT, break-glass, segregation-of-duties, and Node1/Node2 verifier evidence. See `docs/M23-Enterprise-Identity-MFA-PAM.md`.
