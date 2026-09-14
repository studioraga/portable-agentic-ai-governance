from __future__ import annotations
import hashlib, json, re
from dataclasses import dataclass
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

class LockError(RuntimeError): pass

def sha256_file(path: str | Path) -> str:
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

@dataclass(frozen=True)
class LockResult:
    name:str; artifact_type:str; ok:bool; detail:str

def verify_lock_file(lock_path: str | Path, root: str | Path='.') -> list[LockResult]:
    doc=json.loads(Path(lock_path).read_text())
    results=[]; root=Path(root)
    entries=doc.get('artifacts',[])
    if not entries: raise LockError('lock file contains no artifacts')
    for e in entries:
        name=str(e.get('name','')); typ=str(e.get('type','')); digest=str(e.get('sha256','')).lower()
        if not name or typ not in {'model','container','prompt','tool'} or not SHA256_RE.fullmatch(digest):
            results.append(LockResult(name or '<unnamed>',typ,False,'invalid lock metadata')); continue
        if typ=='container':
            ref=str(e.get('ref',''))
            ok='@sha256:' in ref and ref.rsplit('@sha256:',1)[1]==digest
            results.append(LockResult(name,typ,ok,'digest pinned' if ok else 'container ref must be @sha256 pinned')); continue
        p=e.get('path')
        if p:
            path=(root / p).resolve() if not Path(p).is_absolute() else Path(p)
            if not path.is_file(): results.append(LockResult(name,typ,False,f'missing file: {path}')); continue
            actual=sha256_file(path); ok=actual==digest
            results.append(LockResult(name,typ,ok,'verified' if ok else f'digest mismatch: {actual}'))
        else:
            # Remote/model registry locks can be verified structurally here; materialization verification happens on acquisition.
            results.append(LockResult(name,typ,True,'digest locked metadata'))
    return results

def require_locks(lock_path: str | Path, root: str | Path='.') -> list[LockResult]:
    out=verify_lock_file(lock_path,root)
    bad=[x for x in out if not x.ok]
    if bad: raise LockError('; '.join(f'{x.artifact_type}:{x.name}:{x.detail}' for x in bad))
    required={'model','container','prompt','tool'}
    present={x.artifact_type for x in out}
    missing=required-present
    if missing: raise LockError('missing lock categories: '+','.join(sorted(missing)))
    return out
