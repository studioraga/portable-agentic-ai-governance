from __future__ import annotations

COMMON_REQUIRED=['notification_type','title','manufacturer_legal_name','product_name','selected_csirt_coordinator','member_states_product_available','awareness_at']
AEV_REQUIRED={
 'EARLY_WARNING_24H':COMMON_REQUIRED,
 'NOTIFICATION_72H':COMMON_REQUIRED+['general_exploit_nature','vulnerability_description','corrective_or_mitigating_measures_taken','user_mitigation','sensitivity'],
 'FINAL_REPORT':COMMON_REQUIRED+['vulnerability_description','severity','impact','security_update_details']
}
SI_REQUIRED={
 'EARLY_WARNING_24H':COMMON_REQUIRED+['suspected_unlawful_or_malicious'],
 'NOTIFICATION_72H':COMMON_REQUIRED+['incident_nature','initial_assessment','corrective_or_mitigating_measures_taken','user_mitigation','sensitivity'],
 'FINAL_REPORT':COMMON_REQUIRED+['detailed_description','severity','impact','threat_or_root_cause','applied_and_ongoing_mitigations']
}
def required_fields(case_type,stage): return (AEV_REQUIRED if case_type=='AEV' else SI_REQUIRED)[stage]
