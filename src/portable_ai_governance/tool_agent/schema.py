from __future__ import annotations
class ToolSchemaError(RuntimeError): pass

def _fail(path,msg): raise ToolSchemaError(f"{path}: {msg}")
def validate_schema(schema,value,path="$",depth=0):
    if depth>16: _fail(path,"schema nesting limit exceeded")
    if not isinstance(schema,dict): _fail(path,"invalid schema")
    typ=schema.get("type")
    if typ=="object":
        if not isinstance(value,dict): _fail(path,"expected object")
        props=schema.get("properties",{})
        req=set(schema.get("required",[]))
        miss=req-set(value)
        if miss: _fail(path,"missing required properties: "+",".join(sorted(miss)))
        if schema.get("additionalProperties",True) is False:
            extra=set(value)-set(props)
            if extra: _fail(path,"unexpected properties: "+",".join(sorted(extra)))
        for k,v in value.items():
            if k in props: validate_schema(props[k],v,f"{path}.{k}",depth+1)
    elif typ=="array":
        if not isinstance(value,list): _fail(path,"expected array")
        if len(value)<int(schema.get("minItems",0)): _fail(path,"too few items")
        if "maxItems" in schema and len(value)>int(schema["maxItems"]): _fail(path,"too many items")
        if "items" in schema:
            for i,v in enumerate(value): validate_schema(schema["items"],v,f"{path}[{i}]",depth+1)
    elif typ=="string":
        if not isinstance(value,str): _fail(path,"expected string")
        if len(value)<int(schema.get("minLength",0)): _fail(path,"string too short")
        if "maxLength" in schema and len(value)>int(schema["maxLength"]): _fail(path,"string too long")
        if "enum" in schema and value not in schema["enum"]: _fail(path,"value not in enum")
    elif typ=="integer":
        if isinstance(value,bool) or not isinstance(value,int): _fail(path,"expected integer")
        if "minimum" in schema and value<schema["minimum"]: _fail(path,"below minimum")
        if "maximum" in schema and value>schema["maximum"]: _fail(path,"above maximum")
    elif typ=="number":
        if isinstance(value,bool) or not isinstance(value,(int,float)): _fail(path,"expected number")
    elif typ=="boolean":
        if not isinstance(value,bool): _fail(path,"expected boolean")
    elif typ=="null":
        if value is not None: _fail(path,"expected null")
    elif typ is None:
        pass
    else: _fail(path,f"unsupported schema type: {typ}")
    if "enum" in schema and typ!="string" and value not in schema["enum"]: _fail(path,"value not in enum")
    return True
