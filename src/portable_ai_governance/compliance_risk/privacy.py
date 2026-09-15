from __future__ import annotations
from .common import load_json
class PrivacyAssessmentError(RuntimeError): pass
REQ=('assessment_id','system_id','owner','purposes','data_categories','legal_basis','retention','data_subject_rights','cross_border_transfer','security_controls','dpia_required','review_due')
def require_privacy_assessment(path):
    d=load_json(path); missing=[k for k in REQ if k not in d or d[k] in (None,'',[])]
    if missing: raise PrivacyAssessmentError('missing privacy fields: '+','.join(missing))
    if d.get('collect_sensitive_data') and not d.get('sensitive_data_justification'): raise PrivacyAssessmentError('sensitive data justification required')
    if d.get('cross_border_transfer') is True and not d.get('transfer_safeguards'): raise PrivacyAssessmentError('cross-border safeguards required')
    if d.get('dpia_required') is True and d.get('dpia_status')!='approved': raise PrivacyAssessmentError('required DPIA must be approved')
    if d.get('retention') in {'indefinite','unbounded'}: raise PrivacyAssessmentError('unbounded retention prohibited')
    return 'privacy assessment complete'
