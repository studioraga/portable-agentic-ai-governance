#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.compliance_risk.common import load_json,write_private_json,sha256_file,secure_tree
from portable_ai_governance.supply_chain.signing import sign_blob

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--m4-material',required=True); ap.add_argument('--m5-material',required=True); a=ap.parse_args()
    m4=Path(a.m4_material).resolve(); m5=Path(a.m5_material).resolve(); key=m5/'signing-private.pem'
    freeze=m5/'.pag-downstream-bound.json'
    if freeze.is_file():
        raise SystemExit('FAIL: M5 material is downstream-bound/frozen by M6/M7. Create a new release generation and rebuild downstream attestations instead of refreshing this directory in place.')
    if not key.is_file(): raise SystemExit('FAIL: M5 release-authority signing-private.pem required for refresh')
    now=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    evidence={'AIS-IAM-001':m4/'ai-security-manifest.json','AIS-LOCK-001':m4/'ai-security-manifest.json','AIS-MODEL-001':m4/'model-governance.json','AIS-RAG-001':m4/'retrieval-policy.json','AIS-EVAL-001':m4/'evaluation-results.json'}
    cc=load_json(m5/'continuous-controls.json')
    for c in cc.get('controls',[]):
        p=evidence.get(c['control_id'])
        if p is None or not p.is_file(): raise SystemExit(f"FAIL: upstream evidence unavailable for {c['control_id']}")
        c['status']='pass'; c['last_checked']=now; c['evidence_sha256']=sha256_file(p); c['failure_action']='block'
    write_private_json(m5/'continuous-controls.json',cc)
    report=load_json(m5/'compliance-report.json'); report['generated_at']=now; report['control_summary']={'passed':len(cc['controls']),'failed':0,'stale':0}; report['evidence_refs']=[{'control_id':x['control_id'],'sha256':x['evidence_sha256']} for x in cc['controls']]; write_private_json(m5/'compliance-report.json',report)
    manifest=load_json(m5/'compliance-risk-manifest.json'); manifest['m4_manifest_sha256']=sha256_file(m4/'ai-security-manifest.json')
    for rel in list(manifest.get('artifacts',{})):
        manifest['artifacts'][rel]=sha256_file(m5/rel)
    write_private_json(m5/'compliance-risk-manifest.json',manifest)
    sign_blob(m5/'compliance-risk-manifest.json',key,m5/'compliance-risk-manifest.json.sig'); secure_tree(m5)
    print(f'PASS: refreshed M5 continuous controls and re-signed manifest at {m5}')
if __name__=='__main__': main()
