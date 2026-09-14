# Milestone 3 — Supply Chain

Milestone 3 adds deterministic software and AI supply-chain controls on top of the frozen M2 security control plane.

## Trust rule

Agents may recommend artifacts, models, prompts or tools. They never decide whether an artifact is trusted. Promotion and startup rely on deterministic digest, signature, provenance and vulnerability-policy verification.

## Implemented controls

- CycloneDX 1.7 software SBOM generation.
- CycloneDX 1.7 AI/ML BOM generation for locked models.
- SHA-256 locks for models, containers, prompts and tools.
- Container references must be digest pinned using `@sha256:`.
- In-toto Statement v1 with SLSA provenance v1 predicate.
- Ed25519 signing and public-key verification using OpenSSL.
- Vulnerability policy with report freshness, scanner identity, severity and unknown-severity gates.
- Production verifier nodes receive only the public signing key; the private release key remains with the release authority.
- Optional OSV-scanner normalization with `scripts/m3/import_osv_report.py`.
- M3 supply-chain verification can be injected into the M2 production security profile by setting `PAG_SUPPLY_CHAIN_REQUIRED=1`.

## Production boundary

The deterministic implementation is offline-capable. The included `m3-offline-fixture` vulnerability report is test evidence only and is rejected by default by production verification. A real production run must import a scanner report, for example an OSV-Scanner result normalized through `scripts/m3/import_osv_report.py`, or an organization-approved equivalent normalized to the M3 report schema.

For enterprise release signing, Sigstore/Cosign may be layered on top of the same release subjects. The built-in Ed25519 path provides sovereign offline signing/verification and does not claim public transparency-log attestation.

## M3 controls

- `AIS-SBOM-001`
- `AIS-AIBOM-001`
- `AIS-LOCK-001`
- `AIS-PROV-001`
- `AIS-SIG-001`
- `AIS-VULN-001`
