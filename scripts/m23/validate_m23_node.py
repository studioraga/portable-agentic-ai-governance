#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.enterprise_identity.runtime import evaluate_m23_material
from portable_ai_governance.enterprise_identity.federation import FederationPolicy,verify_oidc_assertion
from portable_ai_governance.enterprise_identity.pam import ReplayLedger,authorize_jit

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--material',required=True);ap.add_argument('--repo-root',default=str(ROOT));a=ap.parse_args();m=Path(a.material)
    result=evaluate_m23_material(m,a.repo_root); summary=json.loads((m/'m23-validation-summary.json').read_text());now=int(summary['validation_time'])
    policy=json.loads((m/'enterprise-identity-policy.json').read_text()); fp=FederationPolicy('https://id.example.invalid/realms/enterprise','portable-ai-governance',policy['mfa']['required_acr'],policy['mfa']['max_auth_age_sec'])
    try:
        p=verify_oidc_assertion((m/'positive-federated-assertion.jwt').read_text().strip(),m/'federation-public.pem',fp,now=now,privileged=True)
        authorize_jit((m/'positive-jit-grant.jwt').read_text().strip(),m/'pam-public.pem',ReplayLedger(),subject=p.subject,action='service.restart',resource='prod/api',now=now+10)
        bg=authorize_jit((m/'positive-break-glass-grant.jwt').read_text().strip(),m/'pam-public.pem',ReplayLedger(),subject=p.subject,action='emergency.shell',resource='prod/node1',now=now+10)
        result['checks'] += [('positive-federated-assertion',p.phishing_resistant),('positive-break-glass',bg.emergency and bg.post_review_required)]
    except Exception as exc:
        result['checks'].append(('positive-vector-validation',False));result.setdefault('errors',[]).append(str(exc))
    result['ok']=all(v for _,v in result['checks'])
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['ok'] else 2)
if __name__=='__main__':main()
