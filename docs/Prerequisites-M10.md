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
