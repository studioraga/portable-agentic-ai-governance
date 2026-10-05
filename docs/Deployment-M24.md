# Deployment — M24

## First-time Node1 procedure

### Step 1 — verify M23 baseline

```bash
cd ~/dev/pub/ai-sys1/ai-goverence/portable-agentic-ai-governance
git status --short --branch
git rev-parse HEAD
git describe --tags --exact-match
```

Expected M23 commit/tag are documented in `Prerequisites-M24.md`.

### Step 2 — apply M24 without committing

```bash
git apply --check 0001-security-establish-M24-asset-security-data-protection-and-crypto-lifecycle.patch
git apply 0001-security-establish-M24-asset-security-data-protection-and-crypto-lifecycle.patch
git status
```

HEAD must still point to M23.

### Step 3 — prepare Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

### Step 4 — run M24 unit and local gates

```bash
python -m pytest -q tests/asset_security
./scripts/m24/validate_m24_local.sh
```

### Step 5 — create persistent Node1 evidence

```bash
./deploy/m24/one_shot_node1.sh
```

This creates ignored material under:

```text
var/m24-material/
var/m24-verifier.tar.gz
var/m24-verifier.tar.gz.sha256
```

### Step 6 — inspect Node1 material

```bash
./scripts/m24/verify_node1.sh var/m24-material
find var/m24-material -maxdepth 1 -type f -printf '%f\n' | sort
```

### Step 7 — prove verifier package contains no private key

```bash
sha256sum -c var/m24-verifier.tar.gz.sha256

tar -tzf var/m24-verifier.tar.gz

if tar -tzf var/m24-verifier.tar.gz | grep -Eqi 'private.*pem'; then
    echo 'FAIL: private key leaked into verifier package'
    exit 1
else
    echo 'PASS: verifier package contains no private key'
fi
```

## First-time Node2 procedure

### Step 1 — verify the same M23 baseline

```bash
cd ~/dev/pub/ai-sys1/ai-goverence/portable-agentic-ai-governance
git status --short --branch
git rev-parse HEAD
git describe --tags --exact-match
```

### Step 2 — apply the identical M24 source uncommitted

```bash
git apply --check 0001-security-establish-M24-asset-security-data-protection-and-crypto-lifecycle.patch
git apply 0001-security-establish-M24-asset-security-data-protection-and-crypto-lifecycle.patch
```

### Step 3 — prepare Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

### Step 4 — receive only verifier material

Transfer from Node1 only:

```text
var/m24-verifier.tar.gz
var/m24-verifier.tar.gz.sha256
```

### Step 5 — verify checksum and extract

```bash
sha256sum -c m24-verifier.tar.gz.sha256
rm -rf /tmp/m24-node1
mkdir -p /tmp/m24-node1
tar -C /tmp/m24-node1 -xzf m24-verifier.tar.gz
```

### Step 6 — independent verification

```bash
./scripts/m24/verify_node2.sh /tmp/m24-node1/m24-material
```

A verifier PASS means the supplied evidence is internally valid and source-bound. It is not a certification claim.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
