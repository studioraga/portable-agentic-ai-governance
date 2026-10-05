import json
from pathlib import Path
import pytest
from portable_ai_governance.network_security.policy import validate_network_policy, authorize_flow, NetworkPolicyError
from portable_ai_governance.network_security.egress import authorize_egress, validate_egress_policy
from portable_ai_governance.network_security.detection import detect
from portable_ai_governance.network_security.firewall import render_nftables
from portable_ai_governance.network_security.evaluation import evaluate_m25_policy
ROOT=Path(__file__).resolve().parents[2]
def J(p): return json.loads((ROOT/p).read_text())
def test_policy_validates(): assert validate_network_policy(J('governance/enterprise/m25/network-zone-policy.json'))
def test_default_deny_unknown_flow():
 r=authorize_flow({'source_zone':'verifier','destination_zone':'control-plane','protocol':'tcp','port':22},J('governance/enterprise/m25/network-zone-policy.json'));assert r['decision']=='deny'
def test_mtls_identity_required():
 p=J('governance/enterprise/m25/network-zone-policy.json');r=authorize_flow({'source_zone':'verifier','destination_zone':'control-plane','protocol':'tcp','port':8443,'mtls_verified':False,'encrypted':True,'workload_identity':'spiffe://pag/node2-verifier'},p);assert r['decision']=='deny'
def test_wrong_workload_identity_denied():
 p=J('governance/enterprise/m25/network-zone-policy.json');r=authorize_flow({'source_zone':'verifier','destination_zone':'control-plane','protocol':'tcp','port':8443,'mtls_verified':True,'encrypted':True,'workload_identity':'spiffe://pag/evil'},p);assert r['decision']=='deny'
def test_approved_mtls_flow_allowed():
 p=J('governance/enterprise/m25/network-zone-policy.json');r=authorize_flow({'source_zone':'verifier','destination_zone':'control-plane','protocol':'tcp','port':8443,'mtls_verified':True,'encrypted':True,'workload_identity':'spiffe://pag/node2-verifier'},p);assert r['decision']=='allow'
def test_unauthorized_egress_denied():
 r=authorize_egress({'source_zone':'control-plane','protocol':'tcp','port':443,'destination':'random.example'},J('governance/enterprise/m25/egress-policy.json'));assert r['decision']=='deny'
def test_approved_egress_allowed():
 r=authorize_egress({'source_zone':'control-plane','protocol':'tcp','port':443,'destination':'approved-security-update-endpoint'},J('governance/enterprise/m25/egress-policy.json'));assert r['decision']=='allow'
def test_detection_alerts():
 a=detect([{'event_id':'1','event_type':'denied_flow'},{'event_id':'2','event_type':'unauthorized_egress'}],J('governance/enterprise/m25/network-detection-policy.json'));assert len(a)==2
def test_firewall_render_is_default_drop():
 s=render_nftables(J('governance/enterprise/m25/network-zone-policy.json'));assert 'policy drop' in s and 'dport { 8443 } accept' in s
def test_missing_zone_rejected():
 p=J('governance/enterprise/m25/network-zone-policy.json');p['flows'][0]['source_zone']='missing'
 with pytest.raises(NetworkPolicyError): validate_network_policy(p)
def test_m25_control_set():
 ev=evaluate_m25_policy(J('governance/enterprise/m25/network-zone-policy.json'),J('governance/enterprise/m25/egress-policy.json'),J('governance/enterprise/m25/network-detection-policy.json'),J('governance/controls/control-catalog.json'));assert ev['ok'] and ev['control_count']==7
