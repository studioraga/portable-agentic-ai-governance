# Milestone 4 Deployment

## Node1

```bash
./scripts/m4/preflight_dependencies.sh
./deploy/m4/one_shot_node1.sh "$PWD/var/m3-material" "$PWD/var/m4-material"
```

For complete M0-M4 deployment:

```bash
./deploy/m4/one_shot_node1_full.sh \
  "$PWD/var/m2-bootstrap" \
  "$PWD/var/m3-material" \
  "$PWD/var/m4-material"
```

## Build verifier-only bundle

```bash
./deploy/m4/package_verifier_material.sh \
  "$PWD/var/m4-material" \
  "$PWD/../m4-verifier-material.tar.gz"
```

`signing-private.pem` must not be present in the verifier bundle.

## Node2

```bash
./deploy/m4/one_shot_node2.sh \
  /path/to/m4-material \
  /path/to/m3/artifact-locks.json
```

For complete M0-M4:

```bash
./deploy/m4/one_shot_node2_full.sh \
  /path/to/m2-material-root \
  /path/to/m3-verifier-material \
  /path/to/m4-verifier-material
```
