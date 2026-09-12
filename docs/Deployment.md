# Deployment — Milestones 0 and 1

## 1. Fresh Ubuntu 24.04 Node1

Optional prerequisite installation:

```bash
cd portable-agentic-ai-governance
./deploy/install_prerequisites_ubuntu2404.sh
```

Review `docs/Prerequisites.md` before allowing package installation on a production host.

## 2. Preflight

```bash
./scripts/preflight_node1.sh
```

Resolve every `FAIL`. Review any `WARN`, especially pytest availability if you intend to claim the full M0-M1 acceptance gate.

## 3. One-shot deployment

```bash
./deploy/deploy_node1.sh
```

The deployer is idempotent for the current milestone: it removes and recreates only the local `.venv`, recreates protected runtime directories, and runs validation. It does not modify systemd, firewall, network, user accounts, or external services because M0-M1 has no daemon or listening API.

## 4. Why the source package is not `pip install -e .` by default

M0-M1 deliberately supports an offline sovereign path. `pyproject.toml` has a setuptools build backend, and an editable pip installation can try to resolve build dependencies from a package index on machines where the required backend version is unavailable. Therefore the default deployment uses:

```text
PYTHONPATH=$REPO/src
+
local venv .pth entry
```

This avoids network resolution while preserving a standard Python src layout. An organization may replace this with an internally built wheel or approved internal package index later.

## 5. Production-profile bootstrap validation

The current release validates the contract; it does not claim final enterprise IAM/KMS readiness.

```bash
install -m 700 -d "$HOME/.config/portable-ai-governance"
umask 077
cat > "$HOME/.config/portable-ai-governance/production.env" <<EOF2
PAG_SECURITY_PROFILE=production
PAG_FAIL_CLOSED=1
PAG_EVIDENCE_SIGNING_KEY=$(openssl rand -hex 32)
PAG_REQUEST_SIGNING_KEY=$(openssl rand -hex 32)
PAG_APPROVAL_SIGNING_KEY=$(openssl rand -hex 32)
EOF2

set -a
source "$HOME/.config/portable-ai-governance/production.env"
set +a
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -m portable_ai_governance.cli validate-security
```

Permissions:

```bash
chmod 700 "$HOME/.config/portable-ai-governance"
chmod 600 "$HOME/.config/portable-ai-governance/production.env"
```

Do not commit or package this file.

## 6. Runtime filesystem

Expected local state:

```text
var/evidence/   signed governance evidence
var/runs/       workflow outputs
var/state/      replay/state material
```

These directories are mode `0700` and ignored by Git/release packaging.

## 7. Source-control bootstrap

Release archives contain no `.git` metadata. For a new repository:

```bash
git init
git branch -M main
git add .
git status
git commit -m 'feat: bootstrap portable AI governance M0-M1'
```

## 8. Creating a clean release archive

Use:

```bash
./scripts/package_release.sh 0.1.1
```

The release script excludes machine-local/generated content and regenerates `release/source-manifest.sha256` from the clean payload before creating the tarball and outer SHA-256 file.

## 9. Node2

No Node2 deployment exists for M0-M1 because none is required. Milestone 2 will add a separate generic workload-identity/transport deployment path only when distributed service communication is introduced.

## 10. Future production deployment gates

Milestones 2-9 progressively add mandatory gates for enterprise IdP/OIDC and workload identity, mTLS, ABAC/policy service, managed secrets/KMS, signed software/model/prompt/tool/agent artifacts, SBOM/VEX/vulnerability policy, privacy/retention, SIEM, incident response, backup/restore, and recovery tests. Missing mandatory controls will block production deployment rather than downgrade silently.
