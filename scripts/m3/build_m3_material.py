#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Support direct execution from a source checkout without requiring callers to
# preconfigure PYTHONPATH. Installed-package execution continues to work.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / 'src'
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from portable_ai_governance.supply_chain.bom import generate_ai_bom, generate_sbom
from portable_ai_governance.supply_chain.locks import sha256_file
from portable_ai_governance.supply_chain.provenance import generate_provenance
from portable_ai_governance.supply_chain.signing import generate_ed25519_keypair, sign_blob


def _secure_tree(root: Path) -> None:
    for directory in [root, *[p for p in root.rglob('*') if p.is_dir()]]:
        directory.chmod(0o700)
    for file_path in [p for p in root.rglob('*') if p.is_file()]:
        file_path.chmod(0o600)


def _write_private(path: Path, text: str) -> None:
    path.write_text(text)
    path.chmod(0o600)


def main() -> None:
    os.umask(0o077)

    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    (out / 'assets').mkdir(exist_ok=True, mode=0o700)
    out.chmod(0o700)
    (out / 'assets').chmod(0o700)

    prompt = out / 'assets/system-prompt.txt'
    _write_private(
        prompt,
        'You are a bounded governance agent. Deterministic controls authorize actions.\n',
    )

    tool = out / 'assets/tool-registry.json'
    _write_private(
        tool,
        json.dumps(
            {'tools': ['inventory.read', 'risk.read', 'evidence.verify']},
            indent=2,
        ) + '\n',
    )

    model_seed = b'portable-ai-governance-reference-model-v1'
    model_digest = hashlib.sha256(model_seed).hexdigest()
    container_digest = hashlib.sha256(
        b'portable-ai-governance-container-v1'
    ).hexdigest()

    lock = {
        'lock_version': '0.3.0',
        'artifacts': [
            {
                'type': 'model',
                'name': 'reference-governance-model',
                'version': '1',
                'sha256': model_digest,
                'source': 'registry://approved/reference-governance-model',
                'license': 'organization-reviewed',
                'framework': 'provider-neutral',
                'dataset_provenance': 'documented-by-owner',
                'intended_use': 'governance analysis only',
            },
            {
                'type': 'container',
                'name': 'reference-control-plane-container',
                'sha256': container_digest,
                'ref': (
                    'registry.local/portable-ai-governance/'
                    'control-plane@sha256:' + container_digest
                ),
            },
            {
                'type': 'prompt',
                'name': 'bounded-governance-system-prompt',
                'path': 'assets/system-prompt.txt',
                'sha256': sha256_file(prompt),
            },
            {
                'type': 'tool',
                'name': 'approved-tool-registry',
                'path': 'assets/tool-registry.json',
                'sha256': sha256_file(tool),
            },
        ],
    }
    _write_private(
        out / 'artifact-locks.json',
        json.dumps(lock, indent=2, sort_keys=True) + '\n',
    )

    generate_sbom(root, out / 'software.cdx.json')
    generate_ai_bom(out / 'artifact-locks.json', out / 'ai-ml.cdx.json')

    policy = {
        'max_report_age_hours': 24,
        'block_severities': ['critical', 'high'],
        'block_unknown': True,
        'require_scanner': True,
        'allowed_scanners': [
            'm3-offline-fixture',
            'osv-scanner',
            'grype',
            'trivy',
        ],
    }
    _write_private(
        out / 'vulnerability-policy.json',
        json.dumps(policy, indent=2) + '\n',
    )

    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'scanner': 'm3-offline-fixture',
        'vulnerabilities': [],
    }
    _write_private(
        out / 'vulnerability-report.json',
        json.dumps(report, indent=2) + '\n',
    )

    generate_provenance(
        root,
        [
            out / 'software.cdx.json',
            out / 'ai-ml.cdx.json',
            out / 'artifact-locks.json',
        ],
        out / 'provenance.intoto.json',
    )

    private_key = out / 'signing-private.pem'
    public_key = out / 'signing-public.pem'
    generate_ed25519_keypair(private_key, public_key)

    for filename in (
        'software.cdx.json',
        'ai-ml.cdx.json',
        'provenance.intoto.json',
    ):
        sign_blob(
            out / filename,
            private_key,
            out / (filename + '.sig'),
        )

    # Final deterministic hardening: release material is private by default.
    _secure_tree(out)

    print(f'PASS: M3 supply-chain material generated at {out}')
    print(
        'IMPORTANT: signing-private.pem is release-authority custody material; '
        'do not deploy it to verifier-only nodes.'
    )


if __name__ == '__main__':
    main()
