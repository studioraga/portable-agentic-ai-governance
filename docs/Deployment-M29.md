# M29 Deployment

## Node1

```bash
./deploy/m29/one_shot_node1.sh
sha256sum -c var/m29-verifier.tar.gz.sha256
```

Review `var/m29-material/m29-cross-domain-summary.json`. In the current lab profile `production_ready` is expected to be `false`; that is not a validator failure.

## Node2

Transfer only `var/m29-verifier.tar.gz` and its checksum. Then:

```bash
sha256sum -c m29-verifier.tar.gz.sha256
./deploy/m29/one_shot_node2.sh m29-verifier.tar.gz /tmp/m29-node1
```

Never transfer M29 or nested milestone private keys.
