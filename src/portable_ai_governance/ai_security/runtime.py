from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json, sha256_file
from .model_governance import require_model_governance
from .provenance import require_data_provenance
from .retrieval import require_retrieval_policy
from .embeddings import require_embedding_policy
from .evaluation import require_evaluation
from .threat_model import require_threat_model
from ..supply_chain.signing import require_blob
class AISecurityError(RuntimeError): pass
@dataclass(frozen=True)
class AISecurityReport:
    checks:tuple[tuple[str,bool,str],...]
    @property
    def ok(self): return all(x[1] for x in self.checks)

def evaluate_ai_security(environ=None):
    e=dict(os.environ if environ is None else environ); checks=[]
    names=['PAG_M4_MANIFEST','PAG_M4_MANIFEST_SIG','PAG_M4_PUBLIC_KEY','PAG_M4_MODEL_GOVERNANCE','PAG_M4_DATA_PROVENANCE','PAG_M4_RETRIEVAL_POLICY','PAG_M4_EMBEDDING_POLICY','PAG_M4_EVAL_SUITE','PAG_M4_EVAL_RESULTS','PAG_M4_THREAT_MODEL','PAG_M3_LOCK_FILE']
    for n in names:
        p=Path(e.get(n,'')); ok=p.is_file(); checks.append((n,ok,str(p) if ok else 'required file missing'))
    if not all(x[1] for x in checks): return AISecurityReport(tuple(checks))
    try: require_blob(e['PAG_M4_MANIFEST'],e['PAG_M4_PUBLIC_KEY'],e['PAG_M4_MANIFEST_SIG']); checks.append(('manifest_signature',True,'verified'))
    except Exception as ex: checks.append(('manifest_signature',False,str(ex))); return AISecurityReport(tuple(checks))
    try:
        manifest=load_json(e['PAG_M4_MANIFEST'])
        if manifest.get('m3_model_lock_sha256') != sha256_file(e['PAG_M3_LOCK_FILE']): raise AISecurityError('M3 lock digest does not match M4 manifest')
        root=Path(e.get('PAG_M4_ROOT',Path(e['PAG_M4_MANIFEST']).parent))
        for rel,digest in manifest.get('artifacts',{}).items():
            p=root/rel
            if not p.is_file() or sha256_file(p)!=digest: raise AISecurityError(f'manifest digest mismatch: {rel}')
        checks.append(('manifest_hashes',True,'all AI-security artifacts digest-bound'))
    except Exception as ex: checks.append(('manifest_hashes',False,str(ex)))
    funcs=[('model_governance',lambda:require_model_governance(e['PAG_M4_MODEL_GOVERNANCE'],e['PAG_M3_LOCK_FILE'])),('data_provenance',lambda:require_data_provenance(e['PAG_M4_DATA_PROVENANCE'])),('retrieval_authorization',lambda:require_retrieval_policy(e['PAG_M4_RETRIEVAL_POLICY'])),('embedding_controls',lambda:require_embedding_policy(e['PAG_M4_EMBEDDING_POLICY'],e['PAG_M4_DATA_PROVENANCE'])),('ai_evaluation',lambda:require_evaluation(e['PAG_M4_EVAL_SUITE'],e['PAG_M4_EVAL_RESULTS'])),('ai_threat_model',lambda:require_threat_model(e['PAG_M4_THREAT_MODEL']))]
    for name,fn in funcs:
        try: checks.append((name,True,fn()))
        except Exception as ex: checks.append((name,False,str(ex)))
    return AISecurityReport(tuple(checks))
def require_ai_security(environ=None):
    r=evaluate_ai_security(environ)
    if not r.ok: raise AISecurityError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
    return r
