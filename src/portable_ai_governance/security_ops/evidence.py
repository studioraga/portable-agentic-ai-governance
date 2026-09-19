from __future__ import annotations
import json,os,shutil,time
from pathlib import Path
from .common import sha256_file,write_json
class EvidenceError(RuntimeError):pass
class EvidenceVault:
 def __init__(self,root,max_bytes=10485760):self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(self.root,0o700);self.max_bytes=max_bytes
 def preserve(self,incident_id,paths):
  d=self.root/incident_id;d.mkdir(parents=True,exist_ok=True,mode=0o700);items=[]
  for i,p0 in enumerate(paths):
   p=Path(p0).resolve()
   if not p.is_file():raise EvidenceError(f'evidence missing: {p}')
   if p.name in {'signing-private.pem','approval-signing-private.pem','recovery-signing-private.pem','ca.key'}:raise EvidenceError('private signing/key material cannot be preserved as incident evidence')
   if p.stat().st_size>self.max_bytes:raise EvidenceError('evidence exceeds max bytes')
   out=d/f'{i:03d}-{p.name}';shutil.copyfile(p,out);os.chmod(out,0o600);items.append({'name':out.name,'source':str(p),'size':out.stat().st_size,'sha256':sha256_file(out)})
  m={'incident_id':incident_id,'preserved_at':int(time.time()),'items':items};write_json(d/'manifest.json',m);return m
 def verify(self,incident_id):
  d=self.root/incident_id
  if not (d/'manifest.json').is_file():return False,'evidence manifest missing'
  m=json.loads((d/'manifest.json').read_text())
  for x in m['items']:
   p=d/x['name']
   if not p.is_file() or sha256_file(p)!=x['sha256']:return False,f'evidence mismatch: {x["name"]}'
  return True,f'verified {len(m["items"])} evidence artifacts'
