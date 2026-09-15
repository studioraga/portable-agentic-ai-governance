# Portable Agentic AI Governance

A reusable security and governance control plane for AI/ML, RAG, GenAI, and bounded agentic systems.

The repository is deliberately framework-neutral. LangGraph, CrewAI, custom state machines, or other orchestrators may be attached in later milestones, but they cannot replace the deterministic trust kernel.

## Release status

**v0.6.0 — Milestone 6 first bounded read-only Evidence Analyst implementation candidate.**

The frozen M0-M1 baseline remains tagged `m0-m1-v0.1.2`. Milestone 2 adds deterministic identity, RBAC+ABAC, TLS 1.3 mutual authentication, workload identity, protected secrets, provider-backed crypto, signed requests, persistent anti-replay, rate limiting, signed security audit, and fail-closed production dependency validation.

Milestone 2 remains implemented and validated. Milestone 3 is frozen and adds signed CycloneDX software and AI/ML BOMs, model/container/prompt/tool digest locks, in-toto/SLSA-style provenance, Ed25519 verification, and fail-closed vulnerability policy. Milestone 4 is frozen and adds model governance, data provenance, pre-retrieval authorization, embedding controls, deterministic AI evaluation, AI threat modeling, and an explicit no-LLM-autonomy gate. Milestone 5 adds deterministic impact/privacy assessments, exception governance, third-party risk, continuous-control freshness, and evidence-backed compliance reporting without autonomous approval or certification claims.

See `docs/M5-Compliance-Risk-Automation.md`, `docs/Prerequisites-M5.md`, `docs/Deployment-M5.md`, and `docs/Validation-M5.md`.

## Implemented

### Milestone 5

- Evidence-backed AI/system impact assessments with inherent/residual risk and accountable decisions.
- Privacy assessments covering purpose, data categories, legal basis, retention, data-subject rights, DPIA and transfer safeguards.
- Default-deny exception register with independent approval, compensating controls and expiration.
- Third-party/provider register with security assessment, contract/data terms, residency, review and exit planning.
- Continuous-control records with signed evidence digests, blocking failure action and freshness limits, plus a release-authority refresh workflow and optional six-hour systemd timer.
- Evidence-backed compliance reports that explicitly prohibit automated certification claims.
- Signed SHA-256 M5 compliance/risk manifest bound to the M4 AI-security manifest.
- Combined fail-closed M2+M3+M4+M5 production profile.
- No LLM agent autonomy and no automated risk acceptance, exception approval, legal opinion or certification.

### Milestone 4

- Model governance records bound to immutable M3 model digests.
- Data provenance records with source, ownership, classification, tenant and license/consent evidence.
- Default-deny authorization before retrieval with cross-tenant and clearance enforcement.
- Tenant-partitioned, provenance-bound embedding controls with blocked classifications and dimension limits.
- Deterministic AI-security evaluation suite and minimum-score release gate.
- AI threat model covering prompt injection, sensitive disclosure, poisoning, vector/embedding weaknesses, model theft, retrieval bypass and excessive agency.
- Signed SHA-256 AI-security manifest and verifier-only Node2 deployment.
- Explicit `llm_agent_autonomy=false` and `llm_tool_execution=false` requirement.

### Milestone 3

- CycloneDX 1.7 software SBOM and AI/ML BOM generation.
- SHA-256 model, container, prompt and tool locks.
- Digest-pinned container references.
- In-toto Statement v1 with SLSA provenance v1 predicate.
- Offline Ed25519 release signing and public-key verification.
- Vulnerability freshness/severity/scanner policy; fixture scans are rejected in production by default.
- One-shot Node1/Node2 verifier deployment and combined M2+M3 production validation.

### Milestone 2

- Identity provider interface with bootstrap/local and owner-only file identity adapters.
- Deterministic RBAC + ABAC authorization with deny-by-default behavior.
- TLS 1.3 mutual-authentication contexts and SPIFFE-style workload URI SAN identity.
- Protected workload registry mapping certificates to principals/roles/attributes.
- Protected `SecretProvider` abstraction with independent evidence/request/approval/audit signing domains.
- Provider-backed cryptographic HMAC/SHA-256 service.
- Signed requests integrated with persistent fail-closed anti-replay.
- Deterministic rate limiting.
- Signed/chained security decision audit ledger.
- Fail-closed M2 production profile requiring identity, secrets, policy, mTLS, node identity, audit path and rate-limit dependencies.
- One-shot Node1/Node2 material deployment, local two-node simulation, remote secure-ping validation, and optional hardened systemd Node1 probe.

### Milestones 0-1 retained

