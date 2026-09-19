from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable
from .common import canonical_json_bytes,sha256_bytes
from .schema import validate_schema,ToolSchemaError
from .registry import ToolRegistry
from ..kernel.budgets import RunBudget,BudgetExceeded
from ..kernel.types import Principal
from ..security.audit import SecurityAuditLog,SecurityEvent

class ToolCallDenied(RuntimeError):
    def __init__(self,stage,reason,audit_ref=""):
        super().__init__(f"{stage}: {reason}"); self.stage=stage; self.reason=reason; self.audit_ref=audit_ref
@dataclass(frozen=True)
class ToolCall:
    run_id:str; call_id:str; tool_name:str; arguments:dict[str,Any]
@dataclass(frozen=True)
class ToolCallResult:
    ok:bool; tool_name:str; output:dict[str,Any]; audit_refs:tuple[str,...]; budget_steps:int; budget_tool_calls:int

class ToolBroker:
    """Single deterministic M7 mediation point. Executors are unreachable before all mandatory gates and pre-execution audit."""
    def __init__(self,*,registry:ToolRegistry,principal:Principal,authorization,policy_adapter,budget:RunBudget,audit:SecurityAuditLog,handlers:dict[str,Callable[[dict],dict]]):
        self.registry=registry; self.principal=principal; self.authorization=authorization; self.policy=policy_adapter; self.budget=budget; self.audit=audit; self.handlers=dict(handlers)
    def _audit(self,call,decision,reason,stage,**attrs):
        return self.audit.record(SecurityEvent(event_type="agent.tool.call",decision=decision,principal_id=self.principal.principal_id,action="tool.invoke",resource=f"tool://{call.tool_name}",reason=reason,run_id=call.run_id,attributes={"call_id":call.call_id,"stage":stage,**attrs}))
    def _deny(self,call,stage,reason,stages):
        try: ref=self._audit(call,"deny",reason,stage,stages=stages)
        except Exception as exc: raise ToolCallDenied("audit",f"audit unavailable while recording {stage} denial: {type(exc).__name__}") from exc
        raise ToolCallDenied(stage,reason,ref)
    def invoke(self,call:ToolCall)->ToolCallResult:
        stages=[]; refs=[]
        try: td=self.registry.get(call.tool_name)
        except Exception as exc: self._deny(call,"schema",str(exc),stages)
        try: validate_schema(td.input_schema,call.arguments); stages.append("schema")
        except Exception as exc: self._deny(call,"schema",str(exc),stages)
        allowed,reason=self.authorization.authorize(self.principal,action=td.action,resource=td.resource,resource_attributes={"side_effecting":str(td.side_effecting).lower()})
        if not allowed: self._deny(call,"authorization",reason,stages)
        stages.append("authorization")
        decision=self.policy.evaluate(td.policy_control_id,principal=self.principal,context={"tool_gateway":True,"tool_name":td.name,"side_effecting":False})
        if not decision.allowed: self._deny(call,"policy",decision.reason,stages)
        if decision.approval_required: self._deny(call,"policy","M7 tool policy cannot require approval; side effects belong to M8",stages)
        stages.append("policy")
        try:
            self.budget.consume_step(); self.budget.consume_tool_call(); stages.append("budget")
        except BudgetExceeded as exc: self._deny(call,"budget",str(exc),stages)
        # Audit-before-execute is fail closed. If the signed audit cannot be persisted, executor is never invoked.
        try:
            intent_ref=self._audit(call,"allow","mandatory gates passed","audit",stages=[*stages,"audit"],input_sha256=sha256_bytes(canonical_json_bytes(call.arguments)))
            refs.append(intent_ref); stages.append("audit")
        except Exception as exc: raise ToolCallDenied("audit",f"pre-execution audit unavailable: {type(exc).__name__}") from exc
        if td.side_effecting: self._deny(call,"executor","M7 side-effecting tools prohibited",stages)
        handler=self.handlers.get(td.name)
        if handler is None: self._deny(call,"executor","executor not registered",stages)
        try:
            output=handler(call.arguments)
            validate_schema(td.output_schema,output)
        except Exception as exc:
            try: refs.append(self._audit(call,"deny",str(exc),"output_schema",stages=stages))
            except Exception as aexc: raise ToolCallDenied("audit",f"result audit unavailable: {type(aexc).__name__}") from aexc
            raise ToolCallDenied("output_schema",str(exc),refs[-1]) from exc
        try:
            refs.append(self._audit(call,"allow","tool execution complete","result",stages=stages,output_sha256=sha256_bytes(canonical_json_bytes(output))))
        except Exception as exc: raise ToolCallDenied("audit",f"result audit unavailable: {type(exc).__name__}") from exc
        return ToolCallResult(True,td.name,output,tuple(refs),self.budget.steps,self.budget.tool_calls)
