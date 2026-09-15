from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json,sha256_file
from .policy import require_agent_policy
from .catalog import require_catalog
from ..supply_chain.signing import require_blob
class EvidenceAnalystRuntimeError(RuntimeError): pass
@dataclass(frozen=True)
class EvidenceAnalystReport:
    checks:tuple[tuple[str,bool,str],...]
    @property
    def ok(self): return all(x[1] for x in self.checks)
def evaluate_evidence_analyst(environ=None):
    e=dict(os.environ if environ is None else environ); checks=[]
    names=['PAG_M6_MANIFEST','PAG_M6_MANIFEST_SIG','PAG_M6_PUBLIC_KEY','PAG_M6_AGENT_POLICY','PAG_M6_EVIDENCE_CATALOG','PAG_M6_EVIDENCE_ROOT','PAG_M5_MANIFEST']
    for n in names:
        p=Path(e.get(n,'')); ok=p.is_dir() if n=='PAG_M6_EVIDENCE_ROOT' else p.is_file(); checks.append((n,ok,str(p) if ok else 'required path missing'))
    if not all(x[1] for x in checks): return EvidenceAnalystReport(tuple(checks))
    try: require_blob(e['PAG_M6_MANIFEST'],e['PAG_M6_PUBLIC_KEY'],e['PAG_M6_MANIFEST_SIG']); checks.append(('manifest_signature',True,'verified'))
    except Exception as ex: checks.append(('manifest_signature',False,str(ex))); return EvidenceAnalystReport(tuple(checks))
    try:
        m=load_json(e['PAG_M6_MANIFEST']); root=Path(e.get('PAG_M6_ROOT',Path(e['PAG_M6_MANIFEST']).parent))
        if m.get('m5_manifest_sha256')!=sha256_file(e['PAG_M5_MANIFEST']): raise EvidenceAnalystRuntimeError('M5 manifest digest does not match M6 manifest')
        for rel,dig in m.get('artifacts',{}).items():
            p=root/rel
            if not p.is_file() or sha256_file(p)!=dig: raise EvidenceAnalystRuntimeError(f'manifest digest mismatch: {rel}')
        checks.append(('manifest_hashes',True,'agent policy/catalog digest-bound and M5-bound'))
    except Exception as ex: checks.append(('manifest_hashes',False,str(ex)))
    try: checks.append(('agent_policy',True,require_agent_policy(load_json(e['PAG_M6_AGENT_POLICY']))))
    except Exception as ex: checks.append(('agent_policy',False,str(ex)))
    try: checks.append(('evidence_catalog',True,require_catalog(e['PAG_M6_EVIDENCE_CATALOG'],e['PAG_M6_EVIDENCE_ROOT'])))
    except Exception as ex: checks.append(('evidence_catalog',False,str(ex)))
    return EvidenceAnalystReport(tuple(checks))
def require_evidence_analyst(environ=None):
    r=evaluate_evidence_analyst(environ)
    if not r.ok: raise EvidenceAnalystRuntimeError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
    return r
