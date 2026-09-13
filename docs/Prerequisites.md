# Prerequisites — Milestones 0 and 1

This document defines the machine, software, security, and repository prerequisites for the M0-M1 portable governance foundation. These are deliberately separated into **minimum runtime**, **full acceptance**, and **production-profile validation** requirements.

## 1. Supported deployment target

Primary validated target:

- Ubuntu 24.04 LTS x86_64 on Node1.
- Python 3.11 or newer; Python 3.12 is the recommended Ubuntu 24.04 runtime.
- At least 100 MiB free disk space for M0-M1 validation. Later milestones will require substantially more.
- A normal non-root account with write access to the repository. `sudo` is required only when installing OS packages.

M0-M1 does **not** require a GPU, CUDA, NVIDIA driver, PostgreSQL, Qdrant, Docker, Kubernetes, an LLM, an external identity provider, Internet access, or Node2.

## 2. Required OS commands

The preflight requires:

```text
bash
python3
tar
gzip
sha256sum
openssl
install
df
awk
find
sort
xargs
```

`git` is strongly recommended for source control but is not required by runtime validation.

On Ubuntu 24.04, install the baseline packages with:

```bash
sudo apt update
sudo apt install -y --no-install-recommends \
  python3 python3-venv python3-pip python3-pytest \
  git openssl ca-certificates tar gzip coreutils findutils mawk
```

Or use:

```bash
./deploy/install_prerequisites_ubuntu2404.sh
```

The helper intentionally exits on non-Ubuntu-24.04 systems rather than making unverified package-manager changes.

## 3. Python and virtual environment

Required:

```bash
python3 --version
python3 -m venv --help
```

The repository uses the Python `src/` layout. Therefore `portable_ai_governance` is **not** importable merely because the shell is in the repository root. The deployment script performs both of these safeguards:

1. exports `PYTHONPATH=$REPO/src` for the current process; and
2. writes a `.pth` file into the local virtual environment.

All validation scripts also explicitly export `PYTHONPATH`, so pytest and child processes do not depend on shell history.

## 4. Pytest and full acceptance

The built-in self-test suite is standard-library-only and remains usable offline. The full M0-M1 acceptance gate also includes the tests under `tests/`.

Check:

```bash
python3 -m pytest --version
```

If unavailable on Ubuntu 24.04:

```bash
sudo apt install python3-pytest
```

Or, where approved Internet/package-index access exists:

```bash
python3 -m pip install 'pytest>=7.4,<10'
```

Validation always invokes:

```bash
python -m pytest -q
```

rather than a bare `pytest`, ensuring the active interpreter is used.

## 5. Network requirements

M0-M1 runtime and validation are designed to work with **no network access** once OS prerequisites are present. No package download, model download, cloud API, telemetry service, or external database is required.

The prerequisite installation helper uses Ubuntu repositories and therefore requires network access only when the required OS packages are not already installed.

## 6. Repository prerequisites

The following must exist and be readable:

```text
README.md
instruction.md
pyproject.toml
docs/Architecture.md
docs/Deployment.md
docs/Validation.md
docs/Milestones.md
docs/Prerequisites.md
src/
schemas/
governance/
agents/
tests/
scripts/
deploy/
examples/
release/
```

The repository root must be writable because validation creates `.venv/` and runtime state under `var/`.

A clean source archive must **not** contain:

```text
.git/
.venv/
.pytest_cache/
__pycache__/
*.pyc
runtime evidence/run/state files
```

## 7. Runtime directories and permissions

Deployment creates:

```text
var/
var/evidence/
var/runs/
var/state/
```

with mode `0700`. They contain local runtime material and must not be committed or included in release archives.

Runtime files created beneath these directories must be owner-only mode `0600`. The deployment and validation entry points set `umask 077`, and the evidence writer additionally enforces `0600` explicitly after append/fsync. Acceptance checks must confirm that no file beneath `var/` is group-writable or world-writable.

Verify manually:

```bash
stat -c '%a %U:%G %n' var var/evidence var/runs var/state
find var -type f -perm -0020 -print
find var -type f -perm -0002 -print
```

The two `find` commands must produce no output for the frozen M0-M1 baseline.

## 8. Environment variables

### Lab validation

No secret environment variables are required. Defaults are intentionally local/test-only.

```bash
export PAG_SECURITY_PROFILE=lab
```

### Production-profile contract validation

Required:

```text
PAG_SECURITY_PROFILE=production
PAG_FAIL_CLOSED=1
PAG_EVIDENCE_SIGNING_KEY
PAG_REQUEST_SIGNING_KEY
PAG_APPROVAL_SIGNING_KEY
```

Each bootstrap secret must be at least 32 characters and cryptographically independent from the other two for this M0-M1 contract validator. Production preflight and runtime validation fail closed when any two required signing keys are identical. Generate independent values, for example:

```bash
openssl rand -hex 32
```

Do not commit the secrets. Do not reuse one secret for multiple purposes. The three cryptographic domains are:

```text
PAG_EVIDENCE_SIGNING_KEY   governance/evidence envelopes
PAG_REQUEST_SIGNING_KEY    signed request authentication/integrity
PAG_APPROVAL_SIGNING_KEY   privileged approval artifacts
```

M0-M1 deliberately uses environment-provided symmetric bootstrap secrets only. Milestone 2 adds a `SecretProvider` abstraction, Vault/KMS/HSM adapters, key identifiers/versioning, rotation, historical-key verification, workload identity, and stronger lifecycle controls.

## 9. Git prerequisites and initial commit

A release archive intentionally excludes `.git/`. After extraction, initialize a fresh repository if required:

```bash
git init
git branch -M main
git add .
git status
git commit -m 'feat: bootstrap portable AI governance M0-M1'
```

Configure `user.name` and `user.email` first if Git requests them.

## 10. Node2 prerequisites

None for M0-M1.

Node2 becomes relevant only when an application adapter needs an edge workload. Milestone 2 will define workload identity, mTLS, signed requests, persistent anti-replay, least privilege, and application-specific edge validation. The portable governance kernel must remain independently testable on Node1.

## 11. Preflight

Run before deployment:

```bash
./scripts/preflight_node1.sh
```

A valid baseline ends with:

```text
PREFLIGHT: PASS
```

Warnings such as missing Git or pytest identify optional/full-acceptance capabilities. Missing Python, venv, OpenSSL, archive/hash utilities, required repository paths, write access, or minimum disk space are hard failures. In `production`, preflight also hard-fails when `PAG_FAIL_CLOSED` is disabled, a required signing key is missing/short, or signing keys are reused.

For the hardened M0-M1 acceptance gate, also run:

```bash
PYTHONPATH="$PWD/src" python scripts/check_production_key_separation.py
PYTHONPATH="$PWD/src" python scripts/check_runtime_permissions.py
```

Expected summaries:

```text
KEY-SEPARATION TESTS PASS: 5/5
RUNTIME-PERMISSION TESTS PASS
```
