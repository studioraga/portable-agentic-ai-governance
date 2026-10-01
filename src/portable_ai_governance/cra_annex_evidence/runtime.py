from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file

def evaluate_m17_material(root,repo_root=None):
    root=Path(root)
    required=['annex-i-evidence-policy.json','m17-control-mapping.json','annex-i-evidence-map.json','annex-i-evidence-index.json','annex-i-coverage-summary.json','annex-i-evidence-gaps.json','m17-annex-i-manifest.json','m17-annex-i-manifest.json.sig','signing-public.pem']
    checks=[(f'present:{f}',(root/f).is_file()) for f in required]
    if not all(v for _,v in checks):return {'ok':False,'checks':checks,'errors':['missing material']}
    man=json.loads((root/'m17-annex-i-manifest.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m17-annex-i-manifest.json',root/'signing-public.pem',root/'m17-annex-i-manifest.json.sig')))
    for n,d in man.get('artifacts',{}).items():checks.append((f'digest:{n}',sha256_file(root/n)==d))
    b=man['boundaries'];checks += [('evidence-aggregation-only',b.get('evidence_aggregation_only') is True),('no-conformity-claim',b.get('cra_conformity_claim') is False),('no-conformity-assessment',b.get('conformity_assessment_performed') is False),('no-m11-status-mutation',b.get('m11_status_mutation') is False),('no-technical-file',b.get('technical_file_generated') is False),('no-network-side-effects',b.get('network_side_effects') is False),('node2-verifier-only',b.get('node2_verifier_only') is True)]
    idx=json.loads((root/'annex-i-evidence-index.json').read_text());summary=json.loads((root/'annex-i-coverage-summary.json').read_text());gap=json.loads((root/'annex-i-evidence-gaps.json').read_text())
    ids=[e['requirement_id'] for e in idx['entries']]
    checks += [('22-annex-i-rows',len(ids)==22 and len(set(ids))==22),('part-i-coverage',summary.get('part_i')==14),('part-ii-coverage',summary.get('part_ii')==8),('all-evidence-refs-present',summary.get('all_references_present') is True),('explicit-gap-register',len(gap)>0 and any(x['evidence_state']=='GAP' for x in gap)),('no-entry-conformity-claim',all(e.get('conformity_claim') is False for e in idx['entries']))]
    if repo_root:
        rr=Path(repo_root);binds={'m11_requirement_matrix_sha256':'governance/cra/cra-requirements.json','m12_control_mapping_sha256':'governance/cra/m12/m12-control-mapping.json','m13_control_mapping_sha256':'governance/cra/m13/m13-control-mapping.json','m14_control_mapping_sha256':'governance/cra/m14/m14-control-mapping.json','m15_control_mapping_sha256':'governance/cra/m15/m15-control-mapping.json','m16_control_mapping_sha256':'governance/cra/m16/m16-control-mapping.json'}
        for k,p in binds.items():checks.append((k.replace('_sha256','-bound'),man.get(k)==sha256_file(rr/p)))
        for e in idx['entries']:
            for ev in e['evidence']:
                p=rr/ev['path'];checks.append((f"evidence:{e['requirement_id']}:{ev['path']}",p.is_file() and sha256_file(p)==ev['sha256']))
    ok=all(v for _,v in checks)
    return {'ok':ok,'checks':checks,'errors':[] if ok else ['one or more checks failed'],'counts':{'requirements':len(idx['entries']),'gaps_and_partials':len(gap),'states':summary['states']}}
