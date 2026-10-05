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
