from __future__ import annotations
import json,subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M27_BASELINE_COMMIT,sha256_file
from .evaluation import evaluate_m28_policy
REQUIRED=['organizational-governance-policy.json','personnel-security-policy.json','physical-environmental-policy.json','business-continuity-policy.json','m28-control-mapping.json','m28-gap-closure.json','governance-charter.json','governance-attestation.json','personnel-evidence.json','physical-environmental-evidence.json','bcp-plan.json','bcp-exercise-evidence.json','m28-validation-summary.json','m28-source-manifest.json','m28-organizational-manifest.json','m28-organizational-manifest.json.sig','signing-public.pem']
def evaluate_m28_material(root,repo_root=None):
 root=Path(root);checks=[(f'present:{x}',(root/x).is_file()) for x in REQUIRED]
 if not all(v for _,v in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
 m=json.loads((root/'m28-organizational-manifest.json').read_text()); checks.append(('manifest-signature',verify_blob(root/'m28-organizational-manifest.json',root/'signing-public.pem',root/'m28-organizational-manifest.json.sig')))
 for n,d in m.get('artifacts',{}).items(): checks.append((f'digest:{n}',(root/n).is_file() and sha256_file(root/n)==d))
 checks += [('m27-baseline-bound',m.get('m27_baseline_commit')==M27_BASELINE_COMMIT),('node2-verifier-only',m.get('boundaries',{}).get('node2_verifier_only') is True),('nontechnical-evidence-boundary',m.get('boundaries',{}).get('python_does_not_prove_real_world_control_operation') is True)]
 for k,v in m.get('claim_boundaries',{}).items(): checks.append((f'claim-boundary:{k}',v is False))
 if repo_root:
  repo=Path(repo_root);checks.append(('m27-baseline-exists',subprocess.run(['git','-c',f'safe.directory={repo}','-C',str(repo),'cat-file','-e',f'{M27_BASELINE_COMMIT}^{{commit}}'],capture_output=True).returncode==0))
  src=json.loads((root/'m28-source-manifest.json').read_text())
  for rel,digest in src.get('files',{}).items(): checks.append((f'source:{rel}',(repo/rel).is_file() and sha256_file(repo/rel)==digest))
  J=lambda p:json.loads((repo/p).read_text());ev=evaluate_m28_policy(J('governance/enterprise/m28/m28-control-mapping.json'),J('governance/controls/control-catalog.json'),J('governance/mappings/framework-mapping.json'),J('governance/enterprise/m28/m28-gap-closure.json'));checks.append(('policy-evaluation',ev['ok']))
 return {'ok':all(v for _,v in checks),'checks':checks,'errors':[]}
