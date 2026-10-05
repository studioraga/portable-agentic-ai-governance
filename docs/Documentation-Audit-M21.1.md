# Documentation Audit — M21 v0.21.1

This audit records the documentation refactor performed against the M21 v0.21.1 repository at commit `e83ebf03c6d1ce2f4076ab8e3dae8282e4aeb880`.

## Review basis

The review used:

- the complete Git history present in the source archive;
- current Python/source modules under `src/portable_ai_governance/`;
- milestone scripts under `scripts/m*/`;
- deployment helpers under `deploy/m*/`;
- governance JSON and schemas;
- all tracked Markdown files;
- preserved M21 runtime evidence in the supplied source snapshot for factual release-state checks.

## Commit-by-commit documentation evolution

| Commit | Milestone | Documentation effect |
|---|---|---|
| `4083a0d` | M0–M1 freeze | established the original common README/architecture/deployment/prerequisite/validation baseline |
| `5022e21` | M2 | added security-control-plane docs and introduced `instruction.md` |
| `3773977` | M3 | added supply-chain deployment/validation and release-chain guidance |
| `a0aad3e` | M4 | extended common docs with AI-security boundaries |
| `685eddd` | M5 | extended common docs with compliance/risk automation boundaries |
| `50c31ce` | M6 | documented bounded read-only Evidence Analyst |
| `d3c9d8b` | M7 | documented mediated typed-tool execution |
| `17c266e` | M8 | documented independently approved side effects |
| `6c9a439` | M9 | documented deterministic SecOps and recovery controls |
| `d4ce10a` | M10 | documented supervised multi-agent governance |
| `4741e0a` | M11 | introduced CRA product-security foundation and requirement matrix |
| `d970290` | M12 | added vulnerability/exploitation intelligence; began broad cross-document integration appendages |
| `cb17976` | M13 | added incident classification/statutory clock and appended integration notes to older docs |
| `cdfb06c` | M14 | added reporting/SRP evidence-pack preparation and further historical-document appendages |
| `003e0cf` | M15 | added PSIRT/CVD/user-notification preparation |
| `b7a8f22` | M16 | added secure-update/lifecycle evidence |
| `ad52cbf` | M17 | added Annex-I evidence mapping |
| `9ea7e14` | M18 | added Annex-VII technical-file evidence assembly |
| `367225c` | M19 | added Node1/Node2 production-validation evidence |
| `8b80081` | M20 | added enterprise final-freeze/deployment evidence |
| `558ad17` | M21 v0.21.0 | added embedded Linux/platform-security validation |
| `e83ebf0` | M21 v0.21.1 | corrected M20 baseline vs M21 source binding documentation/behavior |

## Primary findings

### 1. The README had become a changelog plus operator manual

The pre-refactor README still declared v0.10.0 as current while appending M11–M21 integration sections later in the same file. It mixed release status, milestone history, prerequisites, command sequences, architecture, and feature detail.

**Resolution:** README is now orientation-only: project purpose, Node roles, current release, validated state, short reproduction path, safety boundaries, and documentation map.

### 2. `instruction.md` had stale current-state language

The file still described M7 as the current implementation candidate even though the repository had advanced through M21 v0.21.1.

**Resolution:** it is now an execution workflow covering clone → tag selection → prerequisites → environment → validation → current milestone → evidence inspection → negative tests → commit → release/tag.

### 3. Common architecture docs accumulated milestone chronology

`Architecture.md` contained obsolete status statements such as M2 being “NEXT” followed by many later integration appendages.

**Resolution:** architecture now describes durable layers and invariants, while milestone chronology lives in `Milestones.md` and feature-specific documents.

### 4. Common validation docs were M0/M1-centric

`Validation.md` began as an M0/M1 procedure and accumulated later integration notes.

**Resolution:** it now defines a reusable six-layer validation architecture: Environment, Configuration, Tools/static contracts, Local deterministic validation, Cross-node/milestone acceptance, and Signed release/evidence package.

### 5. Deployment documentation overstated “one-shot” maturity

Milestone-specific one-shot helpers exist, but no universal repository-level `deploy.sh --node1/--node2/...` interface exists yet.

**Resolution:** `oneshot-deployment.md` documents the progressive contract and maps it to the current milestone-specific implementation without pretending the universal interface exists.

### 6. M21 deployment text referred to uncommitted source

`Deployment-M21.md` still described applying the same “uncommitted M21 source” to both nodes.

**Resolution:** the M21 document now uses the committed/tagged v0.21.1 workflow and exact source identity.

### 7. Historical milestone docs lacked a clear authority hierarchy

Older docs often contained later integration paragraphs, making it unclear whether they were current operator instructions.

**Resolution:** historical milestone-specific documents now carry a `Documentation role` note that points readers back to the canonical current documents.

## Canonical documentation hierarchy after refactor

```text
README.md
  Human orientation

instruction.md
  Authoritative developer/operator execution

docs/README.md
  Documentation map and authority order

docs/Architecture.md
  Durable architecture and trust boundaries

docs/Validation.md
  Durable validation/evidence model

docs/Prerequisites.md
  Common prerequisites

docs/oneshot-deployment.md
  Progressive deployment contract

docs/Milestones.md
  Release/milestone evolution

docs/M*-*.md
  Milestone-specific historical/feature design

docs/Prerequisites-M*.md
  Milestone-specific prerequisites

docs/Deployment-M*.md
  Milestone-specific deployment

docs/Validation-M*.md
  Milestone-specific validation
```

## M21 v0.21.1 facts preserved by the rewrite

- current tag: `m21-embedded-linux-platform-security-v0.21.1`;
- current source commit: `e83ebf03c6d1ce2f4076ab8e3dae8282e4aeb880`;
- M20 baseline commit: `8b800814e576bcb08e12dc47c1039c5251c79d46`;
- M20 baseline tag: `m20-cra-enterprise-final-freeze-v0.20.0`;
- Node1 remains signing/release authority;
- Node2 remains independent verifier and must not receive private signing material;
- preserved LIVE result: 15 required checks PASS, 2 open;
- open checks: `secure-boot-enabled`, `mac-enforcing`;
- `production_ready=false`;
- `cra_conformity_claim=false`;
- M21 remains non-destructive with respect to fuses, UEFI enrollment, firmware flashing, and MAC installation.

## Validation of this documentation refactor

The refactor was checked for:

- `git diff --check` cleanliness;
- trailing whitespace and final newlines;
- local Markdown-link resolution;
- removal of stale current-release statements from canonical docs;
- consistency with source paths and M21 v0.21.1 manifest/evidence fields.


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

This historical milestone document remains authoritative for its original scope. M23 does not rewrite it; M23 consumes the existing identity/authorization/evidence lineage and adds enterprise federation, strong/phishing-resistant MFA policy, entitlement review, PAM/JIT, break-glass, segregation-of-duties, and Node1/Node2 verifier evidence. See `docs/M23-Enterprise-Identity-MFA-PAM.md`.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.
