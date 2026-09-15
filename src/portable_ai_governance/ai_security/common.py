from __future__ import annotations
import hashlib, json, os
from pathlib import Path

def sha256_file(path: str|Path)->str:
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def load_json(path: str|Path): return json.loads(Path(path).read_text())
def write_private_json(path: str|Path, doc)->None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True,mode=0o700); p.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n'); p.chmod(0o600)
def secure_tree(root: str|Path)->None:
    r=Path(root)
    for d in [r,*[p for p in r.rglob('*') if p.is_dir()]]: d.chmod(0o700)
    for f in [p for p in r.rglob('*') if p.is_file()]: f.chmod(0o600)
