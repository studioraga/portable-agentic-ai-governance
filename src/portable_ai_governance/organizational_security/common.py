from __future__ import annotations
import hashlib,json
from pathlib import Path
M27_BASELINE_COMMIT="13aa11b8c9e8f693068f642e86e2ae9af7343226"
M27_BASELINE_TAG="m27-secure-sdlc-devsecops-appsec-v0.27.0"
M28_VERSION="0.28.0"
def sha256_file(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def write_json(path,obj): Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
