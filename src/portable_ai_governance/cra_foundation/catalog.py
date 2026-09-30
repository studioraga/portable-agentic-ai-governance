from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

VALID_STATUS={'met','partial','gap'}

def load_requirement_matrix(path):
    return json.loads(Path(path).read_text())

def validate_requirement_matrix(matrix, repo_root=None):
    errors=[]; reqs=matrix.get('requirements',[]); ids=set(); controls=set(); proposals=set()
    if matrix.get('matrix_version')!='0.11.0': errors.append('matrix_version must be 0.11.0')
    if not reqs: errors.append('requirements must not be empty')
    if repo_root:
        cat=json.loads((Path(repo_root)/'governance/controls/control-catalog.json').read_text())
        controls={c['control_id'] for c in cat['controls']}
    for r in reqs:
        rid=r.get('requirement_id','')
        if rid in ids: errors.append(f'duplicate requirement_id: {rid}')
        ids.add(rid)
        if r.get('current_status') not in VALID_STATUS: errors.append(f'{rid}: invalid status')
        pc=r.get('proposed_control_id')
        if pc:
            if pc in proposals: errors.append(f'duplicate proposed_control_id: {pc}')
            proposals.add(pc)
        for c in r.get('mapped_controls',[]):
            if controls and c not in controls: errors.append(f'{rid}: unknown mapped control {c}')
        for rel in r.get('mapped_implementation',[]):
            if repo_root and not (Path(repo_root)/rel).exists(): errors.append(f'{rid}: missing mapped implementation {rel}')
        if r.get('current_status') in {'gap','partial'} and not pc: errors.append(f'{rid}: uncovered/partial requirement missing CRA proposed control')
    return errors

def coverage_summary(matrix):
    counts=Counter(r['current_status'] for r in matrix['requirements']); total=len(matrix['requirements'])
    by_domain={}
    for r in matrix['requirements']:
        by_domain.setdefault(r['domain'],Counter())[r['current_status']]+=1
    return {'total_requirements':total,'status_counts':dict(counts),'domains':{k:dict(v) for k,v in sorted(by_domain.items())},'cra_conformity_claim':False}
