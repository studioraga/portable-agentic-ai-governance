from __future__ import annotations
from pathlib import Path
import json
from .common import sha256_file
def evaluate(repo_root,m19_summary,policy):
 rr=Path(repo_root);s=json.loads(Path(m19_summary).read_text()) if not isinstance(m19_summary,dict) else m19_summary
 fps={p:sha256_file(rr/p) for p in policy['source_fingerprint_paths'] if (rr/p).is_file()}
 live=s.get('validation_mode')=='LIVE';complete=s.get('production_validation_complete') is True and int(s.get('failed',1))==0
 state='FINAL_FREEZE_READY' if live and complete else 'RELEASE_CANDIDATE'
 checks=[{'id':'M20-VAL-001','name':'source fingerprint inventory','pass':len(fps)==len(policy['source_fingerprint_paths'])},{'id':'M20-VAL-002','name':'M19 live mode','pass':live},{'id':'M20-VAL-003','name':'M19 production validation complete','pass':complete},{'id':'M20-VAL-004','name':'no CRA conformity claim','pass':s.get('cra_conformity_claim') is False}]
 return {'schema':'pag-m20-final-freeze-v1','version':'0.20.0','freeze_state':state,'m19_validation_mode':s.get('validation_mode'),'m19_production_validation_complete':s.get('production_validation_complete'),'source_fingerprints':fps,'checks':checks,'final_freeze_ready':state=='FINAL_FREEZE_READY','cra_conformity_claim':False,'conformity_assessment_performed':False}
