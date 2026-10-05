from __future__ import annotations
import hashlib,json
from pathlib import Path
M25_BASELINE_COMMIT='138b56eacc8415de489581b15432c26dc1f1add8'
M25_BASELINE_TAG='m25-zero-trust-network-microsegmentation-v0.25.0'
M26_VERSION='0.26.0'
def canonical_json_bytes(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha256_bytes(v): return hashlib.sha256(v).hexdigest()
def sha256_file(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def write_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');p.chmod(0o600)
