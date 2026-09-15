#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M4="${1:?usage: install_continuous_controls_timer.sh <m4-material> <m5-material>}"; M5="${2:?m5 material}"
USER_NAME="${PAG_SERVICE_USER:-$USER}"; PY="${PAG_PYTHON:-$(command -v python3)}"
sudo tee /etc/systemd/system/pag-m5-continuous-controls.service >/dev/null <<EOF2
[Unit]
Description=Portable AI Governance M5 continuous control refresh
After=network.target
[Service]
Type=oneshot
User=$USER_NAME
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$M5
ExecStart=$PY $ROOT/scripts/m5/refresh_continuous_controls.py --m4-material $M4 --m5-material $M5
EOF2
sudo tee /etc/systemd/system/pag-m5-continuous-controls.timer >/dev/null <<'EOF2'
[Unit]
Description=Refresh PAG M5 continuous controls every 6 hours
[Timer]
OnBootSec=10min
OnUnitActiveSec=6h
Persistent=true
[Install]
WantedBy=timers.target
EOF2
sudo systemctl daemon-reload
sudo systemctl enable --now pag-m5-continuous-controls.timer
echo 'PASS: installed M5 continuous-control refresh timer'
