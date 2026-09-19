from __future__ import annotations
import json,os,tempfile,time,uuid,fcntl
from dataclasses import dataclass,asdict,fields
from pathlib import Path
from .common import canonical_json_bytes,sha256_bytes
from ..supply_chain.signing import sign_blob,verify_blob
class RecoveryAuthorizationError(RuntimeError):pass
SCHEMA='pag-m9-recovery-authorization-v1'
@dataclass(frozen=True)
class RecoveryGrant:
 authorization_id:str;incident_id:str;containment_id:str;operator:str;checks_sha256:str;issued_at:int;expires_at:int;max_uses:int=1
@dataclass(frozen=True)
class SignedRecoveryAuthorization:grant:RecoveryGrant;signature:str
class RecoveryIssuer:
 def __init__(self,key):self.key=Path(key)
 def issue(self,incident_id,containment_id,operator,checks,ttl=900):
  now=int(time.time());g=RecoveryGrant(str(uuid.uuid4()),incident_id,containment_id,operator,sha256_bytes(canonical_json_bytes(checks)),now,now+ttl,1)
  with tempfile.TemporaryDirectory() as td:
   b=Path(td)/'g.json';s=Path(td)/'g.sig';b.write_bytes(canonical_json_bytes(asdict(g)));sign_blob(b,self.key,s);return SignedRecoveryAuthorization(g,s.read_text().strip())
class RecoveryVerifier:
 def __init__(self,key,max_ttl=900):self.key=Path(key);self.max_ttl=max_ttl
 def verify(self,a,checks,operators):
  g=a.grant;now=int(time.time())
  with tempfile.TemporaryDirectory() as td:
   b=Path(td)/'g.json';s=Path(td)/'g.sig';b.write_bytes(canonical_json_bytes(asdict(g)));s.write_text(a.signature+'\n')
   if not verify_blob(b,self.key,s):raise RecoveryAuthorizationError('recovery authorization signature invalid')
  if g.operator not in operators:raise RecoveryAuthorizationError('operator not authorized')
  if g.max_uses!=1:raise RecoveryAuthorizationError('recovery authorization must be single-use')
  if g.expires_at<=g.issued_at or now>=g.expires_at:raise RecoveryAuthorizationError('recovery authorization expired')
  if g.expires_at-g.issued_at>self.max_ttl:raise RecoveryAuthorizationError('recovery authorization TTL exceeds policy')
  if g.checks_sha256!=sha256_bytes(canonical_json_bytes(checks)):raise RecoveryAuthorizationError('recovery checks binding mismatch')
def to_dict(a):return {'schema':SCHEMA,'grant':asdict(a.grant),'signature':a.signature}
def from_dict(d):
 if not isinstance(d,dict) or set(d)!={'schema','grant','signature'} or d.get('schema')!=SCHEMA:raise RecoveryAuthorizationError('invalid recovery authorization envelope')
 g=d.get('grant',{});req={x.name for x in fields(RecoveryGrant)}
 if set(g)!=req:raise RecoveryAuthorizationError('recovery grant fields invalid')
 return SignedRecoveryAuthorization(RecoveryGrant(**g),str(d['signature']))
class RecoveryUseStore:
 def __init__(self,path):self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700);self.path.touch(exist_ok=True,mode=0o600);os.chmod(self.path,0o600)
 def used(self,aid):
  with self.path.open('r',encoding='utf-8') as f:
   return any(json.loads(x).get('authorization_id')==aid for x in f if x.strip())
 def claim(self,aid):
  with self.path.open('a+',encoding='utf-8') as f:
   fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.seek(0)
   if any(json.loads(x).get('authorization_id')==aid for x in f if x.strip()):raise RecoveryAuthorizationError('recovery authorization already used')
   f.seek(0,2);f.write(json.dumps({'authorization_id':aid,'used_at':int(time.time())},sort_keys=True,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno())
