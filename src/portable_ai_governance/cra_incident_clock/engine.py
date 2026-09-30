from __future__ import annotations
import json
from pathlib import Path
from .classifier import classify_severe_incident
from .clock import build_case,evaluate_deadlines
from .journal import build_awareness_journal

def evaluate_fixture_set(repo_root,now='2026-10-03T12:00:00Z'):
    root=Path(repo_root);policy=json.loads((root/'governance/cra/m13/incident-classification-policy.json').read_text())
    incidents=[json.loads(p.read_text()) for p in sorted((root/'tests/fixtures/m13/incidents').glob('*.json'))]
    assessments=[classify_severe_incident(x,policy) for x in incidents]
    expected=json.loads((root/'tests/fixtures/m13/expected/classifications.json').read_text())
    actual={x['event_id']:x['decision'] for x in assessments}
    if actual!=expected:raise RuntimeError(f'M13 fixture classification mismatch: {actual}')
    aev=json.loads((root/'tests/fixtures/m13/aev/aev-candidate.json').read_text())
    cases=[build_case('AEV',aev['product_id'],aev['assessment_id'],aev['awareness_at'],policy,aev.get('corrective_available_at'))]
    for e,a in zip(incidents,assessments):
        if a['decision']=='SEVERE_INCIDENT': cases.append(build_case('SEVERE_INCIDENT',e['product_id'],e['event_id'],e['awareness_at'],policy,notification_submitted_at=e.get('notification_submitted_at')))
    states=[evaluate_deadlines(c,now) for c in cases]
    return policy,assessments,cases,states,build_awareness_journal(cases)
