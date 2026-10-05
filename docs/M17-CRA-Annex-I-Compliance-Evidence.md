# M17 — CRA Annex-I Compliance Evidence

M17 aggregates traceable evidence for all 22 Annex I Part I and Part II requirement rows in the authoritative M11 matrix. It does **not** change the M11 legal/status baseline, perform a CRA conformity assessment, generate the Annex VII technical file, or claim CRA conformity.

## Outputs

- `annex-i-evidence-index.json`: requirement-to-evidence traceability with SHA-256 digests.
- `annex-i-coverage-summary.json`: Part I/Part II coverage and `EVIDENCED`/`PARTIAL`/`GAP` counts.
- `annex-i-evidence-gaps.json`: explicit unresolved evidence gaps.
- `m17-annex-i-manifest.json` + signature: digest-bound M11–M16 baseline and M17 artifacts.

## Boundaries

M17 is evidence aggregation only. M18 builds the Annex VII technical file; M19 performs production Node1/Node2 validation; conformity assessment remains a separate manufacturer/notified-body process as applicable.

## Known gaps intentionally retained

- Annex I Part I(2)(b): product-specific secure-by-default/reset evidence.
- Annex I Part I(2)(i): product-specific evidence that negative impact on other devices/networks is minimised.
- Annex I Part I(2)(m): product-specific secure/permanent data-removal and transfer evidence.
- Annex I Part II(3): existing tests are evidence, but M19 production validation is still required for regular product-security test/review closure.

## M18 integration

M18 assembles the CRA Article 31 / Annex VII technical-documentation evidence file from the evidence produced by M3-M17. This document remains an input/reference to that assembly; M18 does not retroactively change this milestone's scope. The M18 technical file is explicitly a draft evidence package: it makes no CRA conformity claim, does not perform a conformity assessment, does not authorize CE marking, and does not fabricate the EU Declaration of Conformity. Product-specific production/security test evidence that remains incomplete is carried forward to M19 as an explicit readiness gap.

## M19 integration — CRA Node1/Node2 Production Validation

M19 consumes this milestone's evidence as part of the heterogeneous Node1/Node2 production-validation chain. The M19 signed validation bundle binds the frozen CRA baselines, checks source/version/platform parity and verifier-key isolation, and supplies a production-evidence candidate for Annex I Part II(3) regular product-security testing. M19 does not rewrite this milestone's historical claims, perform conformity assessment, or make a CRA conformity claim.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

This historical milestone document remains authoritative for its original scope. M23 does not rewrite it; M23 consumes the existing identity/authorization/evidence lineage and adds enterprise federation, strong/phishing-resistant MFA policy, entitlement review, PAM/JIT, break-glass, segregation-of-duties, and Node1/Node2 verifier evidence. See `docs/M23-Enterprise-Identity-MFA-PAM.md`.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.
