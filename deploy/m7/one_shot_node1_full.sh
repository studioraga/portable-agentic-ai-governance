#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 material}"; M3="${2:?m3 material}"; M4="${3:?m4 material}"; M5="${4:?m5 material}"; M6="${5:?m6 material}"; M7="${6:?m7 material}"

# A background M5 refresh changes the M5 manifest and invalidates M6/M7 bindings.
# Release generation must therefore run with the refresh timer quiesced.
if command -v systemctl >/dev/null 2>&1 && systemctl is-active --quiet pag-m5-continuous-controls.timer 2>/dev/null; then
  echo 'FAIL: pag-m5-continuous-controls.timer is active. Disable it before generating a downstream-bound M7 release:'
  echo '  sudo systemctl disable --now pag-m5-continuous-controls.timer'
  exit 2
fi

# Explicit full-release generation replaces the previous freeze marker.
rm -f "$M5/.pag-downstream-bound.json"
"$ROOT/deploy/m6/one_shot_node1_full.sh" "$M2" "$M3" "$M4" "$M5" "$M6"
"$ROOT/deploy/m7/one_shot_node1.sh" "$M6" "$M7"
python3 "$ROOT/scripts/m7/verify_release_chain.py" \
  --m4-material "$M4" \
  --m5-material "$M5" \
  --m6-material "$M6" \
  --m7-material "$M7" \
  --freeze-m5
"$ROOT/scripts/m7/validate_combined_node.sh" "$HOME/.config/portable-ai-governance/m2/production.env" "$HOME/.config/portable-ai-governance/m3/m3.env" "$HOME/.config/portable-ai-governance/m4/m4.env" "$HOME/.config/portable-ai-governance/m5/m5.env" "$HOME/.config/portable-ai-governance/m6/m6.env" "$HOME/.config/portable-ai-governance/m7/m7.env"
echo 'PASS: Node1 full M0-M7 one-shot deployment complete'
