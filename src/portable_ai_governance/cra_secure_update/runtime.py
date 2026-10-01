from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file

def evaluate_m16_material(root,repo_root=None):
 root=Path(root);required=['secure-update-policy.json','m16-control-mapping.json','lifecycle-registry.json','update-catalog.json','update-install-decisions.json','eol-notifications.json','security-update.bin','security-update.json','security-update.json.sig','m16-lifecycle-manifest.json','m16-lifecycle-manifest.json.sig','signing-public.pem']
 checks=[(f'present:{f}',(root/f).is_file()) for f in required]
 if not all(x for _,x in checks):return {'ok':False,'checks':checks,'errors':['missing material']}
 man=json.loads((root/'m16-lifecycle-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m16-lifecycle-manifest.json',root/'signing-public.pem',root/'m16-lifecycle-manifest.json.sig')))
 for n,d in man.get('artifacts',{}).items():checks.append((f'digest:{n}',sha256_file(root/n)==d))
 checks.append(('update-descriptor-signature',verify_blob(root/'security-update.json',root/'signing-public.pem',root/'security-update.json.sig')))
 desc=json.loads((root/'security-update.json').read_text());checks.append(('update-payload-digest',sha256_file(root/'security-update.bin')==desc.get('payload_sha256')))
 b=man.get('boundaries',{});checks.extend([('evidence-only',b.get('evidence_only') is True),('no-host-os-update',b.get('host_os_update_performed') is False),('no-firmware-flash',b.get('firmware_flash_performed') is False),('no-network-distribution',b.get('network_update_distribution') is False),('no-auto-external-rollout',b.get('automatic_external_rollout') is False),('human-release-auth',b.get('human_release_authorization_required') is True),('no-conformity-claim',b.get('cra_conformity_claim') is False),('node2-verifier-only',b.get('node2_verifier_only') is True)])
 life=json.loads((root/'lifecycle-registry.json').read_text());cat=json.loads((root/'update-catalog.json').read_text());dec=json.loads((root/'update-install-decisions.json').read_text());eol=json.loads((root/'eol-notifications.json').read_text())
 checks.extend([('support-period-covered',any(x['support_status']=='SUPPORTED' for x in life) and any(x['support_status']=='END_OF_SUPPORT' for x in life)),('minimum-support-rule',all((x['expected_use_years']<5) or ((int(x['support_period_end'][:4])-int(x['market_placement_date'][:4]))>=5) for x in life)),('update-retention-covered',all(x.get('availability_rule_satisfied') is True for x in cat)),('valid-install-decision',any(x['decision']=='ACCEPT' for x in dec)),('no-real-install',all(x.get('host_os_update_performed') is False and x.get('firmware_flash_performed') is False for x in dec)),('eol-notification-prepared-unsent',any(x['prepared'] and not x['sent'] for x in eol))])
 if repo_root:
  rr=Path(repo_root);checks.extend([('m11-baseline-bound',man.get('m11_requirement_matrix_sha256')==sha256_file(rr/'governance/cra/cra-requirements.json')),('m12-controls-bound',man.get('m12_control_mapping_sha256')==sha256_file(rr/'governance/cra/m12/m12-control-mapping.json')),('m13-controls-bound',man.get('m13_control_mapping_sha256')==sha256_file(rr/'governance/cra/m13/m13-control-mapping.json')),('m14-controls-bound',man.get('m14_control_mapping_sha256')==sha256_file(rr/'governance/cra/m14/m14-control-mapping.json')),('m15-controls-bound',man.get('m15_control_mapping_sha256')==sha256_file(rr/'governance/cra/m15/m15-control-mapping.json'))])
 return {'ok':all(x for _,x in checks),'checks':checks,'errors':[] if all(x for _,x in checks) else ['one or more checks failed'],'counts':{'lifecycle_records':len(life),'updates':len(cat),'install_decisions':len(dec),'eol_notifications':len(eol)}}
