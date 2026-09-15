from __future__ import annotations
from .common import load_json
class ImpactAssessmentError(RuntimeError): pass
REQ=('assessment_id','system_id','owner','purpose','stakeholders','impact_domains','inherent_risk','controls','residual_risk','decision','review_due')
RISK={'low':1,'medium':2,'high':3,'critical':4}
def require_impact_assessment(path):
    d=load_json(path)
    missing=[k for k in REQ if not d.get(k)]
    if missing: raise ImpactAssessmentError('missing impact fields: '+','.join(missing))
    if d['inherent_risk'] not in RISK or d['residual_risk'] not in RISK: raise ImpactAssessmentError('invalid risk level')
    if RISK[d['residual_risk']] > RISK[d['inherent_risk']]: raise ImpactAssessmentError('residual risk cannot exceed inherent risk')
    if d['decision'] not in {'approve','approve-with-conditions','reject'}: raise ImpactAssessmentError('invalid decision')
    if d['decision']!='reject' and d['residual_risk']=='critical': raise ImpactAssessmentError('critical residual risk cannot be approved')
    if not isinstance(d['stakeholders'],list) or not d['stakeholders']: raise ImpactAssessmentError('stakeholders required')
    if not isinstance(d['impact_domains'],list) or not d['impact_domains']: raise ImpactAssessmentError('impact domains required')
    return 'impact assessment complete'
