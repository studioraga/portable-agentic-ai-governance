# M8 validation

Require positive approved execution and negative coverage for self-approval, expiry, future-dated approvals, signature/argument/request binding tampering, run/call drift, replay, authorization/policy/budget/audit failure, malformed approval envelopes, TTL policy enforcement, and M7->M8 drift.

Replay acceptance must use the exact same signed approval file twice: first execution succeeds, second execution is denied as already used, and the effect journal contains only one action. Replay protection must survive a fresh process and M8 redeployment because `runtime/actions` is preserved.

Audit acceptance distinguishes pre-execution and post-effect failures. A pre-execution audit outage after approval claim consumes the approval but must produce no side effect. If the side effect commits and result-audit persistence fails, validation requires `effect_committed=true` plus a durable reconciliation record.

Physical Node1/Node2 must pass combined M2->M8 and full one-shot validation. Node2 must receive the M8 approval public key but no M8 release-signing or approval-signing private key.
