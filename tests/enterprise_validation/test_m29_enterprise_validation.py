import json
from pathlib import Path
from portable_ai_governance.enterprise_validation.coverage import build_requirement_matrix
from portable_ai_governance.enterprise_validation.readiness import assess_production_readiness
ROOT=Path(__file__).resolve().parents[2]
def J(p):return json.loads((ROOT/p).read_text())
def matrix():
 closures={f'M{m}':J(f'governance/enterprise/m{m}/m{m}-gap-closure.json') for m in range(23,29)}
 return build_requirement_matrix(J('governance/enterprise/m22/enterprise-security-requirements.json')['requirements'],closures,J('governance/enterprise/m29/m29-reconciliation.json'))
def test_matrix_has_23_requirements(): assert len(matrix()['requirements'])==23
def test_d8_002_reconciles_from_m27(): assert next(x for x in matrix()['requirements'] if x['requirement_id']=='CISSP-D8-002')['state']=='EVIDENCED'
def test_domain3_remains_partial():
 m=matrix();assert set(m['open_requirements'])=={'CISSP-D3-001','CISSP-D3-002'};assert next(x for x in m['domains'] if x['domain']==3)['state']=='PARTIAL'
def test_production_gate_fails_closed_for_current_lab():
 r=assess_production_readiness(matrix(),{'production_ready':False},{'production_pentest_evidence_present':False},{'production_evidence_present':False},False,True);assert not r['production_ready'];assert 'm21_platform_production_ready' in r['blocking_gates']
def test_production_gate_requires_node2():
 m=matrix();m['all_requirements_evidenced']=True
 r=assess_production_readiness(m,{'production_ready':True},{'production_pentest_evidence_present':True},{'production_evidence_present':True},False,True);assert not r['production_ready'];assert r['blocking_gates']==['node2_independent_verification']
def test_production_gate_can_pass_only_when_all_inputs_real():
 m=matrix();m['all_requirements_evidenced']=True
 r=assess_production_readiness(m,{'production_ready':True},{'production_pentest_evidence_present':True},{'production_evidence_present':True},True,True);assert r['production_ready']
def test_m29_controls_are_catalogued_and_mapped():
 cat={x['control_id'] for x in J('governance/controls/control-catalog.json')['controls']};fm=set(J('governance/mappings/framework-mapping.json')['controls'])
 ids={x['control_id'] for x in J('governance/enterprise/m29/m29-control-mapping.json')['controls']};assert len(ids)==5;assert ids<=cat;assert ids<=fm
