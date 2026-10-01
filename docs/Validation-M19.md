# Validation — M19

Local deterministic acceptance:

```bash
./scripts/m19/validate_m19_local.sh
```

Full release gate:

```bash
./scripts/m19/validate_m19_regression.sh
```

Fixture acceptance is always `SIMULATED`. Production acceptance additionally requires LIVE profiles from both nodes, all ten required validation cases passing, and `production_validation_complete=true`. Negative tests must prove signed-material tamper rejection and private-key rejection on Node2.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.
