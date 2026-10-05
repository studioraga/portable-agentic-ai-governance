from __future__ import annotations
from portable_ai_governance.enterprise_security.runtime import evaluate_m22_material
from portable_ai_governance.enterprise_identity.runtime import evaluate_m23_material
from portable_ai_governance.asset_security.runtime import evaluate_m24_material
from portable_ai_governance.network_security.runtime import evaluate_m25_material
from portable_ai_governance.operational_security.runtime import evaluate_m26_material
from portable_ai_governance.application_security.runtime import evaluate_m27_material
from portable_ai_governance.organizational_security.runtime import evaluate_m28_material
from portable_ai_governance.platform_security.runtime import evaluate_m21_material
EVALS={'m21':evaluate_m21_material,'m22':evaluate_m22_material,'m23':evaluate_m23_material,'m24':evaluate_m24_material,'m25':evaluate_m25_material,'m26':evaluate_m26_material,'m27':evaluate_m27_material,'m28':evaluate_m28_material}
def verify_inputs(inputs,repo_root):
 out={}
 for m,fn in EVALS.items(): out[m]=fn(inputs/m,repo_root=repo_root)
 return out
