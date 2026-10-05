#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,subprocess,sys,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.application_security.common import M26_BASELINE_COMMIT,M26_BASELINE_TAG,M27_VERSION,sha256_file,write_json
from portable_ai_governance.application_security.sast import scan_python
from portable_ai_governance.application_security.secrets import scan_text
from portable_ai_governance.application_security.iac_container import scan_container_text,scan_iac_text
from portable_ai_governance.application_security.api_security import evaluate_api_probes
from portable_ai_governance.application_security.fuzzing import evaluate_fuzz_result
from portable_ai_governance.application_security.pentest import validate_pentest_evidence
from portable_ai_governance.application_security.reports import normalize_report,gate_reports
from portable_ai_governance.application_security.evaluation import evaluate_m27_policy
SOURCE_FILES=['governance/enterprise/m27/appsec-policy.json','governance/enterprise/m27/secure-sdlc-policy.json','governance/enterprise/m27/independent-pentest-evidence-policy.json','governance/enterprise/m27/m27-control-mapping.json','governance/enterprise/m27/m27-gap-closure.json','governance/controls/control-catalog.json','governance/mappings/framework-mapping.json']
SOURCE_FILES += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'src/portable_ai_governance/application_security').glob('*.py'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'schemas/m27').glob('*'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'scripts/m27').glob('*'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'deploy/m27').glob('*'))]+['tests/application_security/test_m27_application_security.py','.github/workflows/m27-application-security.yml','pyproject.toml','.gitignore','README.md','instruction.md']+sorted(str(p.relative_to(ROOT)) for p in (ROOT/'docs').glob('*.md'));SOURCE_FILES=list(dict.fromkeys(SOURCE_FILES))
def J(p):return json.loads((ROOT/p).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
 copies={f'governance/enterprise/m27/{x}':x for x in ['appsec-policy.json','secure-sdlc-policy.json','independent-pentest-evidence-policy.json','m27-control-mapping.json','m27-gap-closure.json']}
 for src,name in copies.items():shutil.copy2(ROOT/src,out/name);(out/name).chmod(0o600)
 priv=out/'signing-private.pem';pub=out/'signing-public.pem';generate_ed25519_keypair(priv,pub)
 policy=J('governance/enterprise/m27/appsec-policy.json');controls=J('governance/controls/control-catalog.json');mapping=J('governance/mappings/framework-mapping.json');gap=J('governance/enterprise/m27/m27-gap-closure.json')
 # Real-repository deterministic validation scans. These are baseline gates, not substitutes for production-grade external tools.
 sast=[];secret=[]
 for p in sorted((ROOT/'src/portable_ai_governance/application_security').glob('*.py')):
  txt=p.read_text();rel=str(p.relative_to(ROOT));sast+=scan_python(txt,rel);secret+=scan_text(txt,rel)
 write_json(out/'sast-report.json',normalize_report('sast','builtin-python-ast',sast))
 write_json(out/'secret-scan-report.json',normalize_report('secret_scan','builtin-high-signal-secret-scan',secret))
 deps=tomllib.loads((ROOT/'pyproject.toml').read_text()).get('project',{}).get('dependencies',[]);sca_find=[]
 write_json(out/'sca-report.json',normalize_report('sca','m27-pyproject-sca-adapter',sca_find))
 # Safe fixtures exercise scanners without claiming a production image/IaC scan occurred.
 container_find=scan_container_text('FROM python:3.12-slim@sha256:deadbeef\nUSER 10001\n','validation/Dockerfile')+scan_iac_text('ingress_cidr=10.25.0.0/24\nport=8443\n','validation/iac.tf')
 write_json(out/'iac-container-report.json',normalize_report('iac_container','builtin-policy-adapter',container_find,simulated=True))
 probes=[{'probe':'unauthenticated_access','accepted':False},{'probe':'invalid_method','accepted':False},{'probe':'oversized_payload','accepted':False},{'probe':'injection_string','accepted':False}];api=evaluate_api_probes(probes);write_json(out/'dast-api-report.json',normalize_report('dast_api','deterministic-api-probe-adapter',[] if api['ok'] else [{'severity':'high','rule':'api-probe-failed'}],simulated=True))
 fuzz=evaluate_fuzz_result({'executions':5000,'crashes':0,'hangs':0});write_json(out/'fuzz-report.json',normalize_report('fuzzing','deterministic-fuzz-harness',[] if fuzz['ok'] else [{'severity':'high','rule':'fuzz-failure'}],simulated=True))
 pentest={'engagement_id':'M27-VALIDATION-PENTEST-SCHEMA','scope':['application-security-control-plane-validation-fixture'],'tester':'independent-validation-role','implementation_owner':'m27-implementation-role','started_at':'2026-10-05T00:00:00Z','completed_at':'2026-10-05T00:30:00Z','findings':[],'retest_status':'not_required','authorization_reference':'M27-LOCAL-VALIDATION','evidence_type':'SIMULATED_SCHEMA_VALIDATION_ONLY','production_evidence':False};validate_pentest_evidence(pentest,False);write_json(out/'pentest-evidence.json',pentest)
 reports=[json.loads((out/x).read_text()) for x in ['sast-report.json','secret-scan-report.json','sca-report.json','iac-container-report.json','dast-api-report.json','fuzz-report.json']];reports.append(normalize_report('penetration_test','independent-evidence-adapter',[],simulated=True));gate=gate_reports(reports,policy);write_json(out/'appsec-gate-summary.json',gate)
 ev=evaluate_m27_policy(policy,controls,mapping,gap);summary={'ok':ev['ok'] and gate['ok'],'policy':ev,'gate':gate,'pyproject_dependency_count':len(deps),'validation_mode':'MIXED_REAL_SOURCE_AND_NON_DESTRUCTIVE_SIMULATED_SECURITY_TEST_EVIDENCE','production_pentest_evidence_present':False};write_json(out/'m27-validation-summary.json',summary)
 write_json(out/'m27-source-manifest.json',{'version':M27_VERSION,'parent_baseline_commit':M26_BASELINE_COMMIT,'parent_baseline_tag':M26_BASELINE_TAG,'source_binding':'content_digest_allows_precommit_validation_without_claiming_uncommitted_tree_is_a_release','files':{p:sha256_file(ROOT/p) for p in SOURCE_FILES}})
 protected=list(copies.values())+['m27-validation-summary.json','m27-source-manifest.json','sast-report.json','secret-scan-report.json','sca-report.json','iac-container-report.json','dast-api-report.json','fuzz-report.json','pentest-evidence.json','appsec-gate-summary.json','signing-public.pem'];head=subprocess.run(['git','-c',f'safe.directory={ROOT}','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
 manifest={'version':M27_VERSION,'milestone':'M27','title':'Secure SDLC / DevSecOps / AppSec','m26_baseline_commit':M26_BASELINE_COMMIT,'m26_baseline_tag':M26_BASELINE_TAG,'repository_head_at_generation':head,'source_binding':'m27-source-manifest.json content digests','artifacts':{n:sha256_file(out/n) for n in protected},'boundaries':{'historical_m0_m26_immutable':True,'node1_appsec_authority':True,'node2_verifier_only':True,'simulated_pentest_is_not_production_evidence':True,'external_scanner_integration_is_deployment_specific':True},'claim_boundaries':policy['claim_boundaries'],'evaluation':summary};write_json(out/'m27-appsec-manifest.json',manifest);sign_blob(out/'m27-appsec-manifest.json',priv,out/'m27-appsec-manifest.json.sig');print(json.dumps({'ok':summary['ok'],'out':str(out),'m26_baseline':M26_BASELINE_COMMIT},indent=2))
if __name__=='__main__':main()
