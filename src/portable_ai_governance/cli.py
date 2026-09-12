from __future__ import annotations
import argparse, hashlib, json, os, secrets, sys
from pathlib import Path
from .agents.governance import ControlMappingAgent, GovernanceEvidenceAgent, AISystemRecord, RiskRecord
from .kernel.authorization import AuthorizationEngine, AuthorizationRule
from .kernel.evidence import EvidenceLedger
from .kernel.policy import PolicyEngine
from .kernel.security_profile import require_security_profile
from .kernel.types import AgentRequest, Principal
from .workflows.onboarding import OnboardingWorkflow

def _root() -> Path:
    return Path(os.getenv("PAG_REPO_ROOT", Path.cwd())).resolve()

def cmd_validate_security(_: argparse.Namespace) -> int:
    report = require_security_profile()
    print(json.dumps({"profile":report.profile,"ok":report.ok,"checks":[c.__dict__ for c in report.checks]}, indent=2))
    return 0

def cmd_onboard(args: argparse.Namespace) -> int:
    root = _root(); require_security_profile()
    signing = os.getenv("PAG_EVIDENCE_SIGNING_KEY", "lab-evidence-key-0123456789abcdef-0123456789abcdef").encode()
    ledger = EvidenceLedger(root / "var/evidence/governance.jsonl", signing)
    evidence = GovernanceEvidenceAgent(ledger)
    mapper = ControlMappingAgent(root / "governance/mappings/framework-mapping.json")
    policy = PolicyEngine(root / "governance/controls/control-catalog.json")
    authz = AuthorizationEngine((AuthorizationRule("ai_system.onboard", ("ai_governance_admin","ai_risk_manager"), "ai-system/"),))
    workflow = OnboardingWorkflow(authz=authz, policy=policy, mapper=mapper, evidence=evidence)
    principal = Principal(args.principal, tuple(args.roles.split(",")))
    request = AgentRequest(args.run_id, principal, "Onboard AI system")
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    system = AISystemRecord(**{**payload["system"], "system_types":tuple(payload["system"]["system_types"]), "environments":tuple(payload["system"]["environments"]), "data_classes":tuple(payload["system"]["data_classes"]), "models":tuple(payload["system"]["models"]), "external_providers":tuple(payload["system"]["external_providers"])})
    risks = tuple(RiskRecord(**{**r, "controls":tuple(r["controls"])}) for r in payload["risks"])
    result = workflow.run(request, system, risks, tuple(payload["controls"]))
    print(json.dumps(result, indent=2, default=str)); return 0 if result["status"] == "COMPLETE" else 2

def cmd_verify_evidence(_: argparse.Namespace) -> int:
    root = _root(); signing = os.getenv("PAG_EVIDENCE_SIGNING_KEY", "lab-evidence-key-0123456789abcdef-0123456789abcdef").encode()
    ok, detail = EvidenceLedger(root / "var/evidence/governance.jsonl", signing).verify(); print(json.dumps({"ok":ok,"detail":detail})); return 0 if ok else 2

def main(argv=None) -> int:
    p=argparse.ArgumentParser(); sub=p.add_subparsers(required=True)
    s=sub.add_parser("validate-security"); s.set_defaults(func=cmd_validate_security)
    o=sub.add_parser("onboard"); o.add_argument("--input",required=True); o.add_argument("--run-id",default="golden-run-001"); o.add_argument("--principal",default="governance-admin"); o.add_argument("--roles",default="ai_governance_admin"); o.set_defaults(func=cmd_onboard)
    v=sub.add_parser("verify-evidence"); v.set_defaults(func=cmd_verify_evidence)
    a=p.parse_args(argv); return a.func(a)

if __name__ == "__main__": raise SystemExit(main())
