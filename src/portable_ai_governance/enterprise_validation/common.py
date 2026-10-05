from __future__ import annotations
import hashlib,json
from pathlib import Path
M28_BASELINE_COMMIT='2c9dfd7fa964faa5f639f44937a2b3e76fdec343'
M28_BASELINE_TAG='m28-personnel-physical-bcp-organizational-v0.28.0'
M29_VERSION='0.29.0'
def sha256_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def write_json(p,obj): Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def load(p): return json.loads(Path(p).read_text())
