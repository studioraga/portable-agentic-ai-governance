from __future__ import annotations
from pathlib import Path
from .common import load_json,sha256_file
class EvidenceCatalogError(RuntimeError): pass

def require_catalog(path,root):
    d=load_json(path); entries=d.get('entries',[])
    if not entries: raise EvidenceCatalogError('evidence catalog empty')
    ids=set(); root=Path(root).resolve()
    for e in entries:
        eid=e.get('evidence_id','')
        if not eid or eid in ids: raise EvidenceCatalogError('missing/duplicate evidence_id')
        ids.add(eid)
        rel=Path(e.get('path',''))
        if rel.is_absolute() or '..' in rel.parts: raise EvidenceCatalogError(f'unsafe evidence path: {rel}')
        p=(root/rel).resolve()
        if root not in p.parents: raise EvidenceCatalogError('evidence escapes root')
        if not p.is_file(): raise EvidenceCatalogError(f'evidence missing: {rel}')
        if sha256_file(p)!=e.get('sha256'): raise EvidenceCatalogError(f'evidence digest mismatch: {eid}')
        if e.get('access')!='read-only': raise EvidenceCatalogError(f'evidence not read-only: {eid}')
    return f'{len(entries)} cataloged evidence artifacts digest-bound'
