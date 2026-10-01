from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.cra_reporting.engine import build_fixture_packs
from .intake import triage_report
from .disclosure import advisory,maintainer_coordination
from .notify import notifications_from_reporting_packs

def build_fixture_material(repo_root):
 root=Path(repo_root);policy=json.loads((root/'governance/cra/m15/psirt-cvd-policy.json').read_text())
 reports=[json.loads(p.read_text()) for p in sorted((root/'tests/fixtures/m15/reports').glob('*.json'))]
 fixes=[json.loads(p.read_text()) for p in sorted((root/'tests/fixtures/m15/fixes').glob('*.json'))]
 cases=[triage_report(r,policy) for r in reports]
 coords=[maintainer_coordination(r) for r in reports]
 advisories=[advisory(f,policy) for f in fixes]
 _,packs,_=build_fixture_packs(root)
 notifications=notifications_from_reporting_packs(packs)
 public_contract={'manufacturer_contact':{'name':'Studio Raga','email':'security@example.invalid','website':'https://example.invalid'},'vulnerability_single_point_of_contact':policy['psirt']['single_point_of_contact'],'cvd_policy_ready':True,'public_disclosure_performed':False}
 return policy,cases,coords,advisories,notifications,public_contract
