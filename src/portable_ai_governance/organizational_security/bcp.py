from .evidence import validate_attestation
def validate_bcp(policy, plan, exercise, as_of, production=False):
 for field in ("bia_reference","continuity_plan_reference","crisis_roles","communications_plan","dependency_register"):
  if not plan.get(field): raise ValueError("missing BCP field: "+field)
 validate_attestation(exercise,authority_roles={"continuity_owner","executive_sponsor","risk_owner"},max_age_days=policy["exercise_max_age_days"],as_of=as_of,production=production,production_type=policy["production_evidence_type"])
 if not exercise.get("lessons_learned"): raise ValueError("BCP exercise lessons learned required")
 return True
