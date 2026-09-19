#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";M4="$1";M5="$2";M6="$3";M7="$4";M8="$5";M9="$6";M10="$7";OUT="$8"
python3 "$ROOT/scripts/m10/verify_release_chain.py" --m4-material "$M4" --m5-material "$M5" --m6-material "$M6" --m7-material "$M7" --m8-material "$M8" --m9-material "$M9" --m10-material "$M10"
rm -rf "$OUT";mkdir -m700 -p "$OUT"
"$ROOT/deploy/m4/package_verifier_material.sh" "$M4" "$OUT/m4-verifier-material.tar.gz"
"$ROOT/deploy/m5/package_verifier_material.sh" "$M5" "$OUT/m5-verifier-material.tar.gz"
"$ROOT/deploy/m6/package_verifier_material.sh" "$M6" "$OUT/m6-verifier-material.tar.gz"
"$ROOT/deploy/m7/package_verifier_material.sh" "$M7" "$OUT/m7-verifier-material.tar.gz"
"$ROOT/deploy/m8/package_verifier_material.sh" "$M8" "$OUT/m8-verifier-material.tar.gz"
"$ROOT/deploy/m9/package_verifier_material.sh" "$M9" "$OUT/m9-verifier-material.tar.gz"
"$ROOT/deploy/m10/package_verifier_material.sh" "$M10" "$OUT/m10-verifier-material.tar.gz"
( cd "$OUT";sha256sum *.tar.gz > verifier-chain.sha256 )
echo "PASS: coherent M4-M10 verifier chain packaged at $OUT"
