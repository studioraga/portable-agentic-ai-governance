from __future__ import annotations
import json,subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M28_BASELINE_COMMIT,sha256_file
from .aggregation import verify_inputs
REQUIRED=['cross-domain-validation-policy.json','m29-control-mapping.json','m29-reconciliation.json','m29-requirement-matrix.json','m29-cross-domain-summary.json','m29-source-manifest.json','m29-input-index.json','m29-enterprise-validation-manifest.json','m29-enterprise-validation-manifest.json.sig','signing-public.pem']
def evaluate_m29_material(root,repo_root=None,require_node2_marker=False):
 root=Path(root);checks=[(f'present:{x}',(root/x).is_file()) for x in REQUIRED];errors=[]
 if not all(v for _,v in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
 m=json.loads((root/'m29-enterprise-validation-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m29-enterprise-validation-manifest.json',root/'signing-public.pem',root/'m29-enterprise-validation-manifest.json.sig')))
 for n,d in m.get('artifacts',{}).items():checks.append((f'digest:{n}',(root/n).is_file() and sha256_file(root/n)==d))
 checks += [('m28-baseline-bound',m.get('m28_baseline_commit')==M28_BASELINE_COMMIT),('node2-verifier-only',m.get('boundaries',{}).get('node2_verifier_only') is True)]
 for k,v in m.get('claim_boundaries',{}).items(): checks.append((f'claim-boundary:{k}',v is False))
 if repo_root:
  repo=Path(repo_root);checks.append(('m28-baseline-exists',subprocess.run(['git','-c',f'safe.directory={repo}','-C',str(repo),'cat-file','-e',f'{M28_BASELINE_COMMIT}^{{commit}}'],capture_output=True).returncode==0))
  src=json.loads((root/'m29-source-manifest.json').read_text())
  for rel,d in src.get('files',{}).items():checks.append((f'source:{rel}',(repo/rel).is_file() and sha256_file(repo/rel)==d))
  nested=verify_inputs(root/'inputs',repo);checks.append(('all-nested-milestones-verify',all(x.get('ok') for x in nested.values())))
 if require_node2_marker: checks.append(('node2-marker',(root/'node2-independent-verification.json').is_file()))
 return {'ok':all(v for _,v in checks),'checks':checks,'errors':errors}
