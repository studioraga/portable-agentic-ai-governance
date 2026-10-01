from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone,timedelta

def canonical_json_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(",",":")).encode()
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def sha256_file(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()
def stable_id(prefix,*parts): return prefix+'-'+sha256_bytes(canonical_json_bytes(parts))[:20]
def parse_ts(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def z(dt): return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
def write_json(path,obj):
 path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');path.chmod(0o600)
