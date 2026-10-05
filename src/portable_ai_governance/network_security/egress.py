from __future__ import annotations
class EgressPolicyError(ValueError): pass

def validate_egress_policy(policy):
    if policy.get('default_egress_decision')!='deny': raise EgressPolicyError('egress default must deny')
    for r in policy.get('rules',[]):
        if not r.get('rule_id') or not r.get('source_zone'): raise EgressPolicyError('invalid rule')
        if r.get('decision')!='allow': raise EgressPolicyError('only explicit allows belong in rules')
    return True

def authorize_egress(req,policy):
    validate_egress_policy(policy)
    for r in policy.get('rules',[]):
        if r['source_zone']!=req.get('source_zone'): continue
        if r.get('protocol') and r['protocol']!=req.get('protocol'): continue
        if r.get('ports') and req.get('port') not in r['ports']: continue
        if r.get('destinations') and req.get('destination') not in r['destinations']: continue
        return {'decision':'allow','rule_id':r['rule_id'],'reason':'explicit-egress-allow'}
    return {'decision':'deny','reason':'egress-default-deny'}
