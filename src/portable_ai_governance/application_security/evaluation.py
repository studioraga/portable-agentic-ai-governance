from __future__ import annotations
from .policy import validate_policy
REQ={"ENT-APPSEC-001","ENT-APPSEC-002","ENT-APPSEC-003","ENT-APPSEC-004","ENT-APPSEC-005","ENT-APPSEC-006","ENT-APPSEC-007","ENT-SDLC-001","ENT-SDLC-002"}
def evaluate_m27_policy(policy,controls,mapping,gap):
 checks=[];ids={x.get("control_id") for x in controls.get("controls",[])};mapped=set(mapping.get("controls",{}));checks.append(("m27-controls-present",REQ<=ids));checks.append(("framework-mapped",REQ<=mapped))
 try: validate_policy(policy);checks.append(("appsec-policy",True))
 except Exception: checks.append(("appsec-policy",False))
 checks.append(("gap-closure",gap.get("requirement_id")=="CISSP-D6-002" and gap.get("m27_state")=="EVIDENCED" and gap.get("closure_scope")=="CONTROL_PLANE_CAPABILITY"))
 for k in ("cissp_certification_claim","iso_iec_27001_certification_claim","iso_iec_42001_certification_claim","cra_conformity_claim","production_pentest_completed_claim"):
  checks.append((f"claim-boundary:{k}",policy.get("claim_boundaries",{}).get(k) is False))
 return {"ok":all(v for _,v in checks),"checks":checks,"control_count":len(REQ)}
