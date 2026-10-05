> Current development milestone: **M27 — Secure SDLC / DevSecOps / AppSec**. Latest immutable tagged parent: **M26 v0.26.0**.

# Developer and Operator Workflow

`README.md` is the human orientation layer. This file is the authoritative execution workflow for developers and operators working with the repository.

## 1. Clone the repository

```bash
git clone git@github.com:studioraga/portable-agentic-ai-governance.git
cd portable-agentic-ai-governance
```

Confirm the remote and working tree before doing any milestone work:

```bash
git remote -v
git status
git log --oneline --decorate -5
```

## 2. Select the milestone release explicitly

Do not assume `main` is the release you intend to reproduce.

For the latest immutable tagged baseline used by M26 development:

```bash
git fetch origin --tags
git checkout m23-enterprise-identity-mfa-pam-v0.23.0
```

For development on `main`, confirm that the expected release ancestry is present:

```bash
git log --oneline --decorate -10
```

Current M26 development ancestry includes:

```text
7f56c13  m23-enterprise-identity-mfa-pam-v0.23.0
f020822  m22-enterprise-security-foundation-v0.22.0
ea95206  M21.1 documentation restructuring
e83ebf0  m21-embedded-linux-platform-security-v0.21.1
```

## 3. Read prerequisites before installing anything

Start with:

- [`docs/Prerequisites.md`](docs/Prerequisites.md) for common requirements;
- the milestone-specific `docs/Prerequisites-M*.md` file for additional tools;
- [`docs/Prerequisites-M21.md`](docs/Prerequisites-M21.md) for the current milestone.

Do not treat an optional audit tool as an implicit reason to mutate the host. M21, in particular, records missing capability as evidence instead of silently installing or enabling platform security features.

## 4. Restore the Python execution environment

The repository uses a Python `src/` layout.

A minimal local development environment is:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

For direct source execution paths, preserve the repository source path explicitly:

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

Scripts under `scripts/` and `deploy/` set this themselves where required; operators should not rely on the current working directory accidentally making imports succeed.

## 5. Run the validation ladder before milestone-specific work

The common validation model is documented in [`docs/Validation.md`](docs/Validation.md).

For M21:

```bash
python3 -m pytest -q tests/platform_security
./scripts/m21/validate_m21_local.sh
./scripts/m21/ci_validate.sh
```

Then run the complete M0–M21 regression:

```bash
set -o pipefail
./scripts/m21/validate_m21_regression.sh 2>&1 | tee /tmp/m21-regression.log

grep -F \
  'PASS: full M0-M21 regression + M20/M21 acceptance complete' \
  /tmp/m21-regression.log
```

Do not convert warnings, skipped suites, or missing platform capabilities into PASS results.

## 6. Run the current milestone

### 6.1 Local deterministic M21 validation

```bash
./scripts/m21/validate_m21_local.sh
```

This uses fixture profiles and validates deterministic M21 logic. It does not prove LIVE platform readiness.

### 6.2 LIVE Node2 profile capture

On the verifier node:

```bash
python3 scripts/m21/collect_platform_profile.py \
  --role independent_verifier \
  --out /tmp/node2-platform-profile.json
```

Transfer only the profile JSON to Node1 through an operator-approved channel.

### 6.3 LIVE Node1 authority run

On Node1:

```bash
./deploy/m21/one_shot_node1.sh \
  /path/to/node2-platform-profile.json \
  "$PWD/var/m21-material"
```

Verify Node1 material:

```bash
./scripts/m21/verify_node1.sh \
  "$PWD/var/m21-material"
```

### 6.4 Package verifier-only material

```bash
./deploy/m21/package_verifier_material.sh \
  "$PWD/var/m21-material" \
  "$PWD/var/m21-verifier.tar.gz"
```

The verifier archive must not contain any private signing key.

### 6.5 Node2 independent verification

After transferring and extracting the verifier-only material on Node2:

```bash
./deploy/m21/one_shot_node2.sh \
  /path/to/m21-material
```

or verify an already installed bundle with:

```bash
./scripts/m21/verify_node2.sh \
  "$HOME/.config/portable-ai-governance/m21"
```

Never run `verify_node1.sh` on Node2. A failure caused by a missing Node1 private signing key is expected on a verifier-only node.

## 7. Inspect evidence, not only exit status

For M21, inspect at least:

