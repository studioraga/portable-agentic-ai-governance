from __future__ import annotations
class CryptoLifecycleError(RuntimeError): pass
APPROVED={'AES-256-GCM','Ed25519','ECDSA-P256','RSA-3072','TLS1.3'}
REQ=('key_id','purpose','algorithm','owner','created_at','rotate_by','status','private_material_location','exportable')

def validate_crypto_lifecycle(policy:dict,now:int)->None:
    if policy.get('default_decision')!='deny-unregistered-key': raise CryptoLifecycleError('key lifecycle default must deny unregistered key')
    if policy.get('private_key_plaintext_storage_allowed') is not False: raise CryptoLifecycleError('plaintext private-key storage must be prohibited')
    seen=set()
    for k in policy.get('keys',[]):
        miss=[x for x in REQ if x not in k or k[x] in (None,'')]
        if miss: raise CryptoLifecycleError('key missing fields: '+','.join(miss))
        if k['key_id'] in seen: raise CryptoLifecycleError('duplicate key id')
        seen.add(k['key_id'])
        if k['algorithm'] not in APPROVED: raise CryptoLifecycleError('unapproved algorithm')
        if k['status']=='active' and int(k['rotate_by'])<=now: raise CryptoLifecycleError('active key rotation overdue')
        if k['purpose'] in {'signing','key-encryption','data-encryption'} and k.get('exportable') is not False: raise CryptoLifecycleError('sensitive production key must be non-exportable')
        if k['status'] not in {'active','retired','revoked','validation-only'}: raise CryptoLifecycleError('invalid key status')
    if not seen: raise CryptoLifecycleError('key inventory required')
