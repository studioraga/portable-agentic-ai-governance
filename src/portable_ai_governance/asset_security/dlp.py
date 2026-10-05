from __future__ import annotations
import re
class DLPError(RuntimeError): pass
class DLPDenied(DLPError): pass

def validate_dlp_policy(policy:dict)->None:
    if policy.get('default_decision')!='deny': raise DLPError('DLP default decision must deny')
    if not policy.get('classification_rules'): raise DLPError('classification rules required')
    for p in policy.get('content_patterns',[]): re.compile(p['regex'])

def scan_content(text:str,policy:dict)->tuple[str,...]:
    validate_dlp_policy(policy);hits=[]
    for p in policy.get('content_patterns',[]):
        if re.search(p['regex'],text):hits.append(p['id'])
    return tuple(sorted(hits))

def authorize_export(request:dict,asset:dict,policy:dict,content:str='')->dict:
    validate_dlp_policy(policy)
    cls=asset.get('classification');rule=policy['classification_rules'].get(cls)
    if not rule: raise DLPDenied('classification has no export rule')
    dest=request.get('destination',''); purpose=request.get('purpose','')
    if not dest or not purpose: raise DLPDenied('destination and purpose required')
    if rule.get('export_allowed') is not True: raise DLPDenied('classification export prohibited')
    if dest not in rule.get('allowed_destinations',[]): raise DLPDenied('destination not allowlisted')
    if rule.get('encryption_required') and request.get('encrypted') is not True: raise DLPDenied('encrypted transfer required')
    if rule.get('approval_required') and not request.get('approved_by'): raise DLPDenied('independent export approval required')
    if request.get('approved_by') and request.get('approved_by')==request.get('actor'): raise DLPDenied('self-approved export prohibited')
    hits=scan_content(content,policy)
    if hits and rule.get('block_pattern_matches',True): raise DLPDenied('sensitive content pattern matched: '+','.join(hits))
    return {'decision':'allow','asset_id':asset['asset_id'],'classification':cls,'destination':dest,'purpose':purpose,'inspection_hits':list(hits)}
