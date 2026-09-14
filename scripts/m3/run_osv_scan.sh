#!/usr/bin/env bash
set -euo pipefail
umask 077

TARGET="${1:-.}"
OUT="${2:-var/m3-scans/raw-osv-output.json}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET_ABS="$(cd "$TARGET" && pwd)"

command -v osv-scanner >/dev/null 2>&1 || {
  echo 'FAIL: osv-scanner not found in PATH'
  echo 'Install with: ./deploy/m3/install_osv_scanner.sh'
  exit 2
}

mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"
TMP_JSON="$(mktemp)"
TMP_ERR="$(mktemp)"
INV_JSON="$(mktemp)"
trap 'rm -f "$TMP_JSON" "$TMP_ERR" "$INV_JSON"' EXIT

set +e
# OSV-Scanner V2 source scan. JSON is written to stdout; diagnostics go to
# stderr, which lets us classify a genuine "no package sources" result.
osv-scanner scan source \
  --recursive \
  --format=json \
  "$TARGET_ABS" \
  >"$TMP_JSON" 2> >(tee "$TMP_ERR" >&2)
rc=$?
set -e

# rc=0 means scan completed without findings; rc=1 means scan completed with
# vulnerabilities. Both are valid evidence for the M3 policy evaluator.
if [ "$rc" -eq 0 ] || [ "$rc" -eq 1 ]; then
  [ -s "$TMP_JSON" ] || {
    echo "FAIL: osv-scanner completed but produced no JSON"
    exit 2
  }
  python3 -m json.tool "$TMP_JSON" >/dev/null || {
    echo "FAIL: invalid JSON from osv-scanner"
    exit 2
  }
  mv "$TMP_JSON" "$OUT"
  chmod 600 "$OUT"
  echo "PASS: OSV-Scanner raw JSON written to $OUT (scanner exit=$rc)"
  exit 0
fi

# OSV-Scanner currently uses rc=128 when it discovers no supported package
# sources. Never treat rc=128 as clean by itself. We only allow this state when
# a deterministic repository inspection proves that this application declares
# zero third-party runtime dependencies and contains no supported dependency
# manifests outside excluded generated/development directories.
if [ "$rc" -eq 128 ] && grep -qi 'No package sources found' "$TMP_ERR"; then
  if ! python3 "$ROOT/scripts/m3/check_dependency_inventory.py" \
      "$TARGET_ABS" \
      --json-out "$INV_JSON" \
      --require-empty-runtime; then
    echo 'FAIL: OSV found no package sources but dependency inventory is not empty'
    exit 3
  fi

  python3 - "$TARGET_ABS" "$INV_JSON" "$OUT" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

target = sys.argv[1]
inv = json.loads(Path(sys.argv[2]).read_text())
out = Path(sys.argv[3])
raw = {
    "results": [],
    "pag_scan_metadata": {
        "scanner": "osv-scanner",
        "status": "no-package-sources",
        "scope": "application-runtime-dependencies",
        "target": target,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dependency_inventory": inv,
        "note": "OSV-Scanner reported no package sources; PAG independently verified zero declared runtime dependencies and zero supported dependency manifests.",
    },
}
out.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
out.chmod(0o600)
PY
  echo "PASS: OSV reported no package sources and zero-runtime-dependency inventory was independently verified"
  echo "PASS: auditable zero-dependency OSV evidence written to $OUT"
  exit 0
fi

echo "FAIL: osv-scanner failed with exit code $rc"
if [ -s "$TMP_ERR" ]; then
  echo '--- osv-scanner diagnostics ---'
  cat "$TMP_ERR"
fi
exit "$rc"
