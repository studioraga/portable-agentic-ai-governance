from __future__ import annotations
from .policy import validate_network_policy

def render_nftables(policy):
    validate_network_policy(policy)
    lines=['table inet pag_m25 {','  chain forward {','    type filter hook forward priority 0; policy drop;']
    for f in policy.get('flows',[]):
        if f['protocol'] not in {'tcp','udp'}: continue
        ports=', '.join(str(x) for x in f['ports'])
        lines.append(f"    # {f['flow_id']}: {f['source_zone']} -> {f['destination_zone']}")
        lines.append(f"    {f['protocol']} dport {{ {ports} }} accept")
    lines += ['  }','}']
    return '\n'.join(lines)+'\n'
