from __future__ import annotations
from .common import stable_id

def advisory(fix,policy):
 delayed=bool(fix.get('delayed_disclosure_requested'))
 justified=(not delayed) or bool(fix.get('delayed_disclosure_justification'))
 ready=bool(fix.get('fix_available')) and justified
 return {'advisory_id':stable_id('ADV',fix['vulnerability_id'],fix['product_id']),'vulnerability_id':fix['vulnerability_id'],'product_id':fix['product_id'],'severity':fix['severity'],'impact':fix['impact'],'fix_available':bool(fix['fix_available']),'security_update_id':fix.get('security_update_id'),'security_update_available_at':fix.get('security_update_available_at'),'remediation_guidance':fix['remediation_guidance'],'delayed_disclosure_requested':delayed,'delayed_disclosure_justification':fix.get('delayed_disclosure_justification',''),'publication_ready':ready,'publication_requires_human_authorization':True,'publication_performed':False}

def maintainer_coordination(report):
 component=report.get('component','')
 third_party=bool(component)
 return {'coordination_id':stable_id('COORD',report['report_id'],component),'report_id':report['report_id'],'vulnerability_id':report.get('vulnerability_id'),'component':component,'third_party_component':third_party,'coordination_required':third_party,'prepared_message':('Share vulnerability details and relevant remediation/fix documentation with component maintainer.' if third_party else ''),'human_authorization_required':True,'contact_performed':False}
