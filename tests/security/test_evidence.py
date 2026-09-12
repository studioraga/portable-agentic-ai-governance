import json
from portable_ai_governance.kernel.evidence import EvidenceLedger

def test_evidence_chain_detects_tampering(tmp_path):
    p=tmp_path/"ledger.jsonl"; l=EvidenceLedger(p,b"e"*32); l.append("x",{"a":1}); l.append("y",{"b":2})
    ok,_=l.verify(); assert ok
    rows=p.read_text().splitlines(); obj=json.loads(rows[0]); obj["payload"]["a"]=999; rows[0]=json.dumps(obj); p.write_text("\n".join(rows)+"\n")
    ok,detail=l.verify(); assert not ok and "mismatch" in detail
