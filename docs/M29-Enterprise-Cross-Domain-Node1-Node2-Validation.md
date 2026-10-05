# M29 — Enterprise Cross-Domain Node1/Node2 Validation

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one independently verifiable cross-domain package. It does not create certification or conformity claims.

## Core distinction

M29 produces two independent outcomes:

1. **evidence integrity** — all nested signed inputs, source digests, control mappings and Node1/Node2 boundaries verify;
2. **production readiness** — every production gate is satisfied with real evidence.

Evidence integrity may pass while production readiness remains false.

## Current expected pre-production verdict

The present lab profile must remain fail-closed because:

- `CISSP-D3-001` and `CISSP-D3-002` remain partial while M21 reports `secure-boot-enabled=false` and `mac-enforcing=false`;
- M27 local validation uses simulated penetration-test evidence, so `production_pentest_evidence_present=false`;
- M28 local validation uses simulated authority-bound organizational records, so `production_evidence_present=false`;
- Node2 independent verification is not true until the physical verifier run occurs.

M29 reconciles `CISSP-D8-002` to `EVIDENCED` because the M27 `ENT-SDLC-001/002` controls directly implement the M22 Secure-SDLC objective. This is a cross-domain reconciliation record, not a rewrite of M27 history.

## Production gates

M30 may consume an M29 package only after all of these are true:

- all 23 M22 enterprise requirements are evidenced;
- M21 platform production readiness is true;
- M27 real authorized penetration-test evidence is present;
- M28 real organizational/personnel/physical/BCP evidence is present;
- Node2 independently verifies the package;
- verifier material contains no private key.

## Evidence topology

`var/m29-material/inputs/m21` through `inputs/m28` contain verifier-only copies of the signed prerequisite evidence. M29 signs an input digest index, requirement matrix, source manifest and cross-domain summary on Node1. Node2 re-runs each nested milestone verifier against the same source tree.
