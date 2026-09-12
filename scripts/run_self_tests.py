#!/usr/bin/env python3
from __future__ import annotations
import json, tempfile
from pathlib import Path
from portable_ai_governance.kernel.state_machine import WorkflowState
from portable_ai_governance.kernel.budgets import RunBudget, BudgetExceeded
from portable_ai_governance.kernel.request_signing import sign_request, verify_request
from portable_ai_governance.kernel.replay_cache import PersistentNonceCache, ReplayDetected
from portable_ai_governance.kernel.evidence import EvidenceLedger
from portable_ai_governance.agents.governance import AIRiskAgent, RiskRecord, ControlMappingAgent, GovernanceEvidenceAgent, AISystemRecord
from portable_ai_governance.kernel.authorization import AuthorizationEngine, AuthorizationRule
from portable_ai_governance.kernel.policy import PolicyEngine
from portable_ai_governance.kernel.types import AgentRequest, Principal
from portable_ai_governance.workflows import OnboardingWorkflow

ROOT=Path(__file__).resolve().parents[1]
passed=0

def check(name, fn):
    global passed
    fn(); passed += 1; print(f"PASS {name}")

def illegal_transition():
    s=WorkflowState()
    try: s.transition('COMPLETE')
    except ValueError: return
    raise AssertionError('illegal transition allowed')

def budget():
    b=RunBudget(max_steps=1); b.consume_step()
    try: b.consume_step()
    except BudgetExceeded: return
    raise AssertionError('budget overflow allowed')

def signing():
    key=b'k'*32; req=sign_request(key,method='POST',path='/x',body=b'hello',timestamp=100,nonce='n')
    assert verify_request(key,req,method='POST',path='/x',body=b'hello',now=100)
    assert not verify_request(key,req,method='POST',path='/x',body=b'evil',now=100)

def replay():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'nonce.json'; PersistentNonceCache(p).consume('abc',now=100)
        try: PersistentNonceCache(p).consume('abc',now=101)
        except ReplayDetected: return
        raise AssertionError('replay allowed')

def risk_acceptance():
    req=AgentRequest('r',Principal('p',('ai_risk_manager',)),'x')
    risk=RiskRecord('r','s','risk',5,5,(),'owner','accept')
    try: AIRiskAgent().analyze(req,risk)
    except ValueError: return
    raise AssertionError('agent accepted risk')

def evidence_tamper():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'ledger.jsonl'; l=EvidenceLedger(p,b'e'*32); l.append('x',{'a':1}); l.append('y',{'b':2}); assert l.verify()[0]
        rows=p.read_text().splitlines(); obj=json.loads(rows[0]); obj['payload']['a']=999; rows[0]=json.dumps(obj); p.write_text('\n'.join(rows)+'\n')
        assert not l.verify()[0]

def workflow(authorized=True):
    with tempfile.TemporaryDirectory() as d:
        mapper=ControlMappingAgent(ROOT/'governance/mappings/framework-mapping.json')
        evidence=GovernanceEvidenceAgent(EvidenceLedger(Path(d)/'ledger.jsonl',b'e'*32))
        wf=OnboardingWorkflow(authz=AuthorizationEngine((AuthorizationRule('ai_system.onboard',('ai_governance_admin',),'ai-system/'),)),policy=PolicyEngine(ROOT/'governance/controls/control-catalog.json'),mapper=mapper,evidence=evidence)
        s=AISystemRecord('s','n',('agentic_ai',),'b','t',('prod',),('restricted',),(),(),1,'required','high')
        roles=('ai_governance_admin',) if authorized else ('viewer',)
        req=AgentRequest('run',Principal('p',roles),'onboard')
        r=RiskRecord('r','s','unauthorized access',4,5,('AIS-AUTH-001',),'owner','mitigate')
        result=wf.run(req,s,(r,),('AIS-GOV-001','AIS-RISK-001','AIS-EVID-001','AIS-AUTH-001'))
        assert result['status']==('COMPLETE' if authorized else 'DENIED')

def mapping_complete():
    catalog=json.loads((ROOT/'governance/controls/control-catalog.json').read_text())
    mapping=json.loads((ROOT/'governance/mappings/framework-mapping.json').read_text())['controls']
    assert not [c['control_id'] for c in catalog['controls'] if c['control_id'] not in mapping]

for name, fn in [
 ('illegal-transition',illegal_transition),('budget-fail-closed',budget),('request-signing-tamper',signing),('persistent-replay',replay),('risk-acceptance-prohibited',risk_acceptance),('evidence-tamper',evidence_tamper),('golden-onboarding',lambda: workflow(True)),('unauthorized-onboarding',lambda: workflow(False)),('mapping-complete',mapping_complete)]:
    check(name,fn)
print(f"SELF-TESTS PASS: {passed}/9")
