from __future__ import annotations
import json
from pathlib import Path
from .common import sha256_file

def build_evidence_index(repo_root):
    root=Path(repo_root)
    mapping=json.loads((root/'governance/cra/m17/annex-i-evidence-map.json').read_text())['requirements']
    entries=[]
    for row in mapping:
        evidence=[]
        for rel in row['evidence_refs']:
            p=root/rel
            evidence.append({'path':rel,'present':p.is_file(),'sha256':sha256_file(p) if p.is_file() else None})
        entries.append({**row,'evidence':evidence,'all_references_present':all(x['present'] for x in evidence)})
    return {'version':'0.17.0','milestone':'M17','entries':entries}

def summarize(index):
    entries=index['entries'];states={}
    for e in entries:states[e['evidence_state']]=states.get(e['evidence_state'],0)+1
    return {'version':'0.17.0','total':len(entries),'part_i':sum('Annex I Part I(' in e['legal_reference'] for e in entries),'part_ii':sum('Annex I Part II(' in e['legal_reference'] for e in entries),'states':states,'all_references_present':all(e['all_references_present'] for e in entries),'cra_conformity_claim':False,'conformity_assessment_performed':False}

def gaps(index):
    return [{'requirement_id':e['requirement_id'],'legal_reference':e['legal_reference'],'evidence_state':e['evidence_state'],'reason':e.get('gap_reason') or 'Additional product-specific acceptance evidence is required.','planned_followup': 'M19 production validation' if e['requirement_id']=='CRA-REQ-060' else 'product-specific evidence closure'} for e in index['entries'] if e['evidence_state'] in {'PARTIAL','GAP'}]
