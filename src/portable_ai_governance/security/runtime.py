from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from ..kernel.identity import FileIdentityProvider, IdentityProvider, LocalIdentityProvider
from .secrets import EnvironmentSecretProvider, FileSecretProvider, SecretProvider
from .tls_transport import TLSMaterial


class SecurityDependencyError(RuntimeError):
    pass


@dataclass(frozen=True)
class SecurityRuntimeDependencies:
    identity: IdentityProvider
    secrets: SecretProvider
    tls: TLSMaterial | None
    policy_catalog: Path
    audit_log: Path


def build_runtime_dependencies(environ: dict[str, str] | None = None) -> SecurityRuntimeDependencies:
    env = dict(os.environ if environ is None else environ)
    profile = env.get("PAG_SECURITY_PROFILE", "lab").strip().lower()

    identity_kind = env.get("PAG_IDENTITY_PROVIDER", "local" if profile == "lab" else "")
    if identity_kind == "file":
        path = env.get("PAG_IDENTITY_FILE", "")
        if not path:
            raise SecurityDependencyError("PAG_IDENTITY_FILE required for file identity provider")
        identity: IdentityProvider = FileIdentityProvider(path)
    elif identity_kind == "local" and profile == "lab":
        identity = LocalIdentityProvider([])
    else:
        raise SecurityDependencyError("production requires a supported non-local identity provider")

    secret_kind = env.get("PAG_SECRET_PROVIDER", "environment" if profile == "lab" else "")
    if secret_kind == "file":
        root = env.get("PAG_SECRETS_DIR", "")
        if not root:
            raise SecurityDependencyError("PAG_SECRETS_DIR required for file secret provider")
        secrets: SecretProvider = FileSecretProvider(root)
    elif secret_kind == "environment" and profile == "lab":
        secrets = EnvironmentSecretProvider()
    else:
        raise SecurityDependencyError("production requires a protected secret provider")

    policy_catalog = Path(env.get("PAG_POLICY_CATALOG", "governance/controls/control-catalog.json"))
    audit_log = Path(env.get("PAG_SECURITY_AUDIT_LOG", "var/evidence/security-audit.jsonl"))

    tls: TLSMaterial | None = None
    if profile == "production" or env.get("PAG_MTLS_REQUIRED", "0") == "1":
        ca = env.get("PAG_TLS_CA_FILE", "")
        cert = env.get("PAG_TLS_CERT_FILE", "")
        key = env.get("PAG_TLS_KEY_FILE", "")
        if not all((ca, cert, key)):
            raise SecurityDependencyError("mTLS CA/cert/key are required")
        tls = TLSMaterial.from_paths(ca, cert, key, require_client_cert=True)

    return SecurityRuntimeDependencies(identity, secrets, tls, policy_catalog, audit_log)
