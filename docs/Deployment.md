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

## Milestone 6 deployment

Use `deploy/m6/one_shot_node1.sh <m3-material> <m4-material> <m5-material> <m6-material>` on the release authority. Package verifier-only material with `deploy/m6/package_verifier_material.sh`; never transfer `signing-private.pem`. Deploy verifier material on Node2 with `deploy/m6/one_shot_node2.sh`. Full M0–M6 one-shot scripts are provided for both nodes.


## Milestone 7 deployment

Node1 generates M7 material with `deploy/m7/one_shot_node1.sh <m6-material> <m7-material>`. Package verifier-only material with `deploy/m7/package_verifier_material.sh` and never transfer `signing-private.pem`. Node2 uses `deploy/m7/one_shot_node2.sh <m7-verifier-material> <m6-manifest>`. Full M0-M7 one-shot scripts are provided for both nodes. Runtime tool smoke tests additionally use the installed M2 environment for policy and signed audit, and the installed M6 environment for evidence tools.


## Milestone 8 — Approval-controlled actions
M8 adds exactly four typed side effects behind independently issued signed single-use approvals. See `docs/M8-Approval-Controlled-Actions.md`.


## Milestone 9 — Security operations

See `docs/Deployment-M9.md` for Node1 generation, verifier-only Node2 deployment, M4-M9 chain packaging, and full one-shot deployment.

## Milestone 10 deployment

M10 material is generated only by the release authority and is bound to the exact M9 security-operations manifest. Use `deploy/m10/one_shot_node1_full.sh` to create the final M0-M10 generation, then package one coherent verifier chain with `deploy/m10/package_verifier_chain.sh`. Node2 receives `workflow-decision-public.pem` but never `workflow-decision-private.pem` or the M10 release signing private key. See `docs/Deployment-M10.md`.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.
