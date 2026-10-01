from __future__ import annotations
from datetime import timedelta
from .common import parse_ts,z,stable_id

def triage_report(report,policy):
 missing=[f for f in policy['psirt']['required_intake_fields'] if report.get(f) in (None,'')]
 received=parse_ts(report['received_at'])
 return {'case_id':stable_id('PSIRT',report['report_id'],report['product_id']),'report_id':report['report_id'],'product_id':report['product_id'],'vulnerability_id':report.get('vulnerability_id'),'source_type':report['source_type'],'state':'INCOMPLETE' if missing else 'TRIAGED','missing_fields':missing,'ack_due_at':z(received+timedelta(hours=policy['cvd']['acknowledgement_target_hours'])),'reporter_confidentiality_requested':bool(report.get('confidentiality_requested')),'external_side_effects_performed':False}
