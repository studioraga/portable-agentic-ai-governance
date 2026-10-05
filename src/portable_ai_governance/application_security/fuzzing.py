from __future__ import annotations
def evaluate_fuzz_result(result):
 return {"ok":int(result.get("executions",0))>0 and int(result.get("crashes",0))==0 and int(result.get("hangs",0))==0,"executions":int(result.get("executions",0)),"crashes":int(result.get("crashes",0)),"hangs":int(result.get("hangs",0))}
