from __future__ import annotations
import hashlib,json
from pathlib import Path
M24_BASELINE_COMMIT='62a1713ff468117cefc256c03d2a71f26928f8cc'
M24_BASELINE_TAG='m24-asset-security-data-lifecycle-v0.24.0'
M25_VERSION='0.25.0'
def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8');p.chmod(0o600)
def load_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
