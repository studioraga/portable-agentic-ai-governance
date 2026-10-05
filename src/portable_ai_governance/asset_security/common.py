from __future__ import annotations
import hashlib,json
from pathlib import Path
M23_BASELINE_COMMIT='7f56c13bdc33993998ca8750d0cab9510e3157aa'
M23_BASELINE_TAG='m23-enterprise-identity-mfa-pam-v0.23.0'
M24_VERSION='0.24.0'
CLASSIFICATIONS=('public','internal','confidential','restricted')
CRITICALITIES=('low','medium','high','critical')

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def write_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8');p.chmod(0o600)

def load_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
