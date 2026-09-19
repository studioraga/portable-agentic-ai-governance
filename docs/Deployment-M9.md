# M9 deployment

Build on Node1:

```bash
python3 scripts/m9/build_m9_material.py --m8-material var/m8-material --out var/m9-material
./deploy/m9/one_shot_node1.sh var/m8-material var/m9-material
```

Package verifier material:

```bash
./deploy/m9/package_verifier_material.sh var/m9-material ../m9-verifier-material.tar.gz
```

Node2 receives only `security-ops-manifest.json`, its signature, public verification key, and signed policy. `signing-private.pem` must never be transferred.

The M9 deployer preserves `~/.config/portable-ai-governance/m9/runtime/secops` across redeployment so SIEM, incident, containment, recovery and preserved-evidence state remains durable.

Recovery authorization uses a dedicated M9 Ed25519 authority. Node1 retains `recovery-signing-private.pem`; verifier nodes receive only `recovery-signing-public.pem`. Recovery grants are incident/containment/check-digest bound, short-lived and single-use.
