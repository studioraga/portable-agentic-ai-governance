#!/usr/bin/env python3
import argparse,json,hashlib
from pathlib import Path
ap=argparse.ArgumentParser()
for x in ('m4','m5','m6','m7','m8','m9'):ap.add_argument(f'--{x}-material',required=True)
a=ap.parse_args();P={x:Path(getattr(a,f'{x}_material')) for x in ('m4','m5','m6','m7','m8','m9')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
f={'m4':P['m4']/'ai-security-manifest.json','m5':P['m5']/'compliance-risk-manifest.json','m6':P['m6']/'evidence-analyst-manifest.json','m7':P['m7']/'tool-agent-manifest.json','m8':P['m8']/'action-agent-manifest.json','m9':P['m9']/'security-ops-manifest.json'}
s={k:sha(v) for k,v in f.items()};o={k:json.loads(v.read_text()) for k,v in f.items()}
checks={'m4_to_m5':o['m5']['m4_manifest_sha256']==s['m4'],'m5_to_m6':o['m6']['m5_manifest_sha256']==s['m5'],'m6_to_m7':o['m7']['m6_manifest_sha256']==s['m6'],'m7_to_m8':o['m8']['m7_manifest_sha256']==s['m7'],'m8_to_m9':o['m9']['m8_manifest_sha256']==s['m8']};ok=all(checks.values());print(json.dumps({'ok':ok,'checks':checks,'sha256':s},indent=2));
if ok:print('PASS: M4 -> M5 -> M6 -> M7 -> M8 -> M9 release chain coherent')
raise SystemExit(0 if ok else 2)
