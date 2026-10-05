from __future__ import annotations
from .soc import validate_soc_policy
from .vulnerability import validate_vulnerability_policy
from .incident import validate_incident_policy
from .backup import validate_backup_policy
REQ={'ENT-SOC-001','ENT-SOC-002','ENT-SOC-003','ENT-VULN-001','ENT-VULN-002','ENT-IR-001','ENT-IR-002','ENT-DR-001','ENT-DR-002','ENT-DR-003'}
def evaluate_m26_policy(soc,vuln,ir,backup,controls):
 checks=[];ids={x.get('control_id') for x in controls.get('controls',[])};checks.append(('m26-controls-present',REQ<=ids))
 for name,fn,obj in [('soc-policy',validate_soc_policy,soc),('vulnerability-policy',validate_vulnerability_policy,vuln),('incident-policy',validate_incident_policy,ir),('backup-policy',validate_backup_policy,backup)]:
  try: fn(obj);checks.append((name,True))
  except Exception: checks.append((name,False))
 for k in ('cissp_certification_claim','iso_iec_27001_certification_claim','iso_iec_42001_certification_claim','cra_conformity_claim'):
  checks.append((f'claim-boundary:{k}',backup.get('claim_boundaries',{}).get(k) is False))
 return {'ok':all(v for _,v in checks),'checks':checks,'control_count':len(REQ)}
