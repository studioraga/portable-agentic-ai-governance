#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'governance/controls/control-catalog.json').read_text())
mapping=json.loads((root/'governance/mappings/framework-mapping.json').read_text())['controls']
missing=[c['control_id'] for c in catalog['controls'] if c['control_id'] not in mapping]
if missing:
    raise SystemExit('FAIL missing mappings: '+','.join(missing))
print(f'PASS: {len(catalog["controls"])} controls mapped')
