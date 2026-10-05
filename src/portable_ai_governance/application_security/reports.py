from __future__ import annotations
class SecurityGateError(ValueError): pass
VALID={"critical","high","medium","low","info"}
def normalize_report(category,tool,findings,simulated=False):
 out=[]
 for i,f in enumerate(findings):
  sev=str(f.get("severity","info")).lower()
  if sev not in VALID: raise SecurityGateError("invalid severity")
  out.append({**f,"severity":sev,"finding_id":f.get("finding_id",f"{category}-{i+1}"),"tool":f.get("tool",tool)})
 return {"category":category,"tool":tool,"simulated":bool(simulated),"findings":out}
def gate_reports(reports,policy):
 req=set(policy["required_security_tests"]);got={r["category"] for r in reports};missing=sorted(req-got)
 blocking=[]
 block=set(policy["release_gate"]["block_severities"])
 for r in reports:
  for f in r.get("findings",[]):
   if f.get("severity") in block and f.get("status","open") not in {"accepted","fixed","false_positive"}: blocking.append(f)
 return {"ok":not missing and not blocking,"missing_categories":missing,"blocking_findings":blocking,"categories":sorted(got)}
