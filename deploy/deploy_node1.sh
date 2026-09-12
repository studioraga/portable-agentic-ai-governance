#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo '=== Portable Agentic AI Governance: Node1 deploy + validation ==='
./scripts/preflight_node1.sh
BASE_PYTHON="$(command -v python3)"

rm -rf .venv
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

# src-layout repositories are not importable from the repository root by default.
# Export PYTHONPATH explicitly for all scripts and also install a local .pth file.
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
SITE="$(python - <<'PY'
import site
print(site.getsitepackages()[0])
PY
)"
printf '%s\n' "$ROOT/src" > "$SITE/portable_agentic_ai_governance.pth"

install -d -m 700 var var/evidence var/runs var/state
printf '%s\n' "$BASE_PYTHON" > var/state/base_python.path
chmod 600 var/state/base_python.path
export PAG_BASE_PYTHON="$BASE_PYTHON"

python - <<'PY'
import portable_ai_governance
print('package import: PASS', portable_ai_governance.__version__)
PY

./scripts/validate_node1.sh
