import pytest
from portable_ai_governance.agents.governance import AISystemInventoryAgent, AISystemRecord, AIRiskAgent, RiskRecord
from portable_ai_governance.kernel.types import AgentRequest, Principal

REQ=AgentRequest("r",Principal("p",("ai_risk_manager",)),"x")

def test_inventory_validates_autonomy():
    rec=AISystemRecord("s","n",("agentic_ai",),"b","t",("prod",),("restricted",),(),(),6,"required","high")
    with pytest.raises(ValueError): AISystemInventoryAgent().analyze(REQ,rec)

def test_risk_agent_cannot_accept_risk():
    risk=RiskRecord("r","s","risk",5,5,(),"owner","accept")
    with pytest.raises(ValueError): AIRiskAgent().analyze(REQ,risk)
