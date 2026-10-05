# M22 Prerequisites

M22 is additive to the M21.1 baseline and requires:

1. Git repository containing commit `ea952069938a6435ccb298f5424bab158197ce05`.
2. Python 3.10 or later.
3. OpenSSL with Ed25519 support.
4. `pytest` for validation (`python3 -m pip install -e '.[dev]'` recommended).
5. Node1 and Node2 must contain the same M22 source tree for source-digest verification.
6. Node2 must never receive M22 private signing material.

Before starting:

```bash
git status --short --branch
git rev-parse HEAD
git cat-file -e ea952069938a6435ccb298f5424bab158197ce05^{commit}
python3 --version
openssl version
```

Expected parent HEAD before M22 changes: `ea95206...`. M22 development is intentionally allowed with uncommitted changes; do not commit generated `var/m22-*` material.
