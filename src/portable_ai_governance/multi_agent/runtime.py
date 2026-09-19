from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json,sha256_file
from ..supply_chain.signing import require_blob
class MultiAgentRuntimeError(RuntimeError):pass
@dataclass(frozen=True)
class MultiAgentReport:
 checks:tuple[tuple[str,bool,str],...]
 @property
 def ok(self):return all(x[1] for x in self.checks)
def evaluate_multi_agent(environ=None):
 e=dict(os.environ if environ is None else environ);checks=[];names=['PAG_M10_MANIFEST','PAG_M10_MANIFEST_SIG','PAG_M10_PUBLIC_KEY','PAG_M10_POLICY','PAG_M10_TOPOLOGY','PAG_M10_DECISION_PUBLIC_KEY','PAG_M9_MANIFEST']
 for n in names:
  p=Path(e.get(n,''));checks.append((n,p.is_file(),str(p) if p.is_file() else 'required path missing'))
 root=e.get('PAG_M10_RUNTIME_ROOT','');checks.append(('PAG_M10_RUNTIME_ROOT',bool(root),root or 'required path missing'))
 if not all(x[1] for x in checks):return MultiAgentReport(tuple(checks))
 try:require_blob(e['PAG_M10_MANIFEST'],e['PAG_M10_PUBLIC_KEY'],e['PAG_M10_MANIFEST_SIG']);checks.append(('manifest_signature',True,'verified'))
 except Exception as ex:checks.append(('manifest_signature',False,str(ex)));return MultiAgentReport(tuple(checks))
 try:
  m=load_json(e['PAG_M10_MANIFEST']);base=Path(e.get('PAG_M10_ROOT',Path(e['PAG_M10_MANIFEST']).parent))
  if m.get('m9_manifest_sha256')!=sha256_file(e['PAG_M9_MANIFEST']):raise MultiAgentRuntimeError('M9 manifest digest does not match M10 manifest')
  for rel,dig in m['artifacts'].items():
   if not (base/rel).is_file() or sha256_file(base/rel)!=dig:raise MultiAgentRuntimeError(f'manifest digest mismatch: {rel}')
  checks.append(('manifest_hashes',True,'M10 policy/topology/decision key digest-bound and M9-bound'))
 except Exception as ex:checks.append(('manifest_hashes',False,str(ex)))
 try:
  p=load_json(e['PAG_M10_POLICY']);t=load_json(e['PAG_M10_TOPOLOGY'])
  if p.get('version')!='0.10.0' or p.get('side_effect_authority') is not False or p.get('direct_agent_delegation') is not False:raise MultiAgentRuntimeError('invalid multi-agent policy')
  if p.get('m8_side_effect_boundary') is not True or p.get('m9_secops_boundary') is not True:raise MultiAgentRuntimeError('M8/M9 boundaries required')
  if not t.get('fixed_topology') or t.get('direct_peer_calls') is not False:raise MultiAgentRuntimeError('fixed no-peer-call topology required')
  expected={'GOVERNANCE-SUPERVISOR-001','RISK-AGENT-001','THREAT-AGENT-001','PRIVACY-AGENT-001','CONTROL-AGENT-001','ASSURANCE-AGENT-001'}
  if set(t.get('agents',{}))!=expected:raise MultiAgentRuntimeError('multi-agent topology agent set invalid')
  checks.append(('multi_agent_policy',True,'fixed typed bounded human-approved multi-agent workflow valid'))
 except Exception as ex:checks.append(('multi_agent_policy',False,str(ex)))
 return MultiAgentReport(tuple(checks))
def require_multi_agent(environ=None):
 r=evaluate_multi_agent(environ)
 if not r.ok:raise MultiAgentRuntimeError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
 return r
