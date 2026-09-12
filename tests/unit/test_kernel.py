import time
import pytest
from portable_ai_governance.kernel.state_machine import WorkflowState
from portable_ai_governance.kernel.budgets import RunBudget, BudgetExceeded
from portable_ai_governance.kernel.request_signing import sign_request, verify_request
from portable_ai_governance.kernel.replay_cache import PersistentNonceCache, ReplayDetected

def test_state_machine_blocks_illegal_transition():
    s=WorkflowState()
    with pytest.raises(ValueError): s.transition("COMPLETE")

def test_budget_fails_closed():
    b=RunBudget(max_steps=1); b.consume_step()
    with pytest.raises(BudgetExceeded): b.consume_step()

def test_request_signing_tamper_detection():
    key=b"k"*32; req=sign_request(key, method="POST", path="/x", body=b"hello", timestamp=100, nonce="n")
    assert verify_request(key, req, method="POST", path="/x", body=b"hello", now=100)
    assert not verify_request(key, req, method="POST", path="/x", body=b"evil", now=100)

def test_replay_cache_persists(tmp_path):
    path=tmp_path/"nonce.json"; a=PersistentNonceCache(path); a.consume("abc", now=100)
    b=PersistentNonceCache(path)
    with pytest.raises(ReplayDetected): b.consume("abc", now=101)
