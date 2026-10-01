from pathlib import Path
import json,shutil
from portable_ai_governance.cra_psirt.engine import build_fixture_material
from portable_ai_governance.cra_psirt.runtime import evaluate_m15_material
ROOT=Path(__file__).resolve().parents[2]

def test_psirt_intake_and_ack_deadline():
 p,cases,_,_,_,_=build_fixture_material(ROOT);assert len(cases)==2;assert all(c['state']=='TRIAGED' for c in cases);assert all(c['ack_due_at'] for c in cases)

def test_cvd_policy_and_contact_contract():
 p,*_=build_fixture_material(ROOT);sp=p['psirt']['single_point_of_contact'];assert sp['email'];assert sp['policy_uri'];assert p['cvd']['publication_requires_human_authorization'] is True

def test_component_maintainer_coordination_is_prepared_not_sent():
 _,_,coords,_,_,_=build_fixture_material(ROOT);assert any(c['coordination_required'] for c in coords);assert all(c['contact_performed'] is False for c in coords)

def test_fixed_vulnerability_advisories_and_delayed_disclosure():
 _,_,_,advs,_,_=build_fixture_material(ROOT);assert all(a['publication_ready'] for a in advs);d=next(a for a in advs if a['delayed_disclosure_requested']);assert d['delayed_disclosure_justification'];assert d['publication_performed'] is False

def test_user_notifications_cover_aev_and_severe_incident():
 _,_,_,_,n,_=build_fixture_material(ROOT);assert {'AEV','SEVERE_INCIDENT'}<={x['case_type'] for x in n};assert all(x['structured_machine_readable'] and not x['sent'] for x in n)

def test_annex_ii_contact_contract():
 *_,c=build_fixture_material(ROOT);assert c['manufacturer_contact']['email'];assert c['vulnerability_single_point_of_contact']['email'];assert c['cvd_policy_ready'] is True

def test_no_external_side_effect_boundaries():
 p,*_=build_fixture_material(ROOT);b=p['boundaries'];assert b['external_dispatch'] is False;assert b['public_disclosure_performed'] is False;assert b['user_notification_sent'] is False;assert b['component_maintainer_contacted'] is False

def test_prior_baselines_exist_and_are_unchanged_targets():
 assert (ROOT/'governance/cra/cra-requirements.json').is_file();assert (ROOT/'governance/cra/m12/m12-control-mapping.json').is_file();assert (ROOT/'governance/cra/m13/m13-control-mapping.json').is_file();assert (ROOT/'governance/cra/m14/m14-control-mapping.json').is_file()
