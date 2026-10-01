from __future__ import annotations
import json,time,uuid
from pathlib import Path
from portable_ai_governance.multi_agent.workflow import GovernanceSupervisor
from portable_ai_governance.multi_agent.approval import WorkflowDecisionGrant,DecisionIssuer,DecisionVerifier,to_dict,from_dict
from portable_ai_governance.multi_agent.common import sha256_obj
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair
POLICY={'version':'0.10.0','side_effect_authority':False,'direct_agent_delegation':False,'m8_side_effect_boundary':True,'m9_secops_boundary':True,'budgets':{'max_agent_invocations':6,'max_total_signals':48,'max_findings_per_specialist':16,'max_workflow_output_bytes':262144},'human_decision':{'required':True,'reviewers':['HUMAN-GOVERNANCE-REVIEWER-001'],'ttl_default_seconds':1800,'ttl_max_seconds':1800,'clock_skew_seconds':60}}
TOPOLOGY={'fixed_topology':True,'direct_peer_calls':False,'agents':{x:{} for x in ['GOVERNANCE-SUPERVISOR-001','RISK-AGENT-001','THREAT-AGENT-001','PRIVACY-AGENT-001','CONTROL-AGENT-001','ASSURANCE-AGENT-001']}}
def run_node1(case,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);priv=out/'human-review-private.pem';pub=out/'human-review-public.pem';generate_ed25519_keypair(priv,pub);sup=GovernanceSupervisor(POLICY,TOPOLOGY,out/'runtime',pub);res=sup.analyze(case);n=int(time.time());g=WorkflowDecisionGrant(str(uuid.uuid4()),res['workflow_id'],res['proposal_sha256'],res['assurance_sha256'],'HUMAN-GOVERNANCE-REVIEWER-001','approve',n,n+600,1);decision=to_dict(g,DecisionIssuer(priv).sign(g));final=sup.finalize(res,decision)
 trace={'schema':'pag-m20-secure-agentic-trace-v1','m10_commit':'d4ce10a','proposal':res,'decision':decision,'final':final,'authority':{'agents_side_effect_authority':False,'human_decision_required':True,'direct_peer_calls':False},'traceability':{'proposal_sha256':res['proposal_sha256'],'assurance_sha256':res['assurance_sha256']}}
 (out/'secure-agentic-trace.json').write_text(json.dumps(trace,indent=2,sort_keys=True)+'\n');return trace
def verify_node2(trace_path,pub):
 t=json.loads(Path(trace_path).read_text());r=t['proposal'];g,s=from_dict(t['decision']);DecisionVerifier(pub,1800,60).verify(g,s);checks=[r['proposal_sha256']==sha256_obj(r['proposal']),g.proposal_sha256==r['proposal_sha256'],g.assurance_sha256==r['assurance_sha256'],t['final']['side_effect_authority'] is False,t['authority']['direct_peer_calls'] is False,t['authority']['human_decision_required'] is True];return {'ok':all(checks),'checks':checks}
