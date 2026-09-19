# M7 validation

Local acceptance:

```bash
./scripts/m7/preflight_dependencies.sh
./scripts/m7/validate_m7_local.sh
```

Physical tool smoke test:

```bash
python3 scripts/m7/run_tool_agent.py \
  --m2-env ~/.config/portable-ai-governance/m2/production.env \
  --m6-env ~/.config/portable-ai-governance/m6/m6.env \
  --m7-env ~/.config/portable-ai-governance/m7/m7.env \
  --tool evidence.verify \
  --evidence-id m5:compliance-risk-manifest.json
```

Require success plus two audit references (pre-execution and result). Then verify the M7 audit chain using `SecurityAuditLog.verify()` with the M2 `audit_signing` secret. Negative acceptance requires schema, authorization, policy, budget, audit-unavailable, output-schema, side-effecting-registry and M6-binding failures to remain fail closed.

## Cross-milestone release-generation gate

Before packaging or Node2 deployment, verify the exact signed generation:

```bash
python3 scripts/m7/verify_release_chain.py \
  --m4-material "$PWD/var/m4-material" \
  --m5-material "$PWD/var/m5-material" \
  --m6-material "$PWD/var/m6-material" \
  --m7-material "$PWD/var/m7-material"
```

A mismatch at any of M4->M5, M5->M6 or M6->M7 is a release STOP. Do not weaken the digest check; rebuild the downstream attestations from one coherent upstream generation.
