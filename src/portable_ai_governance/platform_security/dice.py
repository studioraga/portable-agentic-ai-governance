from __future__ import annotations
import hashlib,hmac

def derive_cdi_demo(uds_hex, first_mutable_code_sha256, config=''):
    uds=bytes.fromhex(uds_hex)
    msg=bytes.fromhex(first_mutable_code_sha256)+config.encode()
    return hmac.new(uds,msg,hashlib.sha256).hexdigest()
