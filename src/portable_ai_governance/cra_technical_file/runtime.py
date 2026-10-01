from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file

def evaluate_m18_material(root,repo_root=None):
    root=Path(root)
    required=['technical-file-policy.json','m18-control-mapping.json','annex-vii-map.json','product-technical-profile.json','annex-vii-technical-file-index.json','annex-vii-readiness-summary.json','annex-vii-gap-register.json','technical-file-cover.json','m18-technical-file-manifest.json','m18-technical-file-manifest.json.sig','signing-public.pem']
    checks=[(f'present:{f}',(root/f).is_file()) for f in required]
    if not all(v for _,v in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
    man=json.loads((root/'m18-technical-file-manifest.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m18-technical-file-manifest.json',root/'signing-public.pem',root/'m18-technical-file-manifest.json.sig')))
    for n,d in man.get('artifacts',{}).items(): checks.append((f'digest:{n}',sha256_file(root/n)==d))
    b=man['boundaries']
    checks += [
      ('technical-file-generated',b.get('technical_file_generated') is True),
      ('draft-evidence-file-only',b.get('draft_evidence_file_only') is True),
      ('no-conformity-claim',b.get('cra_conformity_claim') is False),
      ('no-conformity-assessment',b.get('conformity_assessment_performed') is False),
      ('no-eu-doc-generated',b.get('eu_declaration_of_conformity_generated') is False),
      ('no-ce-marking-authorization',b.get('ce_marking_authorized') is False),
      ('no-m11-status-mutation',b.get('m11_status_mutation') is False),
      ('no-m17-state-mutation',b.get('m17_evidence_state_mutation') is False),
      ('no-network-side-effects',b.get('network_side_effects') is False),
      ('node2-verifier-only',b.get('node2_verifier_only') is True)
    ]
    idx=json.loads((root/'annex-vii-technical-file-index.json').read_text())
    s=json.loads((root/'annex-vii-readiness-summary.json').read_text())
    g=json.loads((root/'annex-vii-gap-register.json').read_text())
    ids=[x['section_id'] for x in idx['entries']]
    checks += [
      ('eight-annex-vii-sections',len(ids)==8 and len(set(ids))==8),
      ('all-evidence-refs-present',s.get('all_references_present') is True),
      ('eu-doc-explicit-gap',any(x['section_id']=='ANNEX-VII-7' and x['readiness']=='GAP' for x in g)),
      ('test-reports-partial',any(x['section_id']=='ANNEX-VII-6' and x['readiness']=='PARTIAL' for x in g)),
      ('no-index-conformity-claim',idx.get('cra_conformity_claim') is False)
    ]
    if repo_root:
        rr=Path(repo_root)
        binds={
          'm11_requirement_matrix_sha256':'governance/cra/cra-requirements.json',
          'm12_control_mapping_sha256':'governance/cra/m12/m12-control-mapping.json',
          'm13_control_mapping_sha256':'governance/cra/m13/m13-control-mapping.json',
          'm14_control_mapping_sha256':'governance/cra/m14/m14-control-mapping.json',
          'm15_control_mapping_sha256':'governance/cra/m15/m15-control-mapping.json',
          'm16_control_mapping_sha256':'governance/cra/m16/m16-control-mapping.json',
          'm17_control_mapping_sha256':'governance/cra/m17/m17-control-mapping.json'
        }
        for k,p in binds.items(): checks.append((k.replace('_sha256','-bound'),man.get(k)==sha256_file(rr/p)))
        for e in idx['entries']:
            for ev in e['evidence']:
                p=rr/ev['path'];checks.append((f"evidence:{e['section_id']}:{ev['path']}",p.is_file() and sha256_file(p)==ev['sha256']))
    ok=all(v for _,v in checks)
    return {'ok':ok,'checks':checks,'errors':[] if ok else ['one or more checks failed'],'counts':{'sections':len(idx['entries']),'states':s['states'],'open_readiness_items':len(g)}}
