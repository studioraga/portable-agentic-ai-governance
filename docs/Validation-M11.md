# Validation — M11 CRA Product Security Foundation

Run on Node1:

```bash
./scripts/m11/validate_m11_local.sh
./deploy/m11/one_shot_node1.sh ./var/m11-material
./deploy/m11/package_verifier_material.sh ./var/m11-material ./var/m11-verifier.tar.gz
(
    cd ./var
    sha256sum -c m11-verifier.tar.gz.sha256
)
```

Negative checks covered by pytest include duplicate/invalid mappings, missing implementation paths, tampered requirement matrices, and the no-conformity-claim invariant.

Node2 acceptance requires verifier-only material and fails if `signing-private.pem` is present:

```bash
mkdir -p /tmp/m11-verifier && tar -xzf m11-verifier.tar.gz -C /tmp/m11-verifier
./deploy/m11/one_shot_node2.sh /tmp/m11-verifier/m11-material
```

## M12 hand-off

M12 consumes the signed/frozen M11 CRA requirement matrix without altering M11's 92-row baseline. M12 validation additionally binds its manifest to the SHA-256 of `governance/cra/cra-requirements.json`, so a changed M11 baseline invalidates M12 verification.
