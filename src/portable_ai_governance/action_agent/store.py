from __future__ import annotations
import fcntl, json, os, time
from pathlib import Path

class ActionStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)

    def _append(self, kind, record):
        path = self.root / f"{kind}.jsonl"
        path.touch(exist_ok=True, mode=0o600)
        os.chmod(path, 0o600)
        with path.open("a+", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.seek(0)
            for line in f:
                if line.strip():
                    old = json.loads(line)
                    if old.get("action_id") == record["action_id"]:
                        return old
            f.seek(0, 2)
            f.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return record

    def record_reconciliation(self, record):
        record = dict(record)
        record.setdefault("recorded_at", int(time.time()))
        return self._append("reconciliation", record)

    def create_incident(self, a, x):
        return self._append("incidents", {"action_id": x, "incident_id": f"inc-{x[:12]}", "title": a["title"], "severity": a["severity"], "evidence_ref": a.get("evidence_ref", ""), "status": "open", "created_at": int(time.time())})

    def request_rerun(self, a, x):
        return self._append("reruns", {"action_id": x, "rerun_id": f"rerun-{x[:12]}", "job_id": a["job_id"], "reason": a["reason"], "status": "requested", "created_at": int(time.time())})

    def create_ticket(self, a, x):
        return self._append("tickets", {"action_id": x, "ticket_id": f"ticket-{x[:12]}", "title": a["title"], "queue": a["queue"], "description": a["description"], "status": "open", "created_at": int(time.time())})

    def quarantine_model(self, a, x):
        return self._append("quarantines", {"action_id": x, "quarantine_id": f"quarantine-{x[:12]}", "model_id": a["model_id"], "model_digest": a["model_digest"], "reason": a["reason"], "status": "quarantined", "created_at": int(time.time())})

def action_handlers(store, approval_id_getter):
    return {
        "incident.create": lambda a: store.create_incident(a, approval_id_getter()),
        "rerun.request": lambda a: store.request_rerun(a, approval_id_getter()),
        "ticket.create": lambda a: store.create_ticket(a, approval_id_getter()),
        "model.quarantine": lambda a: store.quarantine_model(a, approval_id_getter()),
    }
