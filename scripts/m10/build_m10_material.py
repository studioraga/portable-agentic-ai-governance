#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.multi_agent.common import write_json,sha256_file
from portable_ai_governance.action_agent.common import secure_tree
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--m9-material',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();m9=Path(a.m9_material).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700);m9m=m9/'security-ops-manifest.json'
 if not m9m.is_file():raise SystemExit(f'FAIL: M9 manifest missing: {m9m}')
 policy={'version':'0.10.0','purpose':'Bounded cooperating governance reasoning agents','reasoning_backend':'deterministic-reference','llm_required':False,'network_access':False,'tool_execution':False,'side_effect_authority':False,'direct_agent_delegation':False,'m8_side_effect_boundary':True,'m9_secops_boundary':True,'budgets':{'max_agent_invocations':6,'max_total_signals':48,'max_findings_per_specialist':16,'max_workflow_output_bytes':262144},'human_decision':{'required':True,'reviewers':['HUMAN-GOVERNANCE-REVIEWER-001'],'ttl_default_seconds':1800,'ttl_max_seconds':1800,'clock_skew_seconds':60,'single_use':True}}
 topology={'version':'0.10.0','fixed_topology':True,'direct_peer_calls':False,'agents':{'GOVERNANCE-SUPERVISOR-001':{'role':'supervisor','may_call':['RISK-AGENT-001','THREAT-AGENT-001','PRIVACY-AGENT-001','CONTROL-AGENT-001','ASSURANCE-AGENT-001'],'may_approve':False,'may_execute_side_effects':False},'RISK-AGENT-001':{'role':'risk','may_call':[],'may_approve':False,'may_execute_side_effects':False},'THREAT-AGENT-001':{'role':'threat','may_call':[],'may_approve':False,'may_execute_side_effects':False},'PRIVACY-AGENT-001':{'role':'privacy','may_call':[],'may_approve':False,'may_execute_side_effects':False},'CONTROL-AGENT-001':{'role':'control','may_call':[],'may_approve':False,'may_execute_side_effects':False},'ASSURANCE-AGENT-001':{'role':'assurance','may_call':[],'may_approve':False,'may_execute_side_effects':False}},'flow':['specialists.parallel-logical','control.synthesis','assurance.check','human.decision'],'handoff_schema':'pag-m10-agent-handoff-v1'}
 write_json(out/'multi-agent-policy.json',policy);write_json(out/'multi-agent-topology.json',topology);generate_ed25519_keypair(out/'workflow-decision-private.pem',out/'workflow-decision-public.pem')
 manifest={'version':'0.10.0','m9_manifest_sha256':sha256_file(m9m),'artifacts':{'multi-agent-policy.json':sha256_file(out/'multi-agent-policy.json'),'multi-agent-topology.json':sha256_file(out/'multi-agent-topology.json'),'workflow-decision-public.pem':sha256_file(out/'workflow-decision-public.pem')},'capabilities':['governance-supervision','risk-reasoning','threat-reasoning','privacy-reasoning','control-synthesis','assurance','human-decision'],'boundary':{'side_effect_authority':False,'m8_side_effect_boundary':True,'m9_secops_boundary':True,'direct_agent_delegation':False}}
 write_json(out/'multi-agent-manifest.json',manifest);generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem');sign_blob(out/'multi-agent-manifest.json',out/'signing-private.pem',out/'multi-agent-manifest.json.sig');secure_tree(out)
 print(f'PASS: M10 multi-agent workflow material generated at {out}');print('PASS: fixed supervisor -> risk/threat/privacy -> control -> assurance -> human decision topology')
if __name__=='__main__':main()
