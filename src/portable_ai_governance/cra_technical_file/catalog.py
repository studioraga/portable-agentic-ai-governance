from __future__ import annotations
import json
from pathlib import Path
from .common import sha256_file

def build_technical_file_index(repo_root):
    root=Path(repo_root)
    m=json.loads((root/'governance/cra/m18/annex-vii-map.json').read_text())
    entries=[]
    for section in m['sections']:
        ev=[]
        for rel in section.get('evidence_refs',[]):
            p=root/rel
            ev.append({'path':rel,'present':p.is_file(),'sha256':sha256_file(p) if p.is_file() else None})
        entries.append({**section,'evidence':ev})
    return {'version':'0.18.0','milestone':'M18','entries':entries,'cra_conformity_claim':False}

def summarize(index):
    states={}
    all_present=True
    for e in index['entries']:
        states[e['readiness']]=states.get(e['readiness'],0)+1
        all_present &= all(x['present'] for x in e['evidence'])
    return {'total_sections':len(index['entries']),'states':states,'all_references_present':all_present,'cra_conformity_claim':False}

def gaps(index):
    return [{'section_id':e['section_id'],'legal_reference':e['legal_reference'],'title':e['title'],'readiness':e['readiness'],'notes':e.get('notes')} for e in index['entries'] if e['readiness']!='READY']
