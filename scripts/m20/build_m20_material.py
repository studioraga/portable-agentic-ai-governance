#!/usr/bin/env python3
import argparse,json,os,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_final_freeze.common import write_json,sha256_file
from portable_ai_governance.cra_final_freeze.evaluation import evaluate
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair,sign_blob
from portable_ai_governance.action_agent.common import secure_tree
ap=argparse.ArgumentParser();ap.add_argument('--m19-summary',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();os.umask(0o077);out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True,mode=0o700)
for rel,name in [('governance/cra/m20/final-freeze-policy.json','final-freeze-policy.json'),('governance/cra/m20/enterprise-deployment-plan.json','enterprise-deployment-plan.json'),('governance/cra/m20/m20-control-mapping.json','m20-control-mapping.json')]:shutil.copy2(ROOT/rel,out/name);os.chmod(out/name,0o600)
pol=json.loads((out/'final-freeze-policy.json').read_text());summary=evaluate(ROOT,a.m19_summary,pol);write_json(out/'release-freeze-summary.json',summary);write_json(out/'release-source-fingerprints.json',summary['source_fingerprints']);generate_ed25519_keypair(out/'signing-private.pem',out/'signing-public.pem')
names=['final-freeze-policy.json','enterprise-deployment-plan.json','m20-control-mapping.json','release-freeze-summary.json','release-source-fingerprints.json','signing-public.pem']
man={'version':'0.20.0','milestone':'M20','purpose':'Enterprise One-Shot Deployment / Final Production Freeze','artifacts':{n:sha256_file(out/n) for n in names},'boundaries':pol['boundaries']}
write_json(out/'m20-final-freeze-manifest.json',man);sign_blob(out/'m20-final-freeze-manifest.json',out/'signing-private.pem',out/'m20-final-freeze-manifest.json.sig');secure_tree(out);print(f"PASS: M20 material generated at {out}");print(f"PASS: freeze_state={summary['freeze_state']} final_freeze_ready={summary['final_freeze_ready']}")
