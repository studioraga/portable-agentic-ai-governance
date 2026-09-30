import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_foundation.catalog import load_requirement_matrix,validate_requirement_matrix,coverage_summary
from portable_ai_governance.cra_foundation.runtime import evaluate_m11_material

def test_cra_matrix_is_authoritative_and_traceable():
 m=load_requirement_matrix(ROOT/'governance/cra/cra-requirements.json');assert len(m['requirements'])>=70;assert validate_requirement_matrix(m,ROOT)==[]
 refs={r['legal_reference'] for r in m['requirements']};assert 'Article 14(2)(a)' in refs;assert 'Annex I Part II(1)' in refs;assert 'Annex VII(2)(b)' in refs

def test_every_gap_or_partial_has_future_cra_control():
 m=load_requirement_matrix(ROOT/'governance/cra/cra-requirements.json');assert all(r['proposed_control_id'] for r in m['requirements'] if r['current_status'] in {'gap','partial'})

def test_m11_does_not_claim_conformity():
 s=coverage_summary(load_requirement_matrix(ROOT/'governance/cra/cra-requirements.json'));assert s['cra_conformity_claim'] is False

def test_node2_role_is_verifier_only():
 r=json.loads((ROOT/'governance/cra/node-role-profile.json').read_text());assert r['nodes']['node2']['role']=='cra_independent_verifier';assert r['boundaries']['private_signing_keys_node1_only'] is True

def test_signed_material_round_trip(tmp_path):
 out=tmp_path/'m11';env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'src')
 subprocess.run([sys.executable,str(ROOT/'scripts/m11/build_m11_material.py'),'--out',str(out)],check=True,env=env)
 assert evaluate_m11_material(out,ROOT)['ok']
 (out/'signing-private.pem').unlink();assert evaluate_m11_material(out,ROOT)['ok']

def test_tampered_matrix_fails_verification(tmp_path):
 out=tmp_path/'m11';env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'src');subprocess.run([sys.executable,str(ROOT/'scripts/m11/build_m11_material.py'),'--out',str(out)],check=True,env=env)
 p=out/'cra-requirements.json';p.write_text(p.read_text()+"\n")
 assert not evaluate_m11_material(out,ROOT)['ok']
