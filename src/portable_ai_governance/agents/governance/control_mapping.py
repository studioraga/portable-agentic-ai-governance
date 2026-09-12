from __future__ import annotations
import json
from pathlib import Path
from ...kernel.types import AgentRequest, AgentResult

class ControlMappingAgent:
    agent_id = "GOV-06"
    def __init__(self, mapping_file: str | Path):
        self.mapping_file = Path(mapping_file)
        self.mapping = json.loads(self.mapping_file.read_text(encoding="utf-8"))

    def analyze(self, request: AgentRequest, control_ids: tuple[str, ...]) -> AgentResult:
        found, missing = [], []
        controls = self.mapping.get("controls", {})
        for cid in control_ids:
            if cid in controls:
                found.append({"control_id": cid, "frameworks": controls[cid]})
            else:
                missing.append(cid)
        status = "ok" if not missing else "incomplete"
        return AgentResult(request.run_id, self.agent_id, status,
            ({"mappings": found, "missing": missing, "mapping_version": self.mapping.get("mapping_version")},), next_state="COMPLETE")
