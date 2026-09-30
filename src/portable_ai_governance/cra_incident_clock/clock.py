from __future__ import annotations
import calendar
from datetime import timedelta
from .common import parse_ts,fmt_ts,stable_id

def add_months(dt,months):
    m=dt.month-1+months;y=dt.year+m//12;m=m%12+1;day=min(dt.day,calendar.monthrange(y,m)[1])
    return dt.replace(year=y,month=m,day=day)

def _stage(name,deadline,now,satisfied_at=None):
    if deadline is None:return {'name':name,'deadline_at':None,'status':'NOT_APPLICABLE','satisfied_at':satisfied_at}
    d=parse_ts(deadline);n=parse_ts(now)
    if satisfied_at:return {'name':name,'deadline_at':deadline,'status':'SATISFIED','satisfied_at':satisfied_at}
    return {'name':name,'deadline_at':deadline,'status':'BREACHED' if n>d else ('DUE' if n==d else 'PENDING'),'satisfied_at':None}

def build_case(case_type,product_id,source_id,awareness_at,policy,corrective_available_at=None,notification_submitted_at=None):
    t0=parse_ts(awareness_at);cp=policy['clock_policy'];deadlines={}
    if case_type=='AEV':
      deadlines={'early_warning_at':fmt_ts(t0+timedelta(hours=cp['aev_early_warning_hours'])),'notification_at':fmt_ts(t0+timedelta(hours=cp['aev_notification_hours'])),'final_report_at':fmt_ts(parse_ts(corrective_available_at)+timedelta(days=cp['aev_final_days_after_corrective_available'])) if corrective_available_at else None}
    elif case_type=='SEVERE_INCIDENT':
      deadlines={'early_warning_at':fmt_ts(t0+timedelta(hours=cp['incident_early_warning_hours'])),'notification_at':fmt_ts(t0+timedelta(hours=cp['incident_notification_hours'])),'final_report_at':fmt_ts(add_months(parse_ts(notification_submitted_at),cp['incident_final_months_after_notification'])) if notification_submitted_at else None}
    else: raise ValueError('unsupported case type')
    return {'case_id':stable_id('CRA-CASE',case_type,product_id,source_id,fmt_ts(t0)),'case_type':case_type,'product_id':product_id,'source_id':source_id,'manufacturer_awareness_at':fmt_ts(t0),'corrective_available_at':corrective_available_at,'notification_submitted_at':notification_submitted_at,'deadlines':deadlines,'classification':{'reportable_candidate':True},'enisa_submission_performed':False,'cra_conformity_claim':False}

def evaluate_deadlines(case,now,satisfied=None):
    satisfied=satisfied or {};d=case['deadlines'];return {'case_id':case['case_id'],'evaluated_at':now,'stages':[
      _stage('EARLY_WARNING_24H',d.get('early_warning_at'),now,satisfied.get('EARLY_WARNING_24H')),
      _stage('NOTIFICATION_72H',d.get('notification_at'),now,satisfied.get('NOTIFICATION_72H')),
      _stage('FINAL_REPORT',d.get('final_report_at'),now,satisfied.get('FINAL_REPORT'))]}
