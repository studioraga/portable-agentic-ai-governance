from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from .common import load_json,sha256_file
from .policy import require_tool_agent_policy
from .registry import ToolRegistry
from .authorization import build_tool_authorization
from ..supply_chain.signing import require_blob
class ToolAgentRuntimeError(RuntimeError): pass
@dataclass(frozen=True)
class ToolAgentReport:
    checks:tuple[tuple[str,bool,str],...]
    @property
    def ok(self): return all(x[1] for x in self.checks)
def evaluate_tool_agent(environ=None):
    e=dict(os.environ if environ is None else environ); checks=[]
    names=['PAG_M7_MANIFEST','PAG_M7_MANIFEST_SIG','PAG_M7_PUBLIC_KEY','PAG_M7_AGENT_POLICY','PAG_M7_TOOL_REGISTRY','PAG_M7_AUTHORIZATION_RULES','PAG_M6_MANIFEST']
    for n in names:
        p=Path(e.get(n,'')); ok=p.is_file(); checks.append((n,ok,str(p) if ok else 'required path missing'))
    if not all(x[1] for x in checks): return ToolAgentReport(tuple(checks))
    try: require_blob(e['PAG_M7_MANIFEST'],e['PAG_M7_PUBLIC_KEY'],e['PAG_M7_MANIFEST_SIG']); checks.append(('manifest_signature',True,'verified'))
    except Exception as ex: checks.append(('manifest_signature',False,str(ex))); return ToolAgentReport(tuple(checks))
    try:
        m=load_json(e['PAG_M7_MANIFEST']); root=Path(e.get('PAG_M7_ROOT',Path(e['PAG_M7_MANIFEST']).parent))
        if m.get('m6_manifest_sha256')!=sha256_file(e['PAG_M6_MANIFEST']): raise ToolAgentRuntimeError('M6 manifest digest does not match M7 manifest')
        for rel,dig in m.get('artifacts',{}).items():
            p=root/rel
            if not p.is_file() or sha256_file(p)!=dig: raise ToolAgentRuntimeError(f'manifest digest mismatch: {rel}')
        checks.append(('manifest_hashes',True,'M7 policy/registry/authorization digest-bound and M6-bound'))
    except Exception as ex: checks.append(('manifest_hashes',False,str(ex)))
    try:
        policy=load_json(e['PAG_M7_AGENT_POLICY']); checks.append(('agent_policy',True,require_tool_agent_policy(policy)))
    except Exception as ex:
        policy={}; checks.append(('agent_policy',False,str(ex)))
    try:
        registry=ToolRegistry(e['PAG_M7_TOOL_REGISTRY']); checks.append(('tool_registry',True,'typed non-side-effecting registry valid'))
    except Exception as ex:
        registry=None; checks.append(('tool_registry',False,str(ex)))
    try:
        authorization=build_tool_authorization(e['PAG_M7_AUTHORIZATION_RULES']); checks.append(('authorization_rules',True,'deny-by-default tool authorization valid'))
    except Exception as ex:
        authorization=None; checks.append(('authorization_rules',False,str(ex)))
    try:
        if registry is None or authorization is None or not policy: raise ToolAgentRuntimeError('cross-policy prerequisites invalid')
        allowed=set(policy.get('allowed_tools',[])); registered=set(registry.tools)
        if allowed!=registered: raise ToolAgentRuntimeError('agent allowed_tools must exactly match signed registry')
        covered={r.resource_prefix.removeprefix('tool://') for r in authorization.rules if r.effect=='allow' and r.action=='tool.invoke'}
        if covered!=registered: raise ToolAgentRuntimeError('authorization rules must exactly cover signed registry')
        checks.append(('cross_binding',True,'agent policy, registry and authorization rules exactly aligned'))
    except Exception as ex: checks.append(('cross_binding',False,str(ex)))
    return ToolAgentReport(tuple(checks))
def require_tool_agent(environ=None):
    r=evaluate_tool_agent(environ)
    if not r.ok: raise ToolAgentRuntimeError('; '.join(f'{n}:{d}' for n,o,d in r.checks if not o))
    return r
