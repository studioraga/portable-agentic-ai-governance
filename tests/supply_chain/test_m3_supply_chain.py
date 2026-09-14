from __future__ import annotations
import json, os
from datetime import datetime, timezone, timedelta
from pathlib import Path
import pytest
from portable_ai_governance.supply_chain.locks import sha256_file, require_locks, LockError
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair, sign_blob, verify_blob
from portable_ai_governance.supply_chain.vulnerability import evaluate_vulnerability_report
from portable_ai_governance.supply_chain.bom import generate_sbom, generate_ai_bom
from portable_ai_governance.supply_chain.provenance import generate_provenance

def fixture_lock(tmp_path:Path):
    prompt=tmp_path/'prompt.txt'; prompt.write_text('system prompt\n')
    tool=tmp_path/'tool.json'; tool.write_text('{"name":"safe_tool"}\n')
    model_digest='a'*64; container_digest='b'*64
    doc={'version':'1','artifacts':[
      {'type':'model','name':'model','version':'1','sha256':model_digest,'source':'registry://model'},
      {'type':'container','name':'container','sha256':container_digest,'ref':'registry.local/app@sha256:'+container_digest},
      {'type':'prompt','name':'prompt','path':prompt.name,'sha256':sha256_file(prompt)},
      {'type':'tool','name':'tool','path':tool.name,'sha256':sha256_file(tool)},]}
    p=tmp_path/'locks.json'; p.write_text(json.dumps(doc)); return p

def test_all_lock_categories_verify(tmp_path):
    assert len(require_locks(fixture_lock(tmp_path),tmp_path))==4

def test_prompt_tamper_rejected(tmp_path):
    p=fixture_lock(tmp_path); (tmp_path/'prompt.txt').write_text('tampered')
    with pytest.raises(LockError): require_locks(p,tmp_path)

def test_container_requires_digest_pin(tmp_path):
    p=fixture_lock(tmp_path); d=json.loads(p.read_text()); d['artifacts'][1]['ref']='registry.local/app:latest'; p.write_text(json.dumps(d))
    with pytest.raises(LockError): require_locks(p,tmp_path)

def test_ed25519_sign_verify_and_tamper(tmp_path):
    priv=tmp_path/'key.pem'; pub=tmp_path/'pub.pem'; blob=tmp_path/'a.json'; sig=tmp_path/'a.sig'; blob.write_text('{}')
    generate_ed25519_keypair(priv,pub); sign_blob(blob,priv,sig); assert verify_blob(blob,pub,sig)
    blob.write_text('{"x":1}'); assert not verify_blob(blob,pub,sig)

def test_boms_and_provenance(tmp_path):
    (tmp_path/'a.py').write_text('print(1)\n'); lock=fixture_lock(tmp_path)
    sb=generate_sbom(tmp_path,tmp_path/'sbom.json'); ai=generate_ai_bom(lock,tmp_path/'ai.json'); pr=generate_provenance(tmp_path,[tmp_path/'sbom.json',tmp_path/'ai.json'],tmp_path/'prov.json')
    assert sb['specVersion']=='1.7' and ai['components'][0]['type']=='machine-learning-model' and pr['predicateType']=='https://slsa.dev/provenance/v1'

def test_vulnerability_policy_blocks_high_and_stale(tmp_path):
    pol=tmp_path/'policy.json'; pol.write_text(json.dumps({'max_report_age_hours':24,'block_severities':['critical','high'],'block_unknown':True,'require_scanner':True}))
    clean=tmp_path/'clean.json'; clean.write_text(json.dumps({'generated_at':datetime.now(timezone.utc).isoformat(),'scanner':'fixture','vulnerabilities':[]})); assert evaluate_vulnerability_report(clean,pol).ok
    bad=tmp_path/'bad.json'; bad.write_text(json.dumps({'generated_at':datetime.now(timezone.utc).isoformat(),'scanner':'fixture','vulnerabilities':[{'id':'CVE-X','severity':'high'}]})); assert not evaluate_vulnerability_report(bad,pol).ok
    stale=tmp_path/'stale.json'; stale.write_text(json.dumps({'generated_at':(datetime.now(timezone.utc)-timedelta(hours=48)).isoformat(),'scanner':'fixture','vulnerabilities':[]})); assert not evaluate_vulnerability_report(stale,pol).ok

def test_osv_no_package_sources_requires_empty_dependency_inventory(tmp_path):
    pol=tmp_path/'policy.json'
    pol.write_text(json.dumps({
        'max_report_age_hours':24,
        'block_severities':['critical','high'],
        'block_unknown':True,
        'require_scanner':True,
        'allowed_scanners':['osv-scanner'],
    }))
    good=tmp_path/'good.json'
    good.write_text(json.dumps({
        'generated_at':datetime.now(timezone.utc).isoformat(),
        'scanner':'osv-scanner',
        'scan_status':'no-package-sources',
        'scan_scope':'application-runtime-dependencies',
        'dependency_inventory':{
            'runtime_dependency_count':0,
            'dependency_manifest_count':0,
        },
        'vulnerabilities':[],
    }))
    assert evaluate_vulnerability_report(good,pol).ok

    bad=tmp_path/'bad-inventory.json'
    bad.write_text(json.dumps({
        'generated_at':datetime.now(timezone.utc).isoformat(),
        'scanner':'osv-scanner',
        'scan_status':'no-package-sources',
        'scan_scope':'application-runtime-dependencies',
        'dependency_inventory':{
            'runtime_dependency_count':1,
            'dependency_manifest_count':0,
        },
        'vulnerabilities':[],
    }))
    assert not evaluate_vulnerability_report(bad,pol).ok


def test_osv_report_requires_scan_status(tmp_path):
    pol=tmp_path/'policy.json'
    pol.write_text(json.dumps({
        'max_report_age_hours':24,
        'block_severities':['critical','high'],
        'block_unknown':True,
        'require_scanner':True,
        'allowed_scanners':['osv-scanner'],
    }))
    report=tmp_path/'report.json'
    report.write_text(json.dumps({
        'generated_at':datetime.now(timezone.utc).isoformat(),
        'scanner':'osv-scanner',
        'vulnerabilities':[],
    }))
    assert not evaluate_vulnerability_report(report,pol).ok


def test_generated_m3_material_is_owner_only(tmp_path):
    import os
    import stat
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[2]
    out = tmp_path / 'material'
    env = dict(os.environ)
    env['PYTHONPATH'] = str(root / 'src')

    subprocess.run(
        [
            sys.executable,
            str(root / 'scripts/m3/build_m3_material.py'),
            '--root',
            str(root),
            '--out',
            str(out),
        ],
        check=True,
        env=env,
        capture_output=True,
        text=True,
    )

    assert stat.S_IMODE(out.stat().st_mode) == 0o700
    for path in out.rglob('*'):
        mode = stat.S_IMODE(path.stat().st_mode)
        if path.is_dir():
            assert mode == 0o700, (path, oct(mode))
        elif path.is_file():
            assert mode == 0o600, (path, oct(mode))
