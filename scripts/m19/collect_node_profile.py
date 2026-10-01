#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from portable_ai_governance.cra_production_validation.collector import collect_profile
from portable_ai_governance.cra_production_validation.common import write_json
ap=argparse.ArgumentParser();ap.add_argument('--role',choices=['node1','node2'],required=True);ap.add_argument('--out',required=True);ap.add_argument('--node-id');a=ap.parse_args()
role='release_validation_authority' if a.role=='node1' else 'independent_product_verifier'
write_json(a.out,collect_profile(ROOT,role,a.node_id));print(f'PASS: live M19 {a.role} runtime profile written to {a.out}')
