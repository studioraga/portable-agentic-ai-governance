#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'src';sys.path.insert(0,str(SRC))
from portable_ai_governance.security_ops.common import write_json,sha256_file
from portable_ai_governance.action_agent.common import secure_tree
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob

def main():
 os.umask(0o077);ap=argparse.ArgumentParser();ap.add_argument('--m8-material',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();m8=Path(a.m8_material).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700);m8m=m8/'action-agent-manifest.json'
 if not m8m.is_file():raise SystemExit(f'FAIL: M8 manifest missing: {m8m}')
 policy={'version':'0.9.0','purpose':'Deterministic security operations','siem':{'append_only':True,'hash_chain':True,'max_event_age_seconds':86400,'max_future_skew_seconds':60},'incident_severities':['high','critical'],'containment_rules':[{'rule_id':'SECOPS-CRITICAL-MODEL','event_types':['model.integrity.failure','model.policy.violation'],'severities':['critical'],'action':'model.quarantine.local'},{'rule_id':'SECOPS-CRITICAL-WORKLOAD','event_types':['workload.identity.compromise','agent.policy.bypass'],'severities':['critical'],'action':'workload.isolate.local'}],'recovery':{'operator_required':True,'operators':['HUMAN-RESPONDER-001'],'authorization_ttl_max_seconds':900,'all_checks_required':True,'evidence_verification_required':True,'automatic_recovery':False},'evidence_max_bytes':10485760,'llm_decision_authority':False,'external_side_effects':False,'m8_external_action_boundary':True}
 write_json(out/'security-ops-policy.json',policy)
 generate_ed25519_keypair(out/'recovery-signing-private.pem',out/'recovery-signing-public.pem')
 manifest={'version':'0.9.0','m8_manifest_sha256':sha256_file(m8m),'artifacts':{'security-ops-policy.json':sha256_file(out/'security-ops-policy.json'),'recovery-signing-public.pem':sha256_file(out/'recovery-signing-public.pem')},'capabilities':['siem','incidents','automated-local-containment','recovery','evidence-preservation'],'boundary':{'llm_decision_authority':False,'external_side_effects':False,'m8_external_action_boundary':True}}
 write_json(out/'security-ops-manifest.json',manifest);generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem');sign_blob(out/'security-ops-manifest.json',out/'signing-private.pem',out/'security-ops-manifest.json.sig');secure_tree(out)
 print(f'PASS: M9 security-operations material generated at {out}')
 print('PASS: deterministic SIEM -> incident -> local containment -> recovery/evidence policy')
if __name__=='__main__':main()
