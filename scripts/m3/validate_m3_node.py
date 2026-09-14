#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path

# Support direct execution from a source checkout without requiring callers to
# preconfigure PYTHONPATH. Installed-package execution continues to work.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / 'src'
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from portable_ai_governance.supply_chain.runtime import evaluate_supply_chain

def load_env(path:Path):
 out=dict(os.environ)
 for line in path.read_text().splitlines():
  line=line.strip()
  if not line or line.startswith('#') or '=' not in line: continue
  k,v=line.split('=',1); out[k]=os.path.expandvars(v.strip().strip('"').strip("'"))
 return out

def main():
 p=argparse.ArgumentParser(); p.add_argument('env'); a=p.parse_args(); env=load_env(Path(a.env)); r=evaluate_supply_chain(env)
 print(json.dumps({'ok':r.ok,'checks':[{'name':n,'ok':o,'detail':d} for n,o,d in r.checks]},indent=2)); return 0 if r.ok else 2
if __name__=='__main__': raise SystemExit(main())
