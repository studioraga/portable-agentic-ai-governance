# M21 — Embedded Linux & Platform Security Validation

M21 extends the M0–M20 governance/CRA baseline into platform security for silicon, embedded Linux and server/edge products. It covers BIOS/UEFI and Jetson-style trusted boot chains, BMC/device-firmware inventory, signed firmware, anti-rollback, debug controls, Linux least privilege/service isolation, AppArmor/SELinux capability evidence, TPM/DICE roots of trust, platform threat modeling and CI/CD security gates.

## Safety boundary
Acceptance is non-destructive. It never burns fuses, enrolls UEFI keys, flashes firmware, disables hardware debug fuses, installs MAC policy, or reconfigures the host. Live collectors observe current state; synthetic firmware is used for signing/rollback demonstrations.

## Node roles
- **Node1**: release/signing authority, x86_64 BIOS/UEFI/TPM-capability evidence, platform profile capture, signed firmware descriptor and M21 manifest.
- **Node2**: independent verifier, Jetson BootROM→MB1→MB2→UEFI chain evidence, verifier-only bundle, local MAC/debug/root-of-trust capability validation.

## Boot-chain model
Node1: hardware/firmware → UEFI → shim/GRUB → kernel → initramfs → rootfs → systemd service.

Node2: BootROM/fuses → MB1 → MB2 → UEFI → kernel/DTB/initrd → rootfs → systemd service.

## Hardware roots of trust
TPM evidence is collected when `/dev/tpm*`/`tpm2-tools` are available. DICE is represented in two ways: a clearly labelled software derivation demo for learning/CI, and a separate `hardware_available` field that must come from actual platform evidence. Software DICE output never claims hardware DICE.

## BMC/device firmware
The live profile detects IPMI/BMC presence and `fwupdmgr` capability. Systems without a BMC record it as absent rather than passing a fictional BMC test. Server products should extend the same signed-update/rollback/control model to the BMC and other privileged device firmware.

## Production readiness
Fixture profiles prove deterministic logic only. `production_ready=true` requires both live Node1 and live Node2 profiles and all platform policy checks to pass.

## External engineering references
- UEFI Forum, UEFI Specification 2.11: https://uefi.org/specifications
- NIST SP 800-193 Platform Firmware Resiliency Guidelines: https://csrc.nist.gov/pubs/sp/800/193/final
- NIST SP 800-147 / 800-147B BIOS Protection Guidelines: https://csrc.nist.gov/pubs/sp/800/147/final
- TCG DICE hardware requirements: https://trustedcomputinggroup.org/resource/hardware-requirements-for-a-device-identifier-composition-engine/
- Linux kernel security documentation: https://www.kernel.org/doc/html/latest/security/
- Ubuntu AppArmor documentation: https://ubuntu.com/server/docs/how-to/security/apparmor/
- NVIDIA Jetson Secure Boot / Rollback Protection: https://docs.nvidia.com/jetson/
