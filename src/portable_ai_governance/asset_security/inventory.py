from __future__ import annotations
from dataclasses import dataclass
from .common import CLASSIFICATIONS,CRITICALITIES
class AssetInventoryError(RuntimeError): pass
REQ=('asset_id','asset_type','system_id','owner','custodian','criticality','classification','location','lifecycle_state','retention_profile')
@dataclass(frozen=True)
class Asset:
    asset_id:str;asset_type:str;system_id:str;owner:str;custodian:str;criticality:str;classification:str;location:str;lifecycle_state:str;retention_profile:str

def validate_asset_register(registry:dict)->tuple[Asset,...]:
    if registry.get('default_decision')!='deny-unregistered': raise AssetInventoryError('default asset decision must deny unregistered')
    seen=set();out=[]
    for a in registry.get('assets',[]):
        miss=[k for k in REQ if a.get(k) in (None,'',[])]
        if miss: raise AssetInventoryError('asset missing fields: '+','.join(miss))
        if a['asset_id'] in seen: raise AssetInventoryError('duplicate asset id')
        seen.add(a['asset_id'])
        if a['classification'] not in CLASSIFICATIONS: raise AssetInventoryError('invalid classification')
        if a['criticality'] not in CRITICALITIES: raise AssetInventoryError('invalid criticality')
        if a['classification'] in {'confidential','restricted'} and not a.get('data_owner'): raise AssetInventoryError('sensitive asset requires data_owner')
        out.append(Asset(**{k:a[k] for k in REQ}))
    if not out: raise AssetInventoryError('asset register must not be empty')
    return tuple(out)

def require_registered_asset(registry:dict,asset_id:str)->dict:
    validate_asset_register(registry)
    for a in registry['assets']:
        if a['asset_id']==asset_id:return a
    raise AssetInventoryError('asset is not registered')
