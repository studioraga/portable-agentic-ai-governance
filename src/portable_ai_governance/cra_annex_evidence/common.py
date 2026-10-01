from __future__ import annotations
import hashlib,json
from pathlib import Path

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def write_json(path,obj):
    p=Path(path);p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');p.chmod(0o600)
