import os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_m4_entrypoints_direct(tmp_path):
    e=os.environ.copy(); e.pop('PYTHONPATH',None)
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m4/build_m4_material.py'),'--help'],env=e,capture_output=True,text=True); assert r.returncode==0
    r=subprocess.run([sys.executable,str(ROOT/'scripts/m4/validate_m4_node.py')],env=e,capture_output=True,text=True); assert r.returncode!=0 and 'usage' in (r.stdout+r.stderr)
def test_m4_material_permissions(tmp_path):
    m3=tmp_path/'m3'; m4=tmp_path/'m4'
    subprocess.run([sys.executable,str(ROOT/'scripts/m3/build_m3_material.py'),'--root',str(ROOT),'--out',str(m3)],check=True,capture_output=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/m4/build_m4_material.py'),'--m3-material',str(m3),'--out',str(m4)],check=True,capture_output=True)
    for p in [m4,*m4.rglob('*')]:
        mode=p.stat().st_mode & 0o777
        assert mode==(0o700 if p.is_dir() else 0o600), (p,oct(mode))
