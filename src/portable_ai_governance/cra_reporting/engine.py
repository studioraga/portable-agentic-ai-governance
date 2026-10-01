from __future__ import annotations
import json
from pathlib import Path
from portable_ai_governance.cra_incident_clock.engine import evaluate_fixture_set
from .pack import build_pack
from .readiness import readiness

def build_fixture_packs(repo_root,now='2026-10-03T12:00:00Z'):
    root=Path(repo_root)
    policy=json.loads((root/'governance/cra/m14/reporting-policy.json').read_text())
    manufacturer=json.loads((root/'tests/fixtures/m14/organization/manufacturer.json').read_text())
    product=json.loads((root/'tests/fixtures/m14/products/product-node2.json').read_text())
    _,_,cases,_,_=evaluate_fixture_set(root,now)
    packs=[]
    for case in cases:
        enr_name='aev.json' if case['case_type']=='AEV' else f"{case['source_id']}.json"
        enrichment=json.loads((root/'tests/fixtures/m14/enrichment'/enr_name).read_text())
        packs.append(build_pack(case,manufacturer,product,enrichment,policy))
    return policy,packs,[readiness(p) for p in packs]
