from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ToolDefinition:
    tool_id: str
    version: str
    side_effects: bool
    required_action: str
    approval_required: bool = False

class ToolRegistry:
    def __init__(self, tools: tuple[ToolDefinition, ...]):
        self.tools = {t.tool_id: t for t in tools}
    def get(self, tool_id: str) -> ToolDefinition:
        if tool_id not in self.tools:
            raise KeyError(f"unknown tool: {tool_id}")
        return self.tools[tool_id]
