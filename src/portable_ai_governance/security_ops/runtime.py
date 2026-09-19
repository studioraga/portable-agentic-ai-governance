from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json,sha256_file
from ..supply_chain.signing import require_blob
class SecOpsRuntimeError(RuntimeError):pass
@dataclass(frozen=True)
class SecOpsReport:
 checks:tuple[tuple[str,bool,str],...]
 @property
 def ok(self):return all(x[1] for x in self.checks)
def evaluate_security_ops(environ=None):
 e=dict(os.environ if environ is None else environ);checks=[];names=['PAG_M9_MANIFEST','PAG_M9_MANIFEST_SIG','PAG_M9_PUBLIC_KEY','PAG_M9_POLICY','PAG_M9_RECOVERY_PUBLIC_KEY','PAG_M8_MANIFEST']
 for n in names:
  p=Path(e.get(n,''));checks.append((n,p.is_file(),str(p) if p.is_file() else 'required path missing'))
 root=e.get('PAG_M9_RUNTIME_ROOT','');checks.append(('PAG_M9_RUNTIME_ROOT',bool(root),root or 'required path missing'))
 if not all(x[1] for x in checks):return SecOpsReport(tuple(checks))
 try:require_blob(e['PAG_M9_MANIFEST'],e['PAG_M9_PUBLIC_KEY'],e['PAG_M9_MANIFEST_SIG']);checks.append(('manifest_signature',True,'verified'))
 except Exception as ex:checks.append(('manifest_signature',False,str(ex)));return SecOpsReport(tuple(checks))
 try:
  m=load_json(e['PAG_M9_MANIFEST']);base=Path(e.get('PAG_M9_ROOT',Path(e['PAG_M9_MANIFEST']).parent))
  if m.get('m8_manifest_sha256')!=sha256_file(e['PAG_M8_MANIFEST']):raise SecOpsRuntimeError('M8 manifest digest does not match M9 manifest')
  for rel,dig in m['artifacts'].items():
   if not (base/rel).is_file() or sha256_file(base/rel)!=dig:raise SecOpsRuntimeError(f'manifest digest mismatch: {rel}')
  checks.append(('manifest_hashes',True,'M9 policy digest-bound and M8-bound'))
 except Exception as ex:checks.append(('manifest_hashes',False,str(ex)))
 try:
  p=load_json(e['PAG_M9_POLICY'])
  if p.get('version')!='0.9.0' or p.get('llm_decision_authority') is not False:raise SecOpsRuntimeError('invalid deterministic SecOps policy')
  if set(p.get('incident_severities',[]))!={'high','critical'}:raise SecOpsRuntimeError('incident severities must be high/critical')
  acts={r.get('action') for r in p.get('containment_rules',[])}
  if not acts or not acts<={'model.quarantine.local','workload.isolate.local'}:raise SecOpsRuntimeError('invalid containment actions')
  sp=p.get('siem',{});rec=p.get('recovery',{})
  if not sp.get('append_only') or not sp.get('hash_chain'):raise SecOpsRuntimeError('SIEM append-only hash chain required')
  if not 1<=int(sp.get('max_future_skew_seconds',0))<=300:raise SecOpsRuntimeError('SIEM future-skew bound invalid')
  if not 60<=int(sp.get('max_event_age_seconds',0))<=604800:raise SecOpsRuntimeError('SIEM event-age bound invalid')
  if rec.get('automatic_recovery') is not False or rec.get('operator_required') is not True:raise SecOpsRuntimeError('operator-gated non-automatic recovery required')
  if not rec.get('operators') or not 60<=int(rec.get('authorization_ttl_max_seconds',0))<=3600:raise SecOpsRuntimeError('recovery authority policy invalid')
  if p.get('external_side_effects') is not False or p.get('m8_external_action_boundary') is not True:raise SecOpsRuntimeError('M8 external action boundary required')
  checks.append(('secops_policy',True,'deterministic SIEM/incident/containment/recovery/evidence policy valid'))
 except Exception as ex:checks.append(('secops_policy',False,str(ex)))
 return SecOpsReport(tuple(checks))
def require_security_ops(environ=None):
 r=evaluate_security_ops(environ)
 if not r.ok:raise SecOpsRuntimeError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
 return r
