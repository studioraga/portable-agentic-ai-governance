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

## M12 integration

Existing milestone validation remains unchanged and must continue to pass. M12 adds its own regression/negative gates in `docs/Validation-M12.md`; the full repository suite is run before M12 acceptance to prove no regression to this milestone.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
