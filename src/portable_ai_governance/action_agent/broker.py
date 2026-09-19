from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .common import canonical_json_bytes,sha256_bytes
from .approval import ApprovalError,ApprovalRequest,request_sha256
from ..tool_agent.schema import validate_schema
from ..kernel.budgets import BudgetExceeded
from ..security.audit import SecurityEvent

class ActionDenied(RuntimeError):
    def __init__(self,stage,reason,audit_ref='',*,effect_committed=False,action_id=''):
        super().__init__(f'{stage}: {reason}')
        self.stage=stage; self.reason=reason; self.audit_ref=audit_ref
        self.effect_committed=effect_committed; self.action_id=action_id

@dataclass(frozen=True)
class ActionCall:
    run_id:str; call_id:str; tool_name:str; arguments:dict[str,Any]

@dataclass(frozen=True)
class ActionCallResult:
    ok:bool; tool_name:str; output:dict[str,Any]; approval_id:str; audit_refs:tuple[str,...]; budget_steps:int; budget_tool_calls:int

class ActionBroker:
    def __init__(self,*,registry,principal,authorization,policy_adapter,budget,audit,approval_authority,approval_store,handlers,reconciliation=None):
        self.registry=registry; self.principal=principal; self.authorization=authorization; self.policy=policy_adapter
        self.budget=budget; self.audit=audit; self.approval_authority=approval_authority; self.approval_store=approval_store
        self.handlers=dict(handlers); self.reconciliation=reconciliation

    def _audit(self,call,decision,reason,stage,**attrs):
        return self.audit.record(SecurityEvent(event_type='agent.action.call',decision=decision,principal_id=self.principal.principal_id,action='action.execute',resource=f'action://{call.tool_name}',reason=reason,run_id=call.run_id,attributes={'call_id':call.call_id,'stage':stage,**attrs}))

    def _deny(self,call,stage,reason,stages):
        try: ref=self._audit(call,'deny',reason,stage,stages=stages)
        except Exception as exc: raise ActionDenied('audit',f'audit unavailable while recording {stage} denial: {type(exc).__name__}') from exc
        raise ActionDenied(stage,reason,ref)

    def invoke(self,call,approval):
        stages=[]; refs=[]
        try: td=self.registry.get(call.tool_name); validate_schema(td.input_schema,call.arguments); stages.append('schema')
        except Exception as exc: self._deny(call,'schema',str(exc),stages)
        allowed,reason=self.authorization.authorize(self.principal,action=td.action,resource=td.resource,resource_attributes={'side_effecting':'true','approval_required':'true'})
        if not allowed:self._deny(call,'authorization',reason,stages)
        stages.append('authorization')
        d=self.policy.evaluate(td.policy_control_id,principal=self.principal,context={'tool_gateway':True,'side_effecting':True,'approval_required':True,'tool_name':td.name})
        if not d.allowed:self._deny(call,'policy',d.reason,stages)
        if not d.approval_required:self._deny(call,'policy','M8 policy must require approval',stages)
        stages.append('policy')
        try:self.budget.consume_step();self.budget.consume_tool_call();stages.append('budget')
        except BudgetExceeded as exc:self._deny(call,'budget',str(exc),stages)
        try:
            self.approval_authority.verify(approval);g=approval.grant;argsha=sha256_bytes(canonical_json_bytes(call.arguments));req=ApprovalRequest(f'{call.run_id}:{call.call_id}',call.run_id,call.call_id,td.name,td.resource,self.principal.principal_id,argsha);reqsha=request_sha256(req)
            if g.tool_name!=td.name or g.resource!=td.resource or g.requester!=self.principal.principal_id or g.arguments_sha256!=argsha or g.request_sha256!=reqsha: raise ApprovalError('approval binding mismatch')
            # Claim before the pre-execution allow audit so replays never receive an allow-intent audit.
            self.approval_store.claim(g.approval_id,run_id=call.run_id,call_id=call.call_id,request_sha256_value=reqsha)
            stages.append('approval')
        except Exception as exc:self._deny(call,'approval',str(exc),stages)
        try:refs.append(self._audit(call,'allow','mandatory gates, single-use claim and approval verified','audit',stages=[*stages,'audit'],approval_id=g.approval_id,input_sha256=argsha));stages.append('audit')
        except Exception as exc:
            # Approval remains consumed: fail closed rather than allowing a retry without a new human approval.
            raise ActionDenied('audit',f'pre-execution audit unavailable after approval claim: {type(exc).__name__}',action_id=g.approval_id) from exc
        handler=self.handlers.get(td.name)
        if handler is None:self._deny(call,'executor','executor not registered',stages)
        try:output=handler(call.arguments);validate_schema(td.output_schema,output)
        except Exception as exc:
            try:refs.append(self._audit(call,'deny',str(exc),'output_schema',stages=stages,approval_id=g.approval_id))
            except Exception as aexc:raise ActionDenied('audit',f'result audit unavailable: {type(aexc).__name__}',effect_committed=True,action_id=g.approval_id) from aexc
            raise ActionDenied('output_schema',str(exc),refs[-1],effect_committed=True,action_id=g.approval_id) from exc
        outsha=sha256_bytes(canonical_json_bytes(output))
        try:refs.append(self._audit(call,'allow','approved side effect complete','result',stages=stages,approval_id=g.approval_id,output_sha256=outsha))
        except Exception as exc:
            if self.reconciliation is not None:
                try:self.reconciliation({'action_id':g.approval_id,'approval_id':g.approval_id,'tool_name':td.name,'run_id':call.run_id,'call_id':call.call_id,'output_sha256':outsha,'reason':f'result audit unavailable: {type(exc).__name__}'})
                except Exception:pass
            raise ActionDenied('audit',f'side effect committed but result audit unavailable: {type(exc).__name__}',effect_committed=True,action_id=g.approval_id) from exc
        return ActionCallResult(True,td.name,output,g.approval_id,tuple(refs),self.budget.steps,self.budget.tool_calls)
