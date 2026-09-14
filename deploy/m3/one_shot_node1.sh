#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAT="${1:-$ROOT/var/m3-material}"
CFG="${PAG_M3_CONFIG_DIR:-$HOME/.config/portable-ai-governance/m3}"

PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m3/build_m3_material.py" --root "$ROOT" --out "$MAT"

if [ "${PAG_M3_ALLOW_FIXTURE_SCAN:-0}" = 1 ]; then
  echo 'WARN: PAG_M3_ALLOW_FIXTURE_SCAN=1; using test-only fixture vulnerability evidence'
elif [ -n "${PAG_M3_VULN_REPORT_SOURCE:-}" ]; then
  install -m 600 "$PAG_M3_VULN_REPORT_SOURCE" "$MAT/vulnerability-report.json"
else
  command -v osv-scanner >/dev/null 2>&1 || {
    echo 'FAIL: real M3 production validation requires OSV-Scanner or PAG_M3_VULN_REPORT_SOURCE'
    echo 'Install OSV-Scanner with: ./deploy/m3/install_osv_scanner.sh'
    exit 2
  }
  "$ROOT/scripts/m3/scan_and_import_osv.sh" "$ROOT" "$MAT/vulnerability-report.json"
fi

if grep -q 'm3-offline-fixture' "$MAT/vulnerability-report.json" && [ "${PAG_M3_ALLOW_FIXTURE_SCAN:-0}" != 1 ]; then
  echo 'FAIL: production M3 requires real vulnerability evidence'
  exit 2
fi

"$ROOT/deploy/m3/deploy_node.sh" "$MAT" "$CFG"
"$ROOT/scripts/m3/preflight_m3.sh" "$CFG/m3.env"
echo 'PASS: Node1 M3 one-shot deployment complete'