```text
platform-validation-summary.json
m21-platform-manifest.json
m21-platform-manifest.json.sig
firmware-descriptor.json
firmware-descriptor.json.sig
rollback-positive.json
rollback-negative.json
dice-demo.json
node1-platform-profile.json
node2-platform-profile.json
```

The M21 v0.21.1 manifest separates:

- `m20_baseline_commit` — immutable M20 baseline;
- `m20_baseline_tag` — immutable M20 release identity;
- `m21_source_commit` — source revision that generated the signed M21 evidence.

Current preserved LIVE qualification is 15 PASS / 2 open required checks, with `production_ready=false`.

## 8. Run negative tests

Security acceptance requires fail-closed behavior, not only positive-path success.

At minimum for M21:

- tamper `firmware.bin` and require verifier failure;
- inject a private signing key into Node2 material and require deployment rejection;
- re-run the untouched bundle afterward and require a clean PASS.

Keep negative-test material under temporary paths such as `/tmp/m21-*`; do not contaminate the authoritative evidence directory.

## 9. Commit rules

Before staging:

```bash
git diff --check
python3 -m pytest -q
```

Stage source and documentation explicitly. Do not use `git add .` when runtime evidence or private material may exist under ignored paths.

Reject staged runtime/private/cache material:

```bash
if git diff --cached --name-only | \
  grep -Eq '(^|/)var/|private.*\.pem|\.pyc$|__pycache__'; then
  echo 'FAIL: runtime/private/cache material staged'
  exit 1
fi
```

Use signed-off commits:

```bash
git commit -s
```

A milestone commit message should state:

- the control/evidence capability added;
- authority boundaries preserved;
- validation completed;
- important open gaps that remain;
- whether the change affects production readiness or conformity claims.

## 10. Release and tag procedure

A release tag is created only after:

1. focused tests pass;
2. common/local validation passes;
3. full regression passes;
4. Node1 evidence generation/verification passes;
5. Node2 independent verification passes;
6. negative tests pass;
7. source parity is confirmed;
8. the working tree is clean;
9. runtime/private material is excluded from release artifacts.

Create an annotated tag and verify that it resolves to the intended release commit before pushing it.

Clean source archives should be produced with `git archive`, not by tarring the whole working tree:

```bash
git archive \
  --format=tar.gz \
  --prefix=portable-agentic-ai-governance/ \
  -o portable-agentic-ai-governance-source.tar.gz \
  <release-tag>
```

## 11. Non-negotiable authority rules

- LLM reasoning never replaces deterministic policy or authorization.
- Risk acceptance and conformity decisions remain human/accountable decisions.
- Private release signing keys remain on the authority side.
- Verifier-only nodes must reject private signing material.
- Agent/tool execution must pass the milestone-defined deterministic gates.
- Runtime evidence and secrets must not be committed.
- A document cannot upgrade a failed or unavailable control to PASS.
- `production_ready=false` is a valid and useful release result when evidence shows open hardening gaps.

## 12. Where to go next

- Architecture: [`docs/Architecture.md`](docs/Architecture.md)
- Validation model: [`docs/Validation.md`](docs/Validation.md)
- Progressive deployment contract: [`docs/oneshot-deployment.md`](docs/oneshot-deployment.md)
- Milestone history: [`docs/Milestones.md`](docs/Milestones.md)
- Current M21 design: [`docs/M21-Embedded-Linux-Platform-Security-Validation.md`](docs/M21-Embedded-Linux-Platform-Security-Validation.md)


## M22 enterprise-security extension

M22 extends the frozen M21.1 baseline with the authoritative CISSP-domain / enterprise-security control foundation. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`, `docs/Prerequisites-M22.md`, `docs/Deployment-M22.md`, and `docs/Validation-M22.md`. M0–M21 historical behavior remains unchanged; M22 records alignment and gaps and does not assert CISSP, ISO/IEC 27001, ISO/IEC 42001, or CRA certification/conformity.

## M23 relationship

M23 extends the frozen M22 enterprise-security foundation with enterprise human identity, OIDC federation evidence, strong MFA context, phishing-resistant privileged authentication, expiring entitlement review, signed single-use JIT privilege grants, dual-approved break-glass access, segregation of duties, and independent Node1/Node2 verification. The authoritative M23 documents are `docs/M23-Enterprise-Identity-MFA-PAM.md`, `docs/Prerequisites-M23.md`, `docs/Deployment-M23.md`, and `docs/Validation-M23.md`. Historical M0-M22 behavior and evidence remain immutable.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.
