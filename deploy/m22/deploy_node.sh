#!/usr/bin/env bash
set -euo pipefail
ROLE="$1";SRC="$2";DEST="$3";mkdir -p "$DEST";chmod 700 "$DEST"
rm -f "$DEST"/*
if [[ "$ROLE" == node1 ]]; then cp -a "$SRC"/. "$DEST"/; else
 for f in cissp-domain-catalog.json enterprise-security-requirements.json enterprise-control-mapping.json gap-register.json evidence-policy.json m22-evaluation-summary.json m22-source-manifest.json m22-enterprise-manifest.json m22-enterprise-manifest.json.sig signing-public.pem; do cp "$SRC/$f" "$DEST/$f";done
fi
find "$DEST" -type f -exec chmod 600 {} +
if [[ "$ROLE" == node2 ]] && find "$DEST" -type f -iname '*private*.pem' | grep -q .; then echo 'FAIL: Node2 private-key boundary violated';exit 2;fi
