# M10 prerequisites

M10 inherits all M0-M9 prerequisites.

Additional runtime requirements are intentionally minimal:

- Python 3.10 or later,
- Python stdlib `fcntl`,
- OpenSSL with Ed25519 support,
- SHA-256 utilities,
- owner-private local storage,
- coherent validated M9 material.

M10 introduces no third-party Python runtime dependency. No GPU, LLM, model server, vector database, Internet access, LangGraph, CrewAI or cloud service is required by the reference implementation.

Before physical validation run:

```bash
./scripts/m10/preflight_dependencies.sh
python3 scripts/m3/validate_m3_node.py ~/.config/portable-ai-governance/m3/m3.env
```

On the release-authority node, keep the M5 continuous-control timer quiesced while generating a downstream release generation.

## M12 integration

M12 adds no mandatory cloud dependency. Its deterministic acceptance requires Python 3.10+, OpenSSL/Ed25519, Bash, `tar`, `sha256sum`, and the frozen M11 source baseline. Live vulnerability-feed access is deliberately not required for M12 acceptance.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.
