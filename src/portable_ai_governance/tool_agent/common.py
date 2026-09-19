from __future__ import annotations
import hashlib,json,os
from pathlib import Path

def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def sha256_bytes(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def sha256_file(path)->str:
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def canonical_json_bytes(value)->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def write_private_json(path,value):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True,mode=0o700); p.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.chmod(p,0o600)
def secure_tree(root):
    r=Path(root)
    for p in [r,*r.rglob("*")]:
        if p.is_dir(): os.chmod(p,0o700)
        elif p.is_file(): os.chmod(p,0o600)
