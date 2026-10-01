from __future__ import annotations
from .common import stable_id
from .fields import required_fields

def _base_fields(case,manufacturer,product,enrichment):
    return {
      'notification_type':'Vulnerability' if case['case_type']=='AEV' else 'Incident',
      'title':enrichment.get('title'),
      'manufacturer_legal_name':manufacturer.get('legal_name'),
      'product_name':product.get('product_name'),
      'product_version':product.get('product_version'),
      'selected_csirt_coordinator':manufacturer.get('selected_csirt_coordinator'),
      'member_states_product_available':manufacturer.get('member_states_product_available'),
      'awareness_at':case.get('manufacturer_awareness_at'),
    }

def _deadline(case,stage):
    m={'EARLY_WARNING_24H':'early_warning_at','NOTIFICATION_72H':'notification_at','FINAL_REPORT':'final_report_at'}
    return case.get('deadlines',{}).get(m[stage])

def build_pack(case,manufacturer,product,enrichment,policy):
    stages=[]
    for stage in policy['stages'][case['case_type']]:
        fields=_base_fields(case,manufacturer,product,enrichment)
        if case['case_type']=='AEV':
            if stage=='NOTIFICATION_72H':
                for k in ('general_exploit_nature','vulnerability_description','corrective_or_mitigating_measures_taken','user_mitigation','sensitivity','pec_requested','pec_justification'): fields[k]=enrichment.get(k)
            elif stage=='FINAL_REPORT':
                for k in ('vulnerability_description','severity','impact','malicious_actor_information','security_update_details'): fields[k]=enrichment.get(k)
        else:
            if stage=='EARLY_WARNING_24H': fields['suspected_unlawful_or_malicious']=enrichment.get('suspected_unlawful_or_malicious')
            elif stage=='NOTIFICATION_72H':
                for k in ('incident_nature','initial_assessment','corrective_or_mitigating_measures_taken','user_mitigation','sensitivity'): fields[k]=enrichment.get(k)
            elif stage=='FINAL_REPORT':
                for k in ('detailed_description','severity','impact','threat_or_root_cause','applied_and_ongoing_mitigations'): fields[k]=enrichment.get(k)
        missing=[k for k in required_fields(case['case_type'],stage) if fields.get(k) in (None,'',[])]
        deadline=_deadline(case,stage)
        readiness='NOT_YET_ANCHORED' if deadline is None else ('READY' if not missing else 'NEEDS_DATA')
        stages.append({'stage':stage,'deadline_at':deadline,'readiness':readiness,'fields':fields,'missing_required_fields':missing,
                       'srp_submission_performed':False,'srp_notification_id':None})
    return {
      'pack_id':stable_id('M14PACK',case['case_id']), 'case_id':case['case_id'],'case_type':case['case_type'],'source_ref':case['source_id'],
      'assigned_representative':manufacturer['assigned_representative'],'stages':stages,
      'human_submission_required':True,'srp_submission_performed':False,'network_submission_performed':False,'cra_conformity_claim':False,
      'srp_glossary_version':policy['srp']['srp_glossary_version']
    }
