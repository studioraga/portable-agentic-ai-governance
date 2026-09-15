from __future__ import annotations
from dataclasses import dataclass
from .policy import require_agent_policy
from .common import load_json
from .tools import ReadOnlyEvidenceTools
class AgentExecutionError(RuntimeError): pass
@dataclass(frozen=True)
class AgentRequest:
    operation:str
    evidence_id:str|None=None
@dataclass(frozen=True)
class AgentResult:
    ok:bool
    operation:str
    result:object
    tool_calls:int
class EvidenceAnalyst:
    def __init__(self,policy_path,catalog_path,evidence_root):
        self.policy=load_json(policy_path); require_agent_policy(self.policy)
        self.tools=ReadOnlyEvidenceTools(catalog_path,evidence_root,max_read_bytes=int(self.policy['limits']['max_read_bytes']))
    def run(self,request:AgentRequest):
        allowed=set(self.policy['permissions']['tools']); op=request.operation
        if op not in allowed: raise AgentExecutionError('operation not allowlisted')
        if int(self.policy['budget']['max_tool_calls']) < 1: raise AgentExecutionError('tool-call budget exhausted')
        if op=='evidence.list': result=self.tools.list()
        elif op=='evidence.metadata': result=self.tools.metadata(request.evidence_id or '')
        elif op=='evidence.read': result=self.tools.read(request.evidence_id or '')
        elif op=='evidence.verify': result=self.tools.verify(request.evidence_id or '')
        elif op=='evidence.summarize': result=self.tools.summarize(request.evidence_id or '')
        else: raise AgentExecutionError('unsupported operation')
        return AgentResult(True,op,result,1)
