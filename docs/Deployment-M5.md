# Milestone 5 deployment

## Node1

```bash
./deploy/m5/one_shot_node1.sh "$PWD/var/m4-material" "$PWD/var/m5-material"
```

Full stack:

```bash
./deploy/m5/one_shot_node1_full.sh \
  "$PWD/var/m2-bootstrap" \
  "$PWD/var/m3-material" \
  "$PWD/var/m4-material" \
  "$PWD/var/m5-material"
```

## Verifier bundle

```bash
./deploy/m5/package_verifier_material.sh \
  "$PWD/var/m5-material" \
  "$PWD/../m5-verifier-material.tar.gz"
```

The verifier bundle must not contain `signing-private.pem`.

## Node2

```bash
./deploy/m5/one_shot_node2.sh \
  /path/to/m5-material \
  /path/to/m4/ai-security-manifest.json
```

Full stack:

```bash
./deploy/m5/one_shot_node2_full.sh \
  /path/to/m2-material-root \
  /path/to/m3-verifier-material \
  /path/to/m4-verifier-material \
  /path/to/m5-verifier-material
```

## Continuous-control refresh on Node1

M5 continuous-control evidence has a 24-hour freshness limit. Refresh it on the release-authority node and redistribute verifier-only material:

```bash
python3 scripts/m5/refresh_continuous_controls.py \
  --m4-material "$PWD/var/m4-material" \
  --m5-material "$PWD/var/m5-material"
```

Optional six-hour systemd timer:

```bash
./deploy/m5/install_continuous_controls_timer.sh \
  "$PWD/var/m4-material" \
  "$PWD/var/m5-material"
```

The timer exists only on the signing/release-authority node. Verifier-only nodes never receive the private M5 signing key; refreshed verifier material must be redistributed through the approved deployment channel.

## Downstream-bound M5 material (M6/M7 and later)

When M6/M7 bind an M5 release, `var/m5-material/.pag-downstream-bound.json` marks that M5 directory immutable. The M5 builder, refresh command, and timer installer refuse to mutate it. To produce new continuous-control evidence after downstream agents exist, create a new release generation through the latest downstream full release workflow so M5, M6, M7 (and later milestones) are rebuilt/re-signed in dependency order and redistributed together.
