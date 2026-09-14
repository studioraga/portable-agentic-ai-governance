from __future__ import annotations
import hashlib, json, platform, sys, uuid
from datetime import datetime, timezone
from pathlib import Path
from .locks import sha256_file

def _serial(payload: bytes)->str: return 'urn:uuid:'+str(uuid.UUID(hashlib.md5(payload).hexdigest()))
def generate_sbom(root: str|Path, output: str|Path)->dict:
    root=Path(root); components=[]
    for p in sorted(root.rglob('*.py')):
        if any(x in p.parts for x in ('.venv','.git','__pycache__')): continue
        rel=str(p.relative_to(root))
        components.append({'type':'file','name':rel,'hashes':[{'alg':'SHA-256','content':sha256_file(p)}]})
    meta={'timestamp':datetime.now(timezone.utc).isoformat(),'tools':{'components':[{'type':'application','name':'portable-ai-governance-m3-sbom','version':'0.3.0'}]},'properties':[{'name':'python.version','value':platform.python_version()}]}
    doc={'bomFormat':'CycloneDX','specVersion':'1.7','serialNumber':_serial(json.dumps(components,sort_keys=True).encode()),'version':1,'metadata':meta,'components':components}
    output_path=Path(output); output_path.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n'); output_path.chmod(0o600); return doc

def generate_ai_bom(lock_path: str|Path, output: str|Path)->dict:
    lock=json.loads(Path(lock_path).read_text()); models=[]
    for a in lock.get('artifacts',[]):
        if a.get('type')!='model': continue
        c={'type':'machine-learning-model','name':a['name'],'version':str(a.get('version','locked')),'hashes':[{'alg':'SHA-256','content':a['sha256']}], 'properties':[]}
        for k in ('source','license','framework','dataset_provenance','intended_use'):
            if a.get(k): c['properties'].append({'name':f'ai.{k}','value':str(a[k])})
        models.append(c)
    doc={'bomFormat':'CycloneDX','specVersion':'1.7','serialNumber':_serial(json.dumps(models,sort_keys=True).encode()),'version':1,'metadata':{'timestamp':datetime.now(timezone.utc).isoformat(),'component':{'type':'application','name':'portable-agentic-ai-governance'}},'components':models}
    output_path=Path(output); output_path.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n'); output_path.chmod(0o600); return doc
