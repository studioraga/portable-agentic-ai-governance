from __future__ import annotations
import ast
DANGEROUS={"eval","exec"}
def scan_python(source,path="<memory>"):
 findings=[]
 try: tree=ast.parse(source,filename=path)
 except SyntaxError as e:return [{"tool":"builtin-sast","rule":"syntax-error","severity":"high","path":path,"line":e.lineno or 0}]
 for n in ast.walk(tree):
  if isinstance(n,ast.Call):
   name=n.func.id if isinstance(n.func,ast.Name) else (n.func.attr if isinstance(n.func,ast.Attribute) else "")
   if name in DANGEROUS: findings.append({"tool":"builtin-sast","rule":f"dangerous-{name}","severity":"high","path":path,"line":getattr(n,"lineno",0)})
   if name in {"run","Popen","call","check_call","check_output"}:
    for kw in n.keywords:
     if kw.arg=="shell" and isinstance(kw.value,ast.Constant) and kw.value.value is True:
      findings.append({"tool":"builtin-sast","rule":"subprocess-shell-true","severity":"high","path":path,"line":getattr(n,"lineno",0)})
 return findings
