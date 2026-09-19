#!/usr/bin/env python3
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.security_ops.siem import SIEMStore
ap=argparse.ArgumentParser();ap.add_argument('--siem-log',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();s=SIEMStore(a.siem_log);n=s.export_events(a.out);print(f'PASS: exported {n} verified SIEM events to {a.out}')
