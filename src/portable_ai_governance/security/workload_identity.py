from __future__ import annotations

import json
import stat
from dataclasses import dataclass
from pathlib import Path

from ..kernel.types import Principal


class WorkloadIdentityError(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkloadIdentity:
    uri: str
    trust_domain: str
    workload: str


def extract_workload_identity(peer_cert: dict, *, trust_domain: str = "pag.local") -> WorkloadIdentity:
    sans = peer_cert.get("subjectAltName", ()) if peer_cert else ()
    prefix = f"spiffe://{trust_domain}/"
    uris = [value for kind, value in sans if kind == "URI" and value.startswith(prefix)]
    if len(uris) != 1:
        raise WorkloadIdentityError("exactly one trusted workload URI SAN required")
    uri = uris[0]
    workload = uri[len(prefix):]
    if not workload or ".." in workload.split("/"):
        raise WorkloadIdentityError("invalid workload identity")
    return WorkloadIdentity(uri, trust_domain, workload)


class FileWorkloadRegistry:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._principals = self._load()

    def _load(self) -> dict[str, Principal]:
        if not self.path.is_file():
            raise WorkloadIdentityError(f"workload registry missing: {self.path}")
        mode = stat.S_IMODE(self.path.stat().st_mode)
        if mode & 0o077:
            raise WorkloadIdentityError(f"workload registry permissions too open: {oct(mode)}")
        try:
            root = json.loads(self.path.read_text(encoding="utf-8"))
            out: dict[str, Principal] = {}
            for item in root["workloads"]:
                uri = str(item["uri"])
                if uri in out:
                    raise ValueError("duplicate workload URI")
                out[uri] = Principal(
                    str(item["principal_id"]),
                    tuple(str(x) for x in item.get("roles", ())),
                    {str(k): str(v) for k, v in item.get("attributes", {}).items()},
                )
            if not out:
                raise ValueError("empty workload registry")
            return out
        except Exception as exc:
            raise WorkloadIdentityError(f"invalid workload registry: {exc}") from exc

    def resolve(self, identity: WorkloadIdentity) -> Principal:
        try:
            return self._principals[identity.uri]
        except KeyError as exc:
            raise WorkloadIdentityError("workload identity not authorized") from exc
