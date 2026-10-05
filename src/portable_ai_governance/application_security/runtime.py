from __future__ import annotations
import json,subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M26_BASELINE_COMMIT,sha256_file
from .evaluation import evaluate_m27_policy
from .pentest import validate_pentest_evidence
REQUIRED=['appsec-policy.json','secure-sdlc-policy.json','independent-pentest-evidence-policy.json','m27-control-mapping.json','m27-gap-closure.json','m27-validation-summary.json','m27-source-manifest.json','sast-report.json','secret-scan-report.json','sca-report.json','iac-container-report.json','dast-api-report.json','fuzz-report.json','pentest-evidence.json','appsec-gate-summary.json','m27-appsec-manifest.json','m27-appsec-manifest.json.sig','signing-public.pem']
def evaluate_m27_material(root,repo_root=None):
 root=Path(root);checks=[(f'present:{x}',(root/x).is_file()) for x in REQUIRED]
 if not all(v for _,v in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
 m=json.loads((root/'m27-appsec-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m27-appsec-manifest.json',root/'signing-public.pem',root/'m27-appsec-manifest.json.sig')))
 for name,digest in m.get('artifacts',{}).items():checks.append((f'digest:{name}',(root/name).is_file() and sha256_file(root/name)==digest))
 checks += [('m26-baseline-bound',m.get('m26_baseline_commit')==M26_BASELINE_COMMIT),('node2-verifier-only',m.get('boundaries',{}).get('node2_verifier_only') is True),('simulated-pentest-not-production',m.get('boundaries',{}).get('simulated_pentest_is_not_production_evidence') is True)]
 for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim','production_pentest_completed_claim'): checks.append((f'manifest-boundary:{k}',m.get('claim_boundaries',{}).get(k) is False))
 gate=json.loads((root/'appsec-gate-summary.json').read_text());checks.append(('appsec-gate-pass',gate.get('ok') is True))
 try: validate_pentest_evidence(json.loads((root/'pentest-evidence.json').read_text()),production=False);checks.append(('pentest-evidence-structure',True))
 except Exception: checks.append(('pentest-evidence-structure',False))
 if repo_root:
  repo=Path(repo_root);exists=subprocess.run(['git','-c',f'safe.directory={repo}','-C',str(repo),'cat-file','-e',f'{M26_BASELINE_COMMIT}^{{commit}}'],capture_output=True).returncode==0;checks.append(('m26-baseline-exists',exists))
  src=json.loads((root/'m27-source-manifest.json').read_text())
  for rel,digest in src.get('files',{}).items():checks.append((f'source:{rel}',(repo/rel).is_file() and sha256_file(repo/rel)==digest))
  J=lambda n:json.loads((root/n).read_text());controls=json.loads((repo/'governance/controls/control-catalog.json').read_text());mapping=json.loads((repo/'governance/mappings/framework-mapping.json').read_text());checks.append(('policy-evaluation',evaluate_m27_policy(J('appsec-policy.json'),controls,mapping,J('m27-gap-closure.json'))['ok']))
 return {'ok':all(v for _,v in checks),'checks':checks,'errors':[]}
