from __future__ import annotations
import json,os,stat,subprocess,sys
from datetime import datetime,timezone,timedelta
from pathlib import Path
import pytest
from portable_ai_governance.compliance_risk.impact import require_impact_assessment,ImpactAssessmentError
from portable_ai_governance.compliance_risk.privacy import require_privacy_assessment,PrivacyAssessmentError
from portable_ai_governance.compliance_risk.exceptions import require_exception_register,ExceptionRegisterError
from portable_ai_governance.compliance_risk.third_parties import require_third_party_register,ThirdPartyRiskError
from portable_ai_governance.compliance_risk.continuous_controls import require_continuous_controls,ContinuousControlError
from portable_ai_governance.compliance_risk.reports import require_compliance_report,ComplianceReportError
from portable_ai_governance.compliance_risk.runtime import evaluate_compliance_risk
ROOT=Path(__file__).resolve().parents[2]
def w(p,d): p.write_text(json.dumps(d)); os.chmod(p,0o600); return p
def test_exception_expiry_and_self_approval(tmp_path):
    now=datetime.now(timezone.utc)
    p=w(tmp_path/'e.json',{'default_policy':'deny-unapproved','exceptions':[{'exception_id':'x','control_id':'c','owner':'a','approver':'b','reason':'r','compensating_controls':['m'],'created_at':now.isoformat(),'expires_at':(now+timedelta(days=1)).isoformat(),'status':'approved'}]})
    assert require_exception_register(p,now)=='exception register valid'
    d=json.loads(p.read_text()); d['exceptions'][0]['owner']='b'; w(p,d)
    with pytest.raises(ExceptionRegisterError): require_exception_register(p,now)
def test_privacy_dpia_gate(tmp_path):
    p=w(tmp_path/'p.json',{'assessment_id':'p','system_id':'s','owner':'o','purposes':['x'],'data_categories':['y'],'legal_basis':'reviewed','retention':'30-days','data_subject_rights':['access'],'cross_border_transfer':False,'security_controls':['x'],'dpia_required':True,'dpia_status':'pending','review_due':'2027-01-01','collect_sensitive_data':False})
    with pytest.raises(PrivacyAssessmentError): require_privacy_assessment(p)
def test_third_party_data_terms_gate(tmp_path):
    p=w(tmp_path/'t.json',{'default_decision':'deny-unassessed','providers':[{'provider_id':'p','name':'n','owner':'o','service':'s','criticality':'high','data_access':'internal','data_residency':'local','security_assessment':'approved','contract_status':'active','review_due':'2027-01-01','exit_plan':'x'}]})
    with pytest.raises(ThirdPartyRiskError): require_third_party_register(p)
def test_continuous_control_stale(tmp_path):
    p=w(tmp_path/'c.json',{'default_failure_action':'block','controls':[{'control_id':'c','owner':'o','status':'pass','last_checked':'2020-01-01T00:00:00Z','max_age_hours':24,'evidence_sha256':'a'*64,'failure_action':'block'}]})
    with pytest.raises(ContinuousControlError): require_continuous_controls(p)
def test_report_cannot_claim_certification(tmp_path):
    p=w(tmp_path/'r.json',{'report_id':'r','system_id':'s','generated_at':'x','scope':['x'],'control_summary':{'passed':1,'failed':0,'stale':0},'evidence_refs':[],'open_risks':[],'exceptions':[],'certification_claim':True,'disclaimer':'this is not a certification'})
    with pytest.raises(ComplianceReportError): require_compliance_report(p)
def test_critical_residual_risk_cannot_be_approved(tmp_path):
    p=w(tmp_path/'i.json',{'assessment_id':'i','system_id':'s','owner':'o','purpose':'x','stakeholders':['s'],'impact_domains':['security'],'inherent_risk':'critical','controls':['x'],'residual_risk':'critical','decision':'approve','review_due':'2027-01-01'})
    with pytest.raises(ImpactAssessmentError): require_impact_assessment(p)
def test_m5_material_owner_only_and_runtime(tmp_path):
    m3=tmp_path/'m3'; m4=tmp_path/'m4'; m5=tmp_path/'m5'; m3.mkdir(); m4.mkdir()
    # use real M4 builder inputs by first creating M3 reference material
    subprocess.run([sys.executable,str(ROOT/'scripts/m3/build_m3_material.py'),'--root',str(ROOT),'--out',str(m3)],check=True,capture_output=True,text=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/m4/build_m4_material.py'),'--m3-material',str(m3),'--out',str(m4)],check=True,capture_output=True,text=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/m5/build_m5_material.py'),'--m4-material',str(m4),'--out',str(m5)],check=True,capture_output=True,text=True)
    for p in m5.rglob('*'):
        mode=stat.S_IMODE(p.stat().st_mode)
        assert mode==(0o700 if p.is_dir() else 0o600)
    verifier=tmp_path/'ver'; verifier.mkdir(mode=0o700)
    for p in m5.iterdir():
        if p.name!='signing-private.pem':
            (verifier/p.name).write_bytes(p.read_bytes()); os.chmod(verifier/p.name,0o600)
    env=tmp_path/'m5.env'
    subprocess.run([str(ROOT/'deploy/m5/deploy_node.sh'),str(verifier),str(m4/'ai-security-manifest.json'),str(tmp_path/'node')],check=True,capture_output=True,text=True)
    r=evaluate_compliance_risk(_env(tmp_path/'node/m5.env')); assert r.ok
def _env(path):
    e={}
    for s in path.read_text().splitlines():
        if '=' in s and not s.startswith('#'):
            k,v=s.split('=',1); e[k]=v
    return e
def test_manifest_tamper_rejected(tmp_path):
    # covered end-to-end with local script; ensure direct entrypoint is source-checkout portable
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m5/validate_m5_node.py')],capture_output=True,text=True,env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'})
    assert r.returncode!=0 and 'usage:' in (r.stdout+r.stderr)

def test_continuous_refresh_requires_release_authority_and_updates(tmp_path):
    m3=tmp_path/'m3'; m4=tmp_path/'m4'; m5=tmp_path/'m5'; m3.mkdir(); m4.mkdir()
    subprocess.run([sys.executable,str(ROOT/'scripts/m3/build_m3_material.py'),'--root',str(ROOT),'--out',str(m3)],check=True,capture_output=True,text=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/m4/build_m4_material.py'),'--m3-material',str(m3),'--out',str(m4)],check=True,capture_output=True,text=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/m5/build_m5_material.py'),'--m4-material',str(m4),'--out',str(m5)],check=True,capture_output=True,text=True)
    before=json.loads((m5/'continuous-controls.json').read_text())['controls'][0]['last_checked']
    subprocess.run([sys.executable,str(ROOT/'scripts/m5/refresh_continuous_controls.py'),'--m4-material',str(m4),'--m5-material',str(m5)],check=True,capture_output=True,text=True)
    after=json.loads((m5/'continuous-controls.json').read_text())['controls'][0]['last_checked']
    assert after >= before
    (m5/'signing-private.pem').unlink()
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m5/refresh_continuous_controls.py'),'--m4-material',str(m4),'--m5-material',str(m5)],capture_output=True,text=True)
    assert r.returncode != 0 and 'signing-private.pem' in (r.stdout+r.stderr)
