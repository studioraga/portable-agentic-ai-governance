from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file
from .firmware import verify_descriptor

def evaluate_m21_material(root,repo_root=None):
    root=Path(root);req=['platform-security-policy.json','m21-control-mapping.json','threat-model.json','key-management-policy.json','measured-boot-policy.json','pag-platform-demo.service','apparmor-profile','selinux-policy.te','node1-platform-profile.json','node2-platform-profile.json','platform-validation-summary.json','firmware.bin','firmware-descriptor.json','firmware-descriptor.json.sig','dice-demo.json','m21-platform-manifest.json','m21-platform-manifest.json.sig','signing-public.pem']
    checks=[(f'present:{x}',(root/x).is_file()) for x in req]
    if not all(v for _,v in checks): return {'ok':False,'checks':checks,'errors':['missing material']}
    man=json.loads((root/'m21-platform-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m21-platform-manifest.json',root/'signing-public.pem',root/'m21-platform-manifest.json.sig')))
    for n,d in man.get('artifacts',{}).items():checks.append((f'digest:{n}',sha256_file(root/n)==d))
    checks.append(('firmware-signature-and-payload',verify_descriptor(root/'firmware-descriptor.json',root/'firmware.bin',root/'signing-public.pem',root/'firmware-descriptor.json.sig')))
    s=json.loads((root/'platform-validation-summary.json').read_text());b=man.get('boundaries',{})
    checks += [('no-fuse-burn',b.get('no_fuse_burn') is True),('no-uefi-key-enrollment',b.get('no_uefi_key_enrollment') is True),('no-firmware-flash',b.get('no_firmware_flash') is True),('no-debug-fuse-change',b.get('no_debug_fuse_change') is True),('no-host-reconfiguration',b.get('no_host_reconfiguration') is True),('no-conformity-claim',b.get('cra_conformity_claim') is False),('node2-verifier-only',b.get('node2_verifier_only') is True),('summary-no-conformity',s.get('cra_conformity_claim') is False)]
    if repo_root:
        rr=Path(repo_root);checks.append(('m20-source-bound',man.get('m20_commit')==( __import__('subprocess').run(['git','-c',f'safe.directory={rr}','-C',str(rr),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())))
    ok=all(v for _,v in checks);return {'ok':ok,'checks':checks,'errors':[] if ok else ['one or more checks failed'],'validation_mode':s.get('validation_mode'),'production_ready':s.get('production_ready')}
