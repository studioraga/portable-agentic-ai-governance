from __future__ import annotations
import hashlib,json,os
from pathlib import Path

def sha256_file(path):
 p=Path(path);h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()

def write_json(path,obj):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');os.chmod(p,0o600)

def version_tuple(v):
 try:return tuple(int(x) for x in str(v).split('.'))
 except Exception: raise ValueError(f'invalid dotted numeric version: {v}')
