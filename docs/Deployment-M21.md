# M21 Deployment

M21 v0.21.1 uses a two-role evidence workflow. It is not a universal host provisioner and it does not make irreversible platform-security changes.

## 1. Synchronize source

Node1 and Node2 should use the same M21 v0.21.1 release source.

Verify on each node:

```bash
git fetch origin --tags
git rev-parse HEAD
git rev-parse origin/main
git rev-list -n1 m21-embedded-linux-platform-security-v0.21.1
```

For the reviewed release all three resolve to:

```text
e83ebf03c6d1ce2f4076ab8e3dae8282e4aeb880
```

## 2. Capture Node2 LIVE profile

On Node2:

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 scripts/m21/collect_platform_profile.py \
  --role independent_verifier \
  --out /tmp/node2-platform-profile.json
```

Transfer only the profile JSON to Node1 through an approved channel.

## 3. Generate and verify Node1 material

On Node1:

```bash
./deploy/m21/one_shot_node1.sh \
  /path/to/node2-platform-profile.json \
  "$PWD/var/m21-material"

./scripts/m21/verify_node1.sh \
  "$PWD/var/m21-material"
```

Node1 is the signing authority. Its private signing key is not verifier material.

## 4. Package verifier-only material

```bash
./deploy/m21/package_verifier_material.sh \
  "$PWD/var/m21-material" \
  "$PWD/var/m21-verifier.tar.gz"
```

Confirm the archive contains no private key before transfer.

## 5. Verify independently on Node2

Extract the verifier bundle to a protected temporary directory, then:

```bash
./deploy/m21/one_shot_node2.sh \
  /path/to/m21-material
```

For an already installed bundle:

```bash
./scripts/m21/verify_node2.sh \
  "$HOME/.config/portable-ai-governance/m21"
```

Do not run `verify_node1.sh` on Node2; it intentionally requires Node1 private signing material.

## 6. Negative acceptance

Before closing a release:

- tamper with a copy of `firmware.bin` and require verifier failure;
- add a private key to a copy of Node2 material and require deployment rejection;
- verify the untouched installed material again afterward.

## Non-destructive boundary

These scripts do not burn fuses, enroll UEFI keys, flash firmware, or enable/install MAC policy. M21 reports observed platform state and open hardening gaps.
