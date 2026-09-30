# Deployment — M12

## Node1

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
./scripts/m12/validate_m12_local.sh
./deploy/m12/one_shot_node1.sh "$PWD/var/m12-material"
./deploy/m12/package_verifier_material.sh "$PWD/var/m12-material" "$PWD/var/m12-verifier.tar.gz"
( cd var && sha256sum -c m12-verifier.tar.gz.sha256 )
```

Transfer only `m12-verifier.tar.gz` and its checksum to Node2.

## Node2

```bash
sha256sum -c m12-verifier.tar.gz.sha256
rm -rf /tmp/m12-verifier && mkdir -m700 /tmp/m12-verifier
tar -xzf m12-verifier.tar.gz -C /tmp/m12-verifier
./deploy/m12/one_shot_node2.sh /tmp/m12-verifier/m12-material
```
