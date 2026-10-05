def evaluate_m28_policy(control_mapping, controls, framework_mapping, gap):
 catalog={x.get("control_id") for x in controls.get("controls",[])}
 fmap=set(framework_mapping.get("controls",{}))
 ids=[x["control_id"] for x in control_mapping.get("controls",[])]
 checks=[("unique-controls",len(ids)==len(set(ids))), ("catalog",all(x in catalog for x in ids)), ("framework-map",all(x in fmap for x in ids))]
 closure={x["requirement_id"] for x in gap.get("closures",[])}
 checks += [("close-d1-001","CISSP-D1-001" in closure),("close-d1-004","CISSP-D1-004" in closure),("close-d7-004","CISSP-D7-004" in closure)]
 return {"ok":all(v for _,v in checks),"checks":checks}
