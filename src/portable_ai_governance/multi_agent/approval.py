from __future__ import annotations
import fcntl,json,os,tempfile,time
from dataclasses import dataclass,asdict,fields
from pathlib import Path
from .common import canonical_json_bytes,sha256_obj
from ..supply_chain.signing import sign_blob,verify_blob
SCHEMA='pag-m10-signed-workflow-decision-v1'
class WorkflowDecisionError(RuntimeError):pass
@dataclass(frozen=True)
class WorkflowDecisionGrant:
 decision_id:str;workflow_id:str;proposal_sha256:str;assurance_sha256:str;reviewer:str;decision:str;issued_at:int;expires_at:int;max_uses:int=1

def _blob(path,g):path.write_bytes(canonical_json_bytes(asdict(g)));os.chmod(path,0o600)
class DecisionIssuer:
 def __init__(self,private_key):self.private_key=Path(private_key)
 def sign(self,g):
  if g.decision not in {'approve','reject'}:raise WorkflowDecisionError('decision invalid')
  with tempfile.TemporaryDirectory() as td:
   b=Path(td)/'grant.json';s=Path(td)/'grant.sig';_blob(b,g);sign_blob(b,self.private_key,s);return s.read_text().strip()
class DecisionVerifier:
 def __init__(self,public_key,max_ttl_seconds=1800,clock_skew_seconds=60):self.public_key=Path(public_key);self.max_ttl_seconds=int(max_ttl_seconds);self.clock_skew_seconds=int(clock_skew_seconds)
 def verify(self,g,sig,now=None):
  n=int(time.time()) if now is None else int(now)
  with tempfile.TemporaryDirectory() as td:
   b=Path(td)/'grant.json';s=Path(td)/'grant.sig';_blob(b,g);s.write_text(sig+'\n')
   if not verify_blob(b,self.public_key,s):raise WorkflowDecisionError('workflow decision signature invalid')
  if g.max_uses!=1:raise WorkflowDecisionError('workflow decision must be single-use')
  if g.issued_at>n+self.clock_skew_seconds:raise WorkflowDecisionError('workflow decision issued in future')
  if g.expires_at<=g.issued_at or n>=g.expires_at:raise WorkflowDecisionError('workflow decision expired')
  if g.expires_at-g.issued_at>self.max_ttl_seconds:raise WorkflowDecisionError('workflow decision TTL exceeds policy')
  if g.decision not in {'approve','reject'}:raise WorkflowDecisionError('workflow decision invalid')
def to_dict(g,sig):return {'schema':SCHEMA,'grant':asdict(g),'signature':sig}
def from_dict(d):
 if not isinstance(d,dict) or set(d)!={'schema','grant','signature'} or d.get('schema')!=SCHEMA:raise WorkflowDecisionError('signed workflow decision envelope invalid')
 gd=d['grant'];req={f.name for f in fields(WorkflowDecisionGrant)}
 if not isinstance(gd,dict) or set(gd)!=req:raise WorkflowDecisionError('workflow decision grant fields invalid')
 try:g=WorkflowDecisionGrant(**gd)
 except Exception as e:raise WorkflowDecisionError('workflow decision grant invalid') from e
 if not isinstance(d['signature'],str) or not d['signature']:raise WorkflowDecisionError('workflow decision signature missing')
 return g,d['signature']
class DecisionUseStore:
 def __init__(self,path):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
  if not self.path.exists():self.path.touch(mode=0o600)
  os.chmod(self.path,0o600)
 def claim(self,decision_id,workflow_id):
  with self.path.open('a+',encoding='utf-8') as f:
   fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.seek(0)
   for line in f:
    if not line.strip():continue
    record=json.loads(line)
    if record.get('decision_id')==decision_id:raise WorkflowDecisionError('workflow decision already used')
    if record.get('workflow_id')==workflow_id:raise WorkflowDecisionError('workflow already finalized')
   f.seek(0,2);f.write(json.dumps({'decision_id':decision_id,'workflow_id':workflow_id,'used_at':int(time.time())},sort_keys=True,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno())
