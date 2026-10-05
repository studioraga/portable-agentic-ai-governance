from __future__ import annotations
import json,subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M25_BASELINE_COMMIT,sha256_file
from .evaluation import evaluate_m26_policy
REQUIRED=['soc-policy.json','vulnerability-operations-policy.json','incident-response-policy.json','backup-dr-policy.json','m26-control-mapping.json','m26-gap-closure.json','m26-validation-summary.json','m26-source-manifest.json','soc-normalized-events.json','soc-correlation-alerts.json','vulnerability-assessments.json','incident-playbook-result.json','backup-record.json','restore-test-report.json','m26-ops-manifest.json','m26-ops-manifest.json.sig','signing-public.pem']
def evaluate_m26_material(root,repo_root=None):
 root=Path(root);checks=[(f'present:{x}',(root/x).is_file()) for x in REQUIRED]
 if not all(v for _,v in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
 m=json.loads((root/'m26-ops-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m26-ops-manifest.json',root/'signing-public.pem',root/'m26-ops-manifest.json.sig')))
 for name,digest in m.get('artifacts',{}).items(): checks.append((f'digest:{name}',(root/name).is_file() and sha256_file(root/name)==digest))
 checks += [('m25-baseline-bound',m.get('m25_baseline_commit')==M25_BASELINE_COMMIT),('node2-verifier-only',m.get('boundaries',{}).get('node2_verifier_only') is True),('non-destructive-validation',m.get('boundaries',{}).get('validation_does_not_modify_live_soc_or_backup_infrastructure') is True)]
 for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'): checks.append((f'manifest-boundary:{k}',m.get('claim_boundaries',{}).get(k) is False))
 if repo_root:
  repo=Path(repo_root);exists=subprocess.run(['git','-c',f'safe.directory={repo}','-C',str(repo),'cat-file','-e',f'{M25_BASELINE_COMMIT}^{{commit}}'],capture_output=True).returncode==0;checks.append(('m25-baseline-exists',exists))
  src=json.loads((root/'m26-source-manifest.json').read_text())
  for rel,digest in src.get('files',{}).items(): checks.append((f'source:{rel}',(repo/rel).is_file() and sha256_file(repo/rel)==digest))
  J=lambda n:json.loads((root/n).read_text());controls=json.loads((repo/'governance/controls/control-catalog.json').read_text());checks.append(('policy-evaluation',evaluate_m26_policy(J('soc-policy.json'),J('vulnerability-operations-policy.json'),J('incident-response-policy.json'),J('backup-dr-policy.json'),controls)['ok']))
 restore=json.loads((root/'restore-test-report.json').read_text());checks += [('restore-digest-match',restore.get('digest_match') is True),('rpo-met',restore.get('rpo_met') is True),('rto-met',restore.get('rto_met') is True),('immutable-source',restore.get('immutable_source') is True)]
 return {'ok':all(v for _,v in checks),'checks':checks,'errors':[]}
