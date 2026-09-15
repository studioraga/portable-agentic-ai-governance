# Milestone 4 — AI System Security

Milestone 4 introduces deterministic controls for model governance, data provenance, retrieval authorization, embedding security, AI evaluation, and AI-specific threat modeling. It deliberately does **not** introduce autonomous LLM agents or LLM-directed tool execution.

## Security invariants

1. A model is deployable only when its governance record is `approved` and its SHA-256 matches the immutable M3 model lock.
2. Every governed data record carries source, digest, owner, classification, tenant, collection time, and license/consent evidence.
3. Retrieval authorization executes **before** retrieval, defaults to deny, denies cross-tenant access, and enforces classification clearance.
4. Embeddings are tenant-partitioned, provenance-bound, dimension-bounded, and cannot include blocked classifications. Raw source text is not stored in the embedding index by this reference policy.
5. Mandatory deterministic evaluations must pass the configured threshold before production acceptance.
6. The AI threat model must cover prompt injection, sensitive-information disclosure, data/model poisoning, vector/embedding weaknesses, model theft, retrieval bypass, and excessive agency.
7. `llm_agent_autonomy=false` and `llm_tool_execution=false` are mandatory in M4.
8. M4 artifacts are SHA-256 bound in a signed Ed25519 AI-security manifest. Verifier nodes receive the public key only.

## Production boundary

The reference implementation uses deterministic fixtures for model/data/retrieval evaluation so that controls can be validated offline. Production integrations must replace fixture provenance records and evaluation inputs with organization-owned ingestion/catalog/evaluation pipelines while preserving these interfaces and fail-closed invariants.

No model inference SDK, vector database, LLM service, GPU, or embedding runtime is required by M4 itself.
