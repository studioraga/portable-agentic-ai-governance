from __future__ import annotations
from .common import load_json
class EmbeddingControlError(RuntimeError): pass

def require_embedding_policy(path, provenance_path):
    p=load_json(path); prov=load_json(provenance_path); ids={x['record_id']:x for x in prov.get('records',[])}
    if p.get('store_raw_source_text') is not False: raise EmbeddingControlError('raw source text storage in embedding index forbidden')
    if p.get('tenant_partitioning') is not True: raise EmbeddingControlError('tenant partitioning required')
    if int(p.get('max_dimensions',0))<=0: raise EmbeddingControlError('max_dimensions required')
    blocked=set(p.get('blocked_classifications',[]))
    for e in p.get('approved_entries',[]):
        src=ids.get(e.get('source_record_id'))
        if not src: raise EmbeddingControlError('embedding lacks provenance source')
        if src.get('classification') in blocked: raise EmbeddingControlError('blocked classification embedded')
        if int(e.get('dimensions',0))>int(p['max_dimensions']): raise EmbeddingControlError('embedding dimensions exceed policy')
        if len(e.get('embedding_model_sha256',''))!=64: raise EmbeddingControlError('embedding model digest required')
        if not e.get('chunk_sha256') or len(e['chunk_sha256'])!=64: raise EmbeddingControlError('chunk digest required')
    return 'embedding provenance/partition/dimension/classification controls verified'
