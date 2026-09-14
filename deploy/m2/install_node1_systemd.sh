#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG="${1:-$HOME/.config/portable-ai-governance/m2}"
ENV_FILE="$CONFIG/production.env"
SERVICE_USER="${PAG_SERVICE_USER:-$USER}"
PORT="${PAG_BIND_PORT:-9443}"
[ -r "$ENV_FILE" ] || { echo "ERROR: missing $ENV_FILE" >&2; exit 2; }
[ -x "$ROOT/.venv/bin/python" ] || { echo 'ERROR: run one-shot Node1 deployment first' >&2; exit 2; }
UNIT=/etc/systemd/system/portable-ai-governance-security-probe.service
TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
cat > "$TMP" <<EOF
[Unit]
Description=Portable Agentic AI Governance M2 Security Probe
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$ROOT
EnvironmentFile=$ENV_FILE
Environment=PYTHONPATH=$ROOT/src
ExecStart=$ROOT/.venv/bin/python -m portable_ai_governance.services.security_probe --host 0.0.0.0 --port $PORT
Restart=on-failure
RestartSec=3
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=read-only
ProtectSystem=strict
ReadWritePaths=$ROOT/var $CONFIG

[Install]
WantedBy=multi-user.target
EOF
sudo install -m 644 "$TMP" "$UNIT"
sudo systemctl daemon-reload
sudo systemctl enable --now portable-ai-governance-security-probe.service
sudo systemctl --no-pager --full status portable-ai-governance-security-probe.service
echo 'PASS: Node1 M2 systemd security probe installed'
