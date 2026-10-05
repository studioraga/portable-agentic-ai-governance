from __future__ import annotations
import json, subprocess
from pathlib import Path
from portable_ai_governance.supply_chain.signing import verify_blob
from .common import M21_1_BASELINE_COMMIT, sha256_file
from .evaluation import evaluate_catalog

REQUIRED=["cissp-domain-catalog.json","enterprise-security-requirements.json","enterprise-control-mapping.json","gap-register.json","evidence-policy.json","m22-evaluation-summary.json","m22-source-manifest.json","m22-enterprise-manifest.json","m22-enterprise-manifest.json.sig","signing-public.pem"]

def evaluate_m22_material(root, repo_root=None):
    root=Path(root); checks=[(f"present:{x}",(root/x).is_file()) for x in REQUIRED]; errors=[]
    if not all(v for _,v in checks): return {"ok":False,"checks":checks,"errors":["missing material"]}
    manifest=json.loads((root/"m22-enterprise-manifest.json").read_text())
    checks.append(("manifest-signature",verify_blob(root/"m22-enterprise-manifest.json",root/"signing-public.pem",root/"m22-enterprise-manifest.json.sig")))
    for name,digest in manifest.get("artifacts",{}).items(): checks.append((f"digest:{name}",(root/name).is_file() and sha256_file(root/name)==digest))
    for key in ("cissp_certification_claim","iso_iec_27001_certification_claim","iso_iec_42001_certification_claim","cra_conformity_claim"):
        checks.append((f"manifest-boundary:{key}",manifest.get("claim_boundaries",{}).get(key) is False))
    checks.append(("node2-verifier-only",manifest.get("boundaries",{}).get("node2_verifier_only") is True))
    checks.append(("m21.1-baseline-bound",manifest.get("m21_1_baseline_commit")==M21_1_BASELINE_COMMIT))
    if repo_root:
        repo=Path(repo_root)
        exists=subprocess.run(["git","-c",f"safe.directory={repo}","-C",str(repo),"cat-file","-e",f"{M21_1_BASELINE_COMMIT}^{{commit}}"],capture_output=True).returncode==0
        checks.append(("m21.1-baseline-exists",exists))
        src=json.loads((root/"m22-source-manifest.json").read_text())
        for rel,digest in src.get("files",{}).items(): checks.append((f"source:{rel}",(repo/rel).is_file() and sha256_file(repo/rel)==digest))
        control=json.loads((repo/"governance/controls/control-catalog.json").read_text())
        summary=evaluate_catalog(json.loads((root/"cissp-domain-catalog.json").read_text()),json.loads((root/"enterprise-security-requirements.json").read_text()),json.loads((root/"enterprise-control-mapping.json").read_text()),json.loads((root/"gap-register.json").read_text()),control)
        checks.append(("catalog-evaluation",summary["ok"]))
    return {"ok":all(v for _,v in checks),"checks":checks,"errors":errors}
