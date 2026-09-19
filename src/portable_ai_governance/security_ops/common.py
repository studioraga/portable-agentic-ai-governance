from __future__ import annotations
import hashlib,json,os
from pathlib import Path

def canonical_json_bytes(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha256_bytes(v:bytes): return hashlib.sha256(v).hexdigest()
def sha256_file(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()
def load_json(p): return json.loads(Path(p).read_text())
def write_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True,mode=0o700);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');os.chmod(p,0o600);return p
