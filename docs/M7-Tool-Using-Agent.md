# Milestone 7 — Tool-using agent

## Security objective

M7 introduces a typed-tool agent without introducing uncontrolled agency. `TOOL-ANALYST-001` can request only tools declared in a signed registry. The registry, tool-agent policy and authorization rules are SHA-256 bound in the signed M7 manifest, which is bound to the exact M6 Evidence Analyst manifest.

## Mandatory call path

```text
agent request
   |
   v
input schema
   |
   v
RBAC + ABAC authorization
   |
   v
deterministic governance policy
   |
   v
monotonic step/tool-call budget
   |
   v
signed pre-execution audit
   |
   v
non-side-effecting executor
   |
   v
output schema
   |
   v
signed result audit
```

A failed schema, authorization, policy or budget gate is denied and signed into the audit log. If the pre-execution audit cannot be persisted, the executor is not invoked.

## M7 boundary

M7 tools are non-side-effecting. Shell/network execution, writes, deletion, policy changes, approvals, risk acceptance, compliance certification and delegated execution are not permitted. M8 introduces signed approval-controlled side effects.

## Attestation-generation lifecycle

M7 is bound to the exact M6 manifest, M6 is bound to the exact M5 manifest, and M5 is bound to the exact M4 manifest. Continuous-control refreshes that change M5 are therefore new attestation generations. Once M6/M7 exist, the bound M5 release snapshot is immutable. Refreshing continuous controls requires rebuilding/re-signing M6 and M7 and redistributing the verifier chain.
