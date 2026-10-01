# M16 — CRA Secure Update & Product Lifecycle

M16 implements the secure-update and product-lifecycle evidence layer on the frozen M11-M15 baselines. It covers support-period determination and end-date evidence, update retention, signed update metadata/payload verification, anti-rollback decisions, free/security-only update policy checks, latest-version/free-access policy evidence, EOL notification preparation, and corrective-action readiness.

## Boundaries
M16 does not update the host OS, flash firmware, distribute updates over the network, or make a CRA conformity claim. Node1 is the release/signing authority; Node2 verifies signed M16 material and synthetic update acceptance evidence without holding private keys.

## CRA alignment
The implementation targets Article 13(8)-(10), Article 13(19), Article 13(21), Article 14(2)(c)(iii), Annex I Part I(2)(c), and Annex I Part II(2), (7) and (8), using the M11 requirement IDs already assigned to M16.
