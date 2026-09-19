#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'src'
if str(SRC) not in sys.path:sys.path.insert(0,str(SRC))
from portable_ai_governance.action_agent.common import write_private_json,secure_tree,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
def obj(p,r):return {'type':'object','properties':p,'required':r,'additionalProperties':False}
def s(a=1,b=512,enum=None):
 d={'type':'string','minLength':a,'maxLength':b}
 if enum:d['enum']=enum
 return d
def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--m7-material',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();m7=Path(a.m7_material).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700);m7man=m7/'tool-agent-manifest.json'
 if not m7man.is_file():raise SystemExit(f'FAIL: M7 manifest missing: {m7man}')
 specs=[
 ('incident.create',obj({'title':s(1,200),'severity':s(enum=['low','medium','high','critical']),'evidence_ref':s(0,512)},['title','severity']),obj({'action_id':s(),'incident_id':s(),'title':s(),'severity':s(),'evidence_ref':s(0,512),'status':s(enum=['open']),'created_at':{'type':'integer','minimum':0}},['action_id','incident_id','title','severity','evidence_ref','status','created_at'])),
 ('rerun.request',obj({'job_id':s(1,200),'reason':s(1,1000)},['job_id','reason']),obj({'action_id':s(),'rerun_id':s(),'job_id':s(),'reason':s(),'status':s(enum=['requested']),'created_at':{'type':'integer','minimum':0}},['action_id','rerun_id','job_id','reason','status','created_at'])),
 ('ticket.create',obj({'title':s(1,200),'queue':s(1,100),'description':s(1,2000)},['title','queue','description']),obj({'action_id':s(),'ticket_id':s(),'title':s(),'queue':s(),'description':s(),'status':s(enum=['open']),'created_at':{'type':'integer','minimum':0}},['action_id','ticket_id','title','queue','description','status','created_at'])),
 ('model.quarantine',obj({'model_id':s(1,200),'model_digest':s(64,64),'reason':s(1,1000)},['model_id','model_digest','reason']),obj({'action_id':s(),'quarantine_id':s(),'model_id':s(),'model_digest':s(64,64),'reason':s(),'status':s(enum=['quarantined']),'created_at':{'type':'integer','minimum':0}},['action_id','quarantine_id','model_id','model_digest','reason','status','created_at']))]
 tools=[{'name':n,'version':'1.0.0','action':'action.execute','resource':f'action://{n}','policy_control_id':'AIS-ACTION-POLICY-001','side_effecting':True,'approval_required':True,'input_schema':i,'output_schema':o} for n,i,o in specs]
 registry={'version':'0.8.0','default':'deny','side_effecting_tools':True,'approval_required':True,'tools':tools};write_private_json(out/'action-tool-registry.json',registry);allowed=[x['name'] for x in tools]
 policy={'version':'0.8.0','agent_id':'ACTION-AGENT-001','purpose':'Approval-controlled bounded side effects','principal':{'principal_id':'ACTION-AGENT-001','roles':['action_agent'],'attributes':{'agent_class':'approval-controlled-action-agent'}},'allowed_tools':allowed,'required_pipeline':['schema','authorization','policy','budget','approval','audit'],'budget':{'max_steps':6,'max_tool_calls':4},'side_effecting_tools':True,'approval_required':True,'approval_ttl_default_seconds':1800,'approval_ttl_max_seconds':1800,'approval_clock_skew_seconds':60,'agent_can_approve':False,'self_approval':False,'direct_executor_access':False,'risk_acceptance':False,'compliance_certification':False,'delegation':False};write_private_json(out/'action-agent-policy.json',policy)
 auth={'version':'0.8.0','default':'deny','rules':[{'action':'action.execute','roles':['action_agent'],'resource_prefix':f'action://{n}','effect':'allow','principal_attributes':{'agent_class':['approval-controlled-action-agent']},'resource_attributes':{'side_effecting':['true'],'approval_required':['true']}} for n in allowed]};write_private_json(out/'action-authorization-rules.json',auth)
 approvers={'version':'0.8.0','approvers':[{'principal_id':'HUMAN-APPROVER-001','roles':['human_approver'],'attributes':{'principal_class':'human'}}]}
 write_private_json(out/'approval-authorities.json',approvers)
 generate_ed25519_keypair(out/'approval-signing-private.pem',out/'approval-signing-public.pem')
 arts=['action-tool-registry.json','action-agent-policy.json','action-authorization-rules.json','approval-authorities.json','approval-signing-public.pem'];manifest={'version':'0.8.0','agent_id':'ACTION-AGENT-001','m7_manifest_sha256':sha256_file(m7man),'artifacts':{n:sha256_file(out/n) for n in arts},'pipeline':['schema','authorization','policy','budget','approval','audit'],'boundary':{'side_effecting_tools':True,'approval_required':True,'agent_can_approve':False,'self_approval':False,'direct_executor_access':False,'risk_acceptance':False,'compliance_certification':False,'delegation':False}};write_private_json(out/'action-agent-manifest.json',manifest);generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem');sign_blob(out/'action-agent-manifest.json',out/'signing-private.pem',out/'action-agent-manifest.json.sig');secure_tree(out);print(f'PASS: M8 approval-controlled action material generated at {out}');print('PASS: registered 4 typed side-effect tools requiring independent approval');print('PASS: pipeline schema -> authorization -> policy -> budget -> approval -> audit')
if __name__=='__main__':main()
