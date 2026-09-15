from __future__ import annotations
from .common import load_json
class DataProvenanceError(RuntimeError): pass
REQUIRED={'record_id','source','sha256','owner','classification','tenant','license_or_consent','collected_at'}
def require_data_provenance(path):
    doc=load_json(path); records=doc.get('records',[])
    if not records: raise DataProvenanceError('no provenance records')
    ids=set()
    for r in records:
        miss=REQUIRED-set(r)
        if miss: raise DataProvenanceError(f"missing provenance fields: {sorted(miss)}")
        if len(r['sha256'])!=64: raise DataProvenanceError('invalid provenance digest')
        if not r['license_or_consent']: raise DataProvenanceError('license/consent required')
        if r['record_id'] in ids: raise DataProvenanceError('duplicate record_id')
        ids.add(r['record_id'])
    return 'data provenance complete'
