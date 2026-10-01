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

## v0.21.1 source-binding correction

M21 v0.21.1 separates two evidence bindings that were conflated in
v0.21.0:

- `m20_baseline_commit` identifies the immutable M20 freeze baseline:
  `8b800814e576bcb08e12dc47c1039c5251c79d46`.

- `m21_source_commit` identifies the M21 source revision used to
  generate the signed evidence.

Verifier validation requires the M20 baseline to match exactly and
requires the recorded M21 source revision to be an ancestor of the
currently executing verifier source.

This permits later repository descendants to verify historical M21
evidence while preserving explicit milestone ancestry.

M21 v0.21.0 incorrectly compared the M20 baseline field directly with
the current repository HEAD. After the M21 commit was created, that
caused otherwise valid signed LIVE evidence to fail only the
`m20-source-bound` check.
