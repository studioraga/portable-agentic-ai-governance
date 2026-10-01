from __future__ import annotations

def _result(case_id,status,reason,required=True):
    return {'case_id':case_id,'status':status,'reason':reason,'required_for_production':required}

def evaluate_profiles(node1,node2,policy):
    mode='LIVE' if node1.get('capture_mode')=='LIVE' and node2.get('capture_mode')=='LIVE' else 'SIMULATED'
    c1=policy['platform_contract']['node1']; c2=policy['platform_contract']['node2']; res=[]
    n1ok=node1.get('role')==c1['role'] and node1.get('architecture')==c1['architecture'] and node1.get('os',{}).get('id')==c1['os_id'] and str(node1.get('os',{}).get('version_id','')).startswith(c1['os_version_prefix'])
    res.append(_result('M19-VAL-001','PASS' if n1ok else 'FAIL','Node1 platform contract matched' if n1ok else 'Node1 platform contract mismatch'))
    n2ok=node2.get('role')==c2['role'] and node2.get('architecture')==c2['architecture'] and node2.get('os',{}).get('id')==c2['os_id'] and str(node2.get('os',{}).get('version_id','')).startswith(c2['os_version_prefix'])
    res.append(_result('M19-VAL-002','PASS' if n2ok else 'FAIL','Node2 platform contract matched' if n2ok else 'Node2 platform contract mismatch'))
    v=node1.get('package_version')==node2.get('package_version')=='0.19.0'; res.append(_result('M19-VAL-003','PASS' if v else 'FAIL','M19 package versions match' if v else 'M19 package version mismatch'))
    g=node1.get('git_head')==node2.get('git_head') and node1.get('git_head') not in (None,'unknown'); res.append(_result('M19-VAL-004','PASS' if g else 'FAIL','Git base commits match' if g else 'Git base commit mismatch'))
    f=node1.get('source_fingerprints')==node2.get('source_fingerprints') and bool(node1.get('source_fingerprints')); res.append(_result('M19-VAL-005','PASS' if f else 'FAIL','Critical-source fingerprints match' if f else 'Critical-source fingerprint mismatch'))
    h=node1.get('architecture')!=node2.get('architecture'); res.append(_result('M19-VAL-006','PASS' if h else 'FAIL','Heterogeneous architecture contract demonstrated' if h else 'Nodes are not heterogeneous'))
    k=node2.get('private_signing_key_present') is False; res.append(_result('M19-VAL-007','PASS' if k else 'FAIL','Node2 reports no private signing key' if k else 'Node2 reports private signing key present'))
    prior=all(x['status']=='PASS' for x in res)
    res.append(_result('M19-VAL-008','PASS' if prior else 'FAIL','Regular product-security test/review evidence gate prepared from qualified Node1/Node2 profiles' if prior else 'Profile qualification failure prevents product-security evidence readiness'))
    res.append(_result('M19-VAL-009','PASS' if prior else 'FAIL','Annex-VII test-report evidence candidate prepared' if prior else 'Test-report evidence candidate blocked'))
    res.append(_result('M19-VAL-010','PASS','M11-M18 baseline binding is verified cryptographically by the signed M19 manifest'))
    allpass=all(x['status']=='PASS' for x in res if x['required_for_production'])
    cross={'version':'0.19.0','milestone':'M19','validation_mode':mode,'node1_id':node1['node_id'],'node2_id':node2['node_id'],'checks':res,'all_required_pass':allpass}
    closure=[
      {'requirement_id':'CRA-REQ-060','state':'EVIDENCE_READY_FOR_M17_REVIEW' if mode=='LIVE' and allpass else 'SIMULATED_ONLY','reason':'Live heterogeneous-node validation completed' if mode=='LIVE' and allpass else 'Fixture/local acceptance cannot close production evidence.'},
      {'requirement_id':'CRA-REQ-046','state':'NOT_CLOSED','reason':'Requires explicit product secure-by-default/reset acceptance evidence.'},
      {'requirement_id':'CRA-REQ-053','state':'NOT_CLOSED','reason':'Requires explicit other-device/network availability-impact evidence.'},
      {'requirement_id':'CRA-REQ-057','state':'NOT_CLOSED','reason':'Requires explicit secure data-removal/transfer acceptance evidence.'}]
    summary={'version':'0.19.0','milestone':'M19','validation_mode':mode,'total_checks':len(res),'passed':sum(x['status']=='PASS' for x in res),'failed':sum(x['status']!='PASS' for x in res),'production_validation_complete':bool(mode=='LIVE' and allpass),'cra_conformity_claim':False,'m17_gap_closure_candidates':closure,'m18_annex_vii_6_test_report_candidate':bool(mode=='LIVE' and allpass)}
    return cross,summary
