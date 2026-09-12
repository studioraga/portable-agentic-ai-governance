# Portable Agentic AI Governance

A reusable security and governance control plane for AI/ML, RAG, GenAI, and bounded agentic systems.

The repository is deliberately framework-neutral. LangGraph, CrewAI, custom state machines, or other orchestrators may be attached in later milestones, but they cannot replace the deterministic trust kernel.

## Release status

**v0.1.1 — Milestones 0 and 1.** This revision hardens portable deployment, src-layout imports, prerequisites, clean source packaging, and validation after Node1 testing exposed a pytest import-path defect in v0.1.0.

## Implemented

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
- GOV-01 AI System Inventory Agent.
- GOV-03 AI Risk Agent; the agent is prohibited from accepting risk.
- GOV-06 Control Mapping Agent.
- GOV-10 Governance Evidence Agent.
- Golden AI System Onboarding workflow.
- Framework mapping data foundation for NIST AI RMF, NIST CSF 2.0, ISO/IEC 42001, and OWASP-oriented controls.
- Built-in sovereign self-tests plus extended pytest tests.
- One-shot Node1 preflight, deployment, validation, and clean release packaging.

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

Minimum M0-M1 dependencies are Python 3.11+, Python venv support, Bash, OpenSSL, tar/gzip, SHA-256 utilities, writable local storage, and the repository files. Pytest is required to execute the full extended acceptance suite. GPU/CUDA, LLMs, databases, vector stores, containers, Internet access, and Node2 are not required.

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

These are bootstrap validation secrets, not the final enterprise secret-management design. Milestone 2 introduces managed identity and secrets-provider interfaces.

## Reuse from the sovereign edge-AI source project

M0-M1 generalizes proven patterns from the supplied edge-AI evidence project: fail-closed profiles, signed requests, persistent nonce replay defense, explicit authorization, cryptographic evidence chaining, digest verification, immutable evidence thinking, and executable positive/negative acceptance gates. Camera-specific code is intentionally excluded from the portable kernel.

## Documentation

- `instruction.md` — repository operating and security rules.
- `docs/Prerequisites.md` — complete M0-M1 machine/software/security prerequisites.
- `docs/Architecture.md` — architecture, trust boundaries, Milestones 0-10, and reusable workflows 88-99.
- `docs/Validation.md` — exact Node1 validation, negative tests, troubleshooting, and Node2 applicability.
- `docs/Deployment.md` — prerequisite installation, one-shot deployment, production-profile bootstrap, and clean release packaging.
- `docs/Milestones.md` — implementation/acceptance matrix.
