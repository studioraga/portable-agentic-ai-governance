#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.platform_security.collector import collect_profile
ap=argparse.ArgumentParser();ap.add_argument('--role',choices=['release_authority','independent_verifier'],required=True);ap.add_argument('--out',required=True);a=ap.parse_args();p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(collect_profile(a.role),indent=2,sort_keys=True)+'\n');p.chmod(0o600);print(f'PASS: M21 LIVE platform profile captured at {p}')
