import json
from pathlib import Path

def test_all_catalog_controls_have_framework_mapping():
    root=Path(__file__).resolve().parents[2]
    catalog=json.loads((root/"governance/controls/control-catalog.json").read_text())
    mapping=json.loads((root/"governance/mappings/framework-mapping.json").read_text())["controls"]
    assert not [c["control_id"] for c in catalog["controls"] if c["control_id"] not in mapping]
