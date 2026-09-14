#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOST="${1:?usage: validate_remote_node1.sh NODE1_HOST [PORT] [NODE2_ENV]}"
PORT="${2:-9443}"
ENV_FILE="${3:-$HOME/.config/portable-ai-governance/m2/production.env}"
set -a; source "$ENV_FILE"; set +a
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python "$ROOT/scripts/m2/secure_ping.py" --host "$HOST" --port "$PORT"
echo 'PASS: remote Node1 M2 secure ping'
