from __future__ import annotations
from .common import load_json
class EvaluationError(RuntimeError): pass
REQUIRED={'retrieval_cross_tenant_denied','retrieval_clearance_enforced','provenance_complete','embedding_policy_enforced','model_lock_binding','no_agent_autonomy'}
def require_evaluation(suite_path, results_path):
    suite=load_json(suite_path); results=load_json(results_path)
    required=set(suite.get('required_evaluations',[]))
    if not REQUIRED.issubset(required): raise EvaluationError('required AI-security evaluations missing')
    by={x['name']:x for x in results.get('results',[])}
    for name in required:
        if name not in by or by[name].get('passed') is not True: raise EvaluationError(f'evaluation failed/missing: {name}')
    score=float(results.get('score',0)); threshold=float(suite.get('minimum_score',1.0))
    if score<threshold: raise EvaluationError(f'evaluation score {score} below {threshold}')
    return f'evaluation score {score:.3f} >= {threshold:.3f}'
