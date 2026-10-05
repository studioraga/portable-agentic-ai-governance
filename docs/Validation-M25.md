# Validation — M25 Zero-Trust Network & Micro-segmentation

## Node1 from scratch

```bash
cd ~/dev/pub/ai-sys1/ai-goverence/portable-agentic-ai-governance
git status
git rev-parse HEAD
git describe --tags --exact-match
```

Expected baseline:

```text
62a1713ff468117cefc256c03d2a71f26928f8cc
m24-asset-security-data-lifecycle-v0.24.0
```

Apply without committing:

```bash
git apply --check 0001-security-establish-M25-zero-trust-network-and-micro-segmentation.patch
git apply 0001-security-establish-M25-zero-trust-network-and-micro-segmentation.patch
```

Prepare Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

Run:

```bash
python -m pytest -q tests/network_security
python -m pytest -q tests/acceptance/test_framework_mapping.py
./scripts/m25/validate_m25_local.sh
./deploy/m25/one_shot_node1.sh
./scripts/m25/verify_node1.sh var/m25-material
sha256sum -c var/m25-verifier.tar.gz.sha256
```

Private-key isolation:

```bash
if tar -tzf var/m25-verifier.tar.gz | grep -Eqi 'private.*pem'; then
  echo 'FAIL: private key leaked'; exit 1
else
  echo 'PASS: no M25 private key in verifier archive'
fi
```

## Node2 from scratch

Apply the same M25 patch to the same M24 baseline, install the package in `.venv`, then receive only the verifier archive and checksum.

```bash
sha256sum -c m25-verifier.tar.gz.sha256
rm -rf /tmp/m25-node1
mkdir -p /tmp/m25-node1
tar -C /tmp/m25-node1 -xzf m25-verifier.tar.gz
./scripts/m25/verify_node2.sh /tmp/m25-node1/m25-material
```

## Tamper test

```bash
rm -rf /tmp/m25-tampered
cp -a /tmp/m25-node1/m25-material /tmp/m25-tampered
printf '\n' >> /tmp/m25-tampered/m25-gap-closure.json
python3 scripts/m25/validate_m25_node.py --material /tmp/m25-tampered --repo-root "$PWD"
```

Expected: non-zero exit.

## Required negative-path evidence

M25 validates at least:

- unlisted Node2-to-Node1 port denied;
- protected flow without mTLS denied;
- wrong workload identity denied;
- unauthorized egress destination denied;
- generated firewall defaults to drop;
- tampered signed material rejected;
- Node2 package contains no private key.

## Final pre-commit gate

```bash
./scripts/m25/validate_m25_regression.sh
python3 -m pytest -q
git diff --check
git status
```

Only after physical Node1/Node2 verification and unrestricted regression should M25 be committed and tagged.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.
