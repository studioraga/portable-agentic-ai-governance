from __future__ import annotations
from dataclasses import dataclass

class BudgetExceeded(RuntimeError):
    pass

@dataclass
class RunBudget:
    max_steps: int = 20
    max_tool_calls: int = 10
    steps: int = 0
    tool_calls: int = 0

    def consume_step(self) -> None:
        self.steps += 1
        if self.steps > self.max_steps:
            raise BudgetExceeded("step budget exceeded")

    def consume_tool_call(self) -> None:
        self.tool_calls += 1
        if self.tool_calls > self.max_tool_calls:
            raise BudgetExceeded("tool-call budget exceeded")
