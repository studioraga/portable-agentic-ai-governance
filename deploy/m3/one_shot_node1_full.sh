#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
M2_MATERIAL="${1:?usage one_shot_node1_full.sh <m2-material-dir> [m3-material-dir]}"
M3_MATERIAL="${2:-$ROOT/var/m3-material}"

"$ROOT/deploy/m2/one_shot_node1.sh" "$M2_MATERIAL"

if [ ! -d "$M3_MATERIAL" ]; then
  PYTHONPATH="$ROOT/src" python3 "$ROOT/scripts/m3/build_m3_material.py" --root "$ROOT" --out "$M3_MATERIAL"
fi

if [ "${PAG_M3_ALLOW_FIXTURE_SCAN:-0}" = 1 ]; then
  echo 'WARN: PAG_M3_ALLOW_FIXTURE_SCAN=1; using test-only fixture vulnerability evidence'
elif [ -n "${PAG_M3_VULN_REPORT_SOURCE:-}" ]; then
  install -m 600 "$PAG_M3_VULN_REPORT_SOURCE" "$M3_MATERIAL/vulnerability-report.json"
else
  command -v osv-scanner >/dev/null 2>&1 || {
    echo 'FAIL: OSV-Scanner is required for automatic production vulnerability evidence'
    echo 'Install with: ./deploy/m3/install_osv_scanner.sh'
    exit 2
  }
  "$ROOT/scripts/m3/scan_and_import_osv.sh" "$ROOT" "$M3_MATERIAL/vulnerability-report.json"
fi

if grep -q 'm3-offline-fixture' "$M3_MATERIAL/vulnerability-report.json" && [ "${PAG_M3_ALLOW_FIXTURE_SCAN:-0}" != 1 ]; then
  echo 'FAIL: production M3 requires a real vulnerability report'
  exit 2
fi

"$ROOT/deploy/m3/deploy_node.sh" "$M3_MATERIAL"
"$ROOT/scripts/m3/validate_combined_node.sh" \
  "$HOME/.config/portable-ai-governance/m2/production.env" \
  "$HOME/.config/portable-ai-governance/m3/m3.env"
echo 'PASS: Node1 full M0-M3 one-shot deployment complete'
