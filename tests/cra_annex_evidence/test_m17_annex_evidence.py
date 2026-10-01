import json
from pathlib import Path
from portable_ai_governance.cra_annex_evidence.catalog import build_evidence_index,summarize,gaps

ROOT=Path(__file__).resolve().parents[2]

def test_annex_i_has_22_rows():
    idx=build_evidence_index(ROOT)
    assert len(idx['entries'])==22
    assert len({x['requirement_id'] for x in idx['entries']})==22

def test_part_i_and_part_ii_coverage():
    s=summarize(build_evidence_index(ROOT))
    assert s['part_i']==14
    assert s['part_ii']==8

def test_all_evidence_references_exist():
    s=summarize(build_evidence_index(ROOT))
    assert s['all_references_present'] is True

def test_no_conformity_claims():
    idx=build_evidence_index(ROOT)
    assert all(x['conformity_claim'] is False for x in idx['entries'])
    assert summarize(idx)['cra_conformity_claim'] is False

def test_explicit_gaps_preserved():
    g=gaps(build_evidence_index(ROOT))
    ids={x['requirement_id'] for x in g if x['evidence_state']=='GAP'}
    assert {'CRA-REQ-046','CRA-REQ-053','CRA-REQ-057'} <= ids

def test_m19_regular_security_test_gap_preserved():
    g={x['requirement_id']:x for x in gaps(build_evidence_index(ROOT))}
    assert g['CRA-REQ-060']['evidence_state']=='PARTIAL'
    assert g['CRA-REQ-060']['planned_followup']=='M19 production validation'

def test_m11_requirement_matrix_is_not_m17_output():
    policy=json.loads((ROOT/'governance/cra/m17/annex-i-evidence-policy.json').read_text())
    assert policy['boundaries']['m11_status_mutation'] is False

def test_m17_is_evidence_not_technical_file_or_assessment():
    policy=json.loads((ROOT/'governance/cra/m17/annex-i-evidence-policy.json').read_text())
    b=policy['boundaries']
    assert b['technical_file_generated'] is False
    assert b['conformity_assessment_performed'] is False
