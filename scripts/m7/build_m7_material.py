#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
from portable_ai_governance.tool_agent.common import write_private_json,secure_tree,sha256_file
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser(); ap.add_argument('--m6-material',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    m6=Path(a.m6_material).resolve(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True,mode=0o700)
    m6man=m6/'evidence-analyst-manifest.json'
    if not m6man.is_file(): raise SystemExit(f'FAIL: M6 manifest missing: {m6man}')
    eid={'type':'string','minLength':1,'maxLength':256}
    registry={'version':'0.7.0','default':'deny','side_effecting_tools':False,'tools':[
      {'name':'evidence.metadata','version':'1.0.0','action':'tool.invoke','resource':'tool://evidence.metadata','policy_control_id':'AIS-TOOL-POLICY-001','side_effecting':False,'input_schema':{'type':'object','properties':{'evidence_id':eid},'required':['evidence_id'],'additionalProperties':False},'output_schema':{'type':'object','properties':{'evidence_id':eid},'required':['evidence_id'],'additionalProperties':True}},
      {'name':'evidence.verify','version':'1.0.0','action':'tool.invoke','resource':'tool://evidence.verify','policy_control_id':'AIS-TOOL-POLICY-001','side_effecting':False,'input_schema':{'type':'object','properties':{'evidence_id':eid},'required':['evidence_id'],'additionalProperties':False},'output_schema':{'type':'object','properties':{'evidence_id':eid,'ok':{'type':'boolean'},'expected_sha256':{'type':'string','minLength':64,'maxLength':64},'actual_sha256':{'type':'string','minLength':64,'maxLength':64}},'required':['evidence_id','ok','expected_sha256','actual_sha256'],'additionalProperties':False}},
      {'name':'evidence.summarize','version':'1.0.0','action':'tool.invoke','resource':'tool://evidence.summarize','policy_control_id':'AIS-TOOL-POLICY-001','side_effecting':False,'input_schema':{'type':'object','properties':{'evidence_id':eid},'required':['evidence_id'],'additionalProperties':False},'output_schema':{'type':'object','properties':{'evidence_id':eid,'format':{'type':'string','enum':['json','text']},'bytes':{'type':'integer','minimum':0}},'required':['evidence_id','format','bytes'],'additionalProperties':True}},
    ]}
    write_private_json(out/'typed-tool-registry.json',registry)
    allowed=[t['name'] for t in registry['tools']]
    policy={'version':'0.7.0','agent_id':'TOOL-ANALYST-001','purpose':'Bounded typed-tool agent over governed evidence','principal':{'principal_id':'TOOL-ANALYST-001','roles':['tool_agent'],'attributes':{'agent_class':'bounded-tool-agent'}},'allowed_tools':allowed,'required_pipeline':['schema','authorization','policy','budget','audit'],'budget':{'max_steps':8,'max_tool_calls':6},'side_effecting_tools':False,'direct_executor_access':False,'approval_decisions':False,'risk_acceptance':False,'compliance_certification':False,'delegation':False}
    write_private_json(out/'tool-agent-policy.json',policy)
    auth={'version':'0.7.0','default':'deny','rules':[{'action':'tool.invoke','roles':['tool_agent'],'resource_prefix':f'tool://{name}','effect':'allow','principal_attributes':{'agent_class':['bounded-tool-agent']},'resource_attributes':{'side_effecting':['false']}} for name in allowed]}
    write_private_json(out/'tool-authorization-rules.json',auth)
    artifacts=['typed-tool-registry.json','tool-agent-policy.json','tool-authorization-rules.json']
    manifest={'version':'0.7.0','agent_id':'TOOL-ANALYST-001','m6_manifest_sha256':sha256_file(m6man),'artifacts':{n:sha256_file(out/n) for n in artifacts},'pipeline':['schema','authorization','policy','budget','audit'],'boundary':{'side_effecting_tools':False,'direct_executor_access':False,'approval_decisions':False,'risk_acceptance':False,'compliance_certification':False,'delegation':False}}
    write_private_json(out/'tool-agent-manifest.json',manifest)
    generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem'); sign_blob(out/'tool-agent-manifest.json',out/'signing-private.pem',out/'tool-agent-manifest.json.sig')
    secure_tree(out)
    print(f'PASS: M7 typed-tool agent material generated at {out}')
    print(f'PASS: registered {len(allowed)} typed non-side-effecting tools')
    print('PASS: mandatory mediation pipeline schema -> authorization -> policy -> budget -> audit')
    print('IMPORTANT: M7 rejects side-effecting tools; approval-controlled side effects remain M8 scope.')
if __name__=='__main__': main()
