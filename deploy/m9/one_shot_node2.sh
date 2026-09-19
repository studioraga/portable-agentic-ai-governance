#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";M9="${1:?m9 verifier material}";M8MAN="${2:?m8 manifest}"
"$ROOT/scripts/m9/preflight_dependencies.sh";test ! -f "$M9/signing-private.pem"||{ echo 'FAIL: M9 private key present on Node2';exit 2;};"$ROOT/deploy/m9/deploy_node.sh" "$M9" "$M8MAN";echo 'PASS: Node2 M9 one-shot deployment complete'
