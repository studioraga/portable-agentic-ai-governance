from pathlib import Path
import json, shutil
from portable_ai_governance.cra_secure_update.lifecycle import support_period_end,lifecycle_record,eol_notification
from portable_ai_governance.cra_secure_update.update import retention_until,make_update_descriptor,evaluate_install
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def test_minimum_support_period():
 assert support_period_end('2027-12-11',8)=='2035-12-11'
 assert support_period_end('2027-12-11',3)=='2030-12-11'

def test_eol_notification():
 r=lifecycle_record({'product_id':'p','market_placement_date':'2027-12-11','expected_use_years':3,'support_period_factors':['short_expected_use']},'2031-01-15')
 n=eol_notification(r);assert r['support_status']=='END_OF_SUPPORT' and n['prepared'] and not n['sent']

def test_retention_rule():
 assert retention_until('2028-01-15','2035-12-11')=='2038-01-15'

def setup_update(tmp_path):
 payload=tmp_path/'u.bin';payload.write_bytes(b'good update')
 priv=tmp_path/'priv.pem';pub=tmp_path/'pub.pem';generate_ed25519_keypair(priv,pub)
 d=make_update_descriptor('p','1.0.0','1.0.1',payload,'2028-01-15','2035-12-11')
 desc=tmp_path/'u.json';desc.write_text(json.dumps(d,sort_keys=True));sig=tmp_path/'u.sig';sign_blob(desc,priv,sig)
 return d,payload,desc,sig,pub

def test_valid_signed_update(tmp_path):
 d,payload,desc,sig,pub=setup_update(tmp_path);r=evaluate_install(d,payload,desc,sig,pub,'1.0.0','2028-02-01','2035-12-11');assert r['decision']=='ACCEPT'

def test_tampered_payload_rejected(tmp_path):
 d,payload,desc,sig,pub=setup_update(tmp_path);payload.write_bytes(b'tampered');r=evaluate_install(d,payload,desc,sig,pub,'1.0.0','2028-02-01','2035-12-11');assert r['decision']=='REJECT' and 'payload_digest_mismatch' in r['reasons']

def test_tampered_descriptor_rejected(tmp_path):
 d,payload,desc,sig,pub=setup_update(tmp_path);desc.write_text(desc.read_text()+' ');r=evaluate_install(d,payload,desc,sig,pub,'1.0.0','2028-02-01','2035-12-11');assert r['decision']=='REJECT' and 'descriptor_signature_invalid' in r['reasons']

def test_rollback_rejected(tmp_path):
 d,payload,desc,sig,pub=setup_update(tmp_path);r=evaluate_install(d,payload,desc,sig,pub,'1.0.1','2028-02-01','2035-12-11');assert r['decision']=='REJECT' and 'rollback_or_non_monotonic_version' in r['reasons']

def test_outside_support_rejected(tmp_path):
 d,payload,desc,sig,pub=setup_update(tmp_path);r=evaluate_install(d,payload,desc,sig,pub,'1.0.0','2036-01-01','2035-12-11');assert r['decision']=='REJECT' and 'outside_support_period' in r['reasons']

def test_nonfree_update_rejected(tmp_path):
 d,payload,desc,sig,pub=setup_update(tmp_path);d['free_of_charge']=False;desc.write_text(json.dumps(d,sort_keys=True)); # resign to prove policy rejection, not sig failure
 # cannot sign without private retained by helper; create another key pair
 priv=tmp_path/'p2.pem';pub2=tmp_path/'p2pub.pem';generate_ed25519_keypair(priv,pub2);sign_blob(desc,priv,sig)
 r=evaluate_install(d,payload,desc,sig,pub2,'1.0.0','2028-02-01','2035-12-11');assert r['decision']=='REJECT' and 'security_update_not_free' in r['reasons']
