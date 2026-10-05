from __future__ import annotations
from datetime import datetime,timezone

def _dt(s): return datetime.fromisoformat(s.replace("Z","+00:00"))
def validate_attestation(record, *, authority_roles, max_age_days, as_of, production=False, production_type=None):
 required=("record_id","subject","authority","authority_role","observed_at","expires_at","evidence_type","evidence_reference","production_evidence")
 missing=[x for x in required if x not in record or record[x] is None or record[x]==""]
 if missing: raise ValueError("missing attestation fields: "+",".join(missing))
 if record["authority_role"] not in authority_roles: raise ValueError("untrusted authority role")
 now=_dt(as_of); observed=_dt(record["observed_at"]); expires=_dt(record["expires_at"])
 if observed>now or expires<now: raise ValueError("attestation not current")
 if (now-observed).days>max_age_days: raise ValueError("attestation stale")
 if record.get("subject")==record.get("authority") and record.get("requires_independence",True): raise ValueError("self-attestation denied")
 if production:
  if not record.get("production_evidence"): raise ValueError("simulated evidence denied in production")
  if production_type and record.get("evidence_type")!=production_type: raise ValueError("wrong production evidence type")
 return True
