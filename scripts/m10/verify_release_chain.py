#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser()
for n in range(4,11):ap.add_argument(f'--m{n}-material',required=True)
a=ap.parse_args();dirs={n:Path(getattr(a,f'm{n}_material')) for n in range(4,11)}
files={4:dirs[4]/'ai-security-manifest.json',5:dirs[5]/'compliance-risk-manifest.json',6:dirs[6]/'evidence-analyst-manifest.json',7:dirs[7]/'tool-agent-manifest.json',8:dirs[8]/'action-agent-manifest.json',9:dirs[9]/'security-ops-manifest.json',10:dirs[10]/'multi-agent-manifest.json'}
try:o={n:json.loads(p.read_text()) for n,p in files.items()};s={n:sha(p) for n,p in files.items()}
except Exception as e:print(json.dumps({'ok':False,'reason':str(e)},indent=2));raise SystemExit(2)
checks={'m4_to_m5':o[5]['m4_manifest_sha256']==s[4],'m5_to_m6':o[6]['m5_manifest_sha256']==s[5],'m6_to_m7':o[7]['m6_manifest_sha256']==s[6],'m7_to_m8':o[8]['m7_manifest_sha256']==s[7],'m8_to_m9':o[9]['m8_manifest_sha256']==s[8],'m9_to_m10':o[10]['m9_manifest_sha256']==s[9]};ok=all(checks.values());print(json.dumps({'ok':ok,**checks,'sha256':{f'm{n}':s[n] for n in s}},indent=2));print('PASS: M4 -> M5 -> M6 -> M7 -> M8 -> M9 -> M10 release chain coherent' if ok else 'FAIL: release chain incoherent');raise SystemExit(0 if ok else 2)
