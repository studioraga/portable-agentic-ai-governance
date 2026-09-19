#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> None:
    ap = argparse.ArgumentParser(description='Verify one coherent M4->M5->M6->M7 release generation.')
    ap.add_argument('--m4-material', required=True)
    ap.add_argument('--m5-material', required=True)
    ap.add_argument('--m6-material', required=True)
    ap.add_argument('--m7-material', required=True)
    ap.add_argument('--freeze-m5', action='store_true', help='write .pag-downstream-bound.json after successful verification')
    args = ap.parse_args()

    m4 = Path(args.m4_material).resolve()
    m5 = Path(args.m5_material).resolve()
    m6 = Path(args.m6_material).resolve()
    m7 = Path(args.m7_material).resolve()

    p4 = m4 / 'ai-security-manifest.json'
    p5 = m5 / 'compliance-risk-manifest.json'
    p6 = m6 / 'evidence-analyst-manifest.json'
    p7 = m7 / 'tool-agent-manifest.json'
    for p in (p4, p5, p6, p7):
        if not p.is_file():
            raise SystemExit(f'FAIL: release-chain artifact missing: {p}')

    s4, s5, s6, s7 = map(sha256_file, (p4, p5, p6, p7))
    o5, o6, o7 = map(load, (p5, p6, p7))

    checks = {
        'm4_to_m5': o5.get('m4_manifest_sha256') == s4,
        'm5_to_m6': o6.get('m5_manifest_sha256') == s5,
        'm6_to_m7': o7.get('m6_manifest_sha256') == s6,
    }
    out = {
        'ok': all(checks.values()),
        'checks': checks,
        'sha256': {'m4': s4, 'm5': s5, 'm6': s6, 'm7': s7},
        'expected': {
            'm5_m4': o5.get('m4_manifest_sha256'),
            'm6_m5': o6.get('m5_manifest_sha256'),
            'm7_m6': o7.get('m6_manifest_sha256'),
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    if not out['ok']:
        raise SystemExit('FAIL: M4->M5->M6->M7 release generation is not coherent')

    if args.freeze_m5:
        marker = m5 / '.pag-downstream-bound.json'
        payload = {
            'schema': 'pag-downstream-bound-v1',
            'reason': 'M5 release material is cryptographically bound by downstream M6/M7; mutate only by creating a new attestation generation.',
            'sha256': {'m4': s4, 'm5': s5, 'm6': s6, 'm7': s7},
        }
        marker.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        os.chmod(marker, 0o600)
        print(f'PASS: froze downstream-bound M5 release material at {marker}')

    print('PASS: M4 -> M5 -> M6 -> M7 release chain coherent')

if __name__ == '__main__':
    main()
