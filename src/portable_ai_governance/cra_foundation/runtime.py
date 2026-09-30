from __future__ import annotations
import json,hashlib
from pathlib import Path
from .catalog import load_requirement_matrix,validate_requirement_matrix,coverage_summary
from portable_ai_governance.supply_chain.signing import verify_blob

def sha256_file(path):
    h=hashlib.sha256();
    with Path(path).open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()

def evaluate_m11_material(root, repo_root=None):
    root=Path(root); checks=[]
    required=['cra-requirements.json','node-role-profile.json','cra-coverage-report.json','m11-cra-manifest.json','m11-cra-manifest.json.sig','signing-public.pem']
    for f in required: checks.append((f'present:{f}',(root/f).is_file()))
    if not all(ok for _,ok in checks): return {'ok':False,'checks':checks}
    manifest=json.loads((root/'m11-cra-manifest.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m11-cra-manifest.json',root/'signing-public.pem',root/'m11-cra-manifest.json.sig')))
    for name,digest in manifest.get('artifacts',{}).items(): checks.append((f'digest:{name}',sha256_file(root/name)==digest))
    matrix=load_requirement_matrix(root/'cra-requirements.json'); errors=validate_requirement_matrix(matrix,repo_root)
    checks.append(('requirement-matrix-valid',not errors))
    roles=json.loads((root/'node-role-profile.json').read_text()); b=roles.get('boundaries',{})
    checks.append(('node1-private-authority',b.get('private_signing_keys_node1_only') is True))
    checks.append(('node2-verifier-only',b.get('node2_verifier_only') is True))
    checks.append(('m11-no-reporting-side-effects',b.get('m11_reporting_side_effects') is False and b.get('m11_network_reporting') is False))
    report=json.loads((root/'cra-coverage-report.json').read_text()); checks.append(('no-conformity-claim',report.get('cra_conformity_claim') is False))
    return {'ok':all(ok for _,ok in checks),'checks':checks,'errors':errors,'coverage':coverage_summary(matrix)}
