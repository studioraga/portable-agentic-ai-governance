from .evidence import validate_attestation
def validate_physical(policy, records, as_of, production=False):
 present={r.get("control") for r in records}
 required={x for xs in policy["required_control_families"].values() for x in xs}
 missing=required-present
 if missing: raise ValueError("missing physical/environmental evidence: "+",".join(sorted(missing)))
 for r in records: validate_attestation(r,authority_roles={"facilities_owner","physical_security_owner","safety_owner"},max_age_days=policy["attestation_max_age_days"],as_of=as_of,production=production,production_type=policy["production_evidence_type"])
 return True
