from __future__ import annotations
import ipaddress
class NetworkPolicyError(ValueError): pass

def validate_network_policy(policy):
    if policy.get('default_decision')!='deny': raise NetworkPolicyError('default decision must be deny')
    zones=policy.get('zones',[]); zn={z.get('zone_id') for z in zones}
    if len(zn)!=len(zones) or None in zn: raise NetworkPolicyError('zone ids must be unique')
    for z in zones:
        if not z.get('trust_level') or not z.get('purpose'): raise NetworkPolicyError('zone metadata required')
        for cidr in z.get('cidrs',[]): ipaddress.ip_network(cidr,strict=False)
    ids=set()
    for f in policy.get('flows',[]):
        fid=f.get('flow_id')
        if not fid or fid in ids: raise NetworkPolicyError('flow ids must be unique')
        ids.add(fid)
        if f.get('source_zone') not in zn or f.get('destination_zone') not in zn: raise NetworkPolicyError('unknown zone')
        if f.get('protocol') not in {'tcp','udp','icmp'}: raise NetworkPolicyError('unsupported protocol')
        ports=f.get('ports',[])
        if f.get('protocol') in {'tcp','udp'} and not ports: raise NetworkPolicyError('ports required')
        if any((not isinstance(p,int) or p<1 or p>65535) for p in ports): raise NetworkPolicyError('invalid port')
        if f.get('requires_mtls') and not f.get('allowed_workload_identities'): raise NetworkPolicyError('mTLS flow needs identities')
    return True

def find_zone(policy,zone_id):
    return next((z for z in policy.get('zones',[]) if z.get('zone_id')==zone_id),None)

def authorize_flow(request,policy):
    validate_network_policy(policy)
    matches=[]
    for f in policy.get('flows',[]):
        if f['source_zone']!=request.get('source_zone') or f['destination_zone']!=request.get('destination_zone'): continue
        if f['protocol']!=request.get('protocol'): continue
        if f['protocol'] in {'tcp','udp'} and request.get('port') not in f.get('ports',[]): continue
        matches.append(f)
    if not matches:return {'decision':'deny','reason':'no-approved-flow'}
    f=matches[0]
    if f.get('requires_mtls'):
        wid=request.get('workload_identity')
        if not request.get('mtls_verified') or wid not in f.get('allowed_workload_identities',[]):
            return {'decision':'deny','reason':'mtls-workload-identity-required','flow_id':f['flow_id']}
    if f.get('requires_encryption') and not request.get('encrypted'):
        return {'decision':'deny','reason':'encryption-required','flow_id':f['flow_id']}
    return {'decision':'allow','reason':'approved-flow','flow_id':f['flow_id']}
