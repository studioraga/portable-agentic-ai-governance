from __future__ import annotations
from .common import canonical_json_bytes,sha256_bytes

def build_awareness_journal(cases):
    out=[];prev='0'*64
    seen={}
    for i,c in enumerate(cases,1):
        cid=c['case_id'];t0=c['manufacturer_awareness_at']
        if cid in seen and seen[cid]!=t0: raise ValueError('manufacturer awareness timestamp is immutable')
        seen[cid]=t0
        core={'case_id':cid,'case_type':c['case_type'],'manufacturer_awareness_at':t0,'journal_seq':i,'prev_sha256':prev}
        rec={**core,'record_sha256':sha256_bytes(canonical_json_bytes(core))};out.append(rec);prev=rec['record_sha256']
    return out

def verify_awareness_journal(rows):
    prev='0'*64
    for i,r in enumerate(rows,1):
        core={k:v for k,v in r.items() if k!='record_sha256'}
        if r.get('journal_seq')!=i or r.get('prev_sha256')!=prev:return False
        if r.get('record_sha256')!=sha256_bytes(canonical_json_bytes(core)):return False
        prev=r['record_sha256']
    return True
