from __future__ import annotations
import fcntl,json,os,time
from pathlib import Path
from .common import sha256_obj
class StoreError(RuntimeError):pass
class WorkflowJournal:
 def __init__(self,path):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
  if not self.path.exists():self.path.touch(mode=0o600)
  os.chmod(self.path,0o600)
 def append(self,workflow_id,event,data):
  with self.path.open('a+',encoding='utf-8') as f:
   fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.seek(0);prev='0'*64;seq=0
   for line in f:
    if line.strip():
     r=json.loads(line);prev=r['record_sha256'];seq=max(seq,int(r['sequence']))
   body={'sequence':seq+1,'previous_record_sha256':prev,'workflow_id':workflow_id,'event':event,'timestamp':int(time.time()),'data':data}
   body['record_sha256']=sha256_obj(body);f.seek(0,2);f.write(json.dumps(body,sort_keys=True,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno());return body
 def verify(self):
  prev='0'*64;seq=0
  for line in self.path.read_text().splitlines():
   if not line.strip():continue
   r=json.loads(line);dig=r.pop('record_sha256')
   if r['sequence']!=seq+1 or r['previous_record_sha256']!=prev or sha256_obj(r)!=dig:return False
   seq=r['sequence'];prev=dig
  return True
 def events(self,workflow_id):
  out=[]
  for line in self.path.read_text().splitlines():
   if line.strip():
    r=json.loads(line)
    if r.get('workflow_id')==workflow_id:out.append(r)
  return out
