from __future__ import annotations
import fcntl,json,os,time,uuid
from .common import canonical_json_bytes,sha256_bytes
from pathlib import Path
class ContainmentStore:
 def __init__(self,path):self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700);self.path.touch(exist_ok=True,mode=0o600);os.chmod(self.path,0o600)
 def _append(self,rec):
  with self.path.open('a+',encoding='utf-8') as f:
   fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.seek(0);rows=[json.loads(x) for x in f if x.strip()];prev=rows[-1].get('record_sha256','0'*64) if rows else '0'*64;core={**rec,'journal_seq':len(rows)+1,'prev_sha256':prev};out={**core,'record_sha256':sha256_bytes(canonical_json_bytes(core))};f.seek(0,2);f.write(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno());return out
 def apply(self,incident,event,action):
  return self._append({'containment_id':'cnt-'+uuid.uuid4().hex[:16],'incident_id':incident['incident_id'],'event_id':event['event_id'],'action':action,'subject':event['subject'],'status':'active','created_at':int(time.time())})
 def release(self,containment_id,incident_id):
  rows=[json.loads(x) for x in self.path.read_text().splitlines() if x.strip() and json.loads(x).get('containment_id')==containment_id]
  if not rows or rows[-1].get('incident_id')!=incident_id or rows[-1].get('status')!='active':raise RuntimeError('active containment not found for incident')
  return self._append({'containment_id':containment_id,'incident_id':incident_id,'status':'released','released_at':int(time.time())})
 def verify(self):
  prev='0'*64;seq=0
  for line in self.path.read_text().splitlines():
   if not line.strip():continue
   r=json.loads(line);seq+=1;core={k:v for k,v in r.items() if k!='record_sha256'}
   if r.get('journal_seq')!=seq or r.get('prev_sha256')!=prev or r.get('record_sha256')!=sha256_bytes(canonical_json_bytes(core)):return False,f'containment journal chain failure at {seq}'
   prev=r['record_sha256']
  return True,f'verified {seq} containment journal records'
