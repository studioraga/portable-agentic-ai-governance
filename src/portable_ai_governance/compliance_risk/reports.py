from __future__ import annotations
from .common import load_json
class ComplianceReportError(RuntimeError): pass

def require_compliance_report(path):
    d=load_json(path)
    for k in ('report_id','system_id','generated_at','scope','control_summary','evidence_refs','open_risks','exceptions','disclaimer'):
        if k not in d: raise ComplianceReportError(f'report missing {k}')
    if d.get('certification_claim') is not False: raise ComplianceReportError('automated report must not claim certification')
    if 'not a certification' not in d.get('disclaimer','').lower(): raise ComplianceReportError('report disclaimer must state not a certification')
    s=d['control_summary']
    if int(s.get('failed',0))>0 or int(s.get('stale',0))>0: raise ComplianceReportError('report contains failed/stale controls')
    return 'evidence-backed compliance report valid'
