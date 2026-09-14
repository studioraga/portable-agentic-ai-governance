from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .locks import require_locks
from .signing import require_blob
from .vulnerability import require_vulnerability_policy

class SupplyChainError(RuntimeError): pass
@dataclass(frozen=True)
class SupplyChainReport:
    checks: tuple[tuple[str,bool,str],...]
    @property
    def ok(self): return all(x[1] for x in self.checks)

def evaluate_supply_chain(environ:dict[str,str]|None=None)->SupplyChainReport:
    e=dict(os.environ if environ is None else environ); checks=[]
    required={'PAG_M3_LOCK_FILE','PAG_M3_SBOM','PAG_M3_AI_BOM','PAG_M3_PROVENANCE','PAG_M3_PUBLIC_KEY','PAG_M3_VULN_REPORT','PAG_M3_VULN_POLICY'}
    for name in sorted(required):
        p=Path(e.get(name,'')); ok=bool(str(p)) and p.is_file(); checks.append((name,ok,str(p) if ok else 'required file missing'))
    if not all(x[1] for x in checks): return SupplyChainReport(tuple(checks))
    try: require_locks(e['PAG_M3_LOCK_FILE'],e.get('PAG_M3_ROOT','.')); checks.append(('artifact_locks',True,'model/container/prompt/tool locks verified'))
    except Exception as ex: checks.append(('artifact_locks',False,str(ex)))
    for key in ('PAG_M3_SBOM','PAG_M3_AI_BOM','PAG_M3_PROVENANCE'):
        sig=e.get(key+'_SIG','')
        try:
            if not sig: raise SupplyChainError(f'{key}_SIG missing')
            require_blob(e[key],e['PAG_M3_PUBLIC_KEY'],sig); checks.append((key+'_signature',True,'verified'))
        except Exception as ex: checks.append((key+'_signature',False,str(ex)))
    try:
        import json
        report_doc=json.loads(Path(e['PAG_M3_VULN_REPORT']).read_text())
        if report_doc.get('scanner') == 'm3-offline-fixture' and e.get('PAG_M3_ALLOW_FIXTURE_SCAN','0') != '1':
            raise SupplyChainError('fixture vulnerability report forbidden in production verification')
        d=require_vulnerability_policy(e['PAG_M3_VULN_REPORT'],e['PAG_M3_VULN_POLICY']); checks.append(('vulnerability_policy',True,d.detail))
    except Exception as ex: checks.append(('vulnerability_policy',False,str(ex)))
    return SupplyChainReport(tuple(checks))

def require_supply_chain(environ=None):
    r=evaluate_supply_chain(environ)
    if not r.ok: raise SupplyChainError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
    return r
