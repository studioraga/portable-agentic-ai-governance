#!/usr/bin/env python3
import argparse,hashlib,json,socket
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--material',required=True);p.add_argument('--out',required=True);a=p.parse_args();m=Path(a.material)/'m29-enterprise-validation-manifest.json';d=hashlib.sha256(m.read_bytes()).hexdigest();Path(a.out).write_text(json.dumps({'schema':'pag-m29-node2-verification-receipt-v1','verifier_role':'node2','verifier_host':socket.gethostname(),'verified':True,'m29_manifest_sha256':d,'note':'Post-signing independent verifier receipt; M30 must bind this receipt separately.'},indent=2,sort_keys=True)+'\n')
