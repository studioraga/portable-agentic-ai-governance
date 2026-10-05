from .evidence import validate_attestation
def validate_governance(policy, charter, attestation, as_of, production=False):
 roles=set(charter.get("roles",{})); missing=set(policy["required_roles"])-roles
 if missing: raise ValueError("missing governance roles: "+",".join(sorted(missing)))
 if policy.get("require_raci") and not charter.get("raci"): raise ValueError("RACI required")
 if policy.get("require_policy_owner") and not charter.get("policy_owners"): raise ValueError("policy ownership required")
 validate_attestation(attestation,authority_roles={"executive_sponsor","security_owner","risk_owner"},max_age_days=policy["review_days"],as_of=as_of,production=production,production_type="AUTHORIZED_GOVERNANCE_RECORD")
 return True
