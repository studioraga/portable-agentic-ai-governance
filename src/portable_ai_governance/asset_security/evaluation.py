from __future__ import annotations
from .inventory import validate_asset_register
from .lifecycle import validate_lifecycle_policy
from .dlp import validate_dlp_policy
from .crypto_lifecycle import validate_crypto_lifecycle
REQ={'ENT-ASSET-001','ENT-ASSET-002','ENT-DATA-001','ENT-DATA-002','ENT-DATA-003','ENT-DLP-001','ENT-DLP-002','ENT-DLP-003','ENT-CRYPTO-001','ENT-CRYPTO-002'}
def evaluate_m24_policy(asset_policy,asset_register,lifecycle,dlp,crypto,controls,now=1700000000):
    checks=[];ids={c.get('control_id') for c in controls.get('controls',[])};checks.append(('m24-controls-present',REQ<=ids))
    for name,fn in [('asset-register',lambda:validate_asset_register(asset_register)),('lifecycle',lambda:validate_lifecycle_policy(lifecycle)),('dlp',lambda:validate_dlp_policy(dlp)),('crypto-lifecycle',lambda:validate_crypto_lifecycle(crypto,now))]:
        try:fn();checks.append((name,True))
        except Exception:checks.append((name,False))
    checks.append(('classification-levels',asset_policy.get('classification_levels')==['public','internal','confidential','restricted']))
    checks.append(('default-unregistered-deny',asset_policy.get('default_unregistered_asset_decision')=='deny'))
    boundaries=asset_policy.get('claim_boundaries',{})
    for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'):
        checks.append((f'claim-boundary:{k}',boundaries.get(k) is False))
    return {'ok':all(v for _,v in checks),'checks':checks,'control_count':len(REQ)}
