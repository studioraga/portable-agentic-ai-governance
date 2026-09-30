# M10 deployment

## Node1 / release authority

Build M10 only on Node1:

```bash
python3 scripts/m10/build_m10_material.py \
  --m9-material "$PWD/var/m9-material" \
  --out "$PWD/var/m10-material"

./deploy/m10/one_shot_node1.sh \
  "$PWD/var/m9-material" \
  "$PWD/var/m10-material"
```

Node1 retains:

- `signing-private.pem`
- `workflow-decision-private.pem`

## Node2 / verifier

Node2 receives verifier material only:

```bash
./deploy/m10/one_shot_node2.sh \
  /path/to/m10-material \
  /path/to/m9-material/security-ops-manifest.json
```

Node2 must not contain either M10 private key.

## Full release generation

```bash
./deploy/m10/one_shot_node1_full.sh \
  var/m2-bootstrap var/m3-material var/m4-material var/m5-material \
  var/m6-material var/m7-material var/m8-material var/m9-material var/m10-material
```

After the final Node1 generation passes, do not regenerate it while validating Node2. Package and transfer one coherent M4-M10 verifier chain.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.
