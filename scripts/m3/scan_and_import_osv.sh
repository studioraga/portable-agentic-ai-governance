#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET="${1:-$ROOT}"
NORMALIZED="${2:-$ROOT/var/m3-material/vulnerability-report.json}"
RAW="${3:-$ROOT/var/m3-scans/raw-osv-output.json}"

"$ROOT/scripts/m3/run_osv_scan.sh" "$TARGET" "$RAW"
python3 "$ROOT/scripts/m3/import_osv_report.py" "$RAW" "$NORMALIZED"
echo "PASS: real OSV vulnerability evidence written to $NORMALIZED"
