from __future__ import annotations

import os
import ssl
import stat
from dataclasses import dataclass
from pathlib import Path


class TLSConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class TLSMaterial:
    ca_file: Path
    cert_file: Path
    key_file: Path
    require_client_cert: bool = True
    minimum_tls: ssl.TLSVersion = ssl.TLSVersion.TLSv1_3

    @classmethod
    def from_paths(cls, ca_file: str, cert_file: str, key_file: str, *, require_client_cert: bool = True):
        return cls(Path(ca_file), Path(cert_file), Path(key_file), require_client_cert)


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def validate_tls_material(material: TLSMaterial) -> tuple[bool, str]:
    for label, path in (("ca", material.ca_file), ("cert", material.cert_file), ("key", material.key_file)):
        if not path.is_file():
            return False, f"{label} file missing: {path}"
        if label == "key" and _mode(path) & 0o077:
            return False, f"private key permissions too open: {oct(_mode(path))}"
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.minimum_version = material.minimum_tls
        ctx.load_cert_chain(str(material.cert_file), str(material.key_file))
        ctx.load_verify_locations(cafile=str(material.ca_file))
    except (ssl.SSLError, OSError) as exc:
        return False, f"TLS material invalid: {exc}"
    return True, "TLS material valid"


def build_server_context(material: TLSMaterial) -> ssl.SSLContext:
    ok, detail = validate_tls_material(material)
    if not ok:
        raise TLSConfigurationError(detail)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = material.minimum_tls
    ctx.load_cert_chain(str(material.cert_file), str(material.key_file))
    ctx.load_verify_locations(cafile=str(material.ca_file))
    ctx.verify_mode = ssl.CERT_REQUIRED if material.require_client_cert else ssl.CERT_OPTIONAL
    return ctx


def build_client_context(material: TLSMaterial, *, check_hostname: bool = True) -> ssl.SSLContext:
    ok, detail = validate_tls_material(material)
    if not ok:
        raise TLSConfigurationError(detail)
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=str(material.ca_file))
    ctx.minimum_version = material.minimum_tls
    ctx.check_hostname = check_hostname
    ctx.load_cert_chain(str(material.cert_file), str(material.key_file))
    return ctx
