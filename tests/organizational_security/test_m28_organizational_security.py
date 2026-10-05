import json,pytest
from portable_ai_governance.organizational_security.evidence import validate_attestation
from portable_ai_governance.organizational_security.governance import validate_governance
from portable_ai_governance.organizational_security.personnel import validate_personnel
from portable_ai_governance.organizational_security.physical import validate_physical
from portable_ai_governance.organizational_security.bcp import validate_bcp
ROOT=__import__('pathlib').Path(__file__).resolve().parents[2]
def J(p):return json.loads((ROOT/p).read_text())
def att(**kw):
 d={'record_id':'r','subject':'subject','authority':'authority','authority_role':'security_owner','observed_at':'2026-10-06T00:00:00Z','expires_at':'2027-10-06T00:00:00Z','evidence_type':'SIMULATED_SCHEMA_VALIDATION_ONLY','evidence_reference':'test','production_evidence':False,'requires_independence':True};d.update(kw);return d
def test_attestation_current(): assert validate_attestation(att(),authority_roles={'security_owner'},max_age_days=365,as_of='2026-10-06T12:00:00Z')
def test_self_attestation_denied():
 with pytest.raises(ValueError):validate_attestation(att(subject='same',authority='same'),authority_roles={'security_owner'},max_age_days=365,as_of='2026-10-06T12:00:00Z')
def test_simulated_denied_in_production():
 with pytest.raises(ValueError):validate_attestation(att(evidence_type='AUTHORIZED_GOVERNANCE_RECORD'),authority_roles={'security_owner'},max_age_days=365,as_of='2026-10-06T12:00:00Z',production=True,production_type='AUTHORIZED_GOVERNANCE_RECORD')
def test_stale_denied():
 with pytest.raises(ValueError):validate_attestation(att(observed_at='2020-01-01T00:00:00Z'),authority_roles={'security_owner'},max_age_days=365,as_of='2026-10-06T12:00:00Z')
def test_governance_missing_role_denied():
 p=J('governance/enterprise/m28/organizational-governance-policy.json');c={'roles':{},'raci':{'a':['b']},'policy_owners':{'x':'y'}}
 with pytest.raises(ValueError):validate_governance(p,c,att(authority_role='executive_sponsor'),'2026-10-06T12:00:00Z')
def test_personnel_missing_training_denied():
 p=J('governance/enterprise/m28/personnel-security-policy.json')
 with pytest.raises(ValueError):validate_personnel(p,[att(kind='security_awareness_training',authority_role='training_owner')],'2026-10-06T12:00:00Z')
def test_termination_sla_denied():
 p=J('governance/enterprise/m28/personnel-security-policy.json');rs=[]
 for k in p['required_evidence']:
  r=att(kind=k,authority_role='hr_owner');rs.append(r)
 [r.update({'terminated':True,'revocation_hours':99}) for r in rs if r['kind']=='joiner_mover_leaver_review']
 with pytest.raises(ValueError):validate_personnel(p,rs,'2026-10-06T12:00:00Z')
def test_physical_missing_control_denied():
 p=J('governance/enterprise/m28/physical-environmental-policy.json')
 with pytest.raises(ValueError):validate_physical(p,[att(control='badge_or_equivalent_access_control',authority_role='facilities_owner')],'2026-10-06T12:00:00Z')
def test_bcp_lessons_required():
 p=J('governance/enterprise/m28/business-continuity-policy.json');plan={'bia_reference':'x','continuity_plan_reference':'x','crisis_roles':['x'],'communications_plan':'x','dependency_register':['x']}
 with pytest.raises(ValueError):validate_bcp(p,plan,att(authority_role='continuity_owner'),'2026-10-06T12:00:00Z')
def test_m28_controls_in_catalog_and_mapping():
 cm=J('governance/enterprise/m28/m28-control-mapping.json');cc={x['control_id'] for x in J('governance/controls/control-catalog.json')['controls']};fm=set(J('governance/mappings/framework-mapping.json')['controls']);assert all(x['control_id'] in cc and x['control_id'] in fm for x in cm['controls'])
