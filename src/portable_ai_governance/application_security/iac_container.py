from __future__ import annotations
def scan_container_text(text,path="Dockerfile"):
 findings=[]
 for i,line in enumerate(text.splitlines(),1):
  u=line.strip().upper()
  if u.startswith("FROM ") and ":LATEST" in u: findings.append({"tool":"builtin-container-scan","rule":"unpinned-latest","severity":"high","path":path,"line":i})
  if u.startswith("USER ROOT"): findings.append({"tool":"builtin-container-scan","rule":"root-user","severity":"high","path":path,"line":i})
 return findings
def scan_iac_text(text,path="iac"):
 findings=[]
 if "0.0.0.0/0" in text and any(x in text for x in ["22","3389","ssh","rdp"]): findings.append({"tool":"builtin-iac-scan","rule":"world-open-admin","severity":"high","path":path})
 return findings
