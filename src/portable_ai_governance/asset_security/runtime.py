from __future__ import annotations
import json,subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M23_BASELINE_COMMIT,sha256_file
from .evaluation import evaluate_m24_policy
REQUIRED=['asset-security-policy.json','asset-register.json','data-lifecycle-policy.json','dlp-policy.json','cryptographic-lifecycle-policy.json','m24-control-mapping.json','m24-gap-closure.json','m24-validation-summary.json','m24-source-manifest.json','m24-asset-data-manifest.json','m24-asset-data-manifest.json.sig','signing-public.pem','positive-sanitization-record.json','positive-export-decision.json']
def evaluate_m24_material(root,repo_root=None):
    root=Path(root);checks=[(f'present:{x}',(root/x).is_file()) for x in REQUIRED]
    if not all(v for _,v in checks):return {'ok':False,'checks':checks,'errors':['missing material']}
    m=json.loads((root/'m24-asset-data-manifest.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m24-asset-data-manifest.json',root/'signing-public.pem',root/'m24-asset-data-manifest.json.sig')))
    for name,digest in m.get('artifacts',{}).items():checks.append((f'digest:{name}',(root/name).is_file() and sha256_file(root/name)==digest))
    checks.append(('m23-baseline-bound',m.get('m23_baseline_commit')==M23_BASELINE_COMMIT))
    checks.append(('node2-verifier-only',m.get('boundaries',{}).get('node2_verifier_only') is True))
    for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'):
        checks.append((f'manifest-boundary:{k}',m.get('claim_boundaries',{}).get(k) is False))
    if repo_root:
        repo=Path(repo_root);exists=subprocess.run(['git','-c',f'safe.directory={repo}','-C',str(repo),'cat-file','-e',f'{M23_BASELINE_COMMIT}^{{commit}}'],capture_output=True).returncode==0;checks.append(('m23-baseline-exists',exists))
        src=json.loads((root/'m24-source-manifest.json').read_text())
        for rel,digest in src.get('files',{}).items():checks.append((f'source:{rel}',(repo/rel).is_file() and sha256_file(repo/rel)==digest))
        objs=[json.loads((root/n).read_text()) for n in ['asset-security-policy.json','asset-register.json','data-lifecycle-policy.json','dlp-policy.json','cryptographic-lifecycle-policy.json']]
        controls=json.loads((repo/'governance/controls/control-catalog.json').read_text())
        checks.append(('policy-evaluation',evaluate_m24_policy(*objs,controls)['ok']))
    return {'ok':all(v for _,v in checks),'checks':checks,'errors':[]}
