from __future__ import annotations
import base64, json, subprocess
from pathlib import Path

class SigningError(RuntimeError): pass

def generate_ed25519_keypair(private_key:str|Path, public_key:str|Path)->None:
    priv,pub=Path(private_key),Path(public_key); priv.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['openssl','genpkey','-algorithm','ED25519','-out',str(priv)],check=True,capture_output=True)
    subprocess.run(['openssl','pkey','-in',str(priv),'-pubout','-out',str(pub)],check=True,capture_output=True)
    priv.chmod(0o600); pub.chmod(0o600)

def sign_blob(blob:str|Path, private_key:str|Path, signature_file:str|Path)->None:
    r=subprocess.run(['openssl','pkeyutl','-sign','-rawin','-inkey',str(private_key),'-in',str(blob)],check=True,capture_output=True)
    Path(signature_file).write_text(base64.b64encode(r.stdout).decode()+'\n'); Path(signature_file).chmod(0o600)

def verify_blob(blob:str|Path, public_key:str|Path, signature_file:str|Path)->bool:
    sig=base64.b64decode(Path(signature_file).read_text().strip())
    p=subprocess.run(['openssl','pkeyutl','-verify','-rawin','-pubin','-inkey',str(public_key),'-in',str(blob),'-sigfile','/dev/stdin'],input=sig,capture_output=True)
    return p.returncode==0

def require_blob(blob,public_key,signature_file):
    if not verify_blob(blob,public_key,signature_file): raise SigningError(f'signature verification failed: {blob}')
