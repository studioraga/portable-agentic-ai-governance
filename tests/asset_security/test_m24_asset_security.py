import copy,json,pytest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
from portable_ai_governance.asset_security.inventory import validate_asset_register,require_registered_asset,AssetInventoryError
from portable_ai_governance.asset_security.lifecycle import retention_decision,validate_sanitization_record,DataLifecycleError
from portable_ai_governance.asset_security.dlp import authorize_export,DLPDenied
from portable_ai_governance.asset_security.crypto_lifecycle import validate_crypto_lifecycle,CryptoLifecycleError
from portable_ai_governance.asset_security.evaluation import evaluate_m24_policy

def J(name):return json.loads((ROOT/'governance/enterprise/m24'/name).read_text())
def test_inventory_and_sensitive_owner(): assert len(validate_asset_register(J('asset-register.json')))>=3
def test_unregistered_denied():
 with pytest.raises(AssetInventoryError):require_registered_asset(J('asset-register.json'),'missing')
def test_legal_hold_overrides_retention(): assert retention_decision({'retention_profile':'temporary-export','created_at':1,'legal_hold':True},J('data-lifecycle-policy.json'),9999999999).action=='retain'
def test_expired_data_requires_sanitization(): assert retention_decision({'retention_profile':'temporary-export','created_at':1},J('data-lifecycle-policy.json'),9999999999).action=='sanitize'
def test_restricted_sanitization_requires_approval():
 with pytest.raises(DataLifecycleError):validate_sanitization_record({'record_id':'x','asset_id':'a','performed_at':1,'performed_by':'u','method':'crypto-erase','evidence_sha256':'0'*64,'classification':'restricted'},J('data-lifecycle-policy.json'))
def test_confidential_export_requires_approval_and_encryption():
 a=require_registered_asset(J('asset-register.json'),'pag-node1-control-plane')
 with pytest.raises(DLPDenied):authorize_export({'actor':'alice','destination':'enterprise-secure-exchange','purpose':'support','encrypted':True},a,J('dlp-policy.json'),'safe')
def test_self_approved_export_denied():
 a=require_registered_asset(J('asset-register.json'),'pag-node1-control-plane')
 with pytest.raises(DLPDenied):authorize_export({'actor':'alice','approved_by':'alice','destination':'enterprise-secure-exchange','purpose':'support','encrypted':True},a,J('dlp-policy.json'),'safe')
def test_sensitive_pattern_denied():
 a=require_registered_asset(J('asset-register.json'),'pag-node1-control-plane')
 with pytest.raises(DLPDenied):authorize_export({'actor':'alice','approved_by':'bob','destination':'enterprise-secure-exchange','purpose':'support','encrypted':True},a,J('dlp-policy.json'),'password=hunter2')
def test_positive_controlled_export():
 a=require_registered_asset(J('asset-register.json'),'pag-node1-control-plane');r=authorize_export({'actor':'alice','approved_by':'bob','destination':'enterprise-secure-exchange','purpose':'support','encrypted':True},a,J('dlp-policy.json'),'non-sensitive validation payload');assert r['decision']=='allow'
def test_overdue_active_key_denied():
 p=copy.deepcopy(J('cryptographic-lifecycle-policy.json'));p['keys'][1]['rotate_by']=10
 with pytest.raises(CryptoLifecycleError):validate_crypto_lifecycle(p,1700000000)
def test_m24_policy_evaluation():
 controls=json.loads((ROOT/'governance/controls/control-catalog.json').read_text());assert evaluate_m24_policy(J('asset-security-policy.json'),J('asset-register.json'),J('data-lifecycle-policy.json'),J('dlp-policy.json'),J('cryptographic-lifecycle-policy.json'),controls)['ok']
