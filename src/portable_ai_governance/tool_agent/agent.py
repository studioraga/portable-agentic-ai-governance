from __future__ import annotations
from dataclasses import dataclass
from .broker import ToolBroker, ToolCall, ToolCallResult

class ToolAgentError(RuntimeError): pass

@dataclass(frozen=True)
class ToolPlan:
    run_id: str
    calls: tuple[ToolCall, ...]

class ToolUsingAgent:
    """Bounded orchestration shell. It can request registered tools only through ToolBroker."""
    def __init__(self, broker: ToolBroker, *, max_plan_calls: int = 8):
        if not 1 <= max_plan_calls <= 20:
            raise ValueError("max_plan_calls outside bounded range")
        self.broker = broker
        self.max_plan_calls = max_plan_calls

    def run_plan(self, plan: ToolPlan) -> tuple[ToolCallResult, ...]:
        if len(plan.calls) > self.max_plan_calls:
            raise ToolAgentError("plan call count exceeds bound")
        out = []
        for call in plan.calls:
            if call.run_id != plan.run_id:
                raise ToolAgentError("tool call run_id does not match plan")
            out.append(self.broker.invoke(call))
        return tuple(out)