- Deterministic workflow state machine with illegal-transition rejection.
- Monotonic step/tool budgets.
- Bootstrap identity and explicit RBAC authorization interfaces.
- Deterministic policy engine with fail-closed unknown-control behavior.
- Signed approval primitive.
- HMAC request signing and tamper verification.
- Persistent bounded anti-replay cache.
- Signed append-only chained governance evidence ledger.
- Artifact digest verification primitive.
- Production-vs-lab fail-closed security-profile contract.
- Production signing-key domain separation: evidence, request, and approval signing keys must be independent.
- Private-by-default runtime filesystem: validation/deployment use `umask 077`; evidence ledgers are explicitly forced to mode `0600`.
- GOV-01 AI System Inventory Agent.
- GOV-03 AI Risk Agent; the agent is prohibited from accepting risk.
- GOV-06 Control Mapping Agent.
- GOV-10 Governance Evidence Agent.
- Golden AI System Onboarding workflow.
- Framework mapping data foundation for NIST AI RMF, NIST CSF 2.0, ISO/IEC 42001, and OWASP-oriented controls.
- Built-in sovereign self-tests plus extended pytest tests.
- One-shot Node1 preflight, deployment, validation, and clean release packaging.
- Standalone security validators for production signing-key separation and runtime evidence permissions.

## Prerequisites first

Read:

```text
docs/Prerequisites.md
```

For Ubuntu 24.04:

```bash
./scripts/preflight_node1.sh
```

If required and permitted:

```bash
./deploy/install_prerequisites_ubuntu2404.sh
```

Minimum portable dependencies are Python 3.10+, Python venv support, Bash, OpenSSL, tar/gzip, SHA-256 utilities, writable local storage, and the repository files. Pytest is required to execute the full extended acceptance suite. GPU/CUDA, LLMs, databases, vector stores, containers, Internet access, and Node2 are not required.

## One-shot Node1 validation

```bash
./deploy/deploy_node1.sh
```

The repository uses a Python `src/` layout. Deployment and validation explicitly set `PYTHONPATH=$REPO/src` and create a local venv `.pth` file; do not rely on being in the repository directory alone to make imports work.

## Golden onboarding workflow

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
export PAG_REPO_ROOT="$PWD"
python -m portable_ai_governance.cli onboard \
  --input examples/golden_onboarding/system.json \
  --run-id manual-001
python -m portable_ai_governance.cli verify-evidence
```

## Production-profile contract validation

```bash
export PAG_SECURITY_PROFILE=production
export PAG_FAIL_CLOSED=1
export PAG_EVIDENCE_SIGNING_KEY="$(openssl rand -hex 32)"
export PAG_REQUEST_SIGNING_KEY="$(openssl rand -hex 32)"
export PAG_APPROVAL_SIGNING_KEY="$(openssl rand -hex 32)"
python -m portable_ai_governance.cli validate-security
```

These are bootstrap validation secrets, not the final enterprise secret-management design. All three values must be independent; production preflight and runtime validation fail closed when any required key is absent, weak, or reused across domains.

Runtime privacy for M0-M1 is also part of the acceptance boundary:

```text
var/            0700
var/evidence/   0700
var/runs/       0700
var/state/      0700
runtime files   0600
```

Deployment and validation run with `umask 077`, and the evidence ledger explicitly enforces mode `0600`. Milestone 2 introduces managed identity, a `SecretProvider` abstraction, Vault/KMS/HSM adapters, key IDs/versioning, rotation, historical verification, and workload identity.

## Reuse from the sovereign edge-AI source project

M0-M1 generalizes proven patterns from the supplied edge-AI evidence project: fail-closed profiles, signed requests, persistent nonce replay defense, explicit authorization, cryptographic evidence chaining, digest verification, immutable evidence thinking, and executable positive/negative acceptance gates. Camera-specific code is intentionally excluded from the portable kernel.

## Documentation

- `instruction.md` — repository operating and security rules.
- `docs/Prerequisites.md` — complete M0-M1 machine/software/security prerequisites.
- `docs/Architecture.md` — architecture, trust boundaries, Milestones 0-10, and reusable workflows 88-99.
- `docs/Validation.md` — exact Node1 validation, negative tests, troubleshooting, and Node2 applicability.
- `docs/Deployment.md` — prerequisite installation, one-shot deployment, production-profile bootstrap, and clean release packaging.
- `docs/Milestones.md` — implementation/acceptance matrix.

## Milestone 6 — First bounded agent

M6 introduces `EVIDENCE-ANALYST-001`, the first bounded production agent. It is read-only, deny-by-default, evidence-catalog constrained, digest-bound to its inputs, budget-limited, and cryptographically chained to M5. It has no shell/network/write/delete/approval/risk-acceptance/compliance-certification/delegation capability. The deterministic M2–M5 controls remain the security and governance boundary.

See `docs/M6-Bounded-Evidence-Analyst.md`, `docs/Prerequisites-M6.md`, `docs/Deployment-M6.md`, and `docs/Validation-M6.md`.
