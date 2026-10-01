from __future__ import annotations
from datetime import date
from .common import version_tuple,sha256_file
from .lifecycle import add_years
from portable_ai_governance.supply_chain.signing import verify_blob

def retention_until(issued_at,support_period_end):
 issued=date.fromisoformat(issued_at[:10]); ten=add_years(issued,10); end=date.fromisoformat(support_period_end)
 return max(ten,end).isoformat()

def make_update_descriptor(product_id,from_version,to_version,payload_path,issued_at,support_end):
 return {'update_id':f'{product_id}-security-{to_version}','product_id':product_id,'from_version':from_version,'to_version':to_version,'payload_sha256':sha256_file(payload_path),'issued_at':issued_at,'available_until':retention_until(issued_at,support_end),'free_of_charge':True,'security_only':True,'functionality_bundled':False,'secure_distribution_required':True,'automatic_update_applicable':True,'automatic_update_enabled':True,'human_release_authorization_required':True,'external_rollout_performed':False}

def evaluate_install(descriptor,payload_path,descriptor_path,signature_path,public_key,current_version,as_of,support_end):
 reasons=[]
 if not verify_blob(descriptor_path,public_key,signature_path): reasons.append('descriptor_signature_invalid')
 if sha256_file(payload_path)!=descriptor.get('payload_sha256'): reasons.append('payload_digest_mismatch')
 try:
  if version_tuple(descriptor['to_version'])<=version_tuple(current_version): reasons.append('rollback_or_non_monotonic_version')
 except Exception: reasons.append('invalid_version')
 if date.fromisoformat(as_of)>date.fromisoformat(support_end): reasons.append('outside_support_period')
 if descriptor.get('free_of_charge') is not True: reasons.append('security_update_not_free')
 if descriptor.get('secure_distribution_required') is not True: reasons.append('secure_distribution_not_required')
 if descriptor.get('security_only') is True and descriptor.get('functionality_bundled') is True: reasons.append('security_functionality_not_separated')
 return {'product_id':descriptor.get('product_id'),'update_id':descriptor.get('update_id'),'current_version':current_version,'target_version':descriptor.get('to_version'),'decision':'ACCEPT' if not reasons else 'REJECT','reasons':reasons,'host_os_update_performed':False,'firmware_flash_performed':False}
