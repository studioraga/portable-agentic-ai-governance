from __future__ import annotations
import hashlib,json
from pathlib import Path
M26_BASELINE_COMMIT="82b9331edbe1d12f30b6283b15584ac506038018"
M26_BASELINE_TAG="m26-soc-incident-backup-dr-v0.26.0"
M27_VERSION="0.27.0"
def sha256_file(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def write_json(path,obj):
 Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
