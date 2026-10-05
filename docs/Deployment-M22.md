# M22 Deployment — Node1 / Node2

## Local pre-commit validation

```bash
./scripts/m22/validate_m22_local.sh
```

## Node1

```bash
./deploy/m22/one_shot_node1.sh
./deploy/m22/package_verifier_material.sh \
  var/m22-material \
  var/m22-verifier.tar.gz
./scripts/m22/verify_node1.sh var/m22-material
```

Copy only `var/m22-verifier.tar.gz` and its `.sha256` to Node2 using your approved transport. Do not copy `signing-private.pem`.

## Node2

After extracting `m22-material`:

```bash
./deploy/m22/one_shot_node2.sh /path/to/m22-material
```

or directly:

```bash
./scripts/m22/verify_node2.sh /path/to/m22-material
```

Node2 verification checks signatures, artifact digests, source digests against its synchronized repository, M21.1 parent-baseline existence, claim boundaries, all eight CISSP domains, mapping completeness, and gap-register completeness.
