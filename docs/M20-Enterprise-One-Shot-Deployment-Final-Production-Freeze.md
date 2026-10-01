# M20 — Enterprise One-Shot Deployment / Final Production Freeze

M20 assembles a signed enterprise release/freeze evidence bundle from the frozen M11–M19 control chain. A deterministic local run is only a `RELEASE_CANDIDATE`; `FINAL_FREEZE_READY` requires M19 `LIVE` production validation with zero failed required checks. M20 does not perform CRA conformity assessment, CE marking, firmware flashing, host OS updates, or external deployment side effects.

## Secure GenAI / agentic demonstration

M20 also exposes a Node1/Node2 demonstration built directly on M10 commit `d4ce10a`: fixed supervisor topology, no peer delegation, typed/digest-bound handoffs, bounded signal/output budgets, assurance gating, a separately signed single-use human disposition, hash-linked workflow journal, and `side_effect_authority=false`. Node1 creates and signs the trace; Node2 independently verifies the proposal digest, assurance binding and human decision signature.
