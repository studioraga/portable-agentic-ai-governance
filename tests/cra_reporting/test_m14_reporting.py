from pathlib import Path
import json,shutil
from portable_ai_governance.cra_reporting.engine import build_fixture_packs
from portable_ai_governance.cra_reporting.runtime import evaluate_m14_material
ROOT=Path(__file__).resolve().parents[2]

def test_build_packs_cover_aev_and_si():
    policy,packs,ready=build_fixture_packs(ROOT)
    assert {p['case_type'] for p in packs}=={'AEV','SEVERE_INCIDENT'}
    assert len(packs)==3
    assert all(len(p['stages'])==3 for p in packs)
    assert all(r['all_currently_anchored_stages_ready'] for r in ready)

def test_aev_fields_and_pec_boundary():
    _,packs,_=build_fixture_packs(ROOT)
    p=next(x for x in packs if x['case_type']=='AEV')
    n=next(s for s in p['stages'] if s['stage']=='NOTIFICATION_72H')
    assert n['fields']['pec_requested'] is False
    assert n['readiness']=='READY'
    assert p['srp_submission_performed'] is False

def test_si_final_report_fields():
    _,packs,_=build_fixture_packs(ROOT)
    for p in [x for x in packs if x['case_type']=='SEVERE_INCIDENT']:
        f=next(s for s in p['stages'] if s['stage']=='FINAL_REPORT')
        assert f['fields']['threat_or_root_cause']
        assert f['fields']['applied_and_ongoing_mitigations']

def test_policy_has_no_api_and_human_handoff():
    policy=json.loads((ROOT/'governance/cra/m14/reporting-policy.json').read_text())
    assert policy['srp']['api_available_initial_release'] is False
    assert policy['srp']['human_portal_submission_required'] is True
    assert policy['boundaries']['network_submission'] is False

def test_m11_m12_m13_bindings_unchanged():
    assert (ROOT/'governance/cra/cra-requirements.json').is_file()
    assert (ROOT/'governance/cra/m12/m12-control-mapping.json').is_file()
    assert (ROOT/'governance/cra/m13/m13-control-mapping.json').is_file()
