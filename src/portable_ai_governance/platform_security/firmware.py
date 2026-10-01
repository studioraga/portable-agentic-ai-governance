from __future__ import annotations
import json,re
from pathlib import Path
from .common import sha256_file,write_json
from portable_ai_governance.supply_chain.signing import sign_blob,verify_blob

def _vtuple(v):
    return tuple(int(x) for x in re.findall(r'\d+',str(v))[:4]) or (0,)

def make_descriptor(payload, firmware_id, version, rollback_counter, out):
    d={'schema_version':'1.0','firmware_id':firmware_id,'version':str(version),'rollback_counter':int(rollback_counter),'payload_sha256':sha256_file(payload),'signed':True}
    write_json(out,d);return d

def sign_descriptor(desc,private_key,sig): sign_blob(desc,private_key,sig)
def verify_descriptor(desc,payload,pub,sig):
    d=json.loads(Path(desc).read_text())
    return verify_blob(desc,pub,sig) and sha256_file(payload)==d.get('payload_sha256')

def evaluate_update(current_version,current_counter,desc):
    d=desc if isinstance(desc,dict) else json.loads(Path(desc).read_text())
    reasons=[]
    if _vtuple(d['version'])<=_vtuple(current_version): reasons.append('rollback_or_non_monotonic_version')
    if int(d['rollback_counter'])<=int(current_counter): reasons.append('rollback_counter_not_advanced')
    return {'decision':'ACCEPT' if not reasons else 'REJECT','reasons':reasons,'current_version':str(current_version),'target_version':d['version'],'current_counter':int(current_counter),'target_counter':int(d['rollback_counter'])}
