from __future__ import annotations
import json, os, platform, subprocess
from datetime import datetime, timezone
from pathlib import Path
from .locks import sha256_file

def git_commit(root: Path)->str:
    try:return subprocess.check_output(['git','-c',f'safe.directory={root}','rev-parse','HEAD'],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return 'unknown'

def generate_provenance(root:str|Path, subjects:list[str|Path], output:str|Path, builder_id='portable-ai-governance/m3')->dict:
    root=Path(root).resolve(); subs=[]
    for s in subjects:
        p=Path(s).resolve(); subs.append({'name':p.name,'digest':{'sha256':sha256_file(p)}})
    stmt={'_type':'https://in-toto.io/Statement/v1','subject':subs,'predicateType':'https://slsa.dev/provenance/v1','predicate':{'buildDefinition':{'buildType':'https://portable-ai-governance.local/release/v1','externalParameters':{},'internalParameters':{'gitCommit':git_commit(root)},'resolvedDependencies':[]},'runDetails':{'builder':{'id':builder_id},'metadata':{'invocationId':os.environ.get('PAG_BUILD_ID','local'),'startedOn':datetime.now(timezone.utc).isoformat(),'finishedOn':datetime.now(timezone.utc).isoformat()},'byproducts':[]}}}
    output_path=Path(output); output_path.write_text(json.dumps(stmt,indent=2,sort_keys=True)+'\n'); output_path.chmod(0o600); return stmt
