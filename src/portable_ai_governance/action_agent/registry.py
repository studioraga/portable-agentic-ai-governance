from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .common import load_json
class ActionRegistryError(RuntimeError): pass
@dataclass(frozen=True)
class ActionDefinition:
 name:str; version:str; action:str; resource:str; policy_control_id:str; side_effecting:bool; approval_required:bool; input_schema:dict[str,Any]; output_schema:dict[str,Any]
class ActionRegistry:
 def __init__(self,path):
  doc=load_json(path)
  if doc.get('version')!='0.8.0' or doc.get('default')!='deny': raise ActionRegistryError('invalid M8 registry')
  tools={}
  for x in doc.get('tools',[]):
   name=str(x.get('name',''))
   if not name or name in tools: raise ActionRegistryError('unique tool name required')
   if x.get('side_effecting') is not True: raise ActionRegistryError('M8 registry contains non-side-effecting tool')
   if x.get('approval_required') is not True: raise ActionRegistryError('M8 side effects require approval')
   resource=str(x.get('resource',''))
   if not resource.startswith('action://'): raise ActionRegistryError('M8 canonical action resource required')
   tools[name]=ActionDefinition(name,str(x.get('version','')),str(x.get('action','')),resource,str(x.get('policy_control_id','')),True,True,dict(x.get('input_schema',{})),dict(x.get('output_schema',{})))
  if set(tools)!={'incident.create','rerun.request','ticket.create','model.quarantine'}: raise ActionRegistryError('M8 registry must exactly contain four approved action tools')
  self.tools=tools
 def get(self,name):
  try:return self.tools[name]
  except KeyError: raise ActionRegistryError(f'unknown M8 action tool: {name}')
