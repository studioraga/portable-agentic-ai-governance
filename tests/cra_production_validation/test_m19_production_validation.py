from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_production_validation.evaluation import evaluate_profiles
from portable_ai_governance.cra_production_validation.runtime import evaluate_m19_material

def load(p): return json.loads((ROOT/p).read_text())

def test_fixture_profiles_are_simulated_and_pass_contracts():
    n1=load('tests/fixtures/m19/node1-runtime-profile.json');n2=load('tests/fixtures/m19/node2-runtime-profile.json');p=load('governance/cra/m19/production-validation-policy.json');cross,s=evaluate_profiles(n1,n2,p);assert cross['all_required_pass'];assert s['validation_mode']=='SIMULATED';assert s['production_validation_complete'] is False

def test_live_mode_can_become_production_ready():
    n1=load('tests/fixtures/m19/node1-runtime-profile.json');n2=load('tests/fixtures/m19/node2-runtime-profile.json');n1['capture_mode']=n2['capture_mode']='LIVE';p=load('governance/cra/m19/production-validation-policy.json');_,s=evaluate_profiles(n1,n2,p);assert s['production_validation_complete'] is True;assert s['m17_gap_closure_candidates'][0]['state']=='EVIDENCE_READY_FOR_M17_REVIEW'

def test_source_mismatch_fails():
    n1=load('tests/fixtures/m19/node1-runtime-profile.json');n2=load('tests/fixtures/m19/node2-runtime-profile.json');n2['source_fingerprints']={'x':'bad'};p=load('governance/cra/m19/production-validation-policy.json');c,_=evaluate_profiles(n1,n2,p);assert not c['all_required_pass']

def test_node2_private_key_fails():
    n1=load('tests/fixtures/m19/node1-runtime-profile.json');n2=load('tests/fixtures/m19/node2-runtime-profile.json');n2['private_signing_key_present']=True;p=load('governance/cra/m19/production-validation-policy.json');c,_=evaluate_profiles(n1,n2,p);assert not c['all_required_pass']

def test_unresolved_m17_gaps_not_auto_closed():
    n1=load('tests/fixtures/m19/node1-runtime-profile.json');n2=load('tests/fixtures/m19/node2-runtime-profile.json');p=load('governance/cra/m19/production-validation-policy.json');_,s=evaluate_profiles(n1,n2,p);states={x['requirement_id']:x['state'] for x in s['m17_gap_closure_candidates']};assert states['CRA-REQ-046']=='NOT_CLOSED';assert states['CRA-REQ-053']=='NOT_CLOSED';assert states['CRA-REQ-057']=='NOT_CLOSED'

def test_builder_and_verifier(tmp_path):
    out=tmp_path/'m';subprocess.run([sys.executable,str(ROOT/'scripts/m19/build_m19_material.py'),'--out',str(out),'--node1-profile',str(ROOT/'tests/fixtures/m19/node1-runtime-profile.json'),'--node2-profile',str(ROOT/'tests/fixtures/m19/node2-runtime-profile.json')],check=True);r=evaluate_m19_material(out,ROOT);assert r['ok'];assert r['validation_mode']=='SIMULATED';assert not r['production_validation_complete']

def test_tamper_rejected(tmp_path):
    out=tmp_path/'m'
    subprocess.run([sys.executable,str(ROOT/'scripts/m19/build_m19_material.py'),'--out',str(out),'--node1-profile',str(ROOT/'tests/fixtures/m19/node1-runtime-profile.json'),'--node2-profile',str(ROOT/'tests/fixtures/m19/node2-runtime-profile.json')],check=True,stdout=subprocess.DEVNULL)
    p=out/'cross-node-validation.json'
    p.write_text(p.read_text()+"\n")
    assert not evaluate_m19_material(out,ROOT)['ok']

def test_m11_target_is_m19_for_regular_tests():
    d=load('governance/cra/cra-requirements.json');rows=d if isinstance(d,list) else d['requirements'];r=next(x for x in rows if x['requirement_id']=='CRA-REQ-060');assert r['target_milestone']=='M19';assert r['legal_reference']=='Annex I Part II(3)'
