from __future__ import annotations
import fcntl,json,os,time,uuid
from pathlib import Path
from .common import canonical_json_bytes,sha256_bytes
SEVERITIES={'low','medium','high','critical'}
class SIEMError(RuntimeError):pass
class SIEMStore:
 def __init__(self,path):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700);self.path.touch(exist_ok=True,mode=0o600);os.chmod(self.path,0o600)
 def ingest(self,event):
  e=dict(event); e.setdefault('event_id',str(uuid.uuid4()));e.setdefault('timestamp',int(time.time()))
  req={'event_id','event_type','severity','source','timestamp','subject'}
  if not req<=set(e):raise SIEMError('missing SIEM event fields')
  if e['severity'] not in SEVERITIES:raise SIEMError('invalid severity')
  if not all(isinstance(e[k],str) and e[k] for k in ('event_id','event_type','source','subject')):raise SIEMError('invalid SIEM event identity')
  if not isinstance(e['timestamp'],int) or e['timestamp']<0:raise SIEMError('invalid timestamp')
  with self.path.open('a+',encoding='utf-8') as f:
   fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.seek(0);rows=[json.loads(x) for x in f if x.strip()]
   if any(x['event']['event_id']==e['event_id'] for x in rows):raise SIEMError('duplicate event_id')
   prev=rows[-1]['record_sha256'] if rows else '0'*64; seq=len(rows)+1
   core={'seq':seq,'prev_sha256':prev,'event':e}; rec={**core,'record_sha256':sha256_bytes(canonical_json_bytes(core))}
   f.seek(0,2);f.write(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno());return rec
 def export_events(self,out_path):
  ok,detail=self.verify()
  if not ok:raise SIEMError(detail)
  out=Path(out_path);out.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
  rows=[json.loads(x)['event'] for x in self.path.read_text().splitlines() if x.strip()]
  out.write_text(''.join(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n' for x in rows));os.chmod(out,0o600);return len(rows)
 def verify(self):
  prev='0'*64;seq=0
  for line in self.path.read_text().splitlines():
   if not line.strip():continue
   r=json.loads(line);seq+=1
   core={'seq':r['seq'],'prev_sha256':r['prev_sha256'],'event':r['event']}
   if r['seq']!=seq or r['prev_sha256']!=prev or r['record_sha256']!=sha256_bytes(canonical_json_bytes(core)):return False,f'chain failure at {seq}'
   prev=r['record_sha256']
  return True,f'verified {seq} SIEM records'
