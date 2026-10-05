# M24 — Asset Security, Data Protection & Cryptographic/Data Lifecycle

## Purpose

M24 extends the frozen M23 identity/MFA/PAM release with deterministic enterprise controls for CISSP Domain 2 Asset Security and adds bounded cryptographic-lifecycle evidence that advances, but does not close, CISSP Domain 3.

M24 closes the three M22 Domain-2 requirements by implementation evidence rather than by editing the historical M22 gap register:

- `CISSP-D2-001` — inventory, ownership, criticality and classification;
- `CISSP-D2-002` — handling, retention, legal hold, disposal and sanitization;
- `CISSP-D2-003` — DLP and controlled export.

M24 adds cryptographic inventory/rotation/exportability policy through `ENT-CRYPTO-001/002`, but intentionally leaves `CISSP-D3-001` and `CISSP-D3-002` PARTIAL because M21 secure-boot, MAC and hardware-root evidence remains authoritative.

## Security invariants

1. Unregistered assets are denied by default.
2. Sensitive assets require owner, custodian, classification and data-owner metadata.
3. Retention expiry never overrides an active legal hold.
4. Sanitization must use an approved method and emit evidence metadata.
5. Sensitive exports are destination-scoped, encrypted where required, independently approved where required and content-inspected before release.
6. Export audit records decision metadata, not the payload itself.
7. Active cryptographic keys are inventoried with owner, purpose, algorithm, rotation deadline and exportability state.
8. Validation keys are not production keys.
9. M24 does not override M21 platform/hardware-root gaps.
10. Node1 remains authority/producer; Node2 remains verifier-only.

## Control set

| Control | Purpose |
|---|---|
| `ENT-ASSET-001` | authoritative deny-unregistered asset inventory |
| `ENT-ASSET-002` | owner/custodian/criticality/classification metadata |
| `ENT-DATA-001` | classification-driven data handling |
| `ENT-DATA-002` | retention and legal-hold enforcement |
| `ENT-DATA-003` | evidence-backed sanitization/disposal |
| `ENT-DLP-001` | default-deny controlled export |
| `ENT-DLP-002` | deterministic sensitive-content inspection |
| `ENT-DLP-003` | independent approval and metadata-only audit |
| `ENT-CRYPTO-001` | cryptographic key inventory and approved algorithms |
| `ENT-CRYPTO-002` | rotation/revocation/exportability lifecycle |

## Architecture

```text
asset/data request
      |
      v
registered asset? -------- no ------> DENY
      |
     yes
      v
classification + owner + custodian
      |
      +--> retention/legal hold -----> retain/sanitize decision
      |
      +--> export request
              |
              +--> destination allowlist
              +--> encryption required?
              +--> independent approval required?
              +--> deterministic DLP scan
              |
              v
          ALLOW / DENY
              |
              v
      signed M24 evidence manifest
              |
        verifier-only package
              |
              v
            Node2
```

## Historical lineage

M24 is additive. M0–M23 source and milestone semantics remain immutable. `m24-gap-closure.json` records how M24 addresses M22 Domain-2 observations without altering `governance/enterprise/m22/gap-register.json`.

## Claim boundary

M24 evidence is an engineering-control/evidence result. It does not assert CISSP certification, ISO/IEC 27001 certification, ISO/IEC 42001 certification, or CRA conformity.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
