from .evidence import validate_attestation
def validate_personnel(policy, records, as_of, production=False):
 kinds={r.get("kind") for r in records}
 missing=set(policy["required_evidence"])-kinds
 if missing: raise ValueError("missing personnel evidence: "+",".join(sorted(missing)))
 for r in records:
  days=policy["privileged_training_max_age_days"] if r.get("kind")=="role_specific_training" else policy["awareness_max_age_days"]
  validate_attestation(r,authority_roles={"hr_owner","security_owner","training_owner"},max_age_days=days,as_of=as_of,production=production,production_type=policy["production_evidence_type"])
 for r in records:
  if r.get("kind")=="joiner_mover_leaver_review" and r.get("terminated") and r.get("revocation_hours",999)>policy["termination_access_revocation_sla_hours"]: raise ValueError("termination revocation SLA missed")
 return True
