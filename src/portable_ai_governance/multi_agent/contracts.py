from __future__ import annotations
from .common import sha256_obj
SEVERITIES={'low','medium','high','critical'}
CATEGORIES={'risk','threat','privacy'}
class ContractError(RuntimeError):pass

def _signal(x,cat):
 if not isinstance(x,dict) or set(x)!={'id','severity','summary','evidence_refs'}:raise ContractError(f'{cat} signal fields invalid')
 if not all(isinstance(x[k],str) and x[k] for k in ('id','severity','summary')):raise ContractError(f'{cat} signal strings invalid')
 if x['severity'] not in SEVERITIES:raise ContractError(f'{cat} signal severity invalid')
 if not isinstance(x['evidence_refs'],list) or not all(isinstance(v,str) and v for v in x['evidence_refs']):raise ContractError(f'{cat} evidence_refs invalid')
 return dict(x)

def validate_case(d):
 if not isinstance(d,dict) or set(d)!={'case_id','system_id','risk_signals','threat_signals','privacy_signals'}:raise ContractError('case fields invalid')
 if not isinstance(d['case_id'],str) or not d['case_id'] or not isinstance(d['system_id'],str) or not d['system_id']:raise ContractError('case identity invalid')
 for key,cat in [('risk_signals','risk'),('threat_signals','threat'),('privacy_signals','privacy')]:
  if not isinstance(d[key],list):raise ContractError(f'{key} must be array')
  ids=set()
  for x in d[key]:
   _signal(x,cat)
   if x['id'] in ids:raise ContractError(f'duplicate {cat} signal id')
   ids.add(x['id'])
 return d

def envelope(agent_id,role,case_id,input_obj,output):
 e={'schema':'pag-m10-agent-handoff-v1','agent_id':agent_id,'role':role,'case_id':case_id,'input_sha256':sha256_obj(input_obj),'output':output}
 e['output_sha256']=sha256_obj(output);return e

def validate_envelope(e,*,agent_id=None,role=None,case_id=None):
 if not isinstance(e,dict) or set(e)!={'schema','agent_id','role','case_id','input_sha256','output','output_sha256'}:raise ContractError('handoff envelope fields invalid')
 if e['schema']!='pag-m10-agent-handoff-v1':raise ContractError('handoff schema invalid')
 if agent_id and e['agent_id']!=agent_id:raise ContractError('handoff agent mismatch')
 if role and e['role']!=role:raise ContractError('handoff role mismatch')
 if case_id and e['case_id']!=case_id:raise ContractError('handoff case mismatch')
 if e['output_sha256']!=sha256_obj(e['output']):raise ContractError('handoff output digest mismatch')
 return e
