from __future__ import annotations
import hashlib, json, os
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def write_private_json(path, obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    os.chmod(p,0o600)

def secure_tree(root):
    r=Path(root)
    for d,dirs,files in os.walk(r):
        os.chmod(d,0o700)
        for f in files: os.chmod(Path(d)/f,0o600)
