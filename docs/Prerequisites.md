# Common Prerequisites

This document covers repository-wide prerequisites. Milestone-specific additions live in `Prerequisites-M*.md` files.

## Supported baseline

The code requires Python 3.10 or newer and is designed for Linux-oriented validation/deployment workflows. Individual milestones may have additional host/platform assumptions.

## Core commands

Common workflows expect:

- `python3`;
- Python `venv` / `pip` for development environments;
- `git`;
- `bash`;
- `openssl`;
- `sha256sum`;
- `tar` / `gzip`;
- standard GNU user/file utilities.

Install only what is appropriate for the host and selected milestone. Do not mutate a production or evidence host merely to make an optional capability appear available.

## Python development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Direct source execution may use:

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

## Git and release prerequisites

Operators should be able to:

- fetch and verify tags;
- inspect exact commit identity;
- keep the working tree clean for release evidence generation;
- create release archives with `git archive`;
- keep runtime evidence and secrets outside tracked source.

## Runtime storage

Generated evidence is runtime state, not source. Keep it in protected local directories such as `var/` or milestone-specific installation paths under the user's configuration directory.

Private signing material must use restrictive permissions and must never be copied into verifier-only bundles.

## Node roles

The repository uses two logical roles:

- **Node1 / release authority** — may generate and sign evidence;
- **Node2 / independent verifier** — verifies signed evidence without the private release signing key.

A milestone may be exercised locally with fixtures, but LIVE cross-node acceptance should preserve this authority split.

## Current M21 additions

See [`Prerequisites-M21.md`](Prerequisites-M21.md) for platform-audit tools such as `mokutil`, `fwupdmgr`, `systemd-analyze`, MAC utilities, and `tpm2-tools`.


## M22 enterprise-security extension

M22 extends the frozen M21.1 baseline with the authoritative CISSP-domain / enterprise-security control foundation. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`, `docs/Prerequisites-M22.md`, `docs/Deployment-M22.md`, and `docs/Validation-M22.md`. M0–M21 historical behavior remains unchanged; M22 records alignment and gaps and does not assert CISSP, ISO/IEC 27001, ISO/IEC 42001, or CRA certification/conformity.


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

M23 extends the frozen M22 enterprise-security foundation with enterprise human identity, OIDC federation evidence, strong MFA context, phishing-resistant privileged authentication, expiring entitlement review, signed single-use JIT privilege grants, dual-approved break-glass access, segregation of duties, and independent Node1/Node2 verification. The authoritative M23 documents are `docs/M23-Enterprise-Identity-MFA-PAM.md`, `docs/Prerequisites-M23.md`, `docs/Deployment-M23.md`, and `docs/Validation-M23.md`. Historical M0-M22 behavior and evidence remain immutable.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.
