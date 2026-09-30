from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import sha256_file
from .journal import verify_awareness_journal

def evaluate_m13_material(root,repo_root=None):
    root=Path(root);required=['incident-classification-policy.json','m13-control-mapping.json','incident-assessments.json','cra-cases.json','deadline-states.json','awareness-journal.json','m13-clock-manifest.json','m13-clock-manifest.json.sig','signing-public.pem'];checks=[]
    for f in required:checks.append((f'present:{f}',(root/f).is_file()))
    if not all(ok for _,ok in checks):return {'ok':False,'checks':checks,'errors':['missing material']}
    manifest=json.loads((root/'m13-clock-manifest.json').read_text());checks.append(('manifest-signature',verify_blob(root/'m13-clock-manifest.json',root/'signing-public.pem',root/'m13-clock-manifest.json.sig')))
    for n,d in manifest.get('artifacts',{}).items():checks.append((f'digest:{n}',sha256_file(root/n)==d))
    b=manifest.get('boundaries',{});checks.extend([('classification-and-clock-only',b.get('classification_and_clock_only') is True),('no-enisa-submission',b.get('enisa_submission') is False),('no-report-generation',b.get('report_generation') is False),('no-conformity-claim',b.get('cra_conformity_claim') is False),('node2-verifier-only',b.get('node2_verifier_only') is True)])
    assessments=json.loads((root/'incident-assessments.json').read_text());decisions={x['decision'] for x in assessments};checks.append(('incident-decision-coverage',{'SEVERE_INCIDENT','NOT_SEVERE','INCOMPLETE'}<=decisions))
    cases=json.loads((root/'cra-cases.json').read_text());checks.append(('aev-and-incident-cases',{'AEV','SEVERE_INCIDENT'}<={x['case_type'] for x in cases}))
    rows=json.loads((root/'awareness-journal.json').read_text());checks.append(('awareness-journal-chain',verify_awareness_journal(rows)))
    checks.append(('awareness-unique',len({r['case_id'] for r in rows})==len(rows)))
    if repo_root:
      rr=Path(repo_root);checks.append(('m11-baseline-bound',manifest.get('m11_requirement_matrix_sha256')==sha256_file(rr/'governance/cra/cra-requirements.json')));checks.append(('m12-controls-bound',manifest.get('m12_control_mapping_sha256')==sha256_file(rr/'governance/cra/m12/m12-control-mapping.json')))
    errors=[]
    for c in cases:
      if c.get('enisa_submission_performed') is not False or c.get('cra_conformity_claim') is not False:errors.append(f"{c.get('case_id')}: forbidden M13 side effect")
    return {'ok':all(ok for _,ok in checks) and not errors,'checks':checks,'errors':errors,'incident_counts':{d:sum(x['decision']==d for x in assessments) for d in sorted(decisions)},'case_counts':{t:sum(x['case_type']==t for x in cases) for t in sorted({x['case_type'] for x in cases})}}
