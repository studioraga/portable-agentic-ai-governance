from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json,sha256_file
from .policy import require_action_policy
from .registry import ActionRegistry
from .authorization import build_action_authorization
from ..supply_chain.signing import require_blob
class ActionRuntimeError(RuntimeError): pass
@dataclass(frozen=True)
class ActionReport:
 checks:tuple[tuple[str,bool,str],...]
 @property
 def ok(self): return all(x[1] for x in self.checks)
def evaluate_action_agent(environ=None):
 e=dict(os.environ if environ is None else environ);checks=[];names=['PAG_M8_MANIFEST','PAG_M8_MANIFEST_SIG','PAG_M8_PUBLIC_KEY','PAG_M8_AGENT_POLICY','PAG_M8_TOOL_REGISTRY','PAG_M8_AUTHORIZATION_RULES','PAG_M8_APPROVAL_AUTHORITIES','PAG_M8_APPROVAL_PUBLIC_KEY','PAG_M7_MANIFEST']
 for n in names:
  p=Path(e.get(n,''));ok=p.is_file();checks.append((n,ok,str(p) if ok else 'required path missing'))
 action_root=e.get('PAG_M8_ACTION_ROOT','');checks.append(('PAG_M8_ACTION_ROOT',bool(action_root),action_root or 'required path missing'))
 if not all(x[1] for x in checks):return ActionReport(tuple(checks))
 try:require_blob(e['PAG_M8_MANIFEST'],e['PAG_M8_PUBLIC_KEY'],e['PAG_M8_MANIFEST_SIG']);checks.append(('manifest_signature',True,'verified'))
 except Exception as ex:checks.append(('manifest_signature',False,str(ex)));return ActionReport(tuple(checks))
 try:
  m=load_json(e['PAG_M8_MANIFEST']);root=Path(e.get('PAG_M8_ROOT',Path(e['PAG_M8_MANIFEST']).parent))
  if m.get('m7_manifest_sha256')!=sha256_file(e['PAG_M7_MANIFEST']):raise ActionRuntimeError('M7 manifest digest does not match M8 manifest')
  for rel,dig in m.get('artifacts',{}).items():
   p=root/rel
   if not p.is_file() or sha256_file(p)!=dig:raise ActionRuntimeError(f'manifest digest mismatch: {rel}')
  checks.append(('manifest_hashes',True,'M8 policy/registry/authorization digest-bound and M7-bound'))
 except Exception as ex:checks.append(('manifest_hashes',False,str(ex)))
 try:policy=load_json(e['PAG_M8_AGENT_POLICY']);checks.append(('agent_policy',True,require_action_policy(policy)))
 except Exception as ex:policy={};checks.append(('agent_policy',False,str(ex)))
 try:registry=ActionRegistry(e['PAG_M8_TOOL_REGISTRY']);checks.append(('tool_registry',True,'four approval-controlled side-effect tools valid'))
 except Exception as ex:registry=None;checks.append(('tool_registry',False,str(ex)))
 try:auth=build_action_authorization(e['PAG_M8_AUTHORIZATION_RULES']);checks.append(('authorization_rules',True,'deny-by-default action authorization valid'))
 except Exception as ex:auth=None;checks.append(('authorization_rules',False,str(ex)))
 try:
  adoc=load_json(e['PAG_M8_APPROVAL_AUTHORITIES']); aps=adoc.get('approvers',[])
  if adoc.get('version')!='0.8.0' or not aps: raise ActionRuntimeError('approval authorities required')
  ids={x.get('principal_id') for x in aps}
  if 'ACTION-AGENT-001' in ids: raise ActionRuntimeError('agent cannot be an approval authority')
  if any('human_approver' not in x.get('roles',[]) for x in aps): raise ActionRuntimeError('human_approver role required')
  checks.append(('approval_authorities',True,'signed human approval authorities valid'))
 except Exception as ex: checks.append(('approval_authorities',False,str(ex)))
 try:
  if registry is None or auth is None or not policy:raise ActionRuntimeError('cross-policy prerequisites invalid')
  if set(policy.get('allowed_tools',[]))!=set(registry.tools):raise ActionRuntimeError('agent allowed_tools must exactly match signed registry')
  covered={r.resource_prefix.removeprefix('action://') for r in auth.rules if r.effect=='allow' and r.action=='action.execute'}
  if covered!=set(registry.tools):raise ActionRuntimeError('authorization rules must exactly cover signed registry')
  checks.append(('cross_binding',True,'policy, side-effect registry and authorization exactly aligned'))
 except Exception as ex:checks.append(('cross_binding',False,str(ex)))
 return ActionReport(tuple(checks))
def require_action_agent(environ=None):
 r=evaluate_action_agent(environ)
 if not r.ok:raise ActionRuntimeError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
 return r
