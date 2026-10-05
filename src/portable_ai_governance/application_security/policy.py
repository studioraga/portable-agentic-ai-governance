from __future__ import annotations
class AppSecPolicyError(ValueError): pass
REQUIRED_CATEGORIES={"sast","dast_api","secret_scan","sca","iac_container","fuzzing","penetration_test"}
def validate_policy(policy):
 cats=set(policy.get("required_security_tests",[]))
 if not REQUIRED_CATEGORIES<=cats: raise AppSecPolicyError("missing mandatory AppSec test category")
 if policy.get("release_gate",{}).get("default")!="DENY": raise AppSecPolicyError("release gate must default deny")
 if policy.get("release_gate",{}).get("block_severities")!=["critical","high"]: raise AppSecPolicyError("critical/high must block")
 if not policy.get("penetration_test",{}).get("independent_tester_required"): raise AppSecPolicyError("independent tester required")
 if not policy.get("penetration_test",{}).get("retest_required_for_blocking_findings"): raise AppSecPolicyError("retest required")
 return True
