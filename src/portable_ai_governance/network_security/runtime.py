from __future__ import annotations
import json,subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M24_BASELINE_COMMIT,sha256_file
from .evaluation import evaluate_m25_policy
REQUIRED=['network-zone-policy.json','egress-policy.json','network-detection-policy.json','m25-control-mapping.json','m25-gap-closure.json','m25-validation-summary.json','m25-source-manifest.json','generated-nftables.conf','positive-flow-decision.json','negative-flow-decision.json','negative-egress-decision.json','m25-network-manifest.json','m25-network-manifest.json.sig','signing-public.pem']
def evaluate_m25_material(root,repo_root=None):
    root=Path(root);checks=[(f'present:{x}',(root/x).is_file()) for x in REQUIRED]
    if not all(v for _,v in checks):return {'ok':False,'checks':checks,'errors':['missing material']}
    m=json.loads((root/'m25-network-manifest.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m25-network-manifest.json',root/'signing-public.pem',root/'m25-network-manifest.json.sig')))
    for name,digest in m.get('artifacts',{}).items():checks.append((f'digest:{name}',(root/name).is_file() and sha256_file(root/name)==digest))
    checks.append(('m24-baseline-bound',m.get('m24_baseline_commit')==M24_BASELINE_COMMIT));checks.append(('node2-verifier-only',m.get('boundaries',{}).get('node2_verifier_only') is True))
    for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'):checks.append((f'manifest-boundary:{k}',m.get('claim_boundaries',{}).get(k) is False))
    if repo_root:
        repo=Path(repo_root);exists=subprocess.run(['git','-c',f'safe.directory={repo}','-C',str(repo),'cat-file','-e',f'{M24_BASELINE_COMMIT}^{{commit}}'],capture_output=True).returncode==0;checks.append(('m24-baseline-exists',exists))
        src=json.loads((root/'m25-source-manifest.json').read_text())
        for rel,digest in src.get('files',{}).items():checks.append((f'source:{rel}',(repo/rel).is_file() and sha256_file(repo/rel)==digest))
        net=json.loads((root/'network-zone-policy.json').read_text());eg=json.loads((root/'egress-policy.json').read_text());de=json.loads((root/'network-detection-policy.json').read_text());controls=json.loads((repo/'governance/controls/control-catalog.json').read_text());checks.append(('policy-evaluation',evaluate_m25_policy(net,eg,de,controls)['ok']))
    return {'ok':all(v for _,v in checks),'checks':checks,'errors':[]}
