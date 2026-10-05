# M27 Validation

## First-time Node1 validation

```bash
cd ~/dev/pub/ai-sys1/ai-goverence/portable-agentic-ai-governance
git status
git rev-parse HEAD
git describe --tags --exact-match
```

Expected parent: `82b9331edbe1d12f30b6283b15584ac506038018` and tag `m26-soc-incident-backup-dr-v0.26.0`.

Apply the patch without committing:

```bash
git apply --check 0001-security-establish-M27-secure-SDLC-DevSecOps-AppSec.patch
git apply 0001-security-establish-M27-secure-SDLC-DevSecOps-AppSec.patch
```

Create the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

Run gates:

```bash
python -m pytest -q tests/application_security
python -m pytest -q tests/acceptance/test_framework_mapping.py
./scripts/m27/validate_m27_local.sh
./deploy/m27/one_shot_node1.sh
./scripts/m27/verify_node1.sh var/m27-material
sha256sum -c var/m27-verifier.tar.gz.sha256
```

Confirm no private key is exported:

```bash
if tar -tzf var/m27-verifier.tar.gz | grep -Eqi 'private.*pem'; then
  echo FAIL; exit 1
else
  echo PASS
fi
```

## First-time Node2 validation

Apply the same source patch uncommitted, create the same Python environment, and transfer only the verifier tar/checksum. Then:

```bash
sha256sum -c m27-verifier.tar.gz.sha256
rm -rf /tmp/m27-node1
mkdir -p /tmp/m27-node1
tar -C /tmp/m27-node1 -xzf m27-verifier.tar.gz
./scripts/m27/verify_node2.sh /tmp/m27-node1/m27-material
```

Tamper test:

```bash
cp -a /tmp/m27-node1/m27-material /tmp/m27-tampered
printf '\n' >> /tmp/m27-tampered/m27-gap-closure.json
python3 scripts/m27/validate_m27_node.py --material /tmp/m27-tampered --repo-root "$PWD"
```

The tampered verification must return non-zero.

## Release gate

Before committing, run:

```bash
./scripts/m27/validate_m27_regression.sh
python3 -m pytest -q
git diff --check
git status
```

For a production release, additionally replace simulated DAST/IaC/fuzz/pentest validation artifacts with authorized scanner and penetration-test evidence.
