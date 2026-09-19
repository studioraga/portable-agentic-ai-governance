# M10 validation

Acceptance requires all inherited M0-M9 gates plus:

1. dependency preflight passes with zero third-party runtime dependencies;
2. focused M10 tests pass;
3. M9->M10 manifest binding passes;
4. static M10 policy/topology verification passes;
5. fixed topology rejects direct peer calls;
6. signal/finding/output budgets fail closed;
7. handoff digest tampering is rejected;
8. Assurance blocks approval when evidence/control coverage is incomplete;
9. unauthorized human reviewer is rejected;
10. decision/proposal binding mismatch is rejected;
11. signed workflow decision is single-use and replay-protected;
12. approved workflow still reports `side_effect_authority=false`;
13. workflow journal hash-chain verification passes;
14. M10 private keys are absent on Node2;
15. full Node2 M0-M10 deployment passes;
16. physical Node2->Node1 M2 mTLS regression passes;
17. combined M2-M10 production security profile passes;
18. clean v0.10.0 source release passes fresh regression.

Run the isolated suite with:

```bash
./scripts/m10/validate_m10_local.sh
```

## Generated/private material Git gate

Before staging M10, verify that no generated milestone material or private key is tracked. In particular, M9 release/recovery private material must never remain under Git control:

```bash
git ls-files | grep -E '(^|/)(var|\.venv|\.pytest_cache|__pycache__)(/|$)|signing-private\.pem|approval-signing-private\.pem|recovery-signing-private\.pem|workflow-decision-private\.pem|ca\.key'
```

Production acceptance requires no matches. If a private key was previously committed, remove it from the current tree, rotate the affected authority, rebuild the downstream generation, and treat the historical key as compromised. If the repository is externally accessible, purge the secret-bearing path from Git history as a separate repository-administration operation.
