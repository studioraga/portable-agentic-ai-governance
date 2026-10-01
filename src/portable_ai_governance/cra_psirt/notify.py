from __future__ import annotations
from .common import stable_id

def notifications_from_reporting_packs(packs):
 out=[]
 for p in packs:
  # Prefer the richest currently prepared reporting stage.
  stages={s['stage']:s for s in p['stages']}
  stage=stages.get('FINAL_REPORT') or stages.get('NOTIFICATION_72H') or stages['EARLY_WARNING_24H']
  f=stage['fields']
  mitig=[]
  for k in ('user_mitigation','corrective_or_mitigating_measures','applied_and_ongoing_mitigations'):
   v=f.get(k)
   if v: mitig.extend(v if isinstance(v,list) else [v])
  summary=f.get('vulnerability_description') or f.get('incident_description') or f.get('general_exploit_nature') or f.get('incident_nature') or p['case_type']
  out.append({'notification_id':stable_id('USER-NOTIFY',p['pack_id'],p['case_type']),'case_id':p['case_id'],'case_type':p['case_type'],'product_id':f.get('product_id') or p.get('product_id','product-node2'),'audience':'IMPACTED_USERS','summary':summary,'risk':f.get('impact') or f.get('severity') or 'See signed reporting evidence','mitigations':mitig or ['Follow manufacturer security advisory and apply available security updates.'],'corrective_measures':mitig or ['Apply available manufacturer corrective measures.'],'structured_machine_readable':True,'human_authorization_required':True,'sent':False,'external_dispatch_performed':False})
 return out
