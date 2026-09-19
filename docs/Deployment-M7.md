# M7 deployment

Node1 release authority:

```bash
./deploy/m7/one_shot_node1.sh "$PWD/var/m6-material" "$PWD/var/m7-material"
./deploy/m7/package_verifier_material.sh "$PWD/var/m7-material" "$PWD/../m7-verifier-material.tar.gz"
```

Node2 verifier:

```bash
./deploy/m7/one_shot_node2.sh /path/to/m7-material /path/to/m6/evidence-analyst-manifest.json
```

Never transfer M7 `signing-private.pem`. M7 execution uses the node's existing M2 audit-signing secret and M6 read-only evidence material.

## Release-generation freeze and M5 continuous-control refresh

M6 and M7 cryptographically bind the exact M5 compliance-risk manifest. Therefore a background refresh of the same release-authority `var/m5-material` after M6/M7 are built invalidates the downstream chain. For an M7 release:

1. Disable `pag-m5-continuous-controls.timer` before generating the final M4-M7 release generation.
2. Run `deploy/m7/one_shot_node1_full.sh`; it verifies M4->M5->M6->M7 and writes `var/m5-material/.pag-downstream-bound.json`.
3. Do not refresh that frozen M5 directory in place. A new continuous-control attestation requires a new M5 generation followed by M6 and M7 rebuild/re-signing and verifier redistribution.
4. Package and distribute M4, M5, M6 and M7 verifier materials from the same frozen generation.

The M5 timer installer and refresh command fail closed when pointed at downstream-bound M5 release material.

For release distribution, prefer the chain packager over four independent commands:

```bash
./deploy/m7/package_verifier_chain.sh \
  "$PWD/var/m4-material" "$PWD/var/m5-material" \
  "$PWD/var/m6-material" "$PWD/var/m7-material" \
  "$PWD/../m7-verifier-chain-final"
```

It verifies M4->M5->M6->M7 first, creates verifier-only bundles for all four milestones, checks private signing keys are absent, and emits `release-chain.json` plus `verifier-chain.sha256`.
