#!/usr/bin/env bash
set -euo pipefail
ROLE="$1";SRC="$2";DEST="$3";mkdir -p "$DEST";chmod 700 "$DEST";rm -f "$DEST"/*
if [[ "$ROLE" == node1 ]];then cp -a "$SRC"/. "$DEST"/;else
  for f in enterprise-identity-policy.json m23-control-mapping.json m23-gap-closure.json m23-validation-summary.json m23-source-manifest.json m23-identity-manifest.json m23-identity-manifest.json.sig federation-public.pem pam-public.pem signing-public.pem positive-federated-assertion.jwt positive-jit-grant.jwt positive-break-glass-grant.jwt;do cp "$SRC/$f" "$DEST/$f";done
fi
find "$DEST" -type f -exec chmod 600 {} +
if [[ "$ROLE" == node2 ]] && find "$DEST" -type f -iname '*private*.pem' | grep -q .;then echo 'FAIL: Node2 M23 private-key boundary violated';exit 2;fi
