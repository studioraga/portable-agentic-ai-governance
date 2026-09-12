import json
from portable_ai_governance.agents.governance import ControlMappingAgent, GovernanceEvidenceAgent, AISystemRecord, RiskRecord
from portable_ai_governance.kernel.authorization import AuthorizationEngine, AuthorizationRule
from portable_ai_governance.kernel.evidence import EvidenceLedger
from portable_ai_governance.kernel.policy import PolicyEngine
from portable_ai_governance.kernel.types import AgentRequest, Principal
from portable_ai_governance.workflows import OnboardingWorkflow

def make(tmp_path, root):
    return OnboardingWorkflow(
      authz=AuthorizationEngine((AuthorizationRule("ai_system.onboard",("ai_governance_admin",),"ai-system/"),)),
      policy=PolicyEngine(root/"governance/controls/control-catalog.json"),
      mapper=ControlMappingAgent(root/"governance/mappings/framework-mapping.json"),
      evidence=GovernanceEvidenceAgent(EvidenceLedger(tmp_path/"ledger.jsonl",b"e"*32)))

def test_golden_onboarding(tmp_path):
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]; data=json.loads((root/"examples/golden_onboarding/system.json").read_text())
    sysd=data["system"]; sys=AISystemRecord(**{**sysd,"system_types":tuple(sysd["system_types"]),"environments":tuple(sysd["environments"]),"data_classes":tuple(sysd["data_classes"]),"models":tuple(sysd["models"]),"external_providers":tuple(sysd["external_providers"])})
    risks=tuple(RiskRecord(**{**r,"controls":tuple(r["controls"])}) for r in data["risks"])
    req=AgentRequest("golden",Principal("admin",("ai_governance_admin",)),"onboard")
    result=make(tmp_path,root).run(req,sys,risks,tuple(data["controls"])); assert result["status"]=="COMPLETE"; assert result["trace"][-1]=="COMPLETE"

def test_unauthorized_onboarding_is_denied(tmp_path):
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]; sys=AISystemRecord("s","n",("agentic_ai",),"b","t",("prod",),(),(),(),1,"required","high")
    req=AgentRequest("bad",Principal("viewer",("viewer",)),"onboard")
    result=make(tmp_path,root).run(req,sys,(),("AIS-GOV-001",)); assert result["status"]=="DENIED"
