from __future__ import annotations
import json, platform, socket, subprocess
from pathlib import Path
from .common import sha256_file

def _run(cmd):
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=4,check=False)
        return p.stdout.strip() if p.returncode==0 else None
    except Exception:
        return None

def _os_release():
    d={}
    try:
        for line in Path('/etc/os-release').read_text().splitlines():
            if '=' in line:
                k,v=line.split('=',1); d[k.lower()]=v.strip().strip('"')
    except Exception:
        pass
    return {'id':d.get('id','unknown'),'version_id':d.get('version_id','unknown'),'pretty_name':d.get('pretty_name','unknown')}

def collect_profile(repo_root, role, node_id=None):
    root=Path(repo_root).resolve();policy=json.loads((root/'governance/cra/m19/production-validation-policy.json').read_text())
    pkg='unknown'
    try:
        ns={};exec((root/'src/portable_ai_governance/__init__.py').read_text(),ns);pkg=ns.get('__version__','unknown')
    except Exception:
        pass
    fps={p:sha256_file(root/p) for p in policy['source_fingerprint_paths'] if (root/p).is_file()}
    gpu=_run(['nvidia-smi','--query-gpu=name,driver_version','--format=csv,noheader'])
    tegra=Path('/etc/nv_tegra_release')
    accel={'kind':'nvidia' if gpu else ('nvidia-jetson' if tegra.exists() else 'unknown'),'description':gpu or (tegra.read_text(errors='replace').splitlines()[0] if tegra.exists() else 'not-detected')}
    cfg=Path.home()/'.config/portable-ai-governance'
    private=any(cfg.rglob('signing-private.pem')) if cfg.exists() else False
    return {'schema_version':'1.0','milestone':'M19','capture_mode':'LIVE','node_id':node_id or socket.gethostname(),'role':role,'hostname':socket.gethostname(),'architecture':platform.machine(),'os':_os_release(),'kernel_release':platform.release(),'python_version':platform.python_version(),'package_version':pkg,'git_head':_run(['git','-C',str(root),'rev-parse','HEAD']) or 'unknown','source_fingerprints':fps,'accelerator':accel,'private_signing_key_present':private}
