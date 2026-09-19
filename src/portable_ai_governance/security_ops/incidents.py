from __future__ import annotations
import fcntl,json,os,time,uuid
from .common import canonical_json_bytes,sha256_bytes
from pathlib import Path
class IncidentError(RuntimeError):pass
ALLOWED={'open':{'contained'},'contained':{'recovering'},'recovering':{'recovered'},'recovered':{'closed'},'closed':set()}
class IncidentStore:
 def __init__(self,path):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700);self.path.touch(exist_ok=True,mode=0o600);os.chmod(self.path,0o600)
 def _rows(self):return [json.loads(x) for x in self.path.read_text().splitlines() if x.strip()]
 def create(self,event):
  iid='inc-'+uuid.uuid4().hex[:16];r={'incident_id':iid,'event_id':event['event_id'],'severity':event['severity'],'status':'open','created_at':int(time.time()),'updated_at':int(time.time()),'subject':event['subject']};self._append(r);return r
 def current(self,iid):
  rows=[x for x in self._rows() if x['incident_id']==iid]
  if not rows:raise IncidentError('incident not found')
  return rows[-1]
 def transition(self,iid,to,reason):
  cur=self.current(iid)
  if to not in ALLOWED.get(cur['status'],set()):raise IncidentError(f'illegal transition {cur["status"]}->{to}')
  r={**cur,'status':to,'reason':reason,'updated_at':int(time.time())};self._append(r);return r
 def _append(self,r):
  with self.path.open('a+',encoding='utf-8') as f:
   fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.seek(0);rows=[json.loads(x) for x in f if x.strip()];prev=rows[-1].get('record_sha256','0'*64) if rows else '0'*64;base={k:v for k,v in r.items() if k not in {'journal_seq','prev_sha256','record_sha256'}};core={**base,'journal_seq':len(rows)+1,'prev_sha256':prev};rec={**core,'record_sha256':sha256_bytes(canonical_json_bytes(core))};f.seek(0,2);f.write(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno())
 def verify(self):
  prev='0'*64;seq=0
  for line in self.path.read_text().splitlines():
   if not line.strip():continue
   r=json.loads(line);seq+=1;core={k:v for k,v in r.items() if k!='record_sha256'}
   if r.get('journal_seq')!=seq or r.get('prev_sha256')!=prev or r.get('record_sha256')!=sha256_bytes(canonical_json_bytes(core)):return False,f'incident journal chain failure at {seq}'
   prev=r['record_sha256']
  return True,f'verified {seq} incident journal records'
