from __future__ import annotations
from .common import load_json
class ThreatModelError(RuntimeError): pass
REQUIRED={'prompt-injection','sensitive-information-disclosure','data-model-poisoning','vector-embedding-weakness','model-theft','retrieval-authorization-bypass','excessive-agency'}
def require_threat_model(path):
    d=load_json(path); threats={x.get('threat_id'):x for x in d.get('threats',[])}
    miss=REQUIRED-set(threats)
    if miss: raise ThreatModelError(f'missing threats: {sorted(miss)}')
    for tid in REQUIRED:
        t=threats[tid]
        if not t.get('mitigations') or not t.get('verification'): raise ThreatModelError(f'incomplete threat: {tid}')
    if d.get('llm_agent_autonomy') is not False or d.get('llm_tool_execution') is not False: raise ThreatModelError('M4 forbids LLM agent autonomy/tool execution')
    return 'required AI threat model coverage present; autonomy disabled'
