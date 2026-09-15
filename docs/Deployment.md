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

The deployer is idempotent for the current milestone: it removes and recreates only the local `.venv`, recreates protected runtime directories, and runs validation. Both deployment and validation execute with `umask 077`, so newly created runtime artifacts are private by default. It does not modify systemd, firewall, network, user accounts, or external services because M0-M1 has no daemon or listening API.

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

Do not commit or package this file. The three signing values must remain pairwise independent. Production preflight fails closed when any required key is missing/short, `PAG_FAIL_CLOSED` is not `1`, or any two signing keys are identical.

Verify explicitly:

```bash
./scripts/preflight_node1.sh
PYTHONPATH="$PWD/src" python scripts/check_production_key_separation.py
```

## 6. Runtime filesystem

Expected local state:

```text
var/evidence/   signed governance evidence
var/runs/       workflow outputs
var/state/      replay/state material
```

These directories are mode `0700` and ignored by Git/release packaging. Runtime files are required to be mode `0600`. `deploy_node1.sh` and `validate_node1.sh` set `umask 077`; the evidence writer additionally forces the ledger to `0600` after durable append.

Verify:

```bash
stat -c '%a %U:%G %n' var var/evidence var/runs var/state
find var -type f -perm -0020 -print
find var -type f -perm -0002 -print
PYTHONPATH="$PWD/src" python scripts/check_runtime_permissions.py
```

The two `find` commands must produce no output.

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
./scripts/package_release.sh 0.1.2
```

The release script excludes machine-local/generated content and regenerates `release/source-manifest.sha256` from the clean payload before creating the tarball and outer SHA-256 file.

## 9. Node2

No Node2 deployment exists for M0-M1 because none is required. Milestone 2 will add a separate generic workload-identity/transport deployment path only when distributed service communication is introduced.

## 10. Future production deployment gates

Milestones 2-9 progressively add mandatory gates for enterprise IdP/OIDC and workload identity, mTLS, ABAC/policy service, managed secrets/KMS, signed software/model/prompt/tool/agent artifacts, SBOM/VEX/vulnerability policy, privacy/retention, SIEM, incident response, backup/restore, and recovery tests. Missing mandatory controls will block production deployment rather than downgrade silently.


## Milestone 4 boundary
Milestone 4 adds deterministic AI-system-security controls for model governance, data provenance, pre-retrieval authorization, embedding policy, AI evaluation, and AI threat modeling. It introduces no autonomous LLM agent and no LLM-directed tool execution. See `docs/M4-AI-System-Security.md`.


## Milestone 5 deployment

Use `deploy/m5/one_shot_node1.sh <m4-material> <m5-material>` on the release-authority node and package verifier-only material with `deploy/m5/package_verifier_material.sh`. Node2 must never receive `signing-private.pem`. Full-stack deployment is available through `deploy/m5/one_shot_node1_full.sh` and `deploy/m5/one_shot_node2_full.sh`. M5 verifier directories are `0700` and files are `0600`.
