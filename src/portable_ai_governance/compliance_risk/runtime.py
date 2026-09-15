from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json,sha256_file
from .impact import require_impact_assessment
from .privacy import require_privacy_assessment
from .exceptions import require_exception_register
from .third_parties import require_third_party_register
from .continuous_controls import require_continuous_controls
from .reports import require_compliance_report
from ..supply_chain.signing import require_blob
class ComplianceRiskError(RuntimeError): pass
@dataclass(frozen=True)
class ComplianceRiskReport:
    checks: tuple[tuple[str,bool,str],...]
    @property
    def ok(self): return all(x[1] for x in self.checks)

def evaluate_compliance_risk(environ=None):
    e=dict(os.environ if environ is None else environ); checks=[]
    names=['PAG_M5_MANIFEST','PAG_M5_MANIFEST_SIG','PAG_M5_PUBLIC_KEY','PAG_M5_IMPACT_ASSESSMENT','PAG_M5_PRIVACY_ASSESSMENT','PAG_M5_EXCEPTION_REGISTER','PAG_M5_THIRD_PARTIES','PAG_M5_CONTINUOUS_CONTROLS','PAG_M5_COMPLIANCE_REPORT','PAG_M4_MANIFEST']
    for n in names:
        p=Path(e.get(n,'')); ok=p.is_file(); checks.append((n,ok,str(p) if ok else 'required file missing'))
    if not all(x[1] for x in checks): return ComplianceRiskReport(tuple(checks))
    try: require_blob(e['PAG_M5_MANIFEST'],e['PAG_M5_PUBLIC_KEY'],e['PAG_M5_MANIFEST_SIG']); checks.append(('manifest_signature',True,'verified'))
    except Exception as ex: checks.append(('manifest_signature',False,str(ex))); return ComplianceRiskReport(tuple(checks))
    try:
        m=load_json(e['PAG_M5_MANIFEST'])
        if m.get('m4_manifest_sha256')!=sha256_file(e['PAG_M4_MANIFEST']): raise ComplianceRiskError('M4 manifest digest does not match M5 manifest')
        root=Path(e.get('PAG_M5_ROOT',Path(e['PAG_M5_MANIFEST']).parent))
        for rel,dig in m.get('artifacts',{}).items():
            p=root/rel
            if not p.is_file() or sha256_file(p)!=dig: raise ComplianceRiskError(f'manifest digest mismatch: {rel}')
        checks.append(('manifest_hashes',True,'all compliance/risk artifacts digest-bound'))
    except Exception as ex: checks.append(('manifest_hashes',False,str(ex)))
    funcs=[
      ('impact_assessment',lambda:require_impact_assessment(e['PAG_M5_IMPACT_ASSESSMENT'])),
      ('privacy',lambda:require_privacy_assessment(e['PAG_M5_PRIVACY_ASSESSMENT'])),
      ('exceptions',lambda:require_exception_register(e['PAG_M5_EXCEPTION_REGISTER'])),
      ('third_parties',lambda:require_third_party_register(e['PAG_M5_THIRD_PARTIES'])),
      ('continuous_controls',lambda:require_continuous_controls(e['PAG_M5_CONTINUOUS_CONTROLS'])),
      ('compliance_report',lambda:require_compliance_report(e['PAG_M5_COMPLIANCE_REPORT'])),
    ]
    for name,fn in funcs:
        try: checks.append((name,True,fn()))
        except Exception as ex: checks.append((name,False,str(ex)))
    return ComplianceRiskReport(tuple(checks))
def require_compliance_risk(environ=None):
    r=evaluate_compliance_risk(environ)
    if not r.ok: raise ComplianceRiskError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
    return r
