#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";M="${1:-$HOME/.config/portable-ai-governance/m20}";[[ ! -e "$M/signing-private.pem" ]]||{ echo 'FAIL: Node2 contains M20 private signing key';exit 2;};python3 "$ROOT/scripts/m20/validate_m20_node.py" --material "$M" --repo-root "$ROOT";echo 'PASS: Node2 M20 verifier-only final-freeze material verified'
