from __future__ import annotations
import hashlib,json,os
from pathlib import Path
def sha256_file(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def write_json(p,o):
 p=Path(p);p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');os.chmod(p,0o600)
