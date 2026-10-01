from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file
def evaluate_m20_material(root,repo_root=None):
 r=Path(root);req=['final-freeze-policy.json','enterprise-deployment-plan.json','m20-control-mapping.json','release-freeze-summary.json','release-source-fingerprints.json','m20-final-freeze-manifest.json','m20-final-freeze-manifest.json.sig','signing-public.pem'];checks=[(f'present:{x}',(r/x).is_file()) for x in req]
 if not all(v for _,v in checks):return {'ok':False,'checks':checks,'errors':['missing material']}
 m=json.loads((r/'m20-final-freeze-manifest.json').read_text());s=json.loads((r/'release-freeze-summary.json').read_text());p=json.loads((r/'final-freeze-policy.json').read_text())
 checks.append(('manifest-signature',verify_blob(r/'m20-final-freeze-manifest.json',r/'signing-public.pem',r/'m20-final-freeze-manifest.json.sig')))
 for n,d in m['artifacts'].items():checks.append((f'digest:{n}',sha256_file(r/n)==d))
 b=p['boundaries'];checks += [('one-shot',b['enterprise_one_shot_deployment'] is True),('simulation-no-final-freeze',b['simulation_must_not_claim_final_freeze'] is True),('no-conformity-claim',b['cra_conformity_claim'] is False),('no-conformity-assessment',b['conformity_assessment_performed'] is False),('node1-authority',b['node1_release_authority'] is True),('node2-verifier-only',b['node2_verifier_only'] is True),('no-host-update',b['host_os_update_performed'] is False),('no-firmware-flash',b['firmware_flash_performed'] is False)]
 if s['m19_validation_mode']!='LIVE':checks.append(('simulation-release-candidate-only',s['final_freeze_ready'] is False and s['freeze_state']=='RELEASE_CANDIDATE'))
 if repo_root:
  rr=Path(repo_root);fps=json.loads((r/'release-source-fingerprints.json').read_text())
  for path,dig in fps.items():checks.append((f'source:{path}',(rr/path).is_file() and sha256_file(rr/path)==dig))
 ok=all(v for _,v in checks);return {'ok':ok,'checks':checks,'errors':[] if ok else ['one or more checks failed'],'freeze_state':s['freeze_state'],'final_freeze_ready':s['final_freeze_ready']}
