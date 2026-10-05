# Prerequisites — M24

This procedure assumes a developer is running M24 for the first time.

## 1. Required baseline

Both Node1 and Node2 must start from the same clean M23 release:

```text
commit: 7f56c13bdc33993998ca8750d0cab9510e3157aa
tag:    m23-enterprise-identity-mfa-pam-v0.23.0
```

Verify:

```bash
git status --short --branch
git rev-parse HEAD
git describe --tags --exact-match
```

Do not continue if the baseline differs.

## 2. Host tools

Required on both nodes:

```bash
python3 --version
git --version
openssl version
tar --version
sha256sum --version | head -1
```

Python 3.10+ is required; CI uses Python 3.12.

## 3. Python environment

From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

## 4. Node roles

**Node1** is the M24 material producer/signing authority for validation. It may hold the generated `signing-private.pem` under ignored runtime material.

**Node2** is verifier-only. It must never receive `signing-private.pem` or any other private-key material.

## 5. Source synchronization

Before cross-node verification, both nodes must contain the exact same M24 source content because Node2 validates `m24-source-manifest.json` digests.

For pre-commit validation apply the M24 patch with `git apply`, not `git am`.

## 6. Safety boundaries

M24 validation does not delete user data, rotate real production keys, change disk encryption, or modify physical media. Sanitization and export flows use deterministic validation records. Production data-disposal operations require separate operator-approved procedures.
