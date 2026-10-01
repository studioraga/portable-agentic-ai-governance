# M21 Validation

Core gates:
- signed firmware descriptor and payload digest verification;
- monotonic version + rollback-counter rejection;
- boot-chain/Secure Boot/lockdown evidence collection;
- debug sysctl validation (`ptrace_scope`, `kptr_restrict`, `dmesg_restrict`, `perf_event_paranoid`);
- hardened systemd service contract;
- AppArmor/SELinux capability and enforcement evidence;
- TPM PCR evidence where available and explicitly-labelled DICE demonstration/hardware evidence;
- BMC/device firmware inventory;
- structured platform threat model;
- local and CI/CD automated validation;
- verifier bundle excludes private keys and rejects tampering.

`production_ready=true` is possible only with LIVE profiles from both nodes and zero failed required checks.
