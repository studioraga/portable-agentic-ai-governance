# M8 deployment

Build M8 from the exact accepted M7 material. Node1 retains M8 release-signing and dedicated Ed25519 approval-signing private material; Node2 receives verifier-only material and `approval-signing-public.pem` only. Approval issuance is an operator workflow and is not an `ACTION-AGENT-001` tool.

Runtime action state is owner-private under `~/.config/portable-ai-governance/m8/runtime/actions` and is deliberately preserved across M8 redeployment. This includes the single-use approval ledger, effect journals, and reconciliation records. Deployment overwrites signed configuration/verifier material but never resets runtime replay state. Do not manually delete the runtime action directory to make a replay test pass.

The signed M8 policy sets approval TTL defaults/maxima and clock-skew tolerance. For manual physical acceptance testing, issue a fresh approval immediately before execution; do not reuse an expired approval merely to test replay semantics.
