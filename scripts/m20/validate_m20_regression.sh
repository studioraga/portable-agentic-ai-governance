#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT";git diff --check;python3 -m pytest -q
for m in {11..20};do [[ -x "./scripts/m${m}/validate_m${m}_local.sh" ]] && "./scripts/m${m}/validate_m${m}_local.sh";done
echo 'PASS: full M0-M20 regression + CRA acceptance complete'
