from __future__ import annotations
import hashlib,json,os
from pathlib import Path

def load_json(path):
    with open(path,'r',encoding='utf-8') as f: return json.load(f)
def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write_private_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    p.write_text(json.dumps(obj,sort_keys=True,indent=2)+"\n",encoding='utf-8'); os.chmod(p,0o600)
def secure_tree(root):
    root=Path(root)
    for p in [root,*root.rglob('*')]:
        if p.is_dir(): os.chmod(p,0o700)
        elif p.is_file(): os.chmod(p,0o600)
