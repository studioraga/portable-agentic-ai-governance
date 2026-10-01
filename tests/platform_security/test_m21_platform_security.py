import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.platform_security.firmware import make_descriptor,evaluate_update,verify_descriptor,sign_descriptor
from portable_ai_governance.platform_security.dice import derive_cdi_demo
from portable_ai_governance.platform_security.evaluation import evaluate_profiles
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair

def load(n): return json.loads((ROOT/'tests/fixtures/m21'/n).read_text())
def test_firmware_positive_and_rollback(tmp_path):
    payload=ROOT/'tests/fixtures/m21/firmware.bin';priv=tmp_path/'priv.pem';pub=tmp_path/'pub.pem';generate_ed25519_keypair(priv,pub);desc=tmp_path/'d.json';d=make_descriptor(payload,'fw','3.0.0',3,desc);sig=tmp_path/'d.sig';sign_descriptor(desc,priv,sig);assert verify_descriptor(desc,payload,pub,sig);assert evaluate_update('2.0.0',2,d)['decision']=='ACCEPT';assert evaluate_update('3.0.0',3,d)['decision']=='REJECT'
def test_tamper_fails(tmp_path):
    p=tmp_path/'fw.bin';p.write_bytes(b'a');priv=tmp_path/'p';pub=tmp_path/'q';generate_ed25519_keypair(priv,pub);desc=tmp_path/'d';make_descriptor(p,'fw','2',2,desc);sig=tmp_path/'s';sign_descriptor(desc,priv,sig);p.write_bytes(b'b');assert not verify_descriptor(desc,p,pub,sig)
def test_dice_deterministic():
    h='aa'*32;a=derive_cdi_demo('11'*32,h,'cfg');b=derive_cdi_demo('11'*32,h,'cfg');assert a==b and len(a)==64
def test_profile_evaluation_simulated():
    r=evaluate_profiles(load('node1-profile.json'),load('node2-profile.json'),json.loads((ROOT/'governance/platform/m21/platform-security-policy.json').read_text()));assert r['validation_mode']=='SIMULATED' and r['failed']==0 and not r['production_ready']
def test_systemd_hardening_contract():
    t=(ROOT/'examples/m21/systemd/pag-platform-demo.service').read_text();required=json.loads((ROOT/'governance/platform/m21/platform-security-policy.json').read_text())['service_required_directives'];assert all(x in t for x in required)
def test_mac_templates_exist():
    assert 'deny /dev/mem' in (ROOT/'examples/m21/apparmor/usr.bin.pag-platform-demo').read_text();assert 'init_daemon_domain' in (ROOT/'examples/m21/selinux/pag_platform_demo.te').read_text()
def test_threat_model_has_platform_threats():
    t=json.loads((ROOT/'governance/platform/m21/threat-model.json').read_text());assert len(t['threats'])>=10 and any('BMC' in x['threat'] for x in t['threats'])
def test_boundaries_non_destructive():
    b=json.loads((ROOT/'governance/platform/m21/platform-security-policy.json').read_text())['boundaries'];assert b['no_fuse_burn'] and b['no_firmware_flash'] and b['no_uefi_key_enrollment'] and not b['cra_conformity_claim']
