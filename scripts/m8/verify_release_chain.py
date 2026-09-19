#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
if __name__=='__main__':
 ap=argparse.ArgumentParser();
 for x in ('m4','m5','m6','m7','m8'):ap.add_argument(f'--{x}-material',required=True)
 a=ap.parse_args();d={x:Path(getattr(a,f'{x}_material')) for x in ('m4','m5','m6','m7','m8')};p={'m4':d['m4']/'ai-security-manifest.json','m5':d['m5']/'compliance-risk-manifest.json','m6':d['m6']/'evidence-analyst-manifest.json','m7':d['m7']/'tool-agent-manifest.json','m8':d['m8']/'action-agent-manifest.json'}
 for x,v in p.items():
  if not v.is_file():raise SystemExit(f'FAIL missing {x}: {v}')
 s={x:h(v) for x,v in p.items()};o5,o6,o7,o8=(load(p[x]) for x in ('m5','m6','m7','m8'));c={'m4_to_m5':o5.get('m4_manifest_sha256')==s['m4'],'m5_to_m6':o6.get('m5_manifest_sha256')==s['m5'],'m6_to_m7':o7.get('m6_manifest_sha256')==s['m6'],'m7_to_m8':o8.get('m7_manifest_sha256')==s['m7']};out={'ok':all(c.values()),'checks':c,'sha256':s};print(json.dumps(out,indent=2,sort_keys=True));
 if not out['ok']:raise SystemExit('FAIL: M4->M5->M6->M7->M8 release generation is not coherent')
 print('PASS: M4 -> M5 -> M6 -> M7 -> M8 release chain coherent')
