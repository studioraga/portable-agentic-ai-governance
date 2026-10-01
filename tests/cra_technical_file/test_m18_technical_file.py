import json
from pathlib import Path
from portable_ai_governance.cra_technical_file.catalog import build_technical_file_index,summarize,gaps
ROOT=Path(__file__).resolve().parents[2]

def test_annex_vii_has_eight_sections():
    idx=build_technical_file_index(ROOT);assert len(idx['entries'])==8;assert len({x['section_id'] for x in idx['entries']})==8

def test_all_referenced_evidence_exists(): assert summarize(build_technical_file_index(ROOT))['all_references_present'] is True

def test_eu_declaration_is_explicit_gap_not_fabricated():
    g={x['section_id']:x for x in gaps(build_technical_file_index(ROOT))};assert g['ANNEX-VII-7']['readiness']=='GAP'

def test_test_reports_remain_partial_until_m19():
    g={x['section_id']:x for x in gaps(build_technical_file_index(ROOT))};assert g['ANNEX-VII-6']['readiness']=='PARTIAL'

def test_standards_section_does_not_invent_harmonised_standard_claim():
    g={x['section_id']:x for x in gaps(build_technical_file_index(ROOT))};assert g['ANNEX-VII-5']['readiness']=='PARTIAL'

def test_software_product_marks_hardware_photos_not_applicable():
    p=json.loads((ROOT/'tests/fixtures/m18/product-technical-profile.json').read_text());assert p['hardware_product'] is False

def test_m18_is_technical_file_but_not_conformity_assessment():
    p=json.loads((ROOT/'governance/cra/m18/technical-file-policy.json').read_text());b=p['boundaries'];assert b['technical_file_generated'] is True;assert b['conformity_assessment_performed'] is False;assert b['cra_conformity_claim'] is False

def test_m11_and_m17_state_mutation_forbidden():
    b=json.loads((ROOT/'governance/cra/m18/technical-file-policy.json').read_text())['boundaries'];assert b['m11_status_mutation'] is False;assert b['m17_evidence_state_mutation'] is False
