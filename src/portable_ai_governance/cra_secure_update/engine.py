from __future__ import annotations
import json
from pathlib import Path
from .lifecycle import lifecycle_record,eol_notification

def build_fixture_lifecycle(repo_root):
 products=json.loads((Path(repo_root)/'tests/fixtures/m16/products.json').read_text())
 as_of='2031-01-15'
 records=[lifecycle_record(x,as_of) for x in products]
 notices=[eol_notification(x) for x in records]
 return records,notices
