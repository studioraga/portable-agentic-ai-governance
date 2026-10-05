from __future__ import annotations
from .policy import validate_network_policy
from .egress import validate_egress_policy
from .detection import validate_detection_policy
REQ={'ENT-NET-001','ENT-NET-002','ENT-NET-003','ENT-NET-004','ENT-NET-005','ENT-NET-006','ENT-NET-007'}
def evaluate_m25_policy(net,egress,detection,controls):
    checks=[];ids={c.get('control_id') for c in controls.get('controls',[])};checks.append(('m25-controls-present',REQ<=ids))
    for n,fn in [('network-policy',lambda:validate_network_policy(net)),('egress-policy',lambda:validate_egress_policy(egress)),('detection-policy',lambda:validate_detection_policy(detection))]:
        try:fn();checks.append((n,True))
        except Exception:checks.append((n,False))
    checks += [('default-deny',net.get('default_decision')=='deny'),('egress-default-deny',egress.get('default_egress_decision')=='deny'),('management-zone-present',any(z.get('zone_id')=='management' for z in net.get('zones',[]))),('verifier-zone-present',any(z.get('zone_id')=='verifier' for z in net.get('zones',[])))]
    boundaries=net.get('claim_boundaries',{})
    for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'):
        checks.append((f'claim-boundary:{k}',boundaries.get(k) is False))
    return {'ok':all(v for _,v in checks),'checks':checks,'control_count':len(REQ)}
