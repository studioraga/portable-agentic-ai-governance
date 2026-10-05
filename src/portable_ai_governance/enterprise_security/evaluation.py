from __future__ import annotations

def evaluate_catalog(domains: dict, requirements: dict, mapping: dict, gaps: dict, control_catalog: dict) -> dict:
    checks=[]
    domain_numbers={d.get("domain") for d in domains.get("domains",[])}
    checks.append(("eight-cissp-domains",domain_numbers==set(range(1,9))))
    reqs=requirements.get("requirements",[])
    req_ids=[r.get("id") for r in reqs]
    checks.append(("unique-requirement-ids",len(req_ids)==len(set(req_ids)) and bool(req_ids)))
    known_controls={c.get("control_id") for c in control_catalog.get("controls",[])}
    referenced={c for r in reqs for c in r.get("existing_controls",[])}
    checks.append(("existing-control-references",referenced <= known_controls))
    mapped={m.get("requirement_id") for m in mapping.get("mappings",[])}
    checks.append(("all-requirements-mapped",mapped==set(req_ids)))
    open_gap_reqs={g.get("requirement_id") for g in gaps.get("open_gaps",[])}
    expected_gap_reqs={r.get("id") for r in reqs if r.get("state") != "EVIDENCED"}
    checks.append(("gap-register-complete",open_gap_reqs==expected_gap_reqs))
    boundaries=mapping.get("claim_boundaries",{})
    for key in ("cissp_certification_claim","iso_iec_27001_certification_claim","iso_iec_42001_certification_claim","cra_conformity_claim"):
        checks.append((f"claim-boundary:{key}",boundaries.get(key) is False))
    by_state={}
    for r in reqs: by_state[r.get("state","UNKNOWN")]=by_state.get(r.get("state","UNKNOWN"),0)+1
    return {"ok":all(v for _,v in checks),"checks":checks,"requirement_count":len(reqs),"state_counts":by_state,"open_gap_count":len(open_gap_reqs)}
