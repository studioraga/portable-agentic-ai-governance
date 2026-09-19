from __future__ import annotations
from ..evidence_analyst.tools import ReadOnlyEvidenceTools
class ToolExecutorError(RuntimeError): pass
def evidence_handlers(catalog_path,evidence_root,max_read_bytes=65536):
    tools=ReadOnlyEvidenceTools(catalog_path,evidence_root,max_read_bytes=max_read_bytes)
    return {
      "evidence.metadata": lambda a: tools.metadata(a["evidence_id"]),
      "evidence.verify": lambda a: tools.verify(a["evidence_id"]),
      "evidence.summarize": lambda a: tools.summarize(a["evidence_id"]),
    }
