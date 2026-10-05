from __future__ import annotations
import re
PATTERNS={"private-key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),"aws-access-key":re.compile(r"AKIA[0-9A-Z]{16}"),"github-token":re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,}"),"password-assignment":re.compile(r"(?i)password\s*=\s*['\"][^'\"]{8,}['\"]") }
def scan_text(text,path="<memory>"):
 out=[]
 for rule,rx in PATTERNS.items():
  for m in rx.finditer(text): out.append({"tool":"builtin-secret-scan","rule":rule,"severity":"critical","path":path,"offset":m.start()})
 return out
