from __future__ import annotations
from datetime import date
import calendar

def add_years(d:date, years:int)->date:
 y=d.year+years;day=min(d.day,calendar.monthrange(y,d.month)[1]);return date(y,d.month,day)

def support_period_end(market_placement_date:str, expected_use_years:int)->str:
 start=date.fromisoformat(market_placement_date)
 years=expected_use_years if expected_use_years<5 else max(5,expected_use_years)
 return add_years(start,years).isoformat()

def lifecycle_record(product,as_of:str):
 end=support_period_end(product['market_placement_date'],int(product['expected_use_years']))
 now=date.fromisoformat(as_of);e=date.fromisoformat(end)
 return {'product_id':product['product_id'],'market_placement_date':product['market_placement_date'],'expected_use_years':product['expected_use_years'],'support_period_end':end,'support_period_factors':product['support_period_factors'],'technical_documentation_basis_recorded':True,'purchase_time_end_date_disclosure_ready':True,'support_status':'SUPPORTED' if now<=e else 'END_OF_SUPPORT','eol_notification_where_technically_feasible':True}

def eol_notification(record):
 ended=record['support_status']=='END_OF_SUPPORT'
 return {'product_id':record['product_id'],'support_period_end':record['support_period_end'],'notification_required':ended and record['eol_notification_where_technically_feasible'],'prepared':ended,'sent':False,'external_dispatch_performed':False,'message':f"Support period ended {record['support_period_end']}" if ended else 'Support period active'}
