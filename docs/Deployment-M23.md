# Deployment — M23 Enterprise Identity, MFA & PAM

## Pre-commit validation model

Apply M23 with `git apply` when validation must occur before committing. Use `git am` only when you want patch application to create the M23 commit.

## Node1

```bash
./deploy/m23/one_shot_node1.sh
```

This creates `var/m23-material/`, verifies it, deploys Node1 authority material under `~/.config/portable-ai-governance/m23`, and checks that a verifier package can be produced without private keys.

Package verifier material:

```bash
./deploy/m23/package_verifier_material.sh \
  var/m23-material \
  var/m23-verifier.tar.gz
```

Transfer only `var/m23-verifier.tar.gz` and its `.sha256` file to Node2.

## Node2

Synchronize the same uncommitted M23 source tree first, then extract the verifier archive and run:

```bash
./deploy/m23/one_shot_node2.sh /path/to/m23-material
```

or directly:

```bash
./scripts/m23/verify_node2.sh /path/to/m23-material
```

Node2 rejects any file matching `*private*.pem`.

## Production IdP integration boundary

The offline M23 validation keys prove the verifier semantics only. They are not production identity keys. In production, configure the enterprise OIDC issuer/audience and use trusted IdP signing keys/JWKS. Never copy a production IdP signing private key into this repository or Node2 verifier material.


## Production OIDC runtime variables

```bash
export PAG_IDENTITY_PROVIDER=oidc
export PAG_OIDC_ISSUER='https://id.example/realms/enterprise'
export PAG_OIDC_AUDIENCE='portable-ai-governance'
export PAG_OIDC_PUBLIC_KEY='/protected/path/idp-signing-public.pem'
export PAG_OIDC_REQUIRED_ACR='urn:studioraga:aal2'
```

These variables configure verification trust only. Never place the IdP signing private key in PAG or Node2 material.
