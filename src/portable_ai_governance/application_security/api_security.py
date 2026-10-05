from __future__ import annotations
def evaluate_api_probes(probes):
 required={"unauthenticated_access","invalid_method","oversized_payload","injection_string"};seen={p.get("probe") for p in probes};fail=[]
 for p in probes:
  if p.get("probe") in required and p.get("accepted") is True: fail.append(p.get("probe"))
 return {"ok":required<=seen and not fail,"missing":sorted(required-seen),"failed":fail}
