#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.network_security.common import M24_BASELINE_COMMIT,M24_BASELINE_TAG,M25_VERSION,sha256_file,write_json
from portable_ai_governance.network_security.policy import authorize_flow
from portable_ai_governance.network_security.egress import authorize_egress
from portable_ai_governance.network_security.detection import detect
from portable_ai_governance.network_security.firewall import render_nftables
from portable_ai_governance.network_security.evaluation import evaluate_m25_policy
SOURCE_FILES=['governance/enterprise/m25/network-zone-policy.json','governance/enterprise/m25/egress-policy.json','governance/enterprise/m25/network-detection-policy.json','governance/enterprise/m25/m25-control-mapping.json','governance/enterprise/m25/m25-gap-closure.json','governance/controls/control-catalog.json','governance/mappings/framework-mapping.json','src/portable_ai_governance/network_security/__init__.py','src/portable_ai_governance/network_security/common.py','src/portable_ai_governance/network_security/policy.py','src/portable_ai_governance/network_security/egress.py','src/portable_ai_governance/network_security/detection.py','src/portable_ai_governance/network_security/firewall.py','src/portable_ai_governance/network_security/evaluation.py','src/portable_ai_governance/network_security/runtime.py','scripts/m25/build_m25_material.py','scripts/m25/validate_m25_node.py','scripts/m25/validate_m25_local.sh','scripts/m25/validate_m25_regression.sh','scripts/m25/verify_node1.sh','scripts/m25/verify_node2.sh','scripts/m25/ci_validate.sh','deploy/m25/deploy_node.sh','deploy/m25/one_shot_node1.sh','deploy/m25/one_shot_node2.sh','deploy/m25/package_verifier_material.sh','tests/network_security/test_m25_network_security.py','.github/workflows/m25-network-security.yml','pyproject.toml','.gitignore']
SOURCE_FILES += ['README.md','instruction.md']+sorted(str(p.relative_to(ROOT)) for p in (ROOT/'docs').glob('*.md'));SOURCE_FILES=list(dict.fromkeys(SOURCE_FILES))
def J(p):return json.loads((ROOT/p).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
 copies={'governance/enterprise/m25/network-zone-policy.json':'network-zone-policy.json','governance/enterprise/m25/egress-policy.json':'egress-policy.json','governance/enterprise/m25/network-detection-policy.json':'network-detection-policy.json','governance/enterprise/m25/m25-control-mapping.json':'m25-control-mapping.json','governance/enterprise/m25/m25-gap-closure.json':'m25-gap-closure.json'}
 for src,name in copies.items():shutil.copy2(ROOT/src,out/name);(out/name).chmod(0o600)
 priv=out/'signing-private.pem';pub=out/'signing-public.pem';generate_ed25519_keypair(priv,pub)
 net=J('governance/enterprise/m25/network-zone-policy.json');eg=J('governance/enterprise/m25/egress-policy.json');de=J('governance/enterprise/m25/network-detection-policy.json');controls=J('governance/controls/control-catalog.json')
 positive=authorize_flow({'source_zone':'verifier','destination_zone':'control-plane','protocol':'tcp','port':8443,'mtls_verified':True,'encrypted':True,'workload_identity':'spiffe://pag/node2-verifier'},net)
 negative=authorize_flow({'source_zone':'verifier','destination_zone':'control-plane','protocol':'tcp','port':22,'mtls_verified':False,'encrypted':False,'workload_identity':'spiffe://pag/node2-verifier'},net)
 neg_eg=authorize_egress({'source_zone':'control-plane','protocol':'tcp','port':443,'destination':'unapproved-internet-host'},eg)
 alerts=detect([{'event_id':'m25-deny-1','event_type':'denied_flow'},{'event_id':'m25-egress-1','event_type':'unauthorized_egress'}],de)
 write_json(out/'positive-flow-decision.json',positive);write_json(out/'negative-flow-decision.json',negative);write_json(out/'negative-egress-decision.json',neg_eg);(out/'generated-nftables.conf').write_text(render_nftables(net))
 ev=evaluate_m25_policy(net,eg,de,controls)
 summary={'ok':ev['ok'] and positive['decision']=='allow' and negative['decision']=='deny' and neg_eg['decision']=='deny' and len(alerts)==2,'policy':ev,'positive_tests':{'approved_mtls_flow':positive['decision']=='allow','generated_firewall':True},'negative_tests':{'unapproved_flow_denied':negative['decision']=='deny','unauthorized_egress_denied':neg_eg['decision']=='deny','detection_events':len(alerts)==2},'apply_mode':'validation-does-not-modify-host-firewall'};write_json(out/'m25-validation-summary.json',summary)
 write_json(out/'m25-source-manifest.json',{'version':M25_VERSION,'parent_baseline_commit':M24_BASELINE_COMMIT,'parent_baseline_tag':M24_BASELINE_TAG,'source_binding':'content_digest_allows_precommit_validation_without_claiming_uncommitted_tree_is_a_release','files':{p:sha256_file(ROOT/p) for p in SOURCE_FILES}})
 protected=list(copies.values())+['m25-validation-summary.json','m25-source-manifest.json','signing-public.pem','generated-nftables.conf','positive-flow-decision.json','negative-flow-decision.json','negative-egress-decision.json'];head=subprocess.run(['git','-c',f'safe.directory={ROOT}','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
 manifest={'version':M25_VERSION,'milestone':'M25','title':'Zero-Trust Network & Micro-segmentation','m24_baseline_commit':M24_BASELINE_COMMIT,'m24_baseline_tag':M24_BASELINE_TAG,'repository_head_at_generation':head,'source_binding':'m25-source-manifest.json content digests','artifacts':{n:sha256_file(out/n) for n in protected},'boundaries':{'historical_m0_m24_immutable':True,'node1_network_policy_authority':True,'node2_verifier_only':True,'validation_does_not_apply_firewall':True,'physical_switch_vlan_evidence_is_environment_specific':True},'claim_boundaries':net['claim_boundaries'],'evaluation':summary};write_json(out/'m25-network-manifest.json',manifest);sign_blob(out/'m25-network-manifest.json',priv,out/'m25-network-manifest.json.sig');print(json.dumps({'ok':summary['ok'],'out':str(out),'m24_baseline':M24_BASELINE_COMMIT},indent=2))
if __name__=='__main__':main()
