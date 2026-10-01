from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file

def evaluate_m19_material(root,repo_root=None,current_node2_profile=None):
    root=Path(root)
    required=['production-validation-policy.json','m19-control-mapping.json','production-validation-plan.json','node1-runtime-profile.json','node2-runtime-profile.json','cross-node-validation.json','production-validation-summary.json','m19-validation-manifest.json','m19-validation-manifest.json.sig','signing-public.pem']
    checks=[(f'present:{f}',(root/f).is_file()) for f in required]
    if not all(v for _,v in checks):
        return {'ok':False,'checks':checks,'errors':['missing material']}
    man=json.loads((root/'m19-validation-manifest.json').read_text()); summary=json.loads((root/'production-validation-summary.json').read_text()); cross=json.loads((root/'cross-node-validation.json').read_text())
    checks.append(('manifest-signature',verify_blob(root/'m19-validation-manifest.json',root/'signing-public.pem',root/'m19-validation-manifest.json.sig')))
    for n,d in man.get('artifacts',{}).items(): checks.append((f'digest:{n}',sha256_file(root/n)==d))
    b=man['boundaries']; checks += [
      ('production-validation-evidence',b.get('production_validation_evidence') is True),('simulation-no-production-claim',b.get('simulation_must_not_claim_production') is True),('no-conformity-claim',b.get('cra_conformity_claim') is False),('no-conformity-assessment',b.get('conformity_assessment_performed') is False),('no-m11-mutation',b.get('m11_status_mutation') is False),('no-m17-mutation',b.get('m17_evidence_state_mutation') is False),('no-m18-mutation',b.get('m18_readiness_mutation') is False),('no-destructive-tests',b.get('destructive_test_execution') is False),('no-firmware-flash',b.get('firmware_flash_performed') is False),('no-host-update',b.get('host_os_update_performed') is False),('no-network-side-effects',b.get('network_side_effects') is False),('node1-authority',b.get('node1_signing_authority') is True),('node2-verifier-only',b.get('node2_verifier_only') is True)]
    checks += [('ten-validation-cases',len(cross.get('checks',[]))==10),('all-required-pass',cross.get('all_required_pass') is True),('no-summary-conformity-claim',summary.get('cra_conformity_claim') is False)]
    if summary.get('validation_mode')=='SIMULATED': checks.append(('simulation-not-production-complete',summary.get('production_validation_complete') is False))
    if repo_root:
        rr=Path(repo_root); binds={'m11_requirement_matrix_sha256':'governance/cra/cra-requirements.json','m12_control_mapping_sha256':'governance/cra/m12/m12-control-mapping.json','m13_control_mapping_sha256':'governance/cra/m13/m13-control-mapping.json','m14_control_mapping_sha256':'governance/cra/m14/m14-control-mapping.json','m15_control_mapping_sha256':'governance/cra/m15/m15-control-mapping.json','m16_control_mapping_sha256':'governance/cra/m16/m16-control-mapping.json','m17_control_mapping_sha256':'governance/cra/m17/m17-control-mapping.json','m18_control_mapping_sha256':'governance/cra/m18/m18-control-mapping.json'}
        for k,p in binds.items(): checks.append((k.replace('_sha256','-bound'),man.get(k)==sha256_file(rr/p)))
    if current_node2_profile:
        cur=json.loads(Path(current_node2_profile).read_text()); claimed=json.loads((root/'node2-runtime-profile.json').read_text())
        stable=['role','architecture','package_version','source_fingerprints']; checks.append(('live-node2-profile-match',all(cur.get(k)==claimed.get(k) for k in stable)))
    ok=all(v for _,v in checks)
    return {'ok':ok,'checks':checks,'errors':[] if ok else ['one or more checks failed'],'validation_mode':summary.get('validation_mode'),'production_validation_complete':summary.get('production_validation_complete'),'counts':{'checks':summary.get('total_checks'),'passed':summary.get('passed'),'failed':summary.get('failed')}}
