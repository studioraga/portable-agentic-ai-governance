import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from portable_ai_governance.enterprise_security.common import M21_1_BASELINE_COMMIT
from portable_ai_governance.enterprise_security.evaluation import evaluate_catalog

def load(p): return json.loads((ROOT/p).read_text())

def test_baseline_is_m21_1_documentation_head():
    assert M21_1_BASELINE_COMMIT == "ea952069938a6435ccb298f5424bab158197ce05"

def test_catalog_has_all_domains_and_no_certification_claim():
    result=evaluate_catalog(load("governance/enterprise/m22/cissp-domain-catalog.json"),load("governance/enterprise/m22/enterprise-security-requirements.json"),load("governance/enterprise/m22/enterprise-control-mapping.json"),load("governance/enterprise/m22/gap-register.json"),load("governance/controls/control-catalog.json"))
    assert result["ok"], result
    assert result["requirement_count"] >= 20
    assert result["open_gap_count"] > 0

def test_m22_does_not_claim_compliance_or_certification():
    m=load("governance/enterprise/m22/enterprise-control-mapping.json")
    assert all(v is False for v in m["claim_boundaries"].values())

def test_gap_register_targets_future_milestones():
    g=load("governance/enterprise/m22/gap-register.json")
    assert {x["target_milestone"].split('/')[0] for x in g["open_gaps"]} <= {"M23","M24","M25","M26","M27","M28","M23/M24","M26/M28"}
