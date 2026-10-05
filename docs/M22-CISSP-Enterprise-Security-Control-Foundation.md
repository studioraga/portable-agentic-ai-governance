# M22 — CISSP / Enterprise Security Control Foundation

## Objective

M22 extends Portable Agentic AI Governance from the frozen M21.1 platform-security baseline into an enterprise security evidence and control-plane foundation. It does **not** claim that an organization, product, or repository is “CISSP certified” or “CISSP compliant.” CISSP is a professional certification knowledge framework. M22 uses its eight domains as an enterprise-security coverage taxonomy and maps that taxonomy to NIST CSF 2.0, ISO/IEC 27001:2022 themes, the existing CRA program, and ISO/IEC 42001:2023 themes.

## Immutable parent baseline

- parent commit: `ea952069938a6435ccb298f5424bab158197ce05`
- released M21 tag: `m21-embedded-linux-platform-security-v0.21.1`
- M0–M21 behavior and evidence contracts remain historical and immutable.

## Security invariant

`Reasoning != Authority`

M22 preserves deterministic authorization, evidence-before-claim, fail-closed validation, and independent Node2 verification.

## Authoritative M22 artifacts

- `governance/enterprise/m22/cissp-domain-catalog.json`
- `governance/enterprise/m22/enterprise-security-requirements.json`
- `governance/enterprise/m22/enterprise-control-mapping.json`
- `governance/enterprise/m22/gap-register.json`
- `governance/enterprise/m22/evidence-policy.json`

M22 contains 23 enterprise-security alignment requirements spanning all eight CISSP domains. `EVIDENCED` means the current repository has a deterministic control/evidence basis; `PARTIAL` means material capability exists but the enterprise requirement is not complete; `GAP` means a later milestone must implement the missing control.

## Framework boundaries

M22 records high-level references only and does not reproduce proprietary ISO standard text. The ISO references are alignment aids and are not certification decisions.

Authoritative public references:

- ISC2 CISSP Exam Outline: https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline
- NIST CSF 2.0: https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
- ISO/IEC 27001:2022 overview: https://www.iso.org/standard/27001
- ISO/IEC 42001:2023 overview: https://www.iso.org/standard/81230.html
- CRA authoritative source already recorded in `governance/cra/cra-requirements.json`.

## Claim boundaries

The following are always false in M22 material:

- `cissp_certification_claim`
- `iso_iec_27001_certification_claim`
- `iso_iec_42001_certification_claim`
- `cra_conformity_claim`

M22 is an evidence/control-foundation milestone, not a conformity-assessment authority.

## Node roles

### Node1

Node1 is the M22 evidence producer and signing authority. It may hold the ephemeral/private M22 signing key and creates the signed control-foundation material.

### Node2

Node2 is verifier-only. It must receive only the public key and verifier material. Any private signing key in the Node2 package is a hard failure.

## Source binding before commit

M22 supports validation while `.git` still contains uncommitted M22 changes. `m22-source-manifest.json` hashes the M22 source/governance files and separately binds the work to the immutable M21.1 parent commit. This avoids claiming that an uncommitted tree is a release while still making Node1/Node2 verification deterministic.

After validation, commit the exact validated tree, rebuild M22 material, rerun verification, and tag the release.

## Planned closure milestones

- M23 — enterprise identity, MFA and PAM
- M24 — asset/data protection, lifecycle and DLP
- M25 — zero-trust network and segmentation
- M26 — SOC, vulnerability, IR, immutable backup and DR
- M27 — secure SDLC / DevSecOps / application security
- M28 — personnel, physical, BCP and organizational controls
- M29 — enterprise Node1/Node2 cross-domain validation
- M30 — enterprise-security production freeze
