from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file

def evaluate_m14_material(root,repo_root=None):
    root=Path(root)
    required=['reporting-policy.json','m14-control-mapping.json','reporting-packs.json','submission-readiness.json','srp-field-checklist.json','m14-reporting-manifest.json','m14-reporting-manifest.json.sig','signing-public.pem']
    checks=[(f'present:{f}',(root/f).is_file()) for f in required]
    if not all(ok for _,ok in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
    manifest=json.loads((root/'m14-reporting-manifest.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m14-reporting-manifest.json',root/'signing-public.pem',root/'m14-reporting-manifest.json.sig')))
    for n,d in manifest.get('artifacts',{}).items(): checks.append((f'digest:{n}',sha256_file(root/n)==d))
    b=manifest.get('boundaries',{})
    checks.extend([
      ('evidence-pack-only',b.get('evidence_pack_only') is True),('no-srp-submission',b.get('srp_submission_performed') is False),
      ('no-network-submission',b.get('network_submission') is False),('ar-handoff-required',b.get('assigned_representative_handoff_required') is True),
      ('no-conformity-claim',b.get('cra_conformity_claim') is False),('node2-verifier-only',b.get('node2_verifier_only') is True),
      ('srp-api-disabled',manifest.get('srp_api_available') is False)
    ])
    packs=json.loads((root/'reporting-packs.json').read_text())
    checks.append(('case-type-coverage',{'AEV','SEVERE_INCIDENT'}<={p['case_type'] for p in packs}))
    checks.append(('three-stage-coverage',all({s['stage'] for s in p['stages']}=={'EARLY_WARNING_24H','NOTIFICATION_72H','FINAL_REPORT'} for p in packs)))
    checks.append(('no-pack-side-effects',all(p['srp_submission_performed'] is False and p['network_submission_performed'] is False and p['cra_conformity_claim'] is False for p in packs)))
    checks.append(('human-submission-required',all(p['human_submission_required'] is True for p in packs)))
    readiness=json.loads((root/'submission-readiness.json').read_text())
    checks.append(('readiness-covered',len(readiness)==len(packs) and all(x['all_currently_anchored_stages_ready'] for x in readiness)))
    if repo_root:
      rr=Path(repo_root)
      checks.extend([
        ('m11-baseline-bound',manifest.get('m11_requirement_matrix_sha256')==sha256_file(rr/'governance/cra/cra-requirements.json')),
        ('m12-controls-bound',manifest.get('m12_control_mapping_sha256')==sha256_file(rr/'governance/cra/m12/m12-control-mapping.json')),
        ('m13-controls-bound',manifest.get('m13_control_mapping_sha256')==sha256_file(rr/'governance/cra/m13/m13-control-mapping.json'))
      ])
    errors=[]
    for p in packs:
      for s in p['stages']:
        if s['readiness']=='NEEDS_DATA': errors.append(f"{p['pack_id']}:{s['stage']}: missing {s['missing_required_fields']}")
    return {'ok':all(ok for _,ok in checks) and not errors,'checks':checks,'errors':errors,
            'pack_counts':{t:sum(p['case_type']==t for p in packs) for t in sorted({p['case_type'] for p in packs})},
            'stage_counts':{stage:sum(1 for p in packs for s in p['stages'] if s['stage']==stage) for stage in ('EARLY_WARNING_24H','NOTIFICATION_72H','FINAL_REPORT')}}
