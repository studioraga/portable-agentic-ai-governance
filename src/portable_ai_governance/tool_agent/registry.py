from __future__ import annotations
from dataclasses import dataclass
from .common import load_json
from .schema import validate_schema
class ToolRegistryError(RuntimeError): pass
@dataclass(frozen=True)
class ToolDefinition:
    name:str; version:str; action:str; resource:str; policy_control_id:str; input_schema:dict; output_schema:dict; side_effecting:bool=False
class ToolRegistry:
    def __init__(self,path):
        doc=load_json(path)
        if doc.get("version")!="0.7.0" or doc.get("default")!="deny": raise ToolRegistryError("invalid M7 registry header")
        self.tools={}
        for item in doc.get("tools",[]):
            td=ToolDefinition(str(item["name"]),str(item["version"]),str(item["action"]),str(item["resource"]),str(item["policy_control_id"]),dict(item["input_schema"]),dict(item["output_schema"]),bool(item.get("side_effecting",False)))
            if td.name in self.tools: raise ToolRegistryError("duplicate tool name")
            if td.side_effecting: raise ToolRegistryError("M7 forbids side-effecting tools; defer to M8")
            if td.action!="tool.invoke": raise ToolRegistryError("tool action must be tool.invoke")
            if td.resource!=f"tool://{td.name}": raise ToolRegistryError("tool resource must be canonical")
            # Validate schemas themselves against simple representative constraints.
            if td.input_schema.get("type")!="object" or td.output_schema.get("type")!="object": raise ToolRegistryError("M7 tool schemas must be objects")
            self.tools[td.name]=td
        if not self.tools: raise ToolRegistryError("empty tool registry")
    def get(self,name):
        if name not in self.tools: raise ToolRegistryError("tool not registered")
        return self.tools[name]
