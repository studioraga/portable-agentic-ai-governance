import json,time
from pathlib import Path
from portable_ai_governance.cra_final_freeze.evaluation import evaluate
from portable_ai_governance.cra_final_freeze.secure_agentic_demo import run_node1,verify_node2

def test_simulation_cannot_claim_final_freeze(tmp_path):
 root=Path(__file__).resolve().parents[2];p=json.loads((root/'governance/cra/m20/final-freeze-policy.json').read_text());s={'validation_mode':'SIMULATED','production_validation_complete':False,'failed':0,'cra_conformity_claim':False};r=evaluate(root,s,p);assert r['freeze_state']=='RELEASE_CANDIDATE';assert r['final_freeze_ready'] is False

def test_live_complete_can_be_freeze_ready():
 root=Path(__file__).resolve().parents[2];p=json.loads((root/'governance/cra/m20/final-freeze-policy.json').read_text());s={'validation_mode':'LIVE','production_validation_complete':True,'failed':0,'cra_conformity_claim':False};r=evaluate(root,s,p);assert r['freeze_state']=='FINAL_FREEZE_READY';assert r['final_freeze_ready'] is True

def test_secure_agentic_demo(tmp_path):
 root=Path(__file__).resolve().parents[2];case=json.loads((root/'examples/secure-agentic-node1-node2/case.json').read_text());t=run_node1(case,tmp_path);assert t['final']['status']=='approved';assert t['final']['side_effect_authority'] is False;v=verify_node2(tmp_path/'secure-agentic-trace.json',tmp_path/'human-review-public.pem');assert v['ok']

def test_secure_agentic_trace_tamper_rejected(tmp_path):
 root=Path(__file__).resolve().parents[2];case=json.loads((root/'examples/secure-agentic-node1-node2/case.json').read_text());run_node1(case,tmp_path);p=tmp_path/'secure-agentic-trace.json';d=json.loads(p.read_text());d['proposal']['proposal']['system_id']='tampered';p.write_text(json.dumps(d));v=verify_node2(p,tmp_path/'human-review-public.pem');assert not v['ok']
