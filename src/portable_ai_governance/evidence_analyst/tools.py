from __future__ import annotations
import json
from pathlib import Path
from .common import load_json,sha256_file
class ToolError(RuntimeError): pass
class ReadOnlyEvidenceTools:
    def __init__(self,catalog_path,evidence_root,max_read_bytes=65536):
        self.root=Path(evidence_root).resolve(); self.catalog=load_json(catalog_path)
        self.entries={e['evidence_id']:e for e in self.catalog.get('entries',[])}; self.max_read_bytes=max_read_bytes
    def _entry(self,eid):
        if eid not in self.entries: raise ToolError('evidence_id not allowlisted')
        return self.entries[eid]
    def _path(self,e):
        p=(self.root/e['path']).resolve()
        if self.root not in p.parents: raise ToolError('catalog path escapes evidence root')
        return p
    def list(self): return [{k:e[k] for k in ('evidence_id','milestone','kind','sha256') if k in e} for e in self.entries.values()]
    def metadata(self,eid):
        e=self._entry(eid); return dict(e)
    def verify(self,eid):
        e=self._entry(eid); actual=sha256_file(self._path(e)); return {'evidence_id':eid,'ok':actual==e['sha256'],'expected_sha256':e['sha256'],'actual_sha256':actual}
    def read(self,eid):
        e=self._entry(eid); p=self._path(e)
        data=p.read_bytes()
        if len(data)>self.max_read_bytes: raise ToolError('evidence exceeds bounded read size')
        try: return {'evidence_id':eid,'content':data.decode('utf-8')}
        except UnicodeDecodeError: raise ToolError('binary evidence content reading prohibited; metadata/verify only')
    def summarize(self,eid):
        obj=self.read(eid)['content'];
        try:
            d=json.loads(obj)
            keys=sorted(d.keys()) if isinstance(d,dict) else []
            return {'evidence_id':eid,'format':'json','top_level_keys':keys[:32],'bytes':len(obj.encode())}
        except Exception:
            lines=obj.splitlines(); return {'evidence_id':eid,'format':'text','lines':len(lines),'bytes':len(obj.encode())}
