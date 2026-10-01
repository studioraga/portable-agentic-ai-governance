from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file

def evaluate_m15_material(root,repo_root=None):
 root=Path(root);required=['psirt-cvd-policy.json','m15-control-mapping.json','psirt-cases.json','maintainer-coordination.json','vulnerability-advisories.json','user-notifications.json','public-contact-cvd-contract.json','m15-psirt-manifest.json','m15-psirt-manifest.json.sig','signing-public.pem']
 checks=[(f'present:{f}',(root/f).is_file()) for f in required]
 if not all(ok for _,ok in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
 manifest=json.loads((root/'m15-psirt-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m15-psirt-manifest.json',root/'signing-public.pem',root/'m15-psirt-manifest.json.sig')))
 for n,d in manifest.get('artifacts',{}).items(): checks.append((f'digest:{n}',sha256_file(root/n)==d))
 b=manifest.get('boundaries',{});checks.extend([('evidence-only',b.get('evidence_only') is True),('no-external-dispatch',b.get('external_dispatch') is False),('no-public-disclosure',b.get('public_disclosure_performed') is False),('no-user-send',b.get('user_notification_sent') is False),('no-maintainer-contact',b.get('component_maintainer_contacted') is False),('human-authorization-required',b.get('human_authorization_required') is True),('no-conformity-claim',b.get('cra_conformity_claim') is False),('node2-verifier-only',b.get('node2_verifier_only') is True)])
 cases=json.loads((root/'psirt-cases.json').read_text());advs=json.loads((root/'vulnerability-advisories.json').read_text());notifs=json.loads((root/'user-notifications.json').read_text());coords=json.loads((root/'maintainer-coordination.json').read_text());contract=json.loads((root/'public-contact-cvd-contract.json').read_text())
 checks.extend([('psirt-intake-covered',len(cases)>=2 and all(c['state']=='TRIAGED' for c in cases)),('fixed-advisory-covered',len(advs)>=2 and all(a['publication_ready'] for a in advs)),('delayed-disclosure-justified',all((not a['delayed_disclosure_requested']) or bool(a['delayed_disclosure_justification']) for a in advs)),('user-notification-covered',{'AEV','SEVERE_INCIDENT'}<={n['case_type'] for n in notifs}),('notifications-unsent',all(n['sent'] is False and n['external_dispatch_performed'] is False for n in notifs)),('maintainer-coordination-unsent',all(c['contact_performed'] is False for c in coords)),('cvd-contact-contract',contract.get('cvd_policy_ready') is True and bool(contract.get('vulnerability_single_point_of_contact',{}).get('email')))])
 if repo_root:
  rr=Path(repo_root);checks.extend([('m11-baseline-bound',manifest.get('m11_requirement_matrix_sha256')==sha256_file(rr/'governance/cra/cra-requirements.json')),('m12-controls-bound',manifest.get('m12_control_mapping_sha256')==sha256_file(rr/'governance/cra/m12/m12-control-mapping.json')),('m13-controls-bound',manifest.get('m13_control_mapping_sha256')==sha256_file(rr/'governance/cra/m13/m13-control-mapping.json')),('m14-controls-bound',manifest.get('m14_control_mapping_sha256')==sha256_file(rr/'governance/cra/m14/m14-control-mapping.json'))])
 errors=[]
 return {'ok':all(ok for _,ok in checks) and not errors,'checks':checks,'errors':errors,'counts':{'psirt_cases':len(cases),'maintainer_coordination':len(coords),'advisories':len(advs),'user_notifications':len(notifs)}}
