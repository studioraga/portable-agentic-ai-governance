# M16 — CRA Secure Update & Product Lifecycle

M16 implements the secure-update and product-lifecycle evidence layer on the frozen M11-M15 baselines. It covers support-period determination and end-date evidence, update retention, signed update metadata/payload verification, anti-rollback decisions, free/security-only update policy checks, latest-version/free-access policy evidence, EOL notification preparation, and corrective-action readiness.

## Boundaries
M16 does not update the host OS, flash firmware, distribute updates over the network, or make a CRA conformity claim. Node1 is the release/signing authority; Node2 verifies signed M16 material and synthetic update acceptance evidence without holding private keys.

## CRA alignment
The implementation targets Article 13(8)-(10), Article 13(19), Article 13(21), Article 14(2)(c)(iii), Annex I Part I(2)(c), and Annex I Part II(2), (7) and (8), using the M11 requirement IDs already assigned to M16.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.

## M18 integration

M18 assembles the CRA Article 31 / Annex VII technical-documentation evidence file from the evidence produced by M3-M17. This document remains an input/reference to that assembly; M18 does not retroactively change this milestone's scope. The M18 technical file is explicitly a draft evidence package: it makes no CRA conformity claim, does not perform a conformity assessment, does not authorize CE marking, and does not fabricate the EU Declaration of Conformity. Product-specific production/security test evidence that remains incomplete is carried forward to M19 as an explicit readiness gap.

## M19 integration — CRA Node1/Node2 Production Validation

M19 consumes this milestone's evidence as part of the heterogeneous Node1/Node2 production-validation chain. The M19 signed validation bundle binds the frozen CRA baselines, checks source/version/platform parity and verifier-key isolation, and supplies a production-evidence candidate for Annex I Part II(3) regular product-security testing. M19 does not rewrite this milestone's historical claims, perform conformity assessment, or make a CRA conformity claim.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.
