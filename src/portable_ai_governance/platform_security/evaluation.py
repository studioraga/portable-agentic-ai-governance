from __future__ import annotations
import json
from pathlib import Path

def _sysctl_ok(actual,minimum):
    return actual is not None and int(actual)>=int(minimum)

def evaluate_profiles(node1,node2,policy):
    pol=policy if isinstance(policy,dict) else json.loads(Path(policy).read_text())
    ps=[node1,node2];checks=[]
    checks.append(('node1-role',node1.get('role')=='release_authority'))
    checks.append(('node2-role',node2.get('role')=='independent_verifier'))
    checks.append(('heterogeneous-arch',node1.get('architecture')!=node2.get('architecture')))
    checks.append(('boot-chain-modeled',all(len(p.get('boot',{}).get('chain',[]))>=6 for p in ps)))
    checks.append(('secure-boot-enabled',all(p.get('boot',{}).get('secure_boot')=='enabled' for p in ps)))
    checks.append(('hardware-root-evidence',all(p.get('root_of_trust',{}).get('platform_hardware_root') is True for p in ps)))
    checks.append((
        'tpm-pcr-or-hardware-dice-evidence',
        all(
            p.get('root_of_trust', {})
             .get('tpm', {})
             .get('pcrs_available') is True
            or
            p.get('root_of_trust', {})
             .get('dice', {})
             .get('hardware_available') is True
            for p in ps
        )
    ))
    checks.append(('mac-enforcing',all(p.get('mac',{}).get('apparmor',{}).get('enforcing') or p.get('mac',{}).get('selinux',{}).get('enforcing') for p in ps)))
    checks.append(('service-isolation-capability',all(p.get('service_isolation',{}).get('systemd_analyze_available') is True for p in ps)))
    for p in ps:
        for k,minv in pol['debug_sysctls'].items(): checks.append((f"{p['node_id']}:{k}",_sysctl_ok(p.get('debug',{}).get(k),minv)))
    mode='LIVE' if all(p.get('capture_mode')=='LIVE' for p in ps) else 'SIMULATED'
    passed=sum(1 for _,v in checks if v);failed=len(checks)-passed
    return {'validation_mode':mode,'checks':[{'name':n,'pass':v} for n,v in checks],'passed':passed,'failed':failed,'production_ready':mode=='LIVE' and failed==0,'cra_conformity_claim':False}
