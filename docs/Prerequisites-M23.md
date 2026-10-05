# Prerequisites — M23 Enterprise Identity, MFA & PAM

## Repository baseline

Start from the clean M22 release:

```bash
git rev-parse HEAD
# f020822162591f7d279f7004dea628efb7989525

git describe --tags --exact-match
# m22-enterprise-security-foundation-v0.22.0
```

M23 may be validated while uncommitted because `m23-source-manifest.json` binds the M23 source content by SHA-256 while separately preserving the immutable M22 Git parent.

## Software

Required on both nodes:

- Python 3.10+
- OpenSSL with Ed25519 support
- Git
- tar, sha256sum
- pytest for source validation

No external IdP is required for the deterministic offline validation profile. Production deployment of the federation contract requires a real enterprise OIDC IdP and its trusted signing keys/JWKS.

## Security prerequisites

- Node1 may hold validation-only M23 private keys.
- Node2 must receive only public/verifier material.
- Production privileged access must require phishing-resistant MFA evidence.
- Self-approved JIT elevation is forbidden.
- Break-glass requires two independent approvers and post-review.

## Environment

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```


## Production OIDC runtime variables

```bash
export PAG_IDENTITY_PROVIDER=oidc
export PAG_OIDC_ISSUER='https://id.example/realms/enterprise'
export PAG_OIDC_AUDIENCE='portable-ai-governance'
export PAG_OIDC_PUBLIC_KEY='/protected/path/idp-signing-public.pem'
export PAG_OIDC_REQUIRED_ACR='urn:studioraga:aal2'
```

These variables configure verification trust only. Never place the IdP signing private key in PAG or Node2 material.
