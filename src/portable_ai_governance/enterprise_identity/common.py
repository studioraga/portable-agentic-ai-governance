from __future__ import annotations
import base64, hashlib, json, subprocess, tempfile
from pathlib import Path
from typing import Any

M22_BASELINE_COMMIT = "f020822162591f7d279f7004dea628efb7989525"
M22_BASELINE_TAG = "m22-enterprise-security-foundation-v0.22.0"
M23_VERSION = "0.23.0"

class EnterpriseIdentityError(RuntimeError): pass

def sha256_file(path: str | Path) -> str:
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def write_json(path: str | Path, obj: Any) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n"); p.chmod(0o600)

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def b64url_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + '='*((4-len(text)%4)%4))

def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj,separators=(',',':'),sort_keys=True).encode()

def sign_compact(header: dict, payload: dict, private_key: str|Path) -> str:
    h=b64url_encode(canonical_json(header)); p=b64url_encode(canonical_json(payload)); data=f"{h}.{p}".encode()
    with tempfile.NamedTemporaryFile() as inp:
        inp.write(data); inp.flush()
        r=subprocess.run(['openssl','pkeyutl','-sign','-rawin','-inkey',str(private_key),'-in',inp.name],check=True,capture_output=True)
    return f"{h}.{p}.{b64url_encode(r.stdout)}"

def verify_compact(token: str, public_key: str|Path) -> tuple[dict,dict]:
    try: h,p,s=token.split('.'); header=json.loads(b64url_decode(h)); payload=json.loads(b64url_decode(p)); sig=b64url_decode(s)
    except Exception as exc: raise EnterpriseIdentityError(f'invalid compact token: {exc}') from exc
    if header.get('alg')!='EdDSA': raise EnterpriseIdentityError('only EdDSA validation profile is accepted')
    data=f"{h}.{p}".encode()
    with tempfile.NamedTemporaryFile() as inp, tempfile.NamedTemporaryFile() as sf:
        inp.write(data); inp.flush(); sf.write(sig); sf.flush()
        r=subprocess.run(['openssl','pkeyutl','-verify','-rawin','-pubin','-inkey',str(public_key),'-in',inp.name,'-sigfile',sf.name],capture_output=True)
    if r.returncode != 0: raise EnterpriseIdentityError('token signature verification failed')
    return header,payload
