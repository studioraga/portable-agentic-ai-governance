# M21 Validation

M21 validation combines focused source tests, deterministic fixture validation, CI/static contracts, LIVE two-node evidence, negative tests, and the full M0–M21 regression chain.

## Focused tests

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/platform_security
```

These tests cover firmware signing/rollback behavior, tamper rejection, DICE determinism, simulated profile evaluation, systemd/MAC reference contracts, safety boundaries, and v0.21.1 source/baseline binding.

## Local deterministic validation

```bash
./scripts/m21/validate_m21_local.sh
```

This builds signed M21 material from fixture profiles, verifies it with the private key present, removes the private key, and verifies the same material as verifier-only evidence.

Expected validation mode: `SIMULATED`.

## CI/static gate

```bash
./scripts/m21/ci_validate.sh
```

This runs focused tests, Python compilation, JSON parsing, systemd unit verification when available, and AppArmor syntax validation when the parser is available.

## Full regression

```bash
set -o pipefail
./scripts/m21/validate_m21_regression.sh 2>&1 | tee /tmp/m21-regression.log
```

Expected terminal result:

```text
PASS: full M0-M21 regression + M20/M21 acceptance complete
```

## LIVE Node1/Node2 acceptance

LIVE acceptance additionally requires:

1. Node2 LIVE profile capture;
2. Node1 LIVE profile capture;
3. Node1 signed M21 material generation;
4. Node1 authority verification;
5. verifier-only package generation;
6. Node2 independent verification;
7. tamper rejection;
8. private-key injection rejection;
9. source/tag parity checks.

## v0.21.1 source-binding correction

v0.21.1 separates milestone ancestry from evidence-generation source identity.

The signed manifest records:

```text
m20_baseline_commit = 8b800814e576bcb08e12dc47c1039c5251c79d46
m20_baseline_tag    = m20-cra-enterprise-final-freeze-v0.20.0
m21_source_commit   = e83ebf03c6d1ce2f4076ab8e3dae8282e4aeb880
```

The verifier checks:

- Git HEAD readability;
- M20 baseline equality;
- M20 baseline commit existence;
- M20 baseline ancestry;
- M20 tag resolution to the exact baseline commit;
- M21 source commit existence;
- M21 source ancestry/lineage.

This permits later descendant source revisions to verify historical M21 evidence without incorrectly requiring the current HEAD to equal the M20 baseline.

## Current preserved LIVE result

| Check | Result |
|---|---|
| Validation mode | `LIVE` |
| Required checks passed | 15 |
| Required checks open | 2 |
| Production ready | `false` |
| CRA conformity claim | `false` |

Open required checks:

- `secure-boot-enabled`;
- `mac-enforcing`.

The verifier may still return `ok=true` for evidence integrity while the platform validation summary truthfully reports `production_ready=false`.


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

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
