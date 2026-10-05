from __future__ import annotations
def assess_production_readiness(matrix,m21_summary,m27_summary,m28_summary,node2_verified=False,no_private_keys=True):
 gates={
 'all_23_requirements_evidenced':matrix['all_requirements_evidenced'],
 'm21_platform_production_ready':m21_summary.get('production_ready') is True,
 'm27_real_authorized_pentest_evidence':m27_summary.get('production_pentest_evidence_present') is True,
 'm28_real_authority_bound_organizational_evidence':m28_summary.get('production_evidence_present') is True,
 'node2_independent_verification':node2_verified is True,
 'no_private_keys_in_verifier_package':no_private_keys is True}
 return {'production_ready':all(gates.values()),'gates':gates,'blocking_gates':[k for k,v in gates.items() if not v]}
